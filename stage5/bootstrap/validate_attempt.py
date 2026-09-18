#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ATTEMPT = ROOT / "stage5/bootstrap/attempt-v0.1.json"
CHECKPOINT = ROOT / "stage5/independent-checkpoints/python-v0.1.json"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    attempt = json.loads(ATTEMPT.read_text(encoding="utf-8"))
    checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))

    if attempt.get("schema") != "nex-stage5-bootstrap-attempt-v0.1":
        fail("unexpected bootstrap-attempt schema")

    contract = attempt.get("acceptance_contract", {})
    required = {
        "requires_exact_versioned_profile",
        "requires_finite_transmitted_artifact",
        "requires_exact_bit_length",
        "requires_dependency_closure",
        "requires_receiver_neutral_profile",
        "requires_verified_nex_wire_static_dynamic_scope",
        "host_source_size_is_not_bootstrap",
    }
    if set(contract) != required or not all(contract.values()):
        fail("acceptance contract is incomplete or weakened")

    candidates = attempt.get("candidates", [])
    if {c.get("id") for c in candidates} != {
        "a1-recursive-rule-description",
        "a2-blc-machine-candidate",
        "host-python-control",
    }:
        fail("unexpected candidate set")

    accepted = []
    for candidate in candidates:
        status = candidate.get("status")
        bits = candidate.get("accepted_bootstrap_bits")
        if status == "accepted":
            checks = [
                candidate.get("receiver_neutral") is True,
                candidate.get("finite_artifact") is True,
                isinstance(candidate.get("exact_bit_length"), int),
                candidate.get("dependency_closure_complete") is True,
                candidate.get("verified_nex_wire_static_dynamic_scope") is True,
                isinstance(bits, int),
                bits == candidate.get("exact_bit_length"),
            ]
            if not all(checks):
                fail(f"accepted candidate violates acceptance contract: {candidate['id']}")
            accepted.append(candidate)
        elif bits is not None:
            fail(f"non-accepted candidate publishes bootstrap bits: {candidate['id']}")

    host = next(c for c in candidates if c["id"] == "host-python-control")
    if host.get("receiver_neutral") is not False or host.get("status") != "engineering_control_only":
        fail("host control must remain explicitly non-neutral")

    files = checkpoint.get("files", [])
    total_author_bytes = sum(int(item["bytes"]) for item in files)
    nex_package_bytes = sum(
        int(item["bytes"])
        for item in files
        if item["path"].startswith("independent/python/nex/")
    )
    if total_author_bytes != host.get("frozen_author_written_checkpoint_bytes"):
        fail("host checkpoint byte total drifted")
    if nex_package_bytes != host.get("frozen_nex_package_source_bytes"):
        fail("host NEX package byte total drifted")

    result = attempt.get("result", {})
    if result.get("accepted_full_bootstrap_candidates") != len(accepted):
        fail("accepted candidate count mismatch")
    if accepted:
        fail("v0.1 audit is expected to remain a negative result")
    if result.get("full_bootstrap_cost_known") is not False:
        fail("bootstrap cost must remain unknown")
    if result.get("total_C_computable") is not False:
        fail("total C must remain non-computable")
    if result.get("classification") != "negative_result":
        fail("audit must be classified as a negative result")

    print("bootstrap feasibility audit verified")
    print(f"accepted full bootstrap candidates: {len(accepted)}")
    print(f"Python host control NEX package bytes: {nex_package_bytes}")
    print(f"Python host control frozen author-written bytes: {total_author_bytes}")
    print("full B | A known: false")
    print("total C | A computable: false")


if __name__ == "__main__":
    main()
