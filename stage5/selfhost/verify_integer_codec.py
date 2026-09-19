#!/usr/bin/env python3
"""Verify Stage 5.12c NEX-written U(n) codec against host controls.

The NEX terms are the objects under test. Python/Go codec functions are only
independent engineering controls for differential comparison.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "integer-codec-v0.1.json"
PYTHON_IMPL = ROOT / "independent" / "python"
GO_IMPL = ROOT / "reference" / "go"

sys.path.insert(0, str(PYTHON_IMPL))

from nex.eval import EvaluationLimits, EvaluationResourceLimitError, evaluate_observed  # noqa: E402
from nex.term import App, Nat  # noqa: E402
from nex.typesys import infer_principal, render_scheme  # noqa: E402
from nex.wire import (  # noqa: E402
    InvalidBitError,
    TruncatedError,
    decode_exact,
    decode_u,
    encode_term,
    encode_u,
)
from python_need import NeedLimits, NeedResourceLimitError, evaluate_need_observed  # noqa: E402

PYTHON_CBN_LIMITS = EvaluationLimits(max_steps=5_000_000, max_depth=700)
PYTHON_NEED_LIMITS = NeedLimits(max_transitions=5_000_000, max_depth=2_000)
GO_MAX_TRANSITIONS = 5_000_000
GO_MAX_DEPTH = 20_000


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12c integer-codec verification failed: {message}")


def unpair_code(z: int) -> tuple[int, int]:
    if z < 0:
        raise ValueError("encoded pair must be non-negative")
    n = z + 1
    a = 0
    while n % 2 == 0:
        a += 1
        n //= 2
    return a, (n - 1) // 2


def seq_items(code: int) -> list[int]:
    items: list[int] = []
    while code != 0:
        head, code = unpair_code(code - 1)
        items.append(head)
    return items


def bits_text(code: int) -> str:
    items = seq_items(code)
    if any(item not in (0, 1) for item in items):
        fail(f"internal Bits result contains non-bit items: {items}")
    return "".join(str(item) for item in items)


def decode_result(code: int) -> dict:
    tag, payload = unpair_code(code)
    if tag == 0:
        value, rest = unpair_code(payload)
        return {"kind": "ok", "value": value, "rest_bits": bits_text(rest)}
    if tag == 1:
        return {"kind": "truncated"}
    if tag == 2:
        return {"kind": "invalid_bit"}
    return {"kind": "unknown", "tag": tag}


def apply_naturals(term, arguments: list[int]):
    result = term
    for argument in arguments:
        result = App(result, Nat(argument))
    return result


def main() -> None:
    build = subprocess.run(
        [sys.executable, str(ROOT / "stage5" / "selfhost" / "build_integer_codec.py"), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if build.returncode != 0:
        fail(build.stderr.strip() or build.stdout.strip())

    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    if data.get("schema") != "nex-selfhost-integer-codec" or data.get("version") != "0.1":
        fail("unexpected artifact schema/version")
    if data.get("core_version") != "NEX-1 v0.1":
        fail("artifact does not target exact NEX-1 v0.1")

    functions = {item["name"]: item for item in data["functions"]}
    if "encodeU" not in functions or "decodeU" not in functions:
        fail("encodeU/decodeU missing from artifact")

    go_eval_requests: list[dict] = []
    go_direct_requests: list[dict] = []
    python_need: dict[str, dict] = {}
    python_cbn: dict[str, dict] = {}

    for item in data["functions"]:
        bits = item["wire_bits"]
        if len(bits) != item["wire_bit_length"]:
            fail(f"{item['name']}: wire length mismatch")
        term = decode_exact(bits)
        if encode_term(term) != bits:
            fail(f"{item['name']}: canonical wire round-trip mismatch")
        inferred = render_scheme(infer_principal(term))
        if inferred != item["expected_type"]:
            fail(f"{item['name']}: principal type {inferred!r} != {item['expected_type']!r}")

        for index, case in enumerate(item["tests"]):
            case_id = f"{item['name']}:{index}"
            applied = apply_naturals(term, case["args"])
            if render_scheme(infer_principal(applied)) != "N":
                fail(f"{case_id}: fully applied term is not N")
            expected = {"kind": "Nat", "value": str(case["result"])}

            try:
                observed, stats = evaluate_need_observed(applied, PYTHON_NEED_LIMITS)
            except NeedResourceLimitError as exc:
                fail(f"{case_id}: Python call-by-need resource refusal: {exc}")
            if observed != expected:
                fail(f"{case_id}: Python call-by-need {observed} != {expected}")
            python_need[case_id] = {
                "result": observed,
                "transitions": stats.transitions,
                "max_depth": stats.max_depth,
            }

            try:
                observed_cbn = evaluate_observed(applied, PYTHON_CBN_LIMITS)
                if observed_cbn != expected:
                    fail(f"{case_id}: Python CBN {observed_cbn} != {expected}")
                python_cbn[case_id] = {"status": "value", "result": observed_cbn}
            except EvaluationResourceLimitError as exc:
                python_cbn[case_id] = {"status": "resource_refusal", "detail": str(exc)}

            go_eval_requests.append(
                {
                    "id": case_id,
                    "level": "eval",
                    "bits": bits,
                    "args": case["args"],
                    "max_transitions": GO_MAX_TRANSITIONS,
                    "max_depth": GO_MAX_DEPTH,
                }
            )

    encode_item = functions["encodeU"]
    for index, case in enumerate(encode_item["tests"]):
        n = case["args"][0]
        expected_bits = case["bits"]
        if encode_u(n) != expected_bits:
            fail(f"encodeU:{index}: Python host EncodeU disagrees with frozen expected bits")
        if bits_text(case["result"]) != expected_bits:
            fail(f"encodeU:{index}: frozen internal Bits code disagrees with expected bits")
        go_direct_requests.append(
            {"id": f"encode:{index}", "operation": "encode", "value": str(n)}
        )

    decode_item = functions["decodeU"]
    for index, case in enumerate(decode_item["tests"]):
        expected = decode_result(case["result"])
        if "items" in case:
            try:
                decode_u("2")
                fail("Python host accepted an invalid bit character")
            except InvalidBitError:
                python_host = {"kind": "invalid_bit"}
            go_direct_requests.append(
                {"id": f"decode:{index}", "operation": "decode", "items": case["items"]}
            )
        else:
            raw = case["bits"]
            try:
                value, consumed = decode_u(raw)
                python_host = {"kind": "ok", "value": value, "rest_bits": raw[consumed:]}
            except TruncatedError:
                python_host = {"kind": "truncated"}
            except InvalidBitError:
                python_host = {"kind": "invalid_bit"}
            go_direct_requests.append(
                {"id": f"decode:{index}", "operation": "decode", "bits": raw}
            )
        if python_host != expected:
            fail(f"decodeU:{index}: Python host {python_host} != frozen result {expected}")

    go_eval = subprocess.run(
        ["go", "run", "./cmd/nexselfhostprobe"],
        cwd=GO_IMPL,
        input=json.dumps(go_eval_requests),
        text=True,
        capture_output=True,
        check=False,
    )
    if go_eval.returncode != 0:
        fail(f"Go NEX evaluator probe failed: {go_eval.stderr.strip()}")
    eval_by_id = {row["id"]: row for row in json.loads(go_eval.stdout)}

    go_direct = subprocess.run(
        ["go", "run", "./cmd/nexucontrol"],
        cwd=GO_IMPL,
        input=json.dumps(go_direct_requests),
        text=True,
        capture_output=True,
        check=False,
    )
    if go_direct.returncode != 0:
        fail(f"Go direct U control failed: {go_direct.stderr.strip()}")
    direct_by_id = {row["id"]: row for row in json.loads(go_direct.stdout)}

    go_cbn_refusals = 0
    for request in go_eval_requests:
        case_id = request["id"]
        row = eval_by_id.get(case_id)
        if row is None:
            fail(f"missing Go eval response {case_id}")
        expected_value = next(
            case["result"]
            for item in data["functions"]
            for index, case in enumerate(item["tests"])
            if f"{item['name']}:{index}" == case_id
        )
        expected = {"kind": "Nat", "value": str(expected_value)}
        if row.get("need_error"):
            fail(f"{case_id}: Go call-by-need resource/error: {row['need_error']}")
        if row.get("need_result") != expected:
            fail(f"{case_id}: Go call-by-need {row.get('need_result')} != {expected}")
        if row.get("need_result") != python_need[case_id]["result"]:
            fail(f"{case_id}: Python/Go call-by-need mismatch")
        if row.get("cbn_error"):
            go_cbn_refusals += 1
        elif row.get("cbn_result") != expected:
            fail(f"{case_id}: Go CBN returned wrong value")

    for index, case in enumerate(encode_item["tests"]):
        row = direct_by_id[f"encode:{index}"]
        if row.get("error") or row.get("bits") != case["bits"]:
            fail(f"encodeU:{index}: Go host control disagrees: {row}")

    for index, case in enumerate(decode_item["tests"]):
        row = direct_by_id[f"decode:{index}"]
        expected = decode_result(case["result"])
        if expected["kind"] == "ok":
            go_host = {
                "kind": "ok",
                "value": int(row["value"]),
                "rest_bits": row.get("rest_bits", ""),
            } if not row.get("error") else {"kind": row["error"]}
        else:
            go_host = {"kind": row.get("error", "")}
        if go_host != expected:
            fail(f"decodeU:{index}: Go host {go_host} != frozen result {expected}")

    python_cbn_refusals = sum(1 for row in python_cbn.values() if row["status"] == "resource_refusal")
    print("stage5.12c NEX integer codec: verified")
    print(f"canonical encodeU bits: {encode_item['wire_bit_length']}")
    print(f"canonical decodeU bits: {decode_item['wire_bit_length']}")
    print(f"NEX test applications: {len(go_eval_requests)}")
    print("Python/Go call-by-need portable observations: matched")
    print("Python/Go direct U codec controls: matched")
    print(f"Python CBN resource refusals: {python_cbn_refusals}")
    print(f"Go CBN resource refusals: {go_cbn_refusals}")


if __name__ == "__main__":
    main()
