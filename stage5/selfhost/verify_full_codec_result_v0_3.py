#!/usr/bin/env python3
"""Validate the frozen Stage 5.12 full-codec v0.3 evidence without rerunning holdout."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SELF = ROOT / "stage5" / "selfhost"
PRE = SELF / "full-codec-preholdout-result-v0.3.json"
RESULT = SELF / "full-codec-holdout-result-v0.3.json"
ART = SELF / "full-codec-v0.3.json"
CONTRACT = SELF / "full-codec-contract-v0.3.json"
DEV = SELF / "full-codec-development-v0.3.json"
HOLD = SELF / "full-codec-holdout-v0.3.json"
GEN = SELF / "build_full_codec_v0_3.py"


def fail(message: str) -> None:
    raise SystemExit("stage5.12 full codec v0.3 result verification failed: " + message)


def blob(path: Path) -> str:
    run = subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if run.returncode:
        fail(f"cannot hash {path.name}: {run.stderr.strip()}")
    return run.stdout.strip()


def main() -> None:
    pre = json.loads(PRE.read_text(encoding="utf-8"))
    result = json.loads(RESULT.read_text(encoding="utf-8"))

    if pre.get("schema") != "nex-selfhost-full-codec-preholdout-result":
        fail("preholdout schema mismatch")
    if pre.get("version") != "0.3" or pre.get("status") != "development_and_exhaustive_passed_candidate_frozen":
        fail("preholdout identity/status mismatch")
    if not pre.get("pre_holdout_historical_regression", {}).get("passed"):
        fail("preholdout historical regression is not recorded as passed")
    if pre.get("holdout_status") != "preregistered_unexecuted":
        fail("preholdout record must preserve unexecuted holdout state")

    if result.get("schema") != "nex-selfhost-full-codec-holdout-result":
        fail("holdout result schema mismatch")
    if result.get("version") != "0.3" or result.get("status") != "accepted_on_preregistered_holdout":
        fail("holdout result identity/status mismatch")
    if result.get("decision") != "accepted":
        fail("holdout result decision is not accepted")

    frozen = pre.get("frozen_git_blobs", {})
    expected = {
        GEN: frozen.get("generator"),
        ART: frozen.get("candidate_artifact"),
        CONTRACT: frozen.get("contract"),
        DEV: frozen.get("development_manifest"),
        HOLD: frozen.get("holdout_workload"),
    }
    for path, expected_blob in expected.items():
        actual = blob(path)
        if not expected_blob or actual != expected_blob:
            fail(f"{path.name}: blob {actual} != frozen {expected_blob}")

    result_frozen = result.get("frozen_git_blobs", {})
    for key in ("generator", "candidate_artifact", "contract", "development_manifest", "holdout_workload"):
        if result_frozen.get(key) != frozen.get(key):
            fail(f"result/preholdout frozen identity mismatch for {key}")

    development = pre.get("development", {})
    if development.get("python_need_resource_refusals") != 0 or development.get("go_need_resource_refusals") != 0:
        fail("development sharing refusal recorded")
    if development.get("python_go_need_values_matched") != 120 or development.get("python_go_need_values_total") != 120:
        fail("development differential count mismatch")
    exhaustive = pre.get("bounded_exhaustive", {})
    if exhaustive.get("complete_terms") != 27:
        fail("bounded exhaustive term count mismatch")
    if exhaustive.get("nex_python_go_need_values_matched") != 108 or exhaustive.get("nex_python_go_need_values_total") != 108:
        fail("bounded exhaustive differential count mismatch")

    surface = result.get("holdout_surface", {})
    if (surface.get("valid_terms"), surface.get("decode_error_cases"), surface.get("encode_error_cases")) != (7, 3, 3):
        fail("holdout surface count mismatch")
    if surface.get("compound_forced_nat_observations") != 34 or surface.get("round_trip_law_valid_terms") != 7:
        fail("holdout observation/law count mismatch")
    observed = result.get("results", {})
    if observed.get("python_need_resource_refusals") != 0 or observed.get("go_need_resource_refusals") != 0:
        fail("holdout sharing refusal recorded")
    if observed.get("python_go_need_values_matched") != 34 or observed.get("python_go_need_values_total") != 34:
        fail("holdout differential count mismatch")
    if int(observed.get("largest_python_need_transitions", 5_000_001)) > 5_000_000:
        fail("holdout Python need transition budget exceeded")
    if int(observed.get("largest_go_need_transitions", 5_000_001)) > 5_000_000:
        fail("holdout Go need transition budget exceeded")

    print("stage5.12 full codec v0.3 frozen result: verified")
    print("development: 120/120 need matches, no sharing refusals")
    print("bounded exhaustive: 27/27 terms, 108/108 need matches")
    print("one-shot holdout: 34/34 need matches, no sharing refusals")
    print(f"holdout Go CBN resource refusals preserved: {observed.get('go_cbn_resource_refusals')}")


if __name__ == "__main__":
    main()
