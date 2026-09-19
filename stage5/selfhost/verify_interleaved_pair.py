#!/usr/bin/env python3
"""Verify the Stage 5.12d bit-interleaving pair candidate.

The candidate is not yet the accepted meta-representation. This verifier asks
whether its exact NEX terms are canonical/well-typed, agree with an independent
mathematical oracle, and remain operational under the two sharing controls.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "interleaved-pair-v0.1.json"
PYTHON_IMPL = ROOT / "independent" / "python"
GO_IMPL = ROOT / "reference" / "go"

sys.path.insert(0, str(PYTHON_IMPL))
sys.setrecursionlimit(max(sys.getrecursionlimit(), 20_000))

from nex.term import App, Nat  # noqa: E402
from nex.typesys import infer_principal, render_scheme  # noqa: E402
from nex.wire import decode_exact, encode_term  # noqa: E402
from python_need import NeedLimits, NeedResourceLimitError, evaluate_need_observed  # noqa: E402

PYTHON_NEED_LIMITS = NeedLimits(max_transitions=5_000_000, max_depth=4_000)
GO_MAX_TRANSITIONS = 5_000_000
GO_MAX_DEPTH = 20_000


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12d interleaved-pair verification failed: {message}")


def interleave_pair(a: int, b: int) -> int:
    result = 0
    position = 0
    while a or b:
        result |= (a & 1) << (2 * position)
        result |= (b & 1) << (2 * position + 1)
        a >>= 1
        b >>= 1
        position += 1
    return result


def interleave_unpair(z: int) -> tuple[int, int]:
    left = 0
    right = 0
    position = 0
    while z:
        left |= (z & 1) << position
        right |= ((z >> 1) & 1) << position
        z >>= 2
        position += 1
    return left, right


def apply_naturals(term, arguments: list[int]):
    result = term
    for argument in arguments:
        result = App(result, Nat(argument))
    return result


def main() -> None:
    build = subprocess.run(
        [sys.executable, str(ROOT / "stage5" / "selfhost" / "build_interleaved_pair.py"), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if build.returncode != 0:
        fail(build.stderr.strip() or build.stdout.strip())

    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    if data.get("schema") != "nex-selfhost-interleaved-pair-candidate":
        fail("unexpected artifact schema")
    if data.get("version") != "0.1" or data.get("core_version") != "NEX-1 v0.1":
        fail("unexpected version/Core target")

    names = [item.get("name") for item in data.get("functions", [])]
    expected_names = [
        "meta_pair_interleaved",
        "unpair_left_interleaved",
        "unpair_right_interleaved",
    ]
    if names != expected_names:
        fail("unexpected function inventory/order")

    go_requests: list[dict] = []
    python_results: dict[str, dict] = {}
    python_refusal_details: list[str] = []

    for item in data["functions"]:
        name = item["name"]
        bits = item["wire_bits"]
        if len(bits) != item["wire_bit_length"]:
            fail(f"{name}: wire bit length mismatch")
        term = decode_exact(bits)
        if encode_term(term) != bits:
            fail(f"{name}: canonical wire round-trip mismatch")
        inferred = render_scheme(infer_principal(term))
        if inferred != item["expected_type"]:
            fail(f"{name}: principal type {inferred!r} != {item['expected_type']!r}")

        go_requests.append({"id": f"static:{name}", "level": "static", "bits": bits})

        for index, case in enumerate(item["tests"]):
            case_id = f"{name}:{index}"
            args = case["args"]
            expected_value = case["result"]

            if name == "meta_pair_interleaved":
                oracle = interleave_pair(args[0], args[1])
            elif name == "unpair_left_interleaved":
                oracle = interleave_unpair(args[0])[0]
            else:
                oracle = interleave_unpair(args[0])[1]
            if oracle != expected_value:
                fail(f"{case_id}: frozen result {expected_value} != independent oracle {oracle}")

            applied = apply_naturals(term, args)
            expected = {"kind": "Nat", "value": str(expected_value)}
            try:
                observed, stats = evaluate_need_observed(applied, PYTHON_NEED_LIMITS)
                if observed != expected:
                    fail(f"{case_id}: Python need {observed} != {expected}")
                python_results[case_id] = {
                    "status": "value",
                    "result": observed,
                    "transitions": stats.transitions,
                    "max_depth": stats.max_depth,
                }
            except NeedResourceLimitError as exc:
                python_refusal_details.append(f"{case_id}{tuple(args)}: {exc}")
                python_results[case_id] = {"status": "resource_refusal", "detail": str(exc)}

            go_requests.append(
                {
                    "id": f"eval:{case_id}",
                    "level": "eval",
                    "bits": bits,
                    "args": args,
                    "max_transitions": GO_MAX_TRANSITIONS,
                    "max_depth": GO_MAX_DEPTH,
                }
            )

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
    if len(by_id) != len(go_requests):
        fail("Go probe response count/IDs differ")

    go_need_refusal_details: list[str] = []
    go_cbn_refusal_details: list[str] = []
    compared_need_values = 0
    cases = 0

    for item in data["functions"]:
        name = item["name"]
        static = by_id.get(f"static:{name}")
        if static is None or static.get("static_error"):
            fail(f"{name}: Go static rejection/missing response: {static}")
        if static.get("type") != item["expected_type"]:
            fail(f"{name}: Go type {static.get('type')!r} != {item['expected_type']!r}")

        for index, case in enumerate(item["tests"]):
            case_id = f"{name}:{index}"
            args = case["args"]
            row = by_id.get(f"eval:{case_id}")
            if row is None or row.get("static_error"):
                fail(f"{case_id}: Go static rejection/missing response: {row}")
            expected = {"kind": "Nat", "value": str(case["result"])}
            if row.get("need_error"):
                go_need_refusal_details.append(
                    f"{case_id}{tuple(args)}: {row['need_error']}"
                )
            elif row.get("need_result") != expected:
                fail(f"{case_id}: Go need {row.get('need_result')} != {expected}")
            if row.get("cbn_error"):
                go_cbn_refusal_details.append(
                    f"{case_id}{tuple(args)}: {row['cbn_error']}"
                )
            elif row.get("cbn_result") != expected:
                fail(f"{case_id}: Go CBN {row.get('cbn_result')} != {expected}")

            py = python_results[case_id]
            if py["status"] == "value" and not row.get("need_error"):
                if row.get("need_result") != py["result"]:
                    fail(f"{case_id}: Python/Go need mismatch")
                compared_need_values += 1
            cases += 1

    for a in range(32):
        for b in range(32):
            if interleave_unpair(interleave_pair(a, b)) != (a, b):
                fail(f"bounded host round-trip failed for ({a},{b})")

    total_bits = sum(item["wire_bit_length"] for item in data["functions"])
    print("stage5.12d interleaved pair candidate: measured")
    print(f"canonical functions: {len(data['functions'])}")
    print(f"canonical bits (separate terms): {total_bits}")
    print(f"execution cases: {cases}")
    print(f"Python call-by-need resource refusals: {len(python_refusal_details)}")
    print(f"Go call-by-need resource refusals: {len(go_need_refusal_details)}")
    print(f"Go CBN resource refusals: {len(go_cbn_refusal_details)}")
    print(f"Python/Go need values compared: {compared_need_values}")
    for row in data["growth_examples"]:
        print(
            "growth sample "
            f"({row['a']},{row['b']}): pow2-adic={row['pow2_adic_code_bit_length']} bits, "
            f"interleaved={row['interleaved_code_bit_length']} bits"
        )

    if go_need_refusal_details:
        fail(
            "Go call-by-need candidate refusals: "
            + " | ".join(go_need_refusal_details)
            + ("; Python refusals: " + " | ".join(python_refusal_details) if python_refusal_details else "")
        )


if __name__ == "__main__":
    main()
