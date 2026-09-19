#!/usr/bin/env python3
"""Build/check the first canonical NEX-in-NEX arithmetic foundation.

The readable names in this file are engineering-only generator notation. The
research artifact is the generated canonical NEX wire recorded in
foundation-v0.1.json.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "foundation-v0.1.json"


@dataclass(frozen=True, slots=True)
class Name:
    name: str


@dataclass(frozen=True, slots=True)
class Lambda:
    name: str
    body: "Source"


@dataclass(frozen=True, slots=True)
class Apply:
    function: "Source"
    argument: "Source"


@dataclass(frozen=True, slots=True)
class LetName:
    name: str
    value: "Source"
    body: "Source"


@dataclass(frozen=True, slots=True)
class Natural:
    value: int


@dataclass(frozen=True, slots=True)
class Primitive:
    primitive_id: int


Source: TypeAlias = Name | Lambda | Apply | LetName | Natural | Primitive
Core: TypeAlias = tuple


def v(name: str) -> Source:
    return Name(name)


def lam(name: str, body: Source) -> Source:
    return Lambda(name, body)


def app(function: Source, *arguments: Source) -> Source:
    result = function
    for argument in arguments:
        result = Apply(result, argument)
    return result


def let(name: str, value: Source, body: Source) -> Source:
    return LetName(name, value, body)


def nat(value: int) -> Source:
    return Natural(value)


def prim(primitive_id: int) -> Source:
    return Primitive(primitive_id)


FIX = prim(0)
SUCC = prim(1)
PRED = prim(2)
IFZ = prim(3)


def lower(source: Source, environment: tuple[str, ...] = ()) -> Core:
    match source:
        case Name(name):
            try:
                index = environment.index(name)
            except ValueError:
                raise ValueError(f"free generator name {name!r}") from None
            return ("var", index)
        case Lambda(name, body):
            return ("lam", lower(body, (name, *environment)))
        case Apply(function, argument):
            return ("app", lower(function, environment), lower(argument, environment))
        case LetName(name, value, body):
            return (
                "let",
                lower(value, environment),
                lower(body, (name, *environment)),
            )
        case Natural(value):
            if value < 0:
                raise ValueError("NEX Nat must be non-negative")
            return ("nat", value)
        case Primitive(primitive_id):
            if primitive_id < 0:
                raise ValueError("primitive id must be non-negative")
            return ("prim", primitive_id)
        case _:
            raise TypeError(type(source).__name__)


def encode_u(value: int) -> str:
    payload = bin(value + 1)[2:]
    return "0" * (len(payload) - 1) + payload


def encode_core(term: Core) -> str:
    kind = term[0]
    if kind == "var":
        return "00" + encode_u(term[1])
    if kind == "lam":
        return "01" + encode_core(term[1])
    if kind == "app":
        return "10" + encode_core(term[1]) + encode_core(term[2])
    if kind == "let":
        return "110" + encode_core(term[1]) + encode_core(term[2])
    if kind == "nat":
        return "1110" + encode_u(term[1])
    if kind == "prim":
        return "1111" + encode_u(term[1])
    raise ValueError(f"unknown lowered kind {kind!r}")


def source_terms() -> dict[str, Source]:
    add_step = app(SUCC, app(v("self"), v("a"), app(PRED, v("b"))))
    add_body = app(IFZ, v("b"), v("a"), add_step)
    add = app(FIX, lam("self", lam("a", lam("b", add_body))))

    mul_step = app(
        v("add"),
        v("a"),
        app(v("self"), v("a"), app(PRED, v("b"))),
    )
    mul_body = app(IFZ, v("b"), nat(0), mul_step)
    mul = let(
        "add",
        add,
        app(FIX, lam("self", lam("a", lam("b", mul_body)))),
    )

    odd_recursive = app(v("self"), app(PRED, app(PRED, v("n"))))
    odd_inner = app(IFZ, app(PRED, v("n")), nat(1), odd_recursive)
    odd_body = app(IFZ, v("n"), nat(0), odd_inner)
    odd = app(FIX, lam("self", lam("n", odd_body)))

    halve_recursive = app(
        SUCC,
        app(v("self"), app(PRED, app(PRED, v("n")))),
    )
    halve_inner = app(IFZ, app(PRED, v("n")), nat(0), halve_recursive)
    halve_body = app(IFZ, v("n"), nat(0), halve_inner)
    halve = app(FIX, lam("self", lam("n", halve_body)))

    previous = app(PRED, v("n"))
    pow2_recursive = app(v("self"), previous)
    pow2_body = app(
        IFZ,
        v("n"),
        nat(1),
        app(v("add"), pow2_recursive, pow2_recursive),
    )
    pow2 = let(
        "add",
        add,
        app(FIX, lam("self", lam("n", pow2_body))),
    )

    shift_body = app(
        IFZ,
        v("k"),
        v("n"),
        app(v("self"), app(v("halve"), v("n")), app(PRED, v("k"))),
    )
    shift_right = let(
        "halve",
        halve,
        app(FIX, lam("self", lam("n", lam("k", shift_body)))),
    )

    return {
        "add": add,
        "mul": mul,
        "odd": odd,
        "halve": halve,
        "pow2": pow2,
        "shift_right": shift_right,
    }


FUNCTION_CONTRACTS = {
    "add": {
        "role": "natural addition",
        "expected_type": "(N -> (N -> N))",
        "tests": [
            {"args": [0, 0], "result": 0},
            {"args": [2, 3], "result": 5},
            {"args": [4, 1], "result": 5},
        ],
    },
    "mul": {
        "role": "natural multiplication",
        "expected_type": "(N -> (N -> N))",
        "tests": [
            {"args": [0, 5], "result": 0},
            {"args": [2, 3], "result": 6},
            {"args": [3, 2], "result": 6},
        ],
    },
    "odd": {
        "role": "parity flag, 0 for even and 1 for odd",
        "expected_type": "(N -> N)",
        "tests": [
            {"args": [0], "result": 0},
            {"args": [1], "result": 1},
            {"args": [2], "result": 0},
            {"args": [5], "result": 1},
        ],
    },
    "halve": {
        "role": "floor division by 2",
        "expected_type": "(N -> N)",
        "tests": [
            {"args": [0], "result": 0},
            {"args": [1], "result": 0},
            {"args": [2], "result": 1},
            {"args": [5], "result": 2},
            {"args": [8], "result": 4},
        ],
    },
    "pow2": {
        "role": "power of two",
        "expected_type": "(N -> N)",
        "tests": [
            {"args": [0], "result": 1},
            {"args": [1], "result": 2},
            {"args": [3], "result": 8},
        ],
    },
    "shift_right": {
        "role": "floor division by 2^k",
        "expected_type": "(N -> (N -> N))",
        "tests": [
            {"args": [8, 0], "result": 8},
            {"args": [8, 1], "result": 4},
            {"args": [9, 1], "result": 4},
            {"args": [15, 3], "result": 1},
        ],
    },
}


def generated_artifact() -> dict:
    functions = []
    for name, source in source_terms().items():
        bits = encode_core(lower(source))
        functions.append(
            {
                "name": name,
                "wire_bits": bits,
                "wire_bit_length": len(bits),
                **FUNCTION_CONTRACTS[name],
            }
        )
    return {
        "schema": "nex-selfhost-foundation",
        "version": "0.1",
        "status": "stage5.12-foundation-candidate",
        "core_version": "NEX-1 v0.1",
        "generator": "stage5/selfhost/build_foundation.py",
        "functions": functions,
    }


def canonical_json(value: dict) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.check == args.write:
        parser.error("choose exactly one of --check or --write")

    expected = canonical_json(generated_artifact())
    if args.write:
        ARTIFACT.write_text(expected, encoding="utf-8")
        print(f"wrote {ARTIFACT.relative_to(ROOT)}")
        return

    actual = ARTIFACT.read_text(encoding="utf-8")
    if actual != expected:
        raise SystemExit(
            "foundation-v0.1.json does not match build_foundation.py; "
            "run with --write and review the diff"
        )
    print("stage5.12 foundation artifact: reproducible")


if __name__ == "__main__":
    main()
