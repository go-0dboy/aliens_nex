#!/usr/bin/env python3
"""Verify Stage 5.12f stream-parser candidate v0.1 on development cases only.

The preregistered holdout is intentionally not read or executed here.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "stream-parser-v0.1.json"
DEVELOPMENT = ROOT / "stage5" / "selfhost" / "parser-development-v0.1.json"
CONTRACT = ROOT / "stage5" / "selfhost" / "parser-contract-v0.1.json"
PYTHON_IMPL = ROOT / "independent" / "python"
GO_IMPL = ROOT / "reference" / "go"

sys.path.insert(0, str(PYTHON_IMPL))
sys.setrecursionlimit(max(sys.getrecursionlimit(), 30_000))

from nex.typesys import infer_principal, render_scheme  # noqa: E402
from nex.wire import decode_exact, encode_term  # noqa: E402
from python_need import NeedLimits, NeedResourceLimitError, evaluate_need_observed  # noqa: E402
from build_foundation import app, encode_core, lower, nat  # noqa: E402
from build_stream_parser import (  # noqa: E402
    EXPECTED_TYPE,
    literal_bit_stream,
    result_projection,
    source_terms_parser,
)

PY_NEED_LIMITS = NeedLimits(max_transitions=5_000_000, max_depth=8_000)
GO_MAX_TRANSITIONS = 5_000_000
GO_MAX_DEPTH = 20_000
FIELD_NAMES = ["status", "a", "b", "next_offset"]
EXPECTED_NAMES = ["decodeUAt", "readHead", "skipTerm", "exactTerm"]


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12f stream-parser v0.1 verification failed: {message}")


def stat_value(stats: dict, name: str) -> int:
    return int(stats.get(name, stats.get(name.capitalize(), 0)))


def main() -> None:
    contract_check = subprocess.run(
        [sys.executable, str(ROOT / "stage5" / "selfhost" / "validate_parser_contract.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if contract_check.returncode != 0:
        fail(contract_check.stderr.strip() or contract_check.stdout.strip())

    build = subprocess.run(
        [sys.executable, str(ROOT / "stage5" / "selfhost" / "build_stream_parser.py"), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if build.returncode != 0:
        fail(build.stderr.strip() or build.stdout.strip())

    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    development = json.loads(DEVELOPMENT.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    if artifact.get("schema") != "nex-selfhost-stream-parser-candidate":
        fail("unexpected artifact schema")
    if artifact.get("version") != "0.1" or artifact.get("core_version") != "NEX-1 v0.1":
        fail("unexpected parser candidate version/Core")
    if artifact.get("status") != "stage5.12f-development-candidate":
        fail("candidate status drifted")
    if artifact.get("contract") != "stage5/selfhost/parser-contract-v0.1.json":
        fail("candidate contract reference drifted")
    if artifact.get("holdout_status") != "preregistered_unexecuted":
        fail("holdout must remain preregistered_unexecuted during development verification")
    if development.get("classification") != "development" or development.get("status") != "frozen_before_parser_implementation":
        fail("development workload classification/status drifted")
    if contract.get("resource_budgets", {}).get("python_call_by_need") != {
        "max_transitions": 5000000,
        "max_depth": 8000,
    }:
        fail("Python resource budget drifted")

    items = artifact.get("functions", [])
    if [item.get("name") for item in items] != EXPECTED_NAMES:
        fail("unexpected parser function inventory/order")

    go_requests: list[dict] = []
    python_results: dict[str, dict] = {}
    py_refusals: list[str] = []
    max_py_transitions = 0
    max_py_case = ""

    # First verify the four frozen candidate research objects themselves.
    for item in items:
        name = item["name"]
        bits = item["wire_bits"]
        if len(bits) != item["wire_bit_length"]:
            fail(f"{name}: stored wire length mismatch")
        term = decode_exact(bits)
        if encode_term(term) != bits:
            fail(f"{name}: canonical wire round-trip mismatch")
        inferred = render_scheme(infer_principal(term))
        if inferred != EXPECTED_TYPE or inferred != item["expected_type"]:
            fail(f"{name}: Python type {inferred!r} != {EXPECTED_TYPE!r}")
        go_requests.append({"id": f"static:{name}", "level": "static", "bits": bits})

    sources = source_terms_parser()
    projected_cases = 0

    # Development only. The holdout file is intentionally not opened here.
    for case in development.get("cases", []):
        case_id = case["id"]
        operation = case["operation"]
        if operation not in sources:
            fail(f"{case_id}: unknown operation {operation!r}")
        expected_fields = case["expected"]
        if len(expected_fields) != 4:
            fail(f"{case_id}: expected ParserResult must have four fields")

        call = app(
            sources[operation],
            literal_bit_stream(case["bits"]),
            nat(case["offset"]),
        )

        for field, expected_value in enumerate(expected_fields):
            projection = result_projection(call, field)
            projection_bits = encode_core(lower(projection))
            projection_term = decode_exact(projection_bits)
            if encode_term(projection_term) != projection_bits:
                fail(f"{case_id}:{FIELD_NAMES[field]}: wrapper wire is not canonical")
            if render_scheme(infer_principal(projection_term)) != "N":
                fail(f"{case_id}:{FIELD_NAMES[field]}: projected test term is not N")

            projected_id = f"{case_id}:{FIELD_NAMES[field]}"
            expected = {"kind": "Nat", "value": str(expected_value)}
            try:
                observed, stats = evaluate_need_observed(projection_term, PY_NEED_LIMITS)
                if observed != expected:
                    fail(f"{projected_id}: Python need {observed} != {expected}")
                python_results[projected_id] = {
                    "status": "value",
                    "result": observed,
                    "transitions": stats.transitions,
                    "max_depth": stats.max_depth,
                }
                if stats.transitions > max_py_transitions:
                    max_py_transitions = stats.transitions
                    max_py_case = projected_id
            except NeedResourceLimitError as exc:
                py_refusals.append(f"{projected_id}: {exc}")
                python_results[projected_id] = {
                    "status": "resource_refusal",
                    "detail": str(exc),
                }

            go_requests.append(
                {
                    "id": f"eval:{projected_id}",
                    "level": "eval",
                    "bits": projection_bits,
                    "max_transitions": GO_MAX_TRANSITIONS,
                    "max_depth": GO_MAX_DEPTH,
                }
            )
            projected_cases += 1

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

    for item in items:
        name = item["name"]
        row = by_id.get(f"static:{name}")
        if row is None or row.get("static_error"):
            fail(f"{name}: Go static rejection/missing response: {row}")
        if row.get("type") != EXPECTED_TYPE:
            fail(f"{name}: Go type {row.get('type')!r} != {EXPECTED_TYPE!r}")

    go_need_refusals: list[str] = []
    go_cbn_refusals: list[str] = []
    matched_need = 0
    max_go_need_transitions = 0
    max_go_need_case = ""

    for case in development.get("cases", []):
        case_id = case["id"]
        for field, expected_value in enumerate(case["expected"]):
            projected_id = f"{case_id}:{FIELD_NAMES[field]}"
            row = by_id.get(f"eval:{projected_id}")
            if row is None or row.get("static_error"):
                fail(f"{projected_id}: Go static rejection/missing response: {row}")
            expected = {"kind": "Nat", "value": str(expected_value)}

            if row.get("need_error"):
                go_need_refusals.append(f"{projected_id}: {row['need_error']}")
            else:
                if row.get("need_result") != expected:
                    fail(f"{projected_id}: Go need {row.get('need_result')} != {expected}")
                transitions = stat_value(row.get("need_stats") or {}, "transitions")
                if transitions > max_go_need_transitions:
                    max_go_need_transitions = transitions
                    max_go_need_case = projected_id

            if row.get("cbn_error"):
                go_cbn_refusals.append(f"{projected_id}: {row['cbn_error']}")
            elif row.get("cbn_result") != expected:
                fail(f"{projected_id}: Go CBN {row.get('cbn_result')} != {expected}")

            py = python_results[projected_id]
            if py["status"] == "value" and not row.get("need_error"):
                if py["result"] != row.get("need_result"):
                    fail(f"{projected_id}: Python/Go need mismatch")
                matched_need += 1

    if py_refusals:
        fail("Python call-by-need refused development cases: " + " | ".join(py_refusals))
    if go_need_refusals:
        fail("Go call-by-need refused development cases: " + " | ".join(go_need_refusals))

    total_bits = sum(item["wire_bit_length"] for item in items)
    print("stage5.12f stream parser v0.1 development: verified")
    print(f"canonical functions: {len(items)}")
    print(f"canonical bits (separate terms): {total_bits}")
    print(f"development cases: {len(development.get('cases', []))}")
    print(f"projected Nat observations: {projected_cases}")
    print("Python call-by-need resource refusals: 0")
    print("Go call-by-need resource refusals: 0")
    print(f"Go CBN resource refusals: {len(go_cbn_refusals)}")
    print(f"Python/Go need values matched: {matched_need}")
    print(f"largest Python need transition count: {max_py_transitions} at {max_py_case}")
    print(f"largest Go need transition count: {max_go_need_transitions} at {max_go_need_case}")
    print("holdout: NOT EXECUTED")


if __name__ == "__main__":
    main()
