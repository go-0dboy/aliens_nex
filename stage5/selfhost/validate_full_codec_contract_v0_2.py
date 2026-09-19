#!/usr/bin/env python3
"""Validate Stage 5.12 full-codec v0.2 preregistration before candidate code exists.

This host-only validator deliberately does not import, build, or execute any
full-codec v0.2 candidate. It proves that v0.2 retains all observed v0.1
inputs as development evidence and that its new holdout is disjoint by input.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SELFHOST = ROOT / "stage5" / "selfhost"
sys.path.insert(0, str(SELFHOST))

from validate_full_codec_contract import (  # noqa: E402
    decode_status,
    encode_ast,
    encode_status,
    exhaustive_terms,
    parse_tokens,
    parse_wire,
    tokens_of,
)

CONTRACT = SELFHOST / "full-codec-contract-v0.2.json"
DEVELOPMENT = SELFHOST / "full-codec-development-v0.2.json"
HOLDOUT = SELFHOST / "full-codec-holdout-v0.2.json"
V1_DEVELOPMENT = SELFHOST / "full-codec-development-v0.1.json"
V1_HOLDOUT = SELFHOST / "full-codec-holdout-v0.1.json"
V1_RESULT = SELFHOST / "full-codec-holdout-result-v0.1.json"
REPRESENTATION = SELFHOST / "meta-representation-v0.3.json"
PROTOCOL = SELFHOST / "experiment-protocol-v0.1.json"


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12 full-codec v0.2 preregistration invalid: {message}")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def case_key(kind: str, case: dict):
    if kind == "valid_terms":
        return (case["bits"], tuple(case["tokens"]))
    if kind == "decode_errors":
        return (case["bits"], int(case["expected_status"]))
    if kind == "encode_errors":
        return (tuple(case["tokens"]), int(case["expected_status"]))
    raise AssertionError(kind)


def input_key(kind: str, case: dict):
    if kind in ("valid_terms", "decode_errors"):
        return ("bits", case["bits"])
    return ("tokens", tuple(case["tokens"]))


def validate_workload(data: dict, classification: str, status: str) -> None:
    if data.get("schema") != "nex-selfhost-full-codec-workload" or data.get("version") != "0.2":
        fail(f"{classification}: schema/version drifted")
    if data.get("classification") != classification or data.get("status") != status:
        fail(f"{classification}: classification/status drifted")

    ids: set[str] = set()
    inputs: set[tuple] = set()
    for case in data.get("valid_terms", []):
        cid = case["id"]
        if cid in ids:
            fail(f"{classification}: duplicate id {cid}")
        ids.add(cid)
        ik = input_key("valid_terms", case)
        if ik in inputs:
            fail(f"{classification}: duplicate valid input {cid}")
        inputs.add(ik)
        bits = case["bits"]
        if any(ch not in "01" for ch in bits):
            fail(f"{classification}:{cid}: non-bit wire")
        if decode_status(bits) != 0:
            fail(f"{classification}:{cid}: declared valid wire is not exact")
        ast, end = parse_wire(bits)
        if end != len(bits):
            fail(f"{classification}:{cid}: valid wire has trailing data")
        tokens = tuple(case["tokens"])
        if tokens_of(ast) != tokens:
            fail(f"{classification}:{cid}: tokens disagree with decoded AST")
        ast2, end2 = parse_tokens(tokens)
        if end2 != len(tokens) or ast2 != ast:
            fail(f"{classification}:{cid}: token grammar round trip failed")
        if encode_ast(ast2) != bits:
            fail(f"{classification}:{cid}: canonical reconstruction mismatch")

    for case in data.get("decode_errors", []):
        cid = case["id"]
        if cid in ids:
            fail(f"{classification}: duplicate id {cid}")
        ids.add(cid)
        ik = input_key("decode_errors", case)
        if ik in inputs:
            fail(f"{classification}: duplicate decode input {cid}")
        inputs.add(ik)
        actual = decode_status(case["bits"])
        if actual != case["expected_status"]:
            fail(f"{classification}:{cid}: decode status {actual} != {case['expected_status']}")

    for case in data.get("encode_errors", []):
        cid = case["id"]
        if cid in ids:
            fail(f"{classification}: duplicate id {cid}")
        ids.add(cid)
        ik = input_key("encode_errors", case)
        if ik in inputs:
            fail(f"{classification}: duplicate encode input {cid}")
        inputs.add(ik)
        actual = encode_status(case["tokens"])
        if actual != case["expected_status"]:
            fail(f"{classification}:{cid}: encode status {actual} != {case['expected_status']}")


def require_all_predecessor_cases(v2dev: dict, predecessor: dict, label: str) -> None:
    for kind in ("valid_terms", "decode_errors", "encode_errors"):
        actual = {case_key(kind, case) for case in v2dev.get(kind, [])}
        for case in predecessor.get(kind, []):
            key = case_key(kind, case)
            if key not in actual:
                fail(f"v0.2 development omits {label}:{kind}:{case['id']}")


def all_inputs(data: dict) -> set[tuple]:
    out: set[tuple] = set()
    for kind in ("valid_terms", "decode_errors", "encode_errors"):
        for case in data.get(kind, []):
            out.add(input_key(kind, case))
    return out


def main() -> None:
    contract = load(CONTRACT)
    development = load(DEVELOPMENT)
    holdout = load(HOLDOUT)
    v1dev = load(V1_DEVELOPMENT)
    v1hold = load(V1_HOLDOUT)
    v1result = load(V1_RESULT)
    representation = load(REPRESENTATION)
    protocol = load(PROTOCOL)

    if contract.get("schema") != "nex-selfhost-full-codec-contract" or contract.get("version") != "0.2":
        fail("contract schema/version drifted")
    if contract.get("status") != "preregistered_before_full_codec_candidate_v0.2":
        fail("contract must remain preregistered before candidate v0.2")
    if v1result.get("status") != "rejected_on_preregistered_holdout" or v1result.get("decision") != "rejected":
        fail("v0.1 rejection is not durably recorded")
    failure = v1result.get("failure", {})
    if failure.get("case") != "law2:deepmixed:stream" or failure.get("observed") != 5000001 or failure.get("limit") != 5000000:
        fail("v0.1 frozen failure record drifted")
    if representation.get("version") != "0.3" or representation.get("status") != "accepted-stage5.11-operational-representation":
        fail("accepted Stage 5.11 v0.3 prerequisite drifted")

    expected_interfaces = {
        "FiniteBits": "(N -> N) * N",
        "FiniteNatTokens": "(N -> N) * N",
        "CodecResult": "N * ((N -> N) * N)",
        "decodeTerm": "((N -> N) * N) -> (N * ((N -> N) * N))",
        "encodeTerm": "((N -> N) * N) -> (N * ((N -> N) * N))",
    }
    if contract.get("interfaces") != expected_interfaces:
        fail("v0.2 changed the full-codec interface")
    if contract.get("status_codes") != {"Ok": 0, "WireUnexpectedEOF": 1, "WireTrailingData": 2, "MalformedMeta": 3}:
        fail("v0.2 status codes drifted")

    budgets = contract.get("resource_budgets", {})
    if budgets.get("python_call_by_need") != {"max_transitions": 5000000, "max_depth": 8000}:
        fail("Python need budget changed")
    if budgets.get("go_call_by_need") != {"max_transitions": 5000000, "max_depth": 20000}:
        fail("Go need budget changed")
    if budgets.get("go_normative_cbn", {}).get("max_transitions") != 5000000 or budgets.get("go_normative_cbn", {}).get("max_depth") != 20000:
        fail("Go CBN budget changed")
    if protocol.get("resource_budgets", {}).get("python_call_by_need") != budgets.get("python_call_by_need"):
        fail("v0.2 Python budget differs from global frozen protocol")
    if protocol.get("resource_budgets", {}).get("go_call_by_need") != budgets.get("go_call_by_need"):
        fail("v0.2 Go need budget differs from global frozen protocol")
    if contract.get("algorithmic_successor_intent", {}).get("representation_change") is not False:
        fail("v0.2 preregistration must not change representation")
    if contract.get("algorithmic_successor_intent", {}).get("wire_change") is not False:
        fail("v0.2 preregistration must not change canonical wire")
    if "opaque original wire" not in contract.get("success_contract", {}).get("decodeTerm", ""):
        fail("anti-identity rule missing")

    validate_workload(development, "development", "frozen_before_full_codec_candidate_v0.2")
    validate_workload(holdout, "holdout", "preregistered_unexecuted")

    require_all_predecessor_cases(development, v1dev, "v0.1-development")
    require_all_predecessor_cases(development, v1hold, "revealed-v0.1-holdout")

    if len(development.get("valid_terms", [])) != 17 or len(development.get("decode_errors", [])) != 9 or len(development.get("encode_errors", [])) != 9:
        fail("v0.2 development expected 17 valid + 9 decode + 9 encode cases")
    if len(holdout.get("valid_terms", [])) != 7 or len(holdout.get("decode_errors", [])) != 3 or len(holdout.get("encode_errors", [])) != 3:
        fail("v0.2 holdout expected 7 valid + 3 decode + 3 encode cases")

    dev_inputs = all_inputs(development)
    hold_inputs = all_inputs(holdout)
    overlap = dev_inputs & hold_inputs
    if overlap:
        fail(f"v0.2 development/holdout inputs overlap: {sorted(map(str, overlap))}")

    generated = tuple(term for nodes in range(1, 4) for term in exhaustive_terms(nodes))
    bounded = contract.get("bounded_exhaustive_class", {})
    if bounded.get("expected_term_count") != 27 or len(generated) != 27:
        fail("bounded exhaustive class changed")
    if bounded.get("leaf_set") != ["Var(0)", "Nat(0)", "Prim(0)"]:
        fail("bounded exhaustive leaf set changed")
    if len({tokens_of(t) for t in generated}) != 27 or len({encode_ast(t) for t in generated}) != 27:
        fail("bounded exhaustive class collision")

    # The exact v0.1 holdout failure must now be an ordinary v0.2 development case.
    deep = [c for c in development["valid_terms"] if c["id"] == "deepmixed"]
    if len(deep) != 1 or deep[0]["bits"] != "100110001111000001001011011100111111010":
        fail("revealed deepmixed failure is not frozen in v0.2 development")

    print("stage5.12 full-codec v0.2 preregistration: host-oracle valid and frozen")
    print("v0.1 rejected holdout: preserved as historical/development evidence")
    print("v0.2 development: 17 valid + 9 decode errors + 9 encode errors")
    print("v0.2 holdout: 7 valid + 3 decode errors + 3 encode errors, disjoint by input")
    print("bounded exhaustive class: unchanged 27 Terms (1..3 AST nodes)")
    print("resource budgets/interface/wire/representation: unchanged")
    print("v0.2 candidate execution: NOT PERFORMED")


if __name__ == "__main__":
    main()
