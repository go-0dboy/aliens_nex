#!/usr/bin/env python3
"""Validate the frozen Stage 5.12 experiment protocol and preregistered hold-out."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = ROOT / "stage5" / "selfhost" / "experiment-protocol-v0.1.json"
HOLDOUT = ROOT / "stage5" / "selfhost" / "functional-stream-holdout-v0.1.json"


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12 experiment protocol invalid: {message}")


def main() -> None:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    if protocol.get("schema") != "nex-selfhost-experiment-protocol" or protocol.get("version") != "0.1":
        fail("unexpected protocol schema/version")
    if protocol.get("core_version") != "NEX-1 v0.1":
        fail("Core target drifted")

    budgets = protocol.get("resource_budgets", {})
    expected_budgets = {
        "python_call_by_need": {"max_transitions": 5_000_000, "max_depth": 8_000},
        "go_call_by_need": {"max_transitions": 5_000_000, "max_depth": 20_000},
    }
    for name, expected in expected_budgets.items():
        actual = budgets.get(name, {})
        for key, value in expected.items():
            if actual.get(key) != value:
                fail(f"{name}.{key} changed from frozen value {value}")
    go_cbn = budgets.get("go_normative_cbn", {})
    if go_cbn.get("max_transitions") != 5_000_000 or go_cbn.get("max_depth") != 20_000:
        fail("Go CBN budget drifted")

    active = protocol.get("active_candidate", {})
    if active.get("artifact") != "stage5/selfhost/functional-stream-v0.2.json":
        fail("active candidate artifact drifted")
    if active.get("builder") != "stage5/selfhost/build_functional_stream_v0_2.py":
        fail("active candidate builder drifted")
    if active.get("verifier") != "stage5/selfhost/verify_functional_stream_v0_2.py":
        fail("active candidate verifier drifted")
    if active.get("runtime_status_at_protocol_freeze") != "not yet executed by CI":
        fail("freeze-time runtime status was rewritten")

    holdout = json.loads(HOLDOUT.read_text(encoding="utf-8"))
    if holdout.get("schema") != "nex-selfhost-functional-stream-holdout" or holdout.get("version") != "0.1":
        fail("unexpected hold-out schema/version")
    if holdout.get("candidate") != active["artifact"]:
        fail("hold-out candidate does not match protocol")
    if holdout.get("status") != "preregistered_unexecuted":
        fail("preregistered hold-out status was rewritten; results must be recorded separately")
    cases = holdout.get("cases", [])
    if len(cases) != 11:
        fail("hold-out case count drifted")
    expected_cases = [
        ([1, 3, 2], 1), ([1, 3, 3], 2),
        ([0, 7, 6], 0), ([0, 7, 7], 2),
        ([1, 15, 14], 1), ([1, 15, 15], 2),
        ([0, 17, 23], 2),
        ([0, 63, 62], 0), ([0, 63, 63], 2),
        ([1, 127, 126], 1), ([1, 127, 127], 2),
    ]
    actual_cases = [(row.get("args"), row.get("result")) for row in cases]
    if actual_cases != expected_cases:
        fail("hold-out cases changed after preregistration")

    print("stage5.12 experiment protocol: valid and frozen")
    print("resource budgets: frozen")
    print("historical cases: development/not hold-out")
    print("functional-stream v0.2 hold-out registration: 11 cases, frozen; execution result is recorded separately")


if __name__ == "__main__":
    main()
