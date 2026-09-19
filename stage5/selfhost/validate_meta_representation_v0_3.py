#!/usr/bin/env python3
"""Validate the Stage 5.11 operational meta-representation v0.3.

This validator is deliberately host-side evidence for the representation
contract. It does not implement Stage 5.12 encodeTerm/decodeTerm in NEX.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "stage5" / "selfhost" / "meta-representation-v0.2.json"
V3 = ROOT / "stage5" / "selfhost" / "meta-representation-v0.3.json"

REQUIRED_REPRESENTATIONS = {
    "Bits",
    "Term",
    "Type",
    "Scheme",
    "Substitution",
    "TypeEnvironment",
    "PortableObservation",
    "StaticResult",
    "ToolRequest",
    "ToolResult",
}


def fail(message: str) -> None:
    raise SystemExit(f"stage5.11 meta-representation v0.3 invalid: {message}")


def u(n: int) -> str:
    if n < 0:
        fail("U(n) received a negative integer")
    binary = f"{n + 1:b}"
    return "0" * (len(binary) - 1) + binary


def parse_term(tokens: tuple[int, ...], pos: int = 0):
    if pos >= len(tokens):
        raise ValueError("truncated Term tokens")
    tag = tokens[pos]
    pos += 1
    if tag in (0, 4, 5):
        if pos >= len(tokens):
            raise ValueError("truncated Term payload")
        value = tokens[pos]
        return (tag, value), pos + 1
    if tag == 1:
        body, pos = parse_term(tokens, pos)
        return (tag, body), pos
    if tag in (2, 3):
        left, pos = parse_term(tokens, pos)
        right, pos = parse_term(tokens, pos)
        return (tag, left, right), pos
    raise ValueError(f"unknown Term tag {tag}")


def term_tokens(ast) -> tuple[int, ...]:
    tag = ast[0]
    if tag in (0, 4, 5):
        return (tag, ast[1])
    if tag == 1:
        return (1,) + term_tokens(ast[1])
    if tag in (2, 3):
        return (tag,) + term_tokens(ast[1]) + term_tokens(ast[2])
    raise ValueError(f"bad Term AST tag {tag}")


def term_wire(ast) -> str:
    tag = ast[0]
    if tag == 0:
        return "00" + u(ast[1])
    if tag == 1:
        return "01" + term_wire(ast[1])
    if tag == 2:
        return "10" + term_wire(ast[1]) + term_wire(ast[2])
    if tag == 3:
        return "110" + term_wire(ast[1]) + term_wire(ast[2])
    if tag == 4:
        return "1110" + u(ast[1])
    if tag == 5:
        return "1111" + u(ast[1])
    raise ValueError(f"bad Term AST tag {tag}")


def parse_type(tokens: tuple[int, ...], pos: int = 0):
    if pos >= len(tokens):
        raise ValueError("truncated Type tokens")
    tag = tokens[pos]
    pos += 1
    if tag == 0:
        if pos >= len(tokens):
            raise ValueError("truncated TypeVar payload")
        return (0, tokens[pos]), pos + 1
    if tag in (1, 2):
        return (tag,), pos
    if tag in (3, 4, 5):
        left, pos = parse_type(tokens, pos)
        right, pos = parse_type(tokens, pos)
        return (tag, left, right), pos
    raise ValueError(f"unknown Type tag {tag}")


def parse_scheme(tokens: tuple[int, ...], pos: int = 0):
    if pos >= len(tokens):
        raise ValueError("truncated Scheme")
    count = tokens[pos]
    pos += 1
    if pos + count > len(tokens):
        raise ValueError("truncated Scheme binder list")
    ids = tokens[pos : pos + count]
    pos += count
    if any(a >= b for a, b in zip(ids, ids[1:])):
        raise ValueError("Scheme bound IDs are not strictly ascending")
    body, pos = parse_type(tokens, pos)
    return (ids, body), pos


def parse_substitution(tokens: tuple[int, ...], pos: int = 0):
    if pos >= len(tokens):
        raise ValueError("truncated Substitution")
    count = tokens[pos]
    pos += 1
    bindings = []
    for _ in range(count):
        if pos >= len(tokens):
            raise ValueError("truncated Substitution key")
        key = tokens[pos]
        pos += 1
        value, pos = parse_type(tokens, pos)
        bindings.append((key, value))
    keys = [key for key, _ in bindings]
    if any(a >= b for a, b in zip(keys, keys[1:])):
        raise ValueError("Substitution keys are not strictly ascending")
    return tuple(bindings), pos


def parse_environment(tokens: tuple[int, ...], pos: int = 0):
    if pos >= len(tokens):
        raise ValueError("truncated TypeEnvironment")
    count = tokens[pos]
    pos += 1
    schemes = []
    for _ in range(count):
        scheme, pos = parse_scheme(tokens, pos)
        schemes.append(scheme)
    return tuple(schemes), pos


def parse_observation(tokens: tuple[int, ...], pos: int = 0):
    if pos >= len(tokens):
        raise ValueError("truncated PortableObservation")
    tag = tokens[pos]
    pos += 1
    if tag == 0:
        if pos >= len(tokens):
            raise ValueError("truncated Nat observation")
        return (0, tokens[pos]), pos + 1
    if tag in (1, 5):
        return (tag,), pos
    if tag == 2:
        left, pos = parse_observation(tokens, pos)
        right, pos = parse_observation(tokens, pos)
        return (2, left, right), pos
    if tag in (3, 4):
        payload, pos = parse_observation(tokens, pos)
        return (tag, payload), pos
    raise ValueError(f"unknown observation tag {tag}")


def require_exact_parser(name: str, tokens: list[int], parser) -> None:
    if any(not isinstance(value, int) or value < 0 for value in tokens):
        fail(f"{name} contains a non-natural token")
    try:
        _, end = parser(tuple(tokens), 0)
    except ValueError as exc:
        fail(f"{name} does not parse: {exc}")
    if end != len(tokens):
        fail(f"{name} has trailing tokens at {end}/{len(tokens)}")


@lru_cache(maxsize=None)
def terms_with_nodes(nodes: int):
    if nodes <= 0:
        return tuple()
    if nodes == 1:
        return tuple(
            [(0, 0), (0, 1), (4, 0), (4, 2), (5, 0), (5, 10)]
        )
    result = []
    for child in terms_with_nodes(nodes - 1):
        result.append((1, child))
    for left_nodes in range(1, nodes - 1):
        right_nodes = nodes - 1 - left_nodes
        for left in terms_with_nodes(left_nodes):
            for right in terms_with_nodes(right_nodes):
                result.append((2, left, right))
                result.append((3, left, right))
    return tuple(result)


def main() -> None:
    old = json.loads(V2.read_text(encoding="utf-8"))
    new = json.loads(V3.read_text(encoding="utf-8"))

    if old.get("version") != "0.2" or new.get("version") != "0.3":
        fail("unexpected version lineage")
    if new.get("schema") != old.get("schema"):
        fail("schema family changed")
    if new.get("core_version") != "NEX-1 v0.1":
        fail("Core target changed")
    if new.get("core_dependencies") != old.get("core_dependencies"):
        fail("Core dependency inventory changed")
    if new.get("semantic_tag_sets") != old.get("tag_sets"):
        fail("semantic tag sets changed from v0.2")
    if new.get("status") != "stage5.11-operational-candidate":
        fail("unexpected v0.3 status")

    forbidden = set(new.get("forbidden_dependencies", []))
    required_forbidden = {
        "recursive types",
        "mutable references",
        "host strings",
        "host byte arrays",
        "host AST objects",
        "host callbacks implementing NEX operations",
        "new Core primitives",
        "incompatible NEX wire changes",
    }
    if forbidden != required_forbidden:
        fail("forbidden dependency guard drifted")

    foundation = new.get("operational_foundation", {})
    if foundation.get("BitStream", {}).get("type") != "N -> N":
        fail("BitStream type drifted")
    if foundation.get("FiniteBits", {}).get("type") != "(N -> N) * N":
        fail("FiniteBits type drifted")
    if foundation.get("FiniteNatTokens", {}).get("type") != "(N -> N) * N":
        fail("FiniteNatTokens type drifted")
    if foundation.get("BitStream", {}).get("symbols") != {"Bit0": 0, "Bit1": 1, "EOF": 2}:
        fail("BitStream symbol contract drifted")

    reps = new.get("representations", {})
    if set(reps) != REQUIRED_REPRESENTATIONS:
        fail(f"representation inventory is {sorted(reps)}, expected {sorted(REQUIRED_REPRESENTATIONS)}")
    if reps["Bits"].get("carrier") != "FiniteBits":
        fail("Bits must use FiniteBits")
    for name in REQUIRED_REPRESENTATIONS - {"Bits"}:
        if reps[name].get("carrier") != "FiniteNatTokens":
            fail(f"{name} must use FiniteNatTokens")

    expected_term_grammar = {
        "Var": "[0,index]",
        "Lam": "[1] ++ Term(body)",
        "App": "[2] ++ Term(function) ++ Term(argument)",
        "Let": "[3] ++ Term(value) ++ Term(body)",
        "Nat": "[4,value]",
        "Prim": "[5,id]",
    }
    if reps["Term"].get("grammar") != expected_term_grammar:
        fail("Term token grammar drifted")
    relation = reps["Term"].get("wire_relation", "")
    if "reconstruct canonical NEX wire" not in relation or "opaque original wire" not in relation:
        fail("Term representation does not prohibit an opaque wire identity shortcut")

    expected_type_grammar = {
        "TypeVar": "[0,id]",
        "Unit": "[1]",
        "Nat": "[2]",
        "Arrow": "[3] ++ Type(left) ++ Type(right)",
        "Product": "[4] ++ Type(left) ++ Type(right)",
        "Sum": "[5] ++ Type(left) ++ Type(right)",
    }
    if reps["Type"].get("grammar") != expected_type_grammar:
        fail("Type token grammar drifted")

    examples = new.get("bounded_examples", {})
    for example in examples.get("bits", []):
        items = example.get("items")
        if example.get("length") != len(items):
            fail(f"Bits example length mismatch: {example}")
        if any(bit not in (0, 1) for bit in items):
            fail(f"Bits example contains a non-bit: {example}")

    for example in examples.get("terms", []):
        tokens = tuple(example["tokens"])
        try:
            ast, end = parse_term(tokens)
        except ValueError as exc:
            fail(f"Term example {example['name']} does not parse: {exc}")
        if end != len(tokens):
            fail(f"Term example {example['name']} has trailing tokens")
        if term_tokens(ast) != tokens:
            fail(f"Term example {example['name']} token round trip failed")
        wire = term_wire(ast)
        if wire != example["canonical_wire"]:
            fail(f"Term example {example['name']} wire {wire} != {example['canonical_wire']}")

    for example in examples.get("types", []):
        require_exact_parser(f"Type example {example['name']}", example["tokens"], parse_type)
    for example in examples.get("schemes", []):
        require_exact_parser(f"Scheme example {example['name']}", example["tokens"], parse_scheme)
    for example in examples.get("substitutions", []):
        require_exact_parser(
            f"Substitution example {example['name']}", example["tokens"], parse_substitution
        )
    for example in examples.get("environments", []):
        require_exact_parser(
            f"Environment example {example['name']}", example["tokens"], parse_environment
        )
    for example in examples.get("observations", []):
        require_exact_parser(
            f"Observation example {example['name']}", example["tokens"], parse_observation
        )

    # Bounded structural evidence: enumerate every generated term with 1..4 nodes,
    # prove injectivity in that complete generated class, and check token/wire round trips.
    seen_tokens = {}
    seen_wire = {}
    generated = 0
    for nodes in range(1, 5):
        for ast in terms_with_nodes(nodes):
            generated += 1
            tokens = term_tokens(ast)
            reparsed, end = parse_term(tokens)
            if end != len(tokens) or reparsed != ast:
                fail(f"bounded Term round trip failed for {ast!r}")
            wire = term_wire(ast)
            prior = seen_tokens.get(tokens)
            if prior is not None and prior != ast:
                fail(f"bounded Term token collision: {prior!r} and {ast!r}")
            seen_tokens[tokens] = ast
            prior = seen_wire.get(wire)
            if prior is not None and prior != ast:
                fail(f"bounded canonical-wire collision: {prior!r} and {ast!r}")
            seen_wire[wire] = ast

    acceptance = new.get("stage5_11_acceptance", {})
    required_true = {
        "finite_carriers_without_recursive_types",
        "canonical_injective_admitted_encodings",
        "wire_vs_scope_vs_primitive_vs_resource_failures_separated",
        "bounded_round_trip_examples_required",
    }
    for field in required_true:
        if acceptance.get(field) is not True:
            fail(f"Stage 5.11 acceptance flag {field} is not true")
    if acceptance.get("malformed_internal_representation_policy") != "explicit":
        fail("malformed internal representation policy is not explicit")

    runtime_policy = new.get("runtime_state_policy", {})
    if runtime_policy.get("status") != "no additional first-class runtime state required by Stage 5.11":
        fail("runtime-state policy drifted")
    if "new meta-representation version" not in runtime_policy.get("future_rule", ""):
        fail("future runtime-state extension is not version-gated")

    print("stage5.11 meta-representation v0.3: valid operational contract")
    print("Core dependencies: unchanged from v0.2")
    print("Bits carrier: FiniteBits = (N -> N) * N")
    print("recursive meta-data carrier: FiniteNatTokens = (N -> N) * N")
    print(f"representation roles: {len(REQUIRED_REPRESENTATIONS)}")
    print(f"bounded complete generated Term class: {generated} terms (1..4 nodes)")
    print("bounded Term token/wire collisions: 0")
    print("5.12 encodeTerm/decodeTerm implementation: deliberately not performed here")


if __name__ == "__main__":
    main()
