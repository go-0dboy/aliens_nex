#!/usr/bin/env python3
"""Validate the Stage 5.11 NEX-in-NEX meta-representation contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "stage5" / "selfhost" / "meta-representation-v0.1.json"

EXPECTED_CONSTRUCTORS = ["Var", "Lam", "App", "Let", "Nat", "Prim"]
EXPECTED_TYPES = ["TypeVar", "Unit", "Nat", "Arrow", "Product", "Sum"]
EXPECTED_PRIMITIVES = {
    "0": "fix",
    "1": "succ",
    "2": "pred",
    "3": "ifz",
    "4": "pair",
    "5": "fst",
    "6": "snd",
    "7": "inl",
    "8": "inr",
    "9": "case",
    "10": "unit",
}
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
    raise SystemExit(f"stage5.11 meta-representation invalid: {message}")


def pair(a: int, b: int) -> int:
    if a < 0 or b < 0:
        fail("pair arguments must be naturals")
    return (1 << a) * (2 * b + 1) - 1


def unpair(z: int) -> tuple[int, int]:
    if z < 0:
        fail("pair code must be a natural")
    n = z + 1
    a = 0
    while n % 2 == 0:
        a += 1
        n //= 2
    b = (n - 1) // 2
    return a, b


def encode_sequence(items: Iterable[int]) -> int:
    result = 0
    materialized = list(items)
    if any(item < 0 for item in materialized):
        fail("sequence items must be naturals")
    for item in reversed(materialized):
        result = 1 + pair(item, result)
    return result


def decode_sequence(code: int, *, max_items: int = 10_000) -> list[int]:
    if code < 0:
        fail("sequence code must be a natural")
    result: list[int] = []
    current = code
    while current:
        if len(result) >= max_items:
            fail("sequence decode exceeded validator safety bound")
        head, tail = unpair(current - 1)
        result.append(head)
        current = tail
    return result


def check_unique_dense_tags(name: str, mapping: dict[str, int]) -> None:
    values = list(mapping.values())
    if len(values) != len(set(values)):
        fail(f"{name} contains duplicate numeric tags")
    if any(not isinstance(value, int) or value < 0 for value in values):
        fail(f"{name} tags must be natural numbers")
    if sorted(values) != list(range(len(values))):
        fail(f"{name} tags must be dense from 0 for the v0.1 contract")


def main() -> None:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))

    if data.get("schema") != "nex-selfhost-meta-representation":
        fail("unexpected schema")
    if data.get("version") != "0.1":
        fail("unexpected version")
    if data.get("core_version") != "NEX-1 v0.1":
        fail("contract must target exact NEX-1 v0.1")

    core = data.get("core_dependencies", {})
    if core.get("term_constructors") != EXPECTED_CONSTRUCTORS:
        fail("term constructors drifted from NEX-1 v0.1")
    if core.get("type_formers") != EXPECTED_TYPES:
        fail("type-former contract drifted from NEX-1 v0.1")
    if core.get("primitive_ids") != EXPECTED_PRIMITIVES:
        fail("primitive table drifted from NEX-1 v0.1")
    if core.get("additional_core_features") != []:
        fail("5.11 must not depend on additional Core features")

    reps = data.get("representations", {})
    if set(reps) != REQUIRED_REPRESENTATIONS:
        missing = sorted(REQUIRED_REPRESENTATIONS - set(reps))
        extra = sorted(set(reps) - REQUIRED_REPRESENTATIONS)
        fail(f"representation set mismatch; missing={missing}, extra={extra}")

    for name, spec in reps.items():
        if spec.get("carrier") != "N":
            fail(f"{name} must use only N as its physical Core carrier")

    tags = data.get("tag_sets", {})
    required_tag_sets = {
        "term_tags",
        "type_tags",
        "observation_tags",
        "static_result_tags",
        "request_tags",
        "tool_result_tags",
    }
    if set(tags) != required_tag_sets:
        fail("tag-set inventory mismatch")
    for name, mapping in tags.items():
        check_unique_dense_tags(name, mapping)

    if tags["term_tags"] != {
        "Var": 0,
        "Lam": 1,
        "App": 2,
        "Let": 3,
        "Nat": 4,
        "Prim": 5,
    }:
        fail("Term meta-tags must preserve the declared v0.1 constructor order")

    if tags["type_tags"] != {
        "TypeVar": 0,
        "Unit": 1,
        "Nat": 2,
        "Arrow": 3,
        "Product": 4,
        "Sum": 5,
    }:
        fail("Type meta-tags changed unexpectedly")

    for example in data.get("bounded_examples", {}).get("pairs", []):
        a, b, expected = example["a"], example["b"], example["code"]
        actual = pair(a, b)
        if actual != expected:
            fail(f"pair example ({a},{b}) expected {expected}, got {actual}")
        if unpair(actual) != (a, b):
            fail(f"pair round-trip failed for ({a},{b})")

    for a in range(8):
        for b in range(16):
            if unpair(pair(a, b)) != (a, b):
                fail(f"bounded pair round-trip failed for ({a},{b})")

    seen: set[int] = set()
    for a in range(7):
        for b in range(12):
            code = pair(a, b)
            if code in seen:
                fail("bounded pair injectivity check found a collision")
            seen.add(code)

    for example in data.get("bounded_examples", {}).get("sequences", []):
        items, expected = example["items"], example["code"]
        actual = encode_sequence(items)
        if actual != expected:
            fail(f"sequence example {items} expected {expected}, got {actual}")
        if decode_sequence(actual) != items:
            fail(f"sequence round-trip failed for {items}")

    for length in range(6):
        for bits_as_int in range(1 << length):
            bits = [
                (bits_as_int >> (length - 1 - i)) & 1
                for i in range(length)
            ]
            if decode_sequence(encode_sequence(bits)) != bits:
                fail(f"bounded Bits round-trip failed for {bits}")

    forbidden = set(data.get("forbidden_dependencies", []))
    required_forbidden = {
        "recursive types",
        "mutable references",
        "host strings",
        "host byte arrays",
        "host AST objects",
        "host callbacks implementing NEX operations",
        "new Core primitives",
        "incompatible wire changes",
    }
    if not required_forbidden.issubset(forbidden):
        fail("forbidden-dependency guard is incomplete")

    print("stage5.11 meta-representation: valid")
    print(f"representations: {len(reps)}")
    print(f"tag sets: {len(tags)}")
    print("carrier closure: N only")
    print("bounded pair/sequence/Bits checks: passed")


if __name__ == "__main__":
    main()
