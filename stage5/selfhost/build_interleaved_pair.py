#!/usr/bin/env python3
"""Build/check the Stage 5.12d pairing alternative candidate.

This candidate does not change NEX-1 v0.1. It tests whether replacing the
pow2-adic meta-pair with a bit-interleaving bijection gives a practical N-only
basis for recursive Term encodings.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_foundation import FIX, IFZ, app, encode_core, lam, let, lower, nat, v, source_terms

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "interleaved-pair-v0.1.json"


def interleave_pair(a: int, b: int) -> int:
    if a < 0 or b < 0:
        raise ValueError("pair arguments must be naturals")
    result = 0
    position = 0
    while a or b:
        result |= (a & 1) << (2 * position)
        result |= (b & 1) << (2 * position + 1)
        a >>= 1
        b >>= 1
        position += 1
    return result


def interleave_unpair(z: int) -> tuple[int, int]:
    if z < 0:
        raise ValueError("pair code must be a natural")
    left = 0
    right = 0
    position = 0
    while z:
        left |= (z & 1) << position
        right |= ((z >> 1) & 1) << position
        z >>= 2
        position += 1
    return left, right


def source_terms_interleaved_pair():
    foundation = source_terms()
    add = foundation["add"]
    odd = foundation["odd"]
    halve = foundation["halve"]

    def double(expr):
        return app(v("add"), expr, expr)

    pair_step = let(
        "abit",
        app(v("odd"), v("a")),
        let(
            "bbit",
            app(v("odd"), v("b")),
            let(
                "rest",
                app(v("self"), app(v("halve"), v("a")), app(v("halve"), v("b"))),
                let(
                    "two_b",
                    double(v("bbit")),
                    let(
                        "two_r",
                        double(v("rest")),
                        let(
                            "four_r",
                            double(v("two_r")),
                            app(v("add"), v("abit"), app(v("add"), v("two_b"), v("four_r"))),
                        ),
                    ),
                ),
            ),
        ),
    )
    pair_body = app(IFZ, v("a"), app(IFZ, v("b"), nat(0), pair_step), pair_step)
    meta_pair_interleaved = let(
        "add",
        add,
        let(
            "odd",
            odd,
            let(
                "halve",
                halve,
                app(FIX, lam("self", lam("a", lam("b", pair_body)))),
            ),
        ),
    )

    left_step = let(
        "bit",
        app(v("odd"), v("z")),
        let(
            "q",
            app(v("halve"), app(v("halve"), v("z"))),
            let(
                "rest",
                app(v("self"), v("q")),
                app(v("add"), v("bit"), double(v("rest"))),
            ),
        ),
    )
    left_body = app(IFZ, v("z"), nat(0), left_step)
    unpair_left_interleaved = let(
        "add",
        add,
        let(
            "odd",
            odd,
            let(
                "halve",
                halve,
                app(FIX, lam("self", lam("z", left_body))),
            ),
        ),
    )

    right_step = let(
        "z1",
        app(v("halve"), v("z")),
        let(
            "bit",
            app(v("odd"), v("z1")),
            let(
                "rest",
                app(v("self"), app(v("halve"), v("z1"))),
                app(v("add"), v("bit"), double(v("rest"))),
            ),
        ),
    )
    right_body = app(IFZ, v("z"), nat(0), right_step)
    unpair_right_interleaved = let(
        "add",
        add,
        let(
            "odd",
            odd,
            let(
                "halve",
                halve,
                app(FIX, lam("self", lam("z", right_body))),
            ),
        ),
    )

    return {
        "meta_pair_interleaved": meta_pair_interleaved,
        "unpair_left_interleaved": unpair_left_interleaved,
        "unpair_right_interleaved": unpair_right_interleaved,
    }


PAIR_CASES = [
    (0, 0),
    (1, 0),
    (0, 1),
    (2, 3),
    (3, 2),
    (5, 7),
    (15, 8),
    (27, 39),
    (95, 111),
]


def generated_artifact() -> dict:
    functions = []
    terms = source_terms_interleaved_pair()
    for name, source in terms.items():
        bits = encode_core(lower(source))
        if name == "meta_pair_interleaved":
            tests = [
                {"args": [a, b], "result": interleave_pair(a, b)}
                for a, b in PAIR_CASES
            ]
            expected_type = "(N -> (N -> N))"
        elif name == "unpair_left_interleaved":
            tests = [
                {"args": [interleave_pair(a, b)], "result": a}
                for a, b in PAIR_CASES
            ]
            expected_type = "(N -> N)"
        else:
            tests = [
                {"args": [interleave_pair(a, b)], "result": b}
                for a, b in PAIR_CASES
            ]
            expected_type = "(N -> N)"
        functions.append(
            {
                "name": name,
                "wire_bits": bits,
                "wire_bit_length": len(bits),
                "expected_type": expected_type,
                "tests": tests,
            }
        )

    growth_examples = []
    old_pair = lambda a, b: (1 << a) * (2 * b + 1) - 1
    for a, b in [(1, 111), (95, 111), (111, 1)]:
        old = old_pair(a, b)
        new = interleave_pair(a, b)
        growth_examples.append(
            {
                "a": a,
                "b": b,
                "pow2_adic_code_bit_length": old.bit_length(),
                "interleaved_code_bit_length": new.bit_length(),
            }
        )

    return {
        "schema": "nex-selfhost-interleaved-pair-candidate",
        "version": "0.1",
        "status": "stage5.12d-pairing-candidate",
        "core_version": "NEX-1 v0.1",
        "definition": {
            "pair": "result bit 2*i = bit i of a; result bit 2*i+1 = bit i of b",
            "left_inverse": "collect even-position result bits",
            "right_inverse": "collect odd-position result bits",
            "bijection": "N x N <-> N",
        },
        "functions": functions,
        "growth_examples": growth_examples,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.check == args.write:
        parser.error("choose exactly one of --check or --write")

    expected = generated_artifact()
    if args.write:
        ARTIFACT.write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {ARTIFACT.relative_to(ROOT)}")
        return

    actual = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    if actual != expected:
        raise SystemExit(
            "interleaved-pair-v0.1.json does not match build_interleaved_pair.py; "
            "run with --write and review the diff"
        )
    print("stage5.12d interleaved pair artifact: reproducible")


if __name__ == "__main__":
    main()
