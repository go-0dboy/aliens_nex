#!/usr/bin/env python3
"""Verify Stage 5.12c NEX-written U(n) codec against independent controls.

The canonical NEX terms are the objects under test. Stage 5.12b already records
bounded pure-CBN resource behavior, so this verifier does not repeat the slow
Python CBN run. It compares the NEX-written U(n) codec with both host codecs,
requires the Go call-by-need control to complete the frozen 5.12c workload, and
records Python call-by-need resource refusal separately from semantic failure.

A resource refusal is not semantic invalidity. A wrong returned value, wire/type
mismatch, or host-codec disagreement remains a hard failure.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "integer-codec-v0.1.json"
PYTHON_IMPL = ROOT / "independent" / "python"
GO_IMPL = ROOT / "reference" / "go"

sys.path.insert(0, str(PYTHON_IMPL))
# Host-stack capacity is an implementation resource. Keep it above the bounded
# Python NeedLimits depth so CPython does not become the accidental first limit.
sys.setrecursionlimit(max(sys.getrecursionlimit(), 10_000))

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


def run_json(command: list[str], payload: list[dict]) -> list[dict]:
    completed = subprocess.run(
        command,
        cwd=GO_IMPL,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"{' '.join(command)} failed: {completed.stderr.strip()}")
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        fail(f"cannot parse {' '.join(command)} output: {exc}")
    if not isinstance(result, list):
        fail(f"{' '.join(command)} did not return a JSON array")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    build = subprocess.run(
        [
            sys.executable,
            str(ROOT / "stage5" / "selfhost" / "build_integer_codec.py"),
            "--check",
        ],
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

    expected_names = [
        "seq_length",
        "seq_reverse",
        "binary_rev",
        "prepend_zeros",
        "encodeU",
        "decodeU",
    ]
    items = data.get("functions", [])
    if [item.get("name") for item in items] != expected_names:
        fail("unexpected integer-codec function inventory/order")
    functions = {item["name"]: item for item in items}

    go_eval_requests: list[dict] = []
    python_need: dict[str, dict] = {}

    for item in items:
        name = item["name"]
        bits = item["wire_bits"]
        if len(bits) != item["wire_bit_length"]:
            fail(f"{name}: wire length mismatch")
        term = decode_exact(bits)
        if encode_term(term) != bits:
            fail(f"{name}: canonical wire round-trip mismatch")
        inferred = render_scheme(infer_principal(term))
        if inferred != item["expected_type"]:
            fail(f"{name}: principal type {inferred!r} != {item['expected_type']!r}")

        go_eval_requests.append({"id": f"static:{name}", "level": "static", "bits": bits})
        for index, case in enumerate(item["tests"]):
            case_id = f"{name}:{index}"
            applied = apply_naturals(term, case["args"])
            if render_scheme(infer_principal(applied)) != "N":
                fail(f"{case_id}: fully applied term is not N")
            expected = {"kind": "Nat", "value": str(case["result"])}
            try:
                observed, stats = evaluate_need_observed(applied, PYTHON_NEED_LIMITS)
                if observed != expected:
                    fail(f"{case_id}: Python call-by-need {observed} != {expected}")
                python_need[case_id] = {
                    "status": "value",
                    "result": observed,
                    "stats": {
                        "transitions": stats.transitions,
                        "max_depth": stats.max_depth,
                        "memo_hits": stats.memo_hits,
                    },
                }
            except NeedResourceLimitError as exc:
                python_need[case_id] = {
                    "status": "resource_refusal",
                    "detail": str(exc),
                }

            go_eval_requests.append(
                {
                    "id": f"eval:{case_id}",
                    "level": "eval",
                    "bits": bits,
                    "args": case["args"],
                    "max_transitions": GO_MAX_TRANSITIONS,
                    "max_depth": GO_MAX_DEPTH,
                }
            )

    # Compare the NEX-written encoder with both existing host codecs.
    encode_item = functions["encodeU"]
    go_host_requests: list[dict] = []
    for index, case in enumerate(encode_item["tests"]):
        n = case["args"][0]
        expected_bits = case["bits"]
        if encode_u(n) != expected_bits:
            fail(f"encodeU:{index}: Python host encoder disagrees with expected bits")
        if bits_text(case["result"]) != expected_bits:
            fail(f"encodeU:{index}: N-only result does not represent expected bits")
        go_host_requests.append(
            {"id": f"encode:{index}", "operation": "encode", "value": str(n)}
        )

    # Compare the NEX-written decoder with both existing host codecs.
    decode_item = functions["decodeU"]
    for index, case in enumerate(decode_item["tests"]):
        case_id = f"decode:{index}"
        expected = decode_result(case["result"])
        if "items" in case:
            try:
                decode_u("2")
                fail("Python host accepted an invalid bit character")
            except InvalidBitError:
                actual = {"kind": "invalid_bit"}
            go_host_requests.append(
                {"id": case_id, "operation": "decode", "items": case["items"]}
            )
        else:
            raw = case["bits"]
            try:
                value, consumed = decode_u(raw)
                actual = {"kind": "ok", "value": value, "rest_bits": raw[consumed:]}
            except TruncatedError:
                actual = {"kind": "truncated"}
            except InvalidBitError:
                actual = {"kind": "invalid_bit"}
            go_host_requests.append(
                {"id": case_id, "operation": "decode", "bits": raw}
            )
        if actual != expected:
            fail(f"decodeU:{index}: Python host {actual} != frozen result {expected}")

    go_eval = run_json(["go", "run", "./cmd/nexselfhostprobe"], go_eval_requests)
    eval_by_id = {row["id"]: row for row in go_eval}
    if len(eval_by_id) != len(go_eval_requests):
        fail("Go selfhost probe response IDs/count differ")

    go_host = run_json(["go", "run", "./cmd/nexucontrol"], go_host_requests)
    host_by_id = {row["id"]: row for row in go_host}
    if len(host_by_id) != len(go_host_requests):
        fail("Go U host-control response IDs/count differ")

    go_cbn_refusals = 0
    execution_cases = 0
    measurements: list[dict] = []
    python_need_refusals = 0

    for item in items:
        name = item["name"]
        static = eval_by_id.get(f"static:{name}")
        if static is None or static.get("static_error"):
            fail(f"{name}: Go static rejection/missing response: {static}")
        if static.get("type") != item["expected_type"]:
            fail(f"{name}: Go type {static.get('type')!r} != {item['expected_type']!r}")

        for index, case in enumerate(item["tests"]):
            case_id = f"{name}:{index}"
            row = eval_by_id.get(f"eval:{case_id}")
            if row is None or row.get("static_error"):
                fail(f"{case_id}: Go static rejection/missing response: {row}")
            expected = {"kind": "Nat", "value": str(case["result"])}

            if row.get("need_error"):
                fail(f"{case_id}: Go call-by-need refusal: {row['need_error']}")
            if row.get("need_result") != expected:
                fail(f"{case_id}: Go call-by-need {row.get('need_result')} != {expected}")

            python_outcome = python_need[case_id]
            if python_outcome["status"] == "value":
                if row.get("need_result") != python_outcome["result"]:
                    fail(f"{case_id}: Python/Go call-by-need observations differ")
            else:
                python_need_refusals += 1

            if row.get("cbn_error"):
                go_cbn_refusals += 1
                go_cbn = {
                    "status": "resource_refusal",
                    "detail": row["cbn_error"],
                    "stats": row.get("cbn_stats", {}),
                }
            else:
                if row.get("cbn_result") != expected:
                    fail(f"{case_id}: Go CBN returned wrong portable value")
                go_cbn = {
                    "status": "value",
                    "result": row.get("cbn_result"),
                    "stats": row.get("cbn_stats", {}),
                }

            measurements.append(
                {
                    "function": name,
                    "args": case["args"],
                    "expected": case["result"],
                    "python_call_by_need": python_outcome,
                    "go_call_by_need": {
                        "status": "value",
                        "result": row.get("need_result"),
                        "stats": row.get("need_stats", {}),
                    },
                    "go_cbn": go_cbn,
                }
            )
            execution_cases += 1

    for index, case in enumerate(encode_item["tests"]):
        row = host_by_id.get(f"encode:{index}")
        if row is None or row.get("error") or row.get("bits") != case["bits"]:
            fail(f"encodeU:{index}: Go host control disagrees: {row}")

    for index, case in enumerate(decode_item["tests"]):
        row = host_by_id.get(f"decode:{index}")
        if row is None:
            fail(f"decodeU:{index}: missing Go host response")
        expected = decode_result(case["result"])
        if expected["kind"] == "ok":
            actual = (
                {
                    "kind": "ok",
                    "value": int(row["value"]),
                    "rest_bits": row.get("rest_bits", ""),
                }
                if not row.get("error")
                else {"kind": row["error"]}
            )
        else:
            actual = {"kind": row.get("error", "")}
        if actual != expected:
            fail(f"decodeU:{index}: Go host {actual} != frozen result {expected}")

    report = {
        "schema": "nex-selfhost-integer-codec-measurement",
        "version": "0.1",
        "core_version": "NEX-1 v0.1",
        "budgets": {
            "python_need_max_transitions": PYTHON_NEED_LIMITS.max_transitions,
            "python_need_max_depth": PYTHON_NEED_LIMITS.max_depth,
            "go_max_transitions": GO_MAX_TRANSITIONS,
            "go_max_depth": GO_MAX_DEPTH,
        },
        "function_count": len(items),
        "separate_term_bits": sum(item["wire_bit_length"] for item in items),
        "execution_case_count": execution_cases,
        "python_need_resource_refusals": python_need_refusals,
        "go_need_resource_refusals": 0,
        "go_cbn_resource_refusals": go_cbn_refusals,
        "cases": measurements,
    }
    if args.report is not None:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    print("stage5.12c NEX integer codec: structurally and differentially verified")
    print(f"canonical functions: {len(items)}")
    print(f"canonical bits (separate terms): {report['separate_term_bits']}")
    print(f"canonical encodeU bits: {encode_item['wire_bit_length']}")
    print(f"canonical decodeU bits: {decode_item['wire_bit_length']}")
    print(f"NEX execution cases: {execution_cases}")
    print(f"Python call-by-need resource refusals: {python_need_refusals}")
    print("Go call-by-need resource refusals: 0")
    print(f"Go CBN resource refusals: {go_cbn_refusals}")
    print("Python/Go call-by-need observations matched wherever Python returned")
    print("Python/Go direct U(n) host controls: matched")
    print("resource refusal remains an experimental outcome, not semantic invalidity")


if __name__ == "__main__":
    main()
