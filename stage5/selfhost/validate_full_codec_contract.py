#!/usr/bin/env python3
"""Validate the Stage 5.12 full Term-codec contract before candidate execution.

This is a host-side preregistration/oracle check. It deliberately does not import,
build, or execute any future NEX decodeTerm/encodeTerm candidate.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "stage5" / "selfhost" / "full-codec-contract-v0.1.json"
DEVELOPMENT = ROOT / "stage5" / "selfhost" / "full-codec-development-v0.1.json"
HOLDOUT = ROOT / "stage5" / "selfhost" / "full-codec-holdout-v0.1.json"
REPRESENTATION = ROOT / "stage5" / "selfhost" / "meta-representation-v0.3.json"
PROTOCOL = ROOT / "stage5" / "selfhost" / "experiment-protocol-v0.1.json"


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12 full-codec preregistration invalid: {message}")


def u(n: int) -> str:
    b = f"{n + 1:b}"
    return "0" * (len(b) - 1) + b


def encode_ast(ast) -> str:
    tag = ast[0]
    if tag == 0:
        return "00" + u(ast[1])
    if tag == 1:
        return "01" + encode_ast(ast[1])
    if tag == 2:
        return "10" + encode_ast(ast[1]) + encode_ast(ast[2])
    if tag == 3:
        return "110" + encode_ast(ast[1]) + encode_ast(ast[2])
    if tag == 4:
        return "1110" + u(ast[1])
    if tag == 5:
        return "1111" + u(ast[1])
    raise ValueError(f"unknown AST tag {tag}")


def tokens_of(ast) -> tuple[int, ...]:
    tag = ast[0]
    if tag in (0, 4, 5):
        return (tag, ast[1])
    if tag == 1:
        return (1,) + tokens_of(ast[1])
    if tag in (2, 3):
        return (tag,) + tokens_of(ast[1]) + tokens_of(ast[2])
    raise ValueError(tag)


def parse_u(bits: str, pos: int) -> tuple[int, int]:
    zeros = 0
    while True:
        if pos >= len(bits):
            raise EOFError
        bit = bits[pos]
        pos += 1
        if bit == "1":
            break
        if bit != "0":
            raise ValueError("non-bit")
        zeros += 1
    value = 1
    for _ in range(zeros):
        if pos >= len(bits):
            raise EOFError
        bit = bits[pos]
        pos += 1
        if bit not in "01":
            raise ValueError("non-bit")
        value = value * 2 + int(bit)
    return value - 1, pos


def parse_wire(bits: str, pos: int = 0):
    def take() -> str:
        nonlocal pos
        if pos >= len(bits):
            raise EOFError
        ch = bits[pos]
        pos += 1
        if ch not in "01":
            raise ValueError("non-bit")
        return ch

    a = take()
    b = take()
    if a == "0" and b == "0":
        n, pos2 = parse_u(bits, pos)
        return (0, n), pos2
    if a == "0" and b == "1":
        child, end = parse_wire(bits, pos)
        return (1, child), end
    if a == "1" and b == "0":
        left, mid = parse_wire(bits, pos)
        right, end = parse_wire(bits, mid)
        return (2, left, right), end
    c = take()
    if c == "0":
        left, mid = parse_wire(bits, pos)
        right, end = parse_wire(bits, mid)
        return (3, left, right), end
    d = take()
    n, end = parse_u(bits, pos)
    return ((4, n) if d == "0" else (5, n)), end


def parse_tokens(tokens: tuple[int, ...], pos: int = 0):
    if pos >= len(tokens):
        raise EOFError
    tag = tokens[pos]
    pos += 1
    if tag in (0, 4, 5):
        if pos >= len(tokens):
            raise EOFError
        return (tag, tokens[pos]), pos + 1
    if tag == 1:
        child, end = parse_tokens(tokens, pos)
        return (1, child), end
    if tag in (2, 3):
        left, mid = parse_tokens(tokens, pos)
        right, end = parse_tokens(tokens, mid)
        return (tag, left, right), end
    raise ValueError(f"unknown tag {tag}")


def decode_status(bits: str) -> int:
    try:
        _, end = parse_wire(bits)
    except EOFError:
        return 1
    except ValueError:
        return 3
    return 0 if end == len(bits) else 2


def encode_status(tokens: list[int]) -> int:
    if any(not isinstance(v, int) or v < 0 for v in tokens):
        return 3
    try:
        _, end = parse_tokens(tuple(tokens))
    except (EOFError, ValueError):
        return 3
    return 0 if end == len(tokens) else 3


@lru_cache(maxsize=None)
def exhaustive_terms(nodes: int):
    if nodes == 1:
        return ((0, 0), (4, 0), (5, 0))
    if nodes <= 0:
        return tuple()
    out = [(1, child) for child in exhaustive_terms(nodes - 1)]
    for left_nodes in range(1, nodes - 1):
        right_nodes = nodes - 1 - left_nodes
        for left in exhaustive_terms(left_nodes):
            for right in exhaustive_terms(right_nodes):
                out.append((2, left, right))
                out.append((3, left, right))
    return tuple(out)


def validate_workload(data: dict, classification: str, expected_status: str) -> set[str]:
    if data.get("schema") != "nex-selfhost-full-codec-workload" or data.get("version") != "0.1":
        fail(f"{classification}: workload schema/version drifted")
    if data.get("classification") != classification or data.get("status") != expected_status:
        fail(f"{classification}: classification/status drifted")
    ids: set[str] = set()
    for case in data.get("valid_terms", []):
        cid = case["id"]
        if cid in ids:
            fail(f"{classification}: duplicate id {cid}")
        ids.add(cid)
        bits = case["bits"]
        if any(ch not in "01" for ch in bits):
            fail(f"{classification}:{cid}: non-bit input")
        if decode_status(bits) != 0:
            fail(f"{classification}:{cid}: valid wire does not decode exactly")
        ast, end = parse_wire(bits)
        if end != len(bits):
            fail(f"{classification}:{cid}: valid wire has trailing data")
        tokens = tuple(case["tokens"])
        if tokens_of(ast) != tokens:
            fail(f"{classification}:{cid}: tokens do not match wire AST")
        ast2, end2 = parse_tokens(tokens)
        if end2 != len(tokens) or ast2 != ast:
            fail(f"{classification}:{cid}: token grammar round trip failed")
        if encode_ast(ast2) != bits:
            fail(f"{classification}:{cid}: canonical wire reconstruction failed")
    for case in data.get("decode_errors", []):
        cid = case["id"]
        if cid in ids:
            fail(f"{classification}: duplicate id {cid}")
        ids.add(cid)
        actual = decode_status(case["bits"])
        if actual != case["expected_status"]:
            fail(f"{classification}:{cid}: decode status {actual} != {case['expected_status']}")
    for case in data.get("encode_errors", []):
        cid = case["id"]
        if cid in ids:
            fail(f"{classification}: duplicate id {cid}")
        ids.add(cid)
        actual = encode_status(case["tokens"])
        if actual != case["expected_status"]:
            fail(f"{classification}:{cid}: encode status {actual} != {case['expected_status']}")
    return ids


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    development = json.loads(DEVELOPMENT.read_text(encoding="utf-8"))
    holdout = json.loads(HOLDOUT.read_text(encoding="utf-8"))
    representation = json.loads(REPRESENTATION.read_text(encoding="utf-8"))
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))

    if contract.get("schema") != "nex-selfhost-full-codec-contract" or contract.get("version") != "0.1":
        fail("contract schema/version drifted")
    if contract.get("status") != "preregistered_before_full_codec_candidate_v0.1":
        fail("contract must remain preregistered before candidate v0.1")
    if representation.get("version") != "0.3" or representation.get("status") != "accepted-stage5.11-operational-representation":
        fail("Stage 5.11 v0.3 is not the accepted prerequisite")
    interfaces = contract.get("interfaces", {})
    expected_interfaces = {
        "FiniteBits": "(N -> N) * N",
        "FiniteNatTokens": "(N -> N) * N",
        "CodecResult": "N * ((N -> N) * N)",
        "decodeTerm": "((N -> N) * N) -> (N * ((N -> N) * N))",
        "encodeTerm": "((N -> N) * N) -> (N * ((N -> N) * N))",
    }
    if interfaces != expected_interfaces:
        fail("full-codec interface drifted")
    if contract.get("status_codes") != {"Ok": 0, "WireUnexpectedEOF": 1, "WireTrailingData": 2, "MalformedMeta": 3}:
        fail("status code contract drifted")
    budgets = contract.get("resource_budgets", {})
    if budgets.get("python_call_by_need") != {"max_transitions": 5000000, "max_depth": 8000}:
        fail("Python need budget drifted")
    if budgets.get("go_call_by_need") != {"max_transitions": 5000000, "max_depth": 20000}:
        fail("Go need budget drifted")
    if budgets.get("go_normative_cbn", {}).get("max_transitions") != 5000000 or budgets.get("go_normative_cbn", {}).get("max_depth") != 20000:
        fail("Go CBN budget drifted")
    if "opaque original wire" not in contract.get("success_contract", {}).get("decodeTerm", ""):
        fail("decodeTerm identity-shortcut prohibition missing")

    dev_ids = validate_workload(development, "development", "frozen_before_full_codec_candidate_v0.1")
    hold_ids = validate_workload(holdout, "holdout", "preregistered_unexecuted")
    if dev_ids & hold_ids:
        fail(f"development/holdout IDs overlap: {sorted(dev_ids & hold_ids)}")

    exhaustive = contract.get("bounded_exhaustive_class", {})
    generated = tuple(term for nodes in range(1, 4) for term in exhaustive_terms(nodes))
    if exhaustive.get("expected_term_count") != len(generated) or len(generated) != 27:
        fail(f"bounded exhaustive class count is {len(generated)}, expected 27")
    token_keys = {tokens_of(term) for term in generated}
    wire_keys = {encode_ast(term) for term in generated}
    if len(token_keys) != 27 or len(wire_keys) != 27:
        fail("bounded exhaustive class has a token/wire collision")

    print("stage5.12 full-codec contract/workloads: preregistered and host-oracle valid")
    print(f"development: {len(development['valid_terms'])} valid + {len(development['decode_errors'])} decode errors + {len(development['encode_errors'])} encode errors")
    print(f"holdout: {len(holdout['valid_terms'])} valid + {len(holdout['decode_errors'])} decode errors + {len(holdout['encode_errors'])} encode errors (candidate unexecuted)")
    print("bounded exhaustive class: 27 complete Terms (1..3 AST nodes)")
    print("candidate execution: NOT PERFORMED")


if __name__ == "__main__":
    main()
