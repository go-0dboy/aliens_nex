#!/usr/bin/env python3
"""Validate and measure the Stage 5.12b N-only pair/sequence candidate.

Static/wire disagreement is a hard failure. Evaluation resource refusal is
recorded as an experimental outcome and is not reclassified as semantic
invalidity.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "meta-sequence-v0.1.json"
PYTHON_IMPL = ROOT / "independent" / "python"
GO_IMPL = ROOT / "reference" / "go"

sys.path.insert(0, str(PYTHON_IMPL))

from nex.eval import (  # noqa: E402
    EvaluationLimits,
    EvaluationResourceLimitError,
    evaluate_observed,
)
from nex.term import App, Nat  # noqa: E402
from nex.typesys import infer_principal, render_scheme  # noqa: E402
from nex.wire import decode_exact, encode_term  # noqa: E402

PYTHON_LIMITS = EvaluationLimits(max_steps=5_000_000, max_depth=700)
GO_MAX_TRANSITIONS = 5_000_000
GO_MAX_DEPTH = 20_000


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12b meta-sequence verification failed: {message}")


def apply_naturals(term, arguments: list[int]):
    result = term
    for argument in arguments:
        result = App(result, Nat(argument))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    build_check = subprocess.run(
        [
            sys.executable,
            str(ROOT / "stage5" / "selfhost" / "build_meta_sequence.py"),
            "--check",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if build_check.returncode != 0:
        fail(build_check.stderr.strip() or build_check.stdout.strip())

    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    if data.get("schema") != "nex-selfhost-meta-sequence":
        fail("unexpected artifact schema")
    if data.get("version") != "0.1":
        fail("unexpected artifact version")
    if data.get("core_version") != "NEX-1 v0.1":
        fail("artifact does not target exact NEX-1 v0.1")

    expected_names = [
        "meta_pair",
        "v2",
        "unpair_left",
        "unpair_right",
        "seq_cons",
        "seq_head",
        "seq_tail",
    ]
    functions = data.get("functions", [])
    if [item.get("name") for item in functions] != expected_names:
        fail("unexpected function inventory/order")

    go_requests: list[dict] = []
    python_outcomes: dict[str, dict] = {}

    for item in functions:
        name = item["name"]
        bits = item["wire_bits"]
        if len(bits) != item["wire_bit_length"]:
            fail(f"{name}: stored wire bit length mismatch")
        term = decode_exact(bits)
        if encode_term(term) != bits:
            fail(f"{name}: Python canonical wire round-trip mismatch")
        principal = render_scheme(infer_principal(term))
        if principal != item["expected_type"]:
            fail(
                f"{name}: Python principal type {principal!r}, "
                f"expected {item['expected_type']!r}"
            )
        go_requests.append(
            {"id": f"static:{name}", "level": "static", "bits": bits}
        )

        for index, case in enumerate(item["tests"]):
            case_id = f"{name}:{index}"
            applied = apply_naturals(term, case["args"])
            applied_type = render_scheme(infer_principal(applied))
            if applied_type != "N":
                fail(f"{case_id}: applied Python type {applied_type!r}, expected 'N'")
            expected = {"kind": "Nat", "value": str(case["result"])}
            try:
                observation = evaluate_observed(applied, PYTHON_LIMITS)
                if observation != expected:
                    fail(
                        f"{case_id}: Python observation {observation}, "
                        f"expected {expected}"
                    )
                python_outcomes[case_id] = {
                    "status": "value",
                    "result": observation,
                }
            except EvaluationResourceLimitError as exc:
                python_outcomes[case_id] = {
                    "status": "resource_refusal",
                    "detail": str(exc),
                }

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
        go_responses = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        fail(f"cannot parse Go probe output: {exc}")
    by_id = {response["id"]: response for response in go_responses}
    if len(by_id) != len(go_requests):
        fail("Go probe response count/IDs do not match requests")

    measurements: list[dict] = []
    for item in functions:
        name = item["name"]
        static = by_id.get(f"static:{name}")
        if static is None:
            fail(f"{name}: missing Go static response")
        if static.get("static_error"):
            fail(f"{name}: Go static rejection: {static['static_error']}")
        if static.get("type") != item["expected_type"]:
            fail(
                f"{name}: Go principal type {static.get('type')!r}, "
                f"expected {item['expected_type']!r}"
            )

        for index, case in enumerate(item["tests"]):
            case_id = f"{name}:{index}"
            response = by_id.get(f"eval:{case_id}")
            if response is None:
                fail(f"{case_id}: missing Go eval response")
            if response.get("static_error"):
                fail(f"{case_id}: Go static rejection: {response['static_error']}")

            expected = {"kind": "Nat", "value": str(case["result"])}
            cbn_result = response.get("cbn_result")
            need_result = response.get("need_result")
            if cbn_result is not None and cbn_result != expected:
                fail(f"{case_id}: Go CBN result {cbn_result}, expected {expected}")
            if need_result is not None and need_result != expected:
                fail(
                    f"{case_id}: Go call-by-need result {need_result}, expected {expected}"
                )
            if cbn_result is not None and need_result is not None and cbn_result != need_result:
                fail(f"{case_id}: Go CBN/call-by-need portable observations differ")

            measurements.append(
                {
                    "function": name,
                    "args": case["args"],
                    "expected": case["result"],
                    "python_cbn": python_outcomes[case_id],
                    "go_cbn": {
                        "status": "resource_refusal"
                        if response.get("cbn_error")
                        else "value",
                        "result": cbn_result,
                        "error": response.get("cbn_error", ""),
                        "stats": response.get("cbn_stats", {}),
                    },
                    "go_call_by_need": {
                        "status": "resource_refusal"
                        if response.get("need_error")
                        else "value",
                        "result": need_result,
                        "error": response.get("need_error", ""),
                        "stats": response.get("need_stats", {}),
                    },
                }
            )

    report = {
        "schema": "nex-selfhost-meta-sequence-measurement",
        "version": "0.1",
        "candidate": "pow2-adic-pair-v0.1 / nat-sequence-v0.1",
        "core_version": "NEX-1 v0.1",
        "budgets": {
            "python_cbn_max_steps": PYTHON_LIMITS.max_steps,
            "python_cbn_max_depth": PYTHON_LIMITS.max_depth,
            "go_max_transitions": GO_MAX_TRANSITIONS,
            "go_max_depth": GO_MAX_DEPTH,
        },
        "function_count": len(functions),
        "separate_term_bits": sum(item["wire_bit_length"] for item in functions),
        "cases": measurements,
    }
    if args.report is not None:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    cbn_refusals = sum(
        1 for row in measurements if row["go_cbn"]["status"] == "resource_refusal"
    )
    need_refusals = sum(
        1
        for row in measurements
        if row["go_call_by_need"]["status"] == "resource_refusal"
    )
    python_refusals = sum(
        1
        for row in measurements
        if row["python_cbn"]["status"] == "resource_refusal"
    )
    successful_pairs = [
        row
        for row in measurements
        if row["go_cbn"]["status"] == "value"
        and row["go_call_by_need"]["status"] == "value"
    ]
    largest_ratio = 0.0
    largest_case = None
    for row in successful_pairs:
        cbn = row["go_cbn"]["stats"].get("transitions", 0)
        need = row["go_call_by_need"]["stats"].get("transitions", 0)
        if need:
            ratio = cbn / need
            if ratio > largest_ratio:
                largest_ratio = ratio
                largest_case = (row["function"], row["args"], cbn, need)

    print("stage5.12b meta-sequence candidate: structurally verified")
    print(f"canonical functions: {len(functions)}")
    print(f"canonical bits (separate terms): {report['separate_term_bits']}")
    print(f"measurement cases: {len(measurements)}")
    print(f"Python CBN resource refusals: {python_refusals}")
    print(f"Go CBN resource refusals: {cbn_refusals}")
    print(f"Go call-by-need resource refusals: {need_refusals}")
    if largest_case is not None:
        fn, fn_args, cbn, need = largest_case
        print(
            "largest successful CBN/need transition ratio: "
            f"{largest_ratio:.2f}x at {fn}{tuple(fn_args)} "
            f"({cbn} vs {need})"
        )
    print("resource refusal remains an experimental outcome, not semantic invalidity")


if __name__ == "__main__":
    main()
