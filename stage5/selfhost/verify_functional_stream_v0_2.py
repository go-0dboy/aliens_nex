#!/usr/bin/env python3
"""Verify Stage 5.12e indexed functional-stream candidate v0.2."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "functional-stream-v0.2.json"
PYTHON_IMPL = ROOT / "independent" / "python"
GO_IMPL = ROOT / "reference" / "go"

sys.path.insert(0, str(PYTHON_IMPL))
sys.setrecursionlimit(max(sys.getrecursionlimit(), 20_000))

from nex.term import App, Nat  # noqa: E402
from nex.typesys import infer_principal, render_scheme  # noqa: E402
from nex.wire import decode_exact, encode_term  # noqa: E402
from python_need import NeedLimits, NeedResourceLimitError, evaluate_need_observed  # noqa: E402

PY_NEED_LIMITS = NeedLimits(max_transitions=5_000_000, max_depth=8_000)
GO_MAX_TRANSITIONS = 5_000_000
GO_MAX_DEPTH = 20_000

EXPECTED_REPRESENTATION = {
    "type": "N -> N",
    "data_values": [0, 1],
    "eof": 2,
    "invariant": "indices before EOF contain 0 or 1; EOF and all later indices return 2",
}
EXPECTED_NAMES = [
    "stream_nil",
    "stream_cons",
    "stream_head",
    "stream_tail",
    "stream_drop",
    "dynamic2_query",
    "dynamic_tail_query",
    "stream_repeat",
    "repeat_query",
    "drop_query",
]


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12e functional-stream v0.2 verification failed: {message}")


def apply_naturals(term, arguments: list[int]):
    result = term
    for argument in arguments:
        result = App(result, Nat(argument))
    return result


def stat_value(stats: dict, name: str) -> int:
    return int(stats.get(name, stats.get(name.capitalize(), 0)))


def main() -> None:
    build = subprocess.run(
        [sys.executable, str(ROOT / "stage5" / "selfhost" / "build_functional_stream_v0_2.py"), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if build.returncode != 0:
        fail(build.stderr.strip() or build.stdout.strip())

    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    if data.get("schema") != "nex-selfhost-functional-stream-candidate":
        fail("unexpected artifact schema")
    if data.get("version") != "0.2" or data.get("core_version") != "NEX-1 v0.1":
        fail("unexpected version/Core target")
    if data.get("supersedes_candidate") != "functional-stream-v0.1.json":
        fail("candidate lineage missing")
    if data.get("representation") != EXPECTED_REPRESENTATION:
        fail("functional stream contract drifted")
    if data.get("repeat_strategy") != "direct indexed recursion over (count,index)":
        fail("unexpected repeat strategy")

    items = data.get("functions", [])
    if [item.get("name") for item in items] != EXPECTED_NAMES:
        fail("unexpected function inventory/order")

    go_requests: list[dict] = []
    python_results: dict[str, dict] = {}
    py_refusals: list[str] = []
    execution_cases = 0
    max_py_transitions = 0
    max_py_case = ""

    for item in items:
        name = item["name"]
        bits = item["wire_bits"]
        if len(bits) != item["wire_bit_length"]:
            fail(f"{name}: stored wire length mismatch")
        term = decode_exact(bits)
        if encode_term(term) != bits:
            fail(f"{name}: canonical wire round-trip mismatch")
        inferred = render_scheme(infer_principal(term))
        if inferred != item["expected_type"]:
            fail(f"{name}: Python type {inferred!r} != {item['expected_type']!r}")

        go_requests.append({"id": f"static:{name}", "level": "static", "bits": bits})

        for index, case in enumerate(item.get("tests", [])):
            case_id = f"{name}:{index}"
            applied = apply_naturals(term, case["args"])
            if render_scheme(infer_principal(applied)) != "N":
                fail(f"{case_id}: fully applied term is not N")
            expected = {"kind": "Nat", "value": str(case["result"])}
            try:
                observed, stats = evaluate_need_observed(applied, PY_NEED_LIMITS)
                if observed != expected:
                    fail(f"{case_id}: Python need {observed} != {expected}")
                python_results[case_id] = {
                    "status": "value",
                    "result": observed,
                    "transitions": stats.transitions,
                    "max_depth": stats.max_depth,
                }
                if stats.transitions > max_py_transitions:
                    max_py_transitions = stats.transitions
                    max_py_case = f"{case_id}{tuple(case['args'])}"
            except NeedResourceLimitError as exc:
                py_refusals.append(f"{case_id}{tuple(case['args'])}: {exc}")
                python_results[case_id] = {"status": "resource_refusal", "detail": str(exc)}

            go_requests.append(
                {
                    "id": f"eval:{case_id}",
                    "level": "eval",
                    "bits": bits,
                    "args": case["args"],
                    "max_transitions": GO_MAX_TRANSITIONS,
                    "max_depth": GO_MAX_DEPTH,
                }
            )
            execution_cases += 1

    completed = subprocess.run(
        ["go", "run", "./cmd/nexselfhostprobe"],
        cwd=GO_IMPL,
        input=json.dumps(go_requests),
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"Go probe failed: {completed.stderr.strip()}")
    try:
        responses = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        fail(f"cannot parse Go probe output: {exc}")
    by_id = {row["id"]: row for row in responses}
    if len(by_id) != len(go_requests):
        fail("Go response IDs/count differ")

    go_need_refusals: list[str] = []
    go_cbn_refusals: list[str] = []
    matched_need = 0
    max_go_need_transitions = 0
    max_go_need_case = ""

    for item in items:
        name = item["name"]
        static = by_id.get(f"static:{name}")
        if static is None or static.get("static_error"):
            fail(f"{name}: Go static rejection/missing response: {static}")
        if static.get("type") != item["expected_type"]:
            fail(f"{name}: Go type {static.get('type')!r} != {item['expected_type']!r}")

        for index, case in enumerate(item.get("tests", [])):
            case_id = f"{name}:{index}"
            row = by_id.get(f"eval:{case_id}")
            if row is None or row.get("static_error"):
                fail(f"{case_id}: Go static rejection/missing response: {row}")
            expected = {"kind": "Nat", "value": str(case["result"])}
            if row.get("need_error"):
                go_need_refusals.append(f"{case_id}{tuple(case['args'])}: {row['need_error']}")
            else:
                if row.get("need_result") != expected:
                    fail(f"{case_id}: Go need {row.get('need_result')} != {expected}")
                transitions = stat_value(row.get("need_stats") or {}, "transitions")
                if transitions > max_go_need_transitions:
                    max_go_need_transitions = transitions
                    max_go_need_case = f"{case_id}{tuple(case['args'])}"
            if row.get("cbn_error"):
                go_cbn_refusals.append(f"{case_id}{tuple(case['args'])}: {row['cbn_error']}")
            elif row.get("cbn_result") != expected:
                fail(f"{case_id}: Go CBN {row.get('cbn_result')} != {expected}")

            py = python_results[case_id]
            if py["status"] == "value" and not row.get("need_error"):
                if py["result"] != row.get("need_result"):
                    fail(f"{case_id}: Python/Go need mismatch")
                matched_need += 1

    if py_refusals:
        fail("Python call-by-need refused candidate cases: " + " | ".join(py_refusals))
    if go_need_refusals:
        fail("Go call-by-need refused candidate cases: " + " | ".join(go_need_refusals))

    total_bits = sum(item["wire_bit_length"] for item in items)
    print("stage5.12e functional stream v0.2: verified")
    print(f"canonical functions: {len(items)}")
    print(f"canonical bits (separate terms): {total_bits}")
    print(f"execution cases: {execution_cases}")
    print("Python call-by-need resource refusals: 0")
    print("Go call-by-need resource refusals: 0")
    print(f"Go CBN resource refusals: {len(go_cbn_refusals)}")
    print(f"Python/Go need values matched: {matched_need}")
    print(f"largest Python need transition count: {max_py_transitions} at {max_py_case}")
    print(f"largest Go need transition count: {max_go_need_transitions} at {max_go_need_case}")
    print("dynamic repeat length 128 reached and EOF boundary tested")


if __name__ == "__main__":
    main()
