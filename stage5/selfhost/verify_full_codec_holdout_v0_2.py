#!/usr/bin/env python3
"""Execute the preregistered Stage 5.12 full-codec v0.2 holdout exactly once.

The verifier requires the frozen v0.2 pre-holdout result and exact candidate,
contract, development and holdout Git blobs. It does not permit budget or
expectation changes.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SELF = ROOT / "stage5" / "selfhost"
ARTIFACT = SELF / "full-codec-v0.2.json"
CONTRACT = SELF / "full-codec-contract-v0.2.json"
DEVELOPMENT = SELF / "full-codec-development-v0.2.json"
HOLDOUT = SELF / "full-codec-holdout-v0.2.json"
PREHOLDOUT_RESULT = SELF / "full-codec-preholdout-result-v0.2.json"
PYTHON_IMPL = ROOT / "independent" / "python"
GO_IMPL = ROOT / "reference" / "go"

sys.path.insert(0, str(PYTHON_IMPL))
sys.setrecursionlimit(max(sys.getrecursionlimit(), 40_000))

from nex.wire import decode_exact  # noqa: E402
from python_need import NeedLimits, NeedResourceLimitError, evaluate_need_observed  # noqa: E402
from build_foundation import app  # noqa: E402
from build_full_codec import literal_finite_bits, literal_finite_tokens  # noqa: E402
from build_full_codec_v0_2 import source_terms_full_codec_v0_2  # noqa: E402
from verify_full_codec_development_v0_2 import (  # noqa: E402
    check_wrapper_static,
    finite_payload,
    length_projection,
    status_projection,
    stream_matches_projection,
    stat_value,
)

PY_NEED_LIMITS = NeedLimits(max_transitions=5_000_000, max_depth=8_000)
GO_MAX_TRANSITIONS = 5_000_000
GO_MAX_DEPTH = 20_000


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12 full codec v0.2 holdout failed: {message}")


def git_blob(path: Path) -> str:
    completed = subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT,
        text=True, capture_output=True, check=False,
    )
    if completed.returncode != 0:
        fail(completed.stderr.strip() or f"cannot hash {path}")
    return completed.stdout.strip()


def main() -> None:
    for script in ("validate_experiment_protocol.py", "validate_full_codec_contract_v0_2.py"):
        completed = subprocess.run(
            [sys.executable, str(SELF / script)], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        if completed.returncode != 0:
            fail(completed.stderr.strip() or completed.stdout.strip())
    completed = subprocess.run(
        [sys.executable, str(SELF / "build_full_codec_v0_2.py"), "--check"], cwd=ROOT,
        text=True, capture_output=True, check=False,
    )
    if completed.returncode != 0:
        fail(completed.stderr.strip() or completed.stdout.strip())

    if not PREHOLDOUT_RESULT.exists():
        fail("frozen v0.2 pre-holdout result is missing")
    result = json.loads(PREHOLDOUT_RESULT.read_text(encoding="utf-8"))
    if result.get("schema") != "nex-selfhost-full-codec-preholdout-result" or result.get("version") != "0.2":
        fail("pre-holdout result schema/version drifted")
    if result.get("status") != "development_and_exhaustive_passed_candidate_frozen":
        fail("pre-holdout result is not an accepted frozen pass")
    if not result.get("pre_holdout_historical_regression", {}).get("passed"):
        fail("pre-holdout historical regression is not recorded green")

    frozen = result.get("frozen_git_blobs", {})
    for path, key in (
        (ARTIFACT, "candidate_artifact"),
        (CONTRACT, "contract"),
        (DEVELOPMENT, "development_workload"),
        (HOLDOUT, "holdout_workload"),
    ):
        actual = git_blob(path)
        expected = frozen.get(key)
        if not expected or actual != expected:
            fail(f"{path.name}: Git blob {actual} differs from frozen {expected}")

    holdout = json.loads(HOLDOUT.read_text(encoding="utf-8"))
    if holdout.get("classification") != "holdout" or holdout.get("status") != "preregistered_unexecuted":
        fail("holdout classification/status drifted")
    if (len(holdout.get("valid_terms", [])), len(holdout.get("decode_errors", [])), len(holdout.get("encode_errors", []))) != (7, 3, 3):
        fail("holdout case counts drifted")

    sources = source_terms_full_codec_v0_2()
    decode = sources["decodeTerm"]
    encode = sources["encodeTerm"]
    wrappers: list[tuple[str, object, int]] = []

    def add(wrapper_id: str, expression, expected_value: int) -> None:
        wrappers.append((wrapper_id, expression, expected_value))

    for case in holdout["valid_terms"]:
        cid, bits, tokens = case["id"], case["bits"], case["tokens"]
        bit_values = [int(ch) for ch in bits]
        decode_call = app(decode, literal_finite_bits(bits))
        encode_call = app(encode, literal_finite_tokens(tokens))
        add(f"decode:{cid}:status", status_projection(decode_call), 0)
        add(f"decode:{cid}:length", length_projection(decode_call), len(tokens))
        add(f"decode:{cid}:stream", stream_matches_projection(decode_call, tokens, 0), 1)
        add(f"encode:{cid}:status", status_projection(encode_call), 0)
        add(f"encode:{cid}:length", length_projection(encode_call), len(bits))
        add(f"encode:{cid}:stream", stream_matches_projection(encode_call, bit_values, 2), 1)
        law1 = app(decode, finite_payload(encode_call))
        law2 = app(encode, finite_payload(decode_call))
        add(f"law1:{cid}:status", status_projection(law1), 0)
        add(f"law1:{cid}:length", length_projection(law1), len(tokens))
        add(f"law1:{cid}:stream", stream_matches_projection(law1, tokens, 0), 1)
        add(f"law2:{cid}:status", status_projection(law2), 0)
        add(f"law2:{cid}:length", length_projection(law2), len(bits))
        add(f"law2:{cid}:stream", stream_matches_projection(law2, bit_values, 2), 1)

    for case in holdout["decode_errors"]:
        add(f"decode-error:{case['id']}:status", status_projection(app(decode, literal_finite_bits(case["bits"]))), case["expected_status"])
    for case in holdout["encode_errors"]:
        add(f"encode-error:{case['id']}:status", status_projection(app(encode, literal_finite_tokens(case["tokens"]))), case["expected_status"])

    python_results = {}
    py_refusals = []
    go_requests = []
    max_py_transitions = 0
    max_py_case = ""
    for wrapper_id, wrapper, expected_value in wrappers:
        wrapper_bits = check_wrapper_static(wrapper, wrapper_id)
        term = decode_exact(wrapper_bits)
        expected = {"kind": "Nat", "value": str(expected_value)}
        try:
            observed, stats = evaluate_need_observed(term, PY_NEED_LIMITS)
            if observed != expected:
                fail(f"{wrapper_id}: Python need {observed} != {expected}")
            python_results[wrapper_id] = {"status": "value", "result": observed}
            if stats.transitions > max_py_transitions:
                max_py_transitions, max_py_case = stats.transitions, wrapper_id
        except NeedResourceLimitError as exc:
            py_refusals.append(f"{wrapper_id}: {exc}")
            python_results[wrapper_id] = {"status": "resource_refusal", "detail": str(exc)}
        go_requests.append({
            "id": f"eval:{wrapper_id}", "level": "eval", "bits": wrapper_bits,
            "max_transitions": GO_MAX_TRANSITIONS, "max_depth": GO_MAX_DEPTH,
        })

    completed = subprocess.run(
        ["go", "run", "./cmd/nexselfhostprobe"], cwd=GO_IMPL,
        input=json.dumps(go_requests), text=True, capture_output=True, check=False,
    )
    if completed.returncode != 0:
        fail(f"Go probe failed: {completed.stderr.strip()}")
    by_id = {row["id"]: row for row in json.loads(completed.stdout)}

    go_need_refusals = []
    go_cbn_refusals = []
    matched = 0
    max_go_transitions = 0
    max_go_case = ""
    expected_by_id = {wid: val for wid, _wrapper, val in wrappers}
    for wrapper_id, expected_value in expected_by_id.items():
        row = by_id.get(f"eval:{wrapper_id}")
        if row is None or row.get("static_error"):
            fail(f"{wrapper_id}: Go missing/static error: {row}")
        expected = {"kind": "Nat", "value": str(expected_value)}
        if row.get("need_error"):
            go_need_refusals.append(f"{wrapper_id}: {row['need_error']}")
        else:
            if row.get("need_result") != expected:
                fail(f"{wrapper_id}: Go need {row.get('need_result')} != {expected}")
            transitions = stat_value(row.get("need_stats") or {}, "transitions")
            if transitions > max_go_transitions:
                max_go_transitions, max_go_case = transitions, wrapper_id
        if row.get("cbn_error"):
            go_cbn_refusals.append(f"{wrapper_id}: {row['cbn_error']}")
        elif row.get("cbn_result") != expected:
            fail(f"{wrapper_id}: Go CBN mismatch: {row.get('cbn_result')}")
        py = python_results[wrapper_id]
        if py["status"] == "value" and not row.get("need_error"):
            if py["result"] != row.get("need_result"):
                fail(f"{wrapper_id}: Python/Go need mismatch")
            matched += 1

    if py_refusals:
        fail("Python call-by-need refusals: " + " | ".join(py_refusals))
    if go_need_refusals:
        fail("Go call-by-need refusals: " + " | ".join(go_need_refusals))

    print("stage5.12 full codec v0.2 preregistered holdout: passed")
    print(f"candidate Git blob: {git_blob(ARTIFACT)}")
    print(f"contract Git blob: {git_blob(CONTRACT)}")
    print(f"development Git blob: {git_blob(DEVELOPMENT)}")
    print(f"holdout Git blob: {git_blob(HOLDOUT)}")
    print("valid terms: 7")
    print("decode error cases: 3")
    print("encode error cases: 3")
    print(f"forced Nat observations: {len(wrappers)}")
    print("Python call-by-need resource refusals: 0")
    print("Go call-by-need resource refusals: 0")
    print(f"Go CBN resource refusals: {len(go_cbn_refusals)}")
    print(f"Python/Go need values matched: {matched}/{len(wrappers)}")
    print(f"largest Python need transition count: {max_py_transitions} at {max_py_case}")
    print(f"largest Go need transition count: {max_go_transitions} at {max_go_case}")
    print("round-trip laws: checked on all v0.2 holdout valid terms")


if __name__ == "__main__":
    main()
