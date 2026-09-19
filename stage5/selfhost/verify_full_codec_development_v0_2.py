#!/usr/bin/env python3
"""Execute Stage 5.12 full codec candidate v0.2 on development evidence only.

The preregistered v0.2 holdout is intentionally never opened here. The v0.2
development set includes all v0.1 development plus the revealed/rejected v0.1
holdout, so the former deepmixed holdout failure is a mandatory regression.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "full-codec-v0.2.json"
DEVELOPMENT = ROOT / "stage5" / "selfhost" / "full-codec-development-v0.2.json"
PYTHON_IMPL = ROOT / "independent" / "python"
GO_IMPL = ROOT / "reference" / "go"

sys.path.insert(0, str(PYTHON_IMPL))
sys.setrecursionlimit(max(sys.getrecursionlimit(), 40_000))

from nex.typesys import infer_principal, render_scheme  # noqa: E402
from nex.wire import decode_exact, encode_term  # noqa: E402
from python_need import NeedLimits, NeedResourceLimitError, evaluate_need_observed  # noqa: E402
from build_foundation import IFZ, app, encode_core, let, lower, nat, v  # noqa: E402
from build_full_codec import (  # noqa: E402
    PAIR,
    codec_length,
    codec_status,
    codec_stream,
    literal_finite_bits,
    literal_finite_tokens,
    source_arithmetic,
)
from build_full_codec_v0_2 import source_terms_full_codec_v0_2  # noqa: E402

PY_NEED_LIMITS = NeedLimits(max_transitions=5_000_000, max_depth=8_000)
GO_MAX_TRANSITIONS = 5_000_000
GO_MAX_DEPTH = 20_000


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12 full codec v0.2 development failed: {message}")


def stat_value(stats: dict, name: str) -> int:
    return int(stats.get(name, stats.get(name.capitalize(), 0)))


def status_projection(call):
    return let("r", call, codec_status(v("r")))


def length_projection(call):
    return let("r", call, codec_length(v("r")))


def stream_matches_projection(call, expected: list[int], sentinel: int):
    _add, _sub, _lt, eq, _bitlen, _u_len, _u_bit = source_arithmetic()
    checks = [(index, value) for index, value in enumerate(expected)]
    checks.append((len(expected), sentinel))
    body = nat(1)
    for index, expected_value in reversed(checks):
        condition = app(eq, app(v("s"), nat(index)), nat(expected_value))
        body = app(IFZ, condition, nat(0), body)
    return let("r", call, let("s", codec_stream(v("r")), body))


def finite_payload(result_call):
    return let(
        "r",
        result_call,
        app(PAIR, codec_stream(v("r")), codec_length(v("r"))),
    )


def check_wrapper_static(wrapper, wrapper_id: str) -> str:
    bits = encode_core(lower(wrapper))
    term = decode_exact(bits)
    if encode_term(term) != bits:
        fail(f"{wrapper_id}: wrapper wire not canonical")
    inferred = render_scheme(infer_principal(term))
    if inferred != "N":
        fail(f"{wrapper_id}: wrapper type {inferred!r} != 'N'")
    return bits


def main() -> None:
    static_check = subprocess.run(
        [sys.executable, str(ROOT / "stage5" / "selfhost" / "verify_full_codec_static_v0_2.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if static_check.returncode != 0:
        fail(static_check.stderr.strip() or static_check.stdout.strip())

    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    development = json.loads(DEVELOPMENT.read_text(encoding="utf-8"))
    if artifact.get("version") != "0.2" or artifact.get("status") != "stage5.12-development-candidate":
        fail("candidate identity/status drifted")
    if artifact.get("holdout_status") != "preregistered_unexecuted":
        fail("candidate no longer records an unexecuted holdout")
    if development.get("classification") != "development" or development.get("status") != "frozen_before_full_codec_candidate_v0.2":
        fail("development workload classification/status drifted")

    sources = source_terms_full_codec_v0_2()
    decode = sources["decodeTerm"]
    encode = sources["encodeTerm"]
    wrappers: list[tuple[str, object, int]] = []

    def add_wrapper(wrapper_id: str, expression, expected_value: int) -> None:
        wrappers.append((wrapper_id, expression, expected_value))

    for case in development.get("valid_terms", []):
        cid = case["id"]
        bits = case["bits"]
        tokens = case["tokens"]
        bit_values = [int(ch) for ch in bits]

        decode_call = app(decode, literal_finite_bits(bits))
        add_wrapper(f"decode:{cid}:status", status_projection(decode_call), 0)
        add_wrapper(f"decode:{cid}:length", length_projection(decode_call), len(tokens))
        add_wrapper(f"decode:{cid}:stream", stream_matches_projection(decode_call, tokens, 0), 1)

        encode_call = app(encode, literal_finite_tokens(tokens))
        add_wrapper(f"encode:{cid}:status", status_projection(encode_call), 0)
        add_wrapper(f"encode:{cid}:length", length_projection(encode_call), len(bits))
        add_wrapper(f"encode:{cid}:stream", stream_matches_projection(encode_call, bit_values, 2), 1)

        law1_call = app(decode, finite_payload(encode_call))
        add_wrapper(f"law1:{cid}:status", status_projection(law1_call), 0)
        add_wrapper(f"law1:{cid}:length", length_projection(law1_call), len(tokens))
        add_wrapper(f"law1:{cid}:stream", stream_matches_projection(law1_call, tokens, 0), 1)

        law2_call = app(encode, finite_payload(decode_call))
        add_wrapper(f"law2:{cid}:status", status_projection(law2_call), 0)
        add_wrapper(f"law2:{cid}:length", length_projection(law2_call), len(bits))
        add_wrapper(f"law2:{cid}:stream", stream_matches_projection(law2_call, bit_values, 2), 1)

    for case in development.get("decode_errors", []):
        call = app(decode, literal_finite_bits(case["bits"]))
        add_wrapper(f"decode-error:{case['id']}:status", status_projection(call), case["expected_status"])

    for case in development.get("encode_errors", []):
        call = app(encode, literal_finite_tokens(case["tokens"]))
        add_wrapper(f"encode-error:{case['id']}:status", status_projection(call), case["expected_status"])

    go_requests: list[dict] = []
    python_results: dict[str, dict] = {}
    py_refusals: list[str] = []
    max_py_transitions = 0
    max_py_case = ""

    for wrapper_id, wrapper, expected_value in wrappers:
        wrapper_bits = check_wrapper_static(wrapper, wrapper_id)
        wrapper_term = decode_exact(wrapper_bits)
        expected = {"kind": "Nat", "value": str(expected_value)}
        try:
            observed, stats = evaluate_need_observed(wrapper_term, PY_NEED_LIMITS)
            if observed != expected:
                fail(f"{wrapper_id}: Python need {observed} != {expected}")
            python_results[wrapper_id] = {
                "status": "value",
                "result": observed,
                "transitions": stats.transitions,
                "max_depth": stats.max_depth,
            }
            if stats.transitions > max_py_transitions:
                max_py_transitions = stats.transitions
                max_py_case = wrapper_id
        except NeedResourceLimitError as exc:
            py_refusals.append(f"{wrapper_id}: {exc}")
            python_results[wrapper_id] = {"status": "resource_refusal", "detail": str(exc)}

        go_requests.append({
            "id": f"eval:{wrapper_id}",
            "level": "eval",
            "bits": wrapper_bits,
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
    try:
        responses = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        fail(f"cannot parse Go probe output: {exc}")
    by_id = {row["id"]: row for row in responses}
    if len(by_id) != len(go_requests):
        fail("Go response ID/count mismatch")

    go_need_refusals: list[str] = []
    go_cbn_refusals: list[str] = []
    matched_need = 0
    max_go_need_transitions = 0
    max_go_need_case = ""
    expected_by_id = {wrapper_id: expected for wrapper_id, _wrapper, expected in wrappers}

    for wrapper_id, expected_value in expected_by_id.items():
        row = by_id.get(f"eval:{wrapper_id}")
        if row is None or row.get("static_error"):
            fail(f"{wrapper_id}: Go static rejection/missing response: {row}")
        expected = {"kind": "Nat", "value": str(expected_value)}
        if row.get("need_error"):
            go_need_refusals.append(f"{wrapper_id}: {row['need_error']}")
        else:
            if row.get("need_result") != expected:
                fail(f"{wrapper_id}: Go need {row.get('need_result')} != {expected}")
            transitions = stat_value(row.get("need_stats") or {}, "transitions")
            if transitions > max_go_need_transitions:
                max_go_need_transitions = transitions
                max_go_need_case = wrapper_id

        if row.get("cbn_error"):
            go_cbn_refusals.append(f"{wrapper_id}: {row['cbn_error']}")
        elif row.get("cbn_result") != expected:
            fail(f"{wrapper_id}: Go CBN {row.get('cbn_result')} != {expected}")

        py = python_results[wrapper_id]
        if py["status"] == "value" and not row.get("need_error"):
            if py["result"] != row.get("need_result"):
                fail(f"{wrapper_id}: Python/Go need mismatch")
            matched_need += 1

    if py_refusals:
        fail("Python call-by-need refusals: " + " | ".join(py_refusals))
    if go_need_refusals:
        fail("Go call-by-need refusals: " + " | ".join(go_need_refusals))

    total_bits = sum(row["wire_bit_length"] for row in artifact["functions"])
    print("stage5.12 full codec v0.2 development: verified")
    print(f"candidate bits (separate decodeTerm+encodeTerm): {total_bits}")
    print(f"valid terms: {len(development.get('valid_terms', []))}")
    print(f"decode error cases: {len(development.get('decode_errors', []))}")
    print(f"encode error cases: {len(development.get('encode_errors', []))}")
    print(f"forced Nat observations: {len(wrappers)}")
    print("Python call-by-need resource refusals: 0")
    print("Go call-by-need resource refusals: 0")
    print(f"Go CBN resource refusals: {len(go_cbn_refusals)}")
    print(f"Python/Go need values matched: {matched_need}/{len(wrappers)}")
    print(f"largest Python need transition count: {max_py_transitions} at {max_py_case}")
    print(f"largest Go need transition count: {max_go_need_transitions} at {max_go_need_case}")
    print("round-trip laws: checked on all development valid terms")
    print("former v0.1 holdout including deepmixed: now development regression and passed")
    print("v0.2 holdout: NOT READ / NOT EXECUTED")


if __name__ == "__main__":
    main()
