#!/usr/bin/env python3
"""Host-oracle validation for Stage 5.12 full-codec v0.3 preregistration.

Must remain independent of any v0.3 candidate builder or runtime execution.
"""
from __future__ import annotations

import json
from pathlib import Path

from validate_full_codec_contract import decode_status, encode_ast, encode_status, parse_tokens, parse_wire, tokens_of

ROOT = Path(__file__).resolve().parents[2]
SELF = ROOT / "stage5" / "selfhost"
CONTRACT = SELF / "full-codec-contract-v0.3.json"
MANIFEST = SELF / "full-codec-development-v0.3.json"
HOLDOUT = SELF / "full-codec-holdout-v0.3.json"
V02_DEV = SELF / "full-codec-development-v0.2.json"
V02_HOLD = SELF / "full-codec-holdout-v0.2.json"
V02_RESULT = SELF / "full-codec-development-result-v0.2.json"
REP = SELF / "meta-representation-v0.3.json"


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12 full-codec v0.3 preregistration invalid: {message}")


def input_key(category: str, case: dict):
    return (category, case.get("bits") if category != "encode_errors" else tuple(case.get("tokens", [])))


def validate_cases(data: dict, version: str, classification: str) -> set[tuple]:
    if data.get("schema") != "nex-selfhost-full-codec-workload" or data.get("version") != version:
        fail(f"{classification}: workload schema/version drifted")
    if data.get("classification") != classification:
        fail(f"{classification}: classification drifted")
    seen_ids = set()
    inputs = set()
    for case in data.get("valid_terms", []):
        cid = case["id"]
        if cid in seen_ids: fail(f"duplicate id {cid}")
        seen_ids.add(cid)
        bits = case["bits"]
        if decode_status(bits) != 0: fail(f"{cid}: valid wire rejected by oracle")
        ast, end = parse_wire(bits)
        if end != len(bits): fail(f"{cid}: trailing wire")
        tokens = tuple(case["tokens"])
        if tokens_of(ast) != tokens: fail(f"{cid}: token projection mismatch")
        ast2, end2 = parse_tokens(tokens)
        if end2 != len(tokens) or ast2 != ast or encode_ast(ast2) != bits:
            fail(f"{cid}: canonical round trip mismatch")
        key = input_key("valid_terms", case)
        if key in inputs: fail(f"duplicate valid input {cid}")
        inputs.add(key)
    for category, oracle in (("decode_errors", decode_status), ("encode_errors", encode_status)):
        for case in data.get(category, []):
            cid = case["id"]
            if cid in seen_ids: fail(f"duplicate id {cid}")
            seen_ids.add(cid)
            actual = oracle(case["bits"] if category == "decode_errors" else case["tokens"])
            if actual != case["expected_status"]:
                fail(f"{cid}: oracle status {actual} != {case['expected_status']}")
            key = input_key(category, case)
            if key in inputs: fail(f"duplicate error input {cid}")
            inputs.add(key)
    return inputs


def main() -> None:
    contract = json.loads(CONTRACT.read_text())
    manifest = json.loads(MANIFEST.read_text())
    holdout = json.loads(HOLDOUT.read_text())
    v02_dev = json.loads(V02_DEV.read_text())
    v02_hold = json.loads(V02_HOLD.read_text())
    v02_result = json.loads(V02_RESULT.read_text())
    rep = json.loads(REP.read_text())

    if contract.get("schema") != "nex-selfhost-full-codec-contract" or contract.get("version") != "0.3":
        fail("contract schema/version drifted")
    if contract.get("status") != "preregistered_before_full_codec_candidate_v0.3":
        fail("contract not frozen before v0.3 candidate")
    if rep.get("version") != "0.3" or rep.get("status") != "accepted-stage5.11-operational-representation":
        fail("Stage 5.11 representation prerequisite drifted")
    if v02_result.get("status") != "rejected_on_frozen_development_resource_refusal" or v02_result.get("decision") != "rejected":
        fail("v0.2 rejection not preserved")

    expected_interfaces = {
        "FiniteBits":"(N -> N) * N", "FiniteNatTokens":"(N -> N) * N",
        "CodecResult":"N * ((N -> N) * N)",
        "decodeTerm":"((N -> N) * N) -> (N * ((N -> N) * N))",
        "encodeTerm":"((N -> N) * N) -> (N * ((N -> N) * N))",
    }
    if contract.get("interfaces") != expected_interfaces: fail("interface drifted")
    if contract.get("status_codes") != {"Ok":0,"WireUnexpectedEOF":1,"WireTrailingData":2,"MalformedMeta":3}:
        fail("status codes drifted")
    budgets = contract.get("resource_budgets", {})
    if budgets.get("python_call_by_need") != {"max_transitions":5000000,"max_depth":8000}: fail("Python budget drifted")
    if budgets.get("go_call_by_need") != {"max_transitions":5000000,"max_depth":20000}: fail("Go need budget drifted")
    if budgets.get("go_normative_cbn", {}).get("max_transitions") != 5000000 or budgets.get("go_normative_cbn", {}).get("max_depth") != 20000:
        fail("Go CBN budget drifted")
    intent = contract.get("algorithmic_successor_intent", {})
    if any(intent.get(k) for k in ("representation_change","wire_change","resource_budget_change","core_change")):
        fail("v0.3 may not change representation/wire/budget/Core")

    if manifest.get("schema") != "nex-selfhost-full-codec-development-manifest" or manifest.get("version") != "0.3":
        fail("development manifest schema/version drifted")
    expected_sources = ["stage5/selfhost/full-codec-development-v0.2.json", "stage5/selfhost/full-codec-holdout-v0.2.json"]
    if manifest.get("sources") != expected_sources: fail("development provenance sources drifted")
    counts = manifest.get("expected_counts")
    actual_counts = {
        "valid_terms": len(v02_dev["valid_terms"]) + len(v02_hold["valid_terms"]),
        "decode_errors": len(v02_dev["decode_errors"]) + len(v02_hold["decode_errors"]),
        "encode_errors": len(v02_dev["encode_errors"]) + len(v02_hold["encode_errors"]),
    }
    if counts != actual_counts or counts != {"valid_terms":24,"decode_errors":12,"encode_errors":12}:
        fail(f"development manifest counts drifted: {actual_counts}")
    compact = manifest.get("observation_compaction", {})
    if compact.get("valid_term_evaluations") != ["decode","encode","law1","law2"] or compact.get("semantic_coverage_change") is not False:
        fail("observation compaction contract drifted")

    known_inputs = set()
    # These are already oracle-validated by the v0.2 validator; still collect exact inputs.
    for data in (v02_dev, v02_hold):
        for category in ("valid_terms","decode_errors","encode_errors"):
            for case in data[category]:
                known_inputs.add(input_key(category, case))

    hold_inputs = validate_cases(holdout, "0.3", "holdout")
    overlap = known_inputs & hold_inputs
    if overlap: fail(f"v0.3 holdout overlaps known prior input(s): {sorted(map(str, overlap))}")
    if (len(holdout["valid_terms"]), len(holdout["decode_errors"]), len(holdout["encode_errors"])) != (7,3,3):
        fail("v0.3 holdout counts drifted")

    frozen = contract.get("bounded_exhaustive_class", {})
    if frozen.get("maximum_ast_nodes") != 3 or frozen.get("expected_term_count") != 27:
        fail("bounded exhaustive class drifted")

    print("stage5.12 full-codec v0.3 preregistration: host-oracle valid and frozen")
    print("v0.2 rejection: preserved")
    print("development manifest: exact v0.2 development + known v0.2 holdout = 24 valid + 12 + 12 errors")
    print("observation compaction: 4 compound success evaluations per valid term, no semantic coverage change")
    print("v0.3 holdout: 7 valid + 3 decode errors + 3 encode errors, input-disjoint from all known prior workloads")
    print("representation/wire/Core/budgets: unchanged")
    print("v0.3 candidate execution: NOT PERFORMED")


if __name__ == "__main__":
    main()
