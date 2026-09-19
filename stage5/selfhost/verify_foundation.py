#!/usr/bin/env python3
"""Verify the Stage 5.12 arithmetic foundation with Python and Go controls."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "foundation-v0.1.json"
PYTHON_IMPL = ROOT / "independent" / "python"
GO_IMPL = ROOT / "reference" / "go"

sys.path.insert(0, str(PYTHON_IMPL))

from nex.eval import EvaluationLimits, evaluate_observed  # noqa: E402
from nex.term import App, Nat  # noqa: E402
from nex.typesys import infer_principal, render_scheme  # noqa: E402
from nex.wire import decode_exact, encode_term  # noqa: E402


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12 foundation verification failed: {message}")


def apply_naturals(term, arguments: list[int]):
    result = term
    for argument in arguments:
        result = App(result, Nat(argument))
    return result


def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    if data.get("schema") != "nex-selfhost-foundation":
        fail("unexpected artifact schema")
    if data.get("version") != "0.1":
        fail("unexpected artifact version")
    if data.get("core_version") != "NEX-1 v0.1":
        fail("foundation does not target exact NEX-1 v0.1")

    functions = data.get("functions", [])
    if [item.get("name") for item in functions] != [
        "add",
        "mul",
        "odd",
        "halve",
        "pow2",
        "shift_right",
    ]:
        fail("unexpected foundation function inventory/order")

    go_requests: list[dict] = []
    python_cases = 0

    for item in functions:
        name = item["name"]
        bits = item["wire_bits"]
        if len(bits) != item["wire_bit_length"]:
            fail(f"{name}: stored wire bit length mismatch")

        term = decode_exact(bits)
        if encode_term(term) != bits:
            fail(f"{name}: Python canonical wire round-trip mismatch")

        rendered = render_scheme(infer_principal(term))
        if rendered != item["expected_type"]:
            fail(
                f"{name}: Python principal type {rendered!r}, "
                f"expected {item['expected_type']!r}"
            )

        go_requests.append(
            {"id": f"type:{name}", "level": "static", "bits": bits}
        )

        for index, case in enumerate(item["tests"]):
            applied = apply_naturals(term, case["args"])
            observation = evaluate_observed(
                applied,
                EvaluationLimits(max_steps=1_000_000, max_depth=700),
            )
            expected_observation = {"kind": "Nat", "value": str(case["result"])}
            if observation != expected_observation:
                fail(
                    f"{name}{tuple(case['args'])}: Python observation "
                    f"{observation}, expected {expected_observation}"
                )
            go_requests.append(
                {
                    "id": f"eval:{name}:{index}",
                    "level": "eval",
                    "bits": encode_term(applied),
                }
            )
            python_cases += 1

    completed = subprocess.run(
        ["go", "run", "./cmd/nexdiffprobe"],
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
    expected_response_count = len(go_requests)
    if len(by_id) != expected_response_count:
        fail(
            f"Go probe returned {len(by_id)} unique responses; "
            f"expected {expected_response_count}"
        )

    go_cases = 0
    for item in functions:
        name = item["name"]
        type_response = by_id.get(f"type:{name}")
        if type_response is None:
            fail(f"{name}: Go type response missing")
        if type_response.get("wire_error") or type_response.get("static_error"):
            fail(f"{name}: Go rejected foundation term: {type_response}")
        if type_response.get("wire_bits") != item["wire_bits"]:
            fail(f"{name}: Go canonical wire round-trip mismatch")
        if type_response.get("type") != item["expected_type"]:
            fail(
                f"{name}: Go principal type {type_response.get('type')!r}, "
                f"expected {item['expected_type']!r}"
            )

        for index, case in enumerate(item["tests"]):
            response = by_id.get(f"eval:{name}:{index}")
            if response is None:
                fail(f"{name} case {index}: Go evaluation response missing")
            if response.get("wire_error") or response.get("static_error") or response.get("eval_error"):
                fail(f"{name} case {index}: Go rejected/eval-refused case: {response}")
            expected = {"kind": "Nat", "value": str(case["result"])}
            if response.get("result") != expected:
                fail(
                    f"{name}{tuple(case['args'])}: Go observation "
                    f"{response.get('result')}, expected {expected}"
                )
            go_cases += 1

    if go_cases != python_cases:
        fail("Python/Go executed case counts differ")

    total_bits = sum(item["wire_bit_length"] for item in functions)
    print("stage5.12 foundation: verified")
    print(f"canonical functions: {len(functions)}")
    print(f"canonical foundation bits (separate terms): {total_bits}")
    print(f"test applications per implementation: {python_cases}")
    print("Python/Go wire, type and Nat observations: matched")


if __name__ == "__main__":
    main()
