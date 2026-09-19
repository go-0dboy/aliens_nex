#!/usr/bin/env python3
"""Verify the frozen negative result of the Stage 5.12d pair candidate.

The candidate verifier is intentionally strict and exits non-zero when the Go
sharing control refuses any frozen case. This wrapper turns that exact negative
outcome into durable evidence: only the pre-recorded resource-refusal surface is
accepted. A wrong value, changed refusal set, build error, or unrelated failure
still fails CI.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "stage5" / "selfhost" / "interleaved-pair-result-v0.1.json"
VERIFIER = ROOT / "stage5" / "selfhost" / "verify_interleaved_pair.py"


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12d negative-result verification failed: {message}")


def main() -> None:
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    if frozen.get("schema") != "nex-selfhost-interleaved-pair-result":
        fail("unexpected result schema")
    if frozen.get("version") != "0.1":
        fail("unexpected result version")
    if frozen.get("decision") != "rejected_as_primary_recursive_meta_representation_under_frozen_budget":
        fail("unexpected frozen decision")

    completed = subprocess.run(
        [sys.executable, str(VERIFIER)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 1:
        fail(
            "candidate verifier no longer reports the frozen negative outcome; "
            f"returncode={completed.returncode}\nstdout={completed.stdout}\nstderr={completed.stderr}"
        )

    summary = frozen["summary"]
    required_stdout = [
        "stage5.12d interleaved pair candidate: measured",
        f"canonical functions: {summary['canonical_functions']}",
        f"canonical bits (separate terms): {summary['canonical_bits_separate_terms']}",
        f"execution cases: {summary['execution_cases']}",
        f"Python call-by-need resource refusals: {summary['python_need_resource_refusals']}",
        f"Go call-by-need resource refusals: {summary['go_need_resource_refusals']}",
        f"Go CBN resource refusals: {summary['go_cbn_resource_refusals']}",
        f"Python/Go need values compared: {summary['python_go_need_values_compared']}",
    ]
    for text in required_stdout:
        if text not in completed.stdout:
            fail(f"missing frozen measurement line: {text!r}")

    for case_id in frozen["go_need_refusal_case_ids"]:
        if case_id not in completed.stderr:
            fail(f"missing frozen Go need refusal {case_id}")
    for case_id in frozen["python_need_refusal_case_ids"]:
        if case_id not in completed.stderr:
            fail(f"missing frozen Python need refusal {case_id}")

    if "depth" not in completed.stderr or "resource" not in completed.stderr:
        fail("negative result is no longer classified as bounded resource refusal")

    unexpected_markers = [
        "principal type",
        "canonical wire round-trip mismatch",
        "independent oracle",
        "Python/Go need mismatch",
        "Go static rejection",
    ]
    for marker in unexpected_markers:
        if marker in completed.stderr:
            fail(f"candidate failed for a semantic/structural reason instead of frozen resource outcome: {marker}")

    print("stage5.12d interleaved pair negative result: reproduced")
    print("candidate remains structurally valid but rejected as primary recursive representation")
    print(f"Go need refusal cases: {len(frozen['go_need_refusal_case_ids'])}")
    print(f"Python need refusal cases: {len(frozen['python_need_refusal_case_ids'])}")
    print("returned portable mismatches: 0")


if __name__ == "__main__":
    main()
