#!/usr/bin/env python3
"""Execute the preregistered functional-stream v0.2 hold-out exactly as frozen."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / "stage5" / "selfhost" / "functional-stream-v0.2.json"
HOLDOUT = ROOT / "stage5" / "selfhost" / "functional-stream-holdout-v0.1.json"
PYTHON_IMPL = ROOT / "independent" / "python"
GO_IMPL = ROOT / "reference" / "go"

FROZEN_CANDIDATE_BLOB_SHA = "7f35e453b7234e9078cf7cf2ca1e962b32e4ed3d"
FROZEN_HOLDOUT_BLOB_SHA = "3ca4ccb6406b5ab7f30edb005a55e2a139b2b8a5"
PY_MAX_TRANSITIONS = 5_000_000
PY_MAX_DEPTH = 8_000
GO_MAX_TRANSITIONS = 5_000_000
GO_MAX_DEPTH = 20_000

sys.path.insert(0, str(PYTHON_IMPL))
sys.setrecursionlimit(max(sys.getrecursionlimit(), 20_000))

from nex.term import App, Nat  # noqa: E402
from nex.typesys import infer_principal, render_scheme  # noqa: E402
from nex.wire import decode_exact, encode_term  # noqa: E402
from python_need import NeedLimits, NeedResourceLimitError, evaluate_need_observed  # noqa: E402


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12e functional-stream holdout failed: {message}")


def git_blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def apply_naturals(term, args: list[int]):
    result = term
    for arg in args:
        result = App(result, Nat(arg))
    return result


def main() -> None:
    if git_blob_sha(CANDIDATE) != FROZEN_CANDIDATE_BLOB_SHA:
        fail("candidate artifact changed after development pass/protocol freeze")
    if git_blob_sha(HOLDOUT) != FROZEN_HOLDOUT_BLOB_SHA:
        fail("preregistered hold-out changed before execution")

    candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
    holdout = json.loads(HOLDOUT.read_text(encoding="utf-8"))
    if candidate.get("version") != "0.2":
        fail("unexpected candidate version")
    if holdout.get("status") != "preregistered_unexecuted":
        fail("hold-out registration was rewritten before first execution")

    repeat_items = [row for row in candidate.get("functions", []) if row.get("name") == "repeat_query"]
    if len(repeat_items) != 1:
        fail("candidate must contain exactly one repeat_query")
    item = repeat_items[0]
    bits = item["wire_bits"]
    term = decode_exact(bits)
    if encode_term(term) != bits:
        fail("repeat_query canonical wire round-trip mismatch")
    if render_scheme(infer_principal(term)) != item["expected_type"]:
        fail("repeat_query principal type changed")

    limits = NeedLimits(max_transitions=PY_MAX_TRANSITIONS, max_depth=PY_MAX_DEPTH)
    python_results: dict[str, dict] = {}
    py_refusals: list[str] = []
    max_py_transitions = 0
    max_py_case = ""
    go_requests: list[dict] = []

    cases = holdout.get("cases", [])
    for index, case in enumerate(cases):
        case_id = f"holdout:{index}"
        applied = apply_naturals(term, case["args"])
        if render_scheme(infer_principal(applied)) != "N":
            fail(f"{case_id}: fully applied term is not N")
        expected = {"kind": "Nat", "value": str(case["result"])}
        try:
            observed, stats = evaluate_need_observed(applied, limits)
        except NeedResourceLimitError as exc:
            py_refusals.append(f"{case_id}{tuple(case['args'])}: {exc}")
            python_results[case_id] = {"status": "resource_refusal", "detail": str(exc)}
        else:
            if observed != expected:
                fail(f"{case_id}: Python need {observed} != {expected}")
            python_results[case_id] = {"status": "value", "result": observed}
            if stats.transitions > max_py_transitions:
                max_py_transitions = stats.transitions
                max_py_case = f"{case_id}{tuple(case['args'])}"

        go_requests.append({
            "id": case_id,
            "level": "eval",
            "bits": bits,
            "args": case["args"],
            "max_transitions": GO_MAX_TRANSITIONS,
            "max_depth": GO_MAX_DEPTH,
        })

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
    responses = json.loads(completed.stdout)
    by_id = {row["id"]: row for row in responses}
    if len(by_id) != len(cases):
        fail("Go response count/IDs differ from hold-out")

    go_need_refusals: list[str] = []
    go_cbn_refusals: list[str] = []
    max_go_transitions = 0
    max_go_case = ""
    matched = 0

    for index, case in enumerate(cases):
        case_id = f"holdout:{index}"
        row = by_id.get(case_id)
        if row is None or row.get("static_error"):
            fail(f"{case_id}: Go static rejection/missing response: {row}")
        expected = {"kind": "Nat", "value": str(case["result"])}
        if row.get("need_error"):
            go_need_refusals.append(f"{case_id}{tuple(case['args'])}: {row['need_error']}")
        else:
            if row.get("need_result") != expected:
                fail(f"{case_id}: Go need {row.get('need_result')} != {expected}")
            transitions = int((row.get("need_stats") or {}).get("transitions", 0))
            if transitions > max_go_transitions:
                max_go_transitions = transitions
                max_go_case = f"{case_id}{tuple(case['args'])}"
        if row.get("cbn_error"):
            go_cbn_refusals.append(f"{case_id}{tuple(case['args'])}: {row['cbn_error']}")
        elif row.get("cbn_result") != expected:
            fail(f"{case_id}: Go CBN {row.get('cbn_result')} != {expected}")

        py = python_results[case_id]
        if py["status"] == "value" and not row.get("need_error"):
            if py["result"] != row.get("need_result"):
                fail(f"{case_id}: Python/Go need mismatch")
            matched += 1

    if py_refusals:
        fail("Python call-by-need refusals: " + " | ".join(py_refusals))
    if go_need_refusals:
        fail("Go call-by-need refusals: " + " | ".join(go_need_refusals))

    print("stage5.12e functional-stream v0.2 preregistered holdout: passed")
    print(f"holdout cases: {len(cases)}")
    print("Python call-by-need resource refusals: 0")
    print("Go call-by-need resource refusals: 0")
    print(f"Go CBN resource refusals: {len(go_cbn_refusals)}")
    print(f"Python/Go need values matched: {matched}")
    print(f"largest Python need transition count: {max_py_transitions} at {max_py_case}")
    print(f"largest Go need transition count: {max_go_transitions} at {max_go_case}")


if __name__ == "__main__":
    main()
