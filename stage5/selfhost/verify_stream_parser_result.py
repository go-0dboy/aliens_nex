#!/usr/bin/env python3
"""Validate frozen Stage 5.12f stream-parser result without re-executing holdout."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "stage5" / "selfhost" / "stream-parser-holdout-result-v0.1.json"
DEVELOPMENT_RESULT = ROOT / "stage5" / "selfhost" / "stream-parser-development-result-v0.1.json"
ARTIFACT = ROOT / "stage5" / "selfhost" / "stream-parser-v0.1.json"
CONTRACT = ROOT / "stage5" / "selfhost" / "parser-contract-v0.1.json"
DEVELOPMENT = ROOT / "stage5" / "selfhost" / "parser-development-v0.1.json"
HOLDOUT = ROOT / "stage5" / "selfhost" / "parser-holdout-v0.1.json"


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12f parser result invalid: {message}")


def git_blob(path: Path) -> str:
    completed = subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        fail(completed.stderr.strip() or f"cannot hash {path}")
    return completed.stdout.strip()


def main() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    dev_result = json.loads(DEVELOPMENT_RESULT.read_text(encoding="utf-8"))

    if result.get("schema") != "nex-selfhost-stream-parser-holdout-result":
        fail("unexpected result schema")
    if result.get("version") != "0.1" or result.get("stage") != "5.12f":
        fail("unexpected result version/stage")
    if result.get("core_version") != "NEX-1 v0.1":
        fail("Core version drifted")
    if result.get("decision") != "holdout_pass":
        fail("frozen decision is not holdout_pass")
    if result.get("checkpoint_status") != "accepted_for_bounded_stream_wire_traversal":
        fail("checkpoint status drifted")
    if dev_result.get("decision") != "development_pass":
        fail("development result is not a pass")

    expected_paths = {
        "candidate_git_blob_sha": ARTIFACT,
        "contract_git_blob_sha": CONTRACT,
        "development_git_blob_sha": DEVELOPMENT,
        "holdout_git_blob_sha": HOLDOUT,
    }
    for field, path in expected_paths.items():
        actual = git_blob(path)
        if result.get(field) != actual:
            fail(f"{field} {result.get(field)!r} != current blob {actual!r}")

    if result.get("candidate_git_blob_sha") != dev_result.get("candidate_git_blob_sha"):
        fail("candidate changed between development and holdout checkpoints")
    if result.get("holdout_git_blob_sha") != dev_result.get("holdout_git_blob_sha"):
        fail("holdout changed between development and holdout checkpoints")

    expected_measurements = {
        "holdout_cases": 12,
        "projected_nat_observations": 48,
        "python_call_by_need_resource_refusals": 0,
        "go_call_by_need_resource_refusals": 0,
        "go_normative_cbn_resource_refusals": 18,
        "python_go_need_values_matched": 48,
        "largest_python_need_transition_count": 15151,
        "largest_python_need_case": "skip-let-complex:a",
        "largest_go_need_transition_count": 6392,
        "largest_go_need_case": "skip-let-complex:a",
    }
    if result.get("measurements") != expected_measurements:
        fail("measurement summary drifted")

    regression = result.get("pre_holdout_historical_regression", {})
    if regression != {
        "workflow": "stage5-self-sufficiency-regression",
        "run_id": 35434076839,
        "conclusion": "success",
    }:
        fail("pre-holdout historical regression identity drifted")
    actions = result.get("github_actions", {})
    if actions != {
        "workflow": "stage5-self-sufficiency-holdout",
        "run_id": 35434195939,
        "job_id": 105873992224,
        "conclusion": "success",
    }:
        fail("holdout Actions identity drifted")

    print("stage5.12f stream parser result: valid")
    print("development: pass")
    print("preregistered holdout: 12/12 pass")
    print("sharing refusals: Python=0 Go=0")
    print("normative Go CBN refusals: 18 (measurement-only)")
    print("candidate/contract/development/holdout Git blobs: unchanged")


if __name__ == "__main__":
    main()
