#!/usr/bin/env python3
"""Build/check the Stage 5.12b N-only pair/sequence experiment.

Readable names exist only in this engineering generator. The research artifacts
are the generated closed canonical NEX-1 v0.1 terms in meta-sequence-v0.1.json.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_foundation import (
    FIX,
    IFZ,
    PRED,
    SUCC,
    app,
    encode_core,
    lam,
    let,
    lower,
    nat,
    source_terms,
    v,
)

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "meta-sequence-v0.1.json"


def source_terms_5_12b():
    foundation = source_terms()
    add = foundation["add"]
    mul = foundation["mul"]
    odd = foundation["odd"]
    halve = foundation["halve"]
    pow2 = foundation["pow2"]
    shift_right = foundation["shift_right"]

    pair_body = app(
        PRED,
        app(
            v("mul"),
            app(v("pow2"), v("a")),
            app(SUCC, app(v("add"), v("b"), v("b"))),
        ),
    )
    meta_pair = let(
        "add",
        add,
        let(
            "mul",
            mul,
            let("pow2", pow2, lam("a", lam("b", pair_body))),
        ),
    )

    v2_recursive = app(SUCC, app(v("self"), app(v("halve"), v("n"))))
    v2_nonzero = app(IFZ, app(v("odd"), v("n")), v2_recursive, nat(0))
    v2_body = app(IFZ, v("n"), nat(0), v2_nonzero)
    v2 = let(
        "odd",
        odd,
        let(
            "halve",
            halve,
            app(FIX, lam("self", lam("n", v2_body))),
        ),
    )

    unpair_left = let(
        "v2",
        v2,
        lam("z", app(v("v2"), app(SUCC, v("z")))),
    )

    unpair_right_body = app(
        v("halve"),
        app(
            PRED,
            app(
                v("shift"),
                app(SUCC, v("z")),
                app(v("left"), v("z")),
            ),
        ),
    )
    unpair_right = let(
        "left",
        unpair_left,
        let(
            "shift",
            shift_right,
            let("halve", halve, lam("z", unpair_right_body)),
        ),
    )

    seq_cons = let(
        "pair",
        meta_pair,
        lam(
            "head",
            lam(
                "tail",
                app(SUCC, app(v("pair"), v("head"), v("tail"))),
            ),
        ),
    )

    seq_head = let(
        "left",
        unpair_left,
        lam(
            "seq",
            app(
                IFZ,
                v("seq"),
                nat(0),
                app(v("left"), app(PRED, v("seq"))),
            ),
        ),
    )

    seq_tail = let(
        "right",
        unpair_right,
        lam(
            "seq",
            app(
                IFZ,
                v("seq"),
                nat(0),
                app(v("right"), app(PRED, v("seq"))),
            ),
        ),
    )

    return {
        "meta_pair": meta_pair,
        "v2": v2,
        "unpair_left": unpair_left,
        "unpair_right": unpair_right,
        "seq_cons": seq_cons,
        "seq_head": seq_head,
        "seq_tail": seq_tail,
    }


FUNCTION_CONTRACTS = {
    "meta_pair": {
        "role": "pow2-adic pair encoder",
        "expected_type": "(N -> (N -> N))",
        "tests": [
            {"args": [0, 0], "result": 0},
            {"args": [1, 0], "result": 1},
            {"args": [0, 1], "result": 2},
            {"args": [2, 3], "result": 27},
            {"args": [3, 2], "result": 39},
        ],
    },
    "v2": {
        "role": "2-adic valuation with total v2(0)=0 guard",
        "expected_type": "(N -> N)",
        "tests": [
            {"args": [0], "result": 0},
            {"args": [1], "result": 0},
            {"args": [2], "result": 1},
            {"args": [4], "result": 2},
            {"args": [12], "result": 2},
        ],
    },
    "unpair_left": {
        "role": "recover first pow2-adic pair component",
        "expected_type": "(N -> N)",
        "tests": [
            {"args": [0], "result": 0},
            {"args": [1], "result": 1},
            {"args": [2], "result": 0},
            {"args": [27], "result": 2},
            {"args": [39], "result": 3},
        ],
    },
    "unpair_right": {
        "role": "recover second pow2-adic pair component",
        "expected_type": "(N -> N)",
        "tests": [
            {"args": [0], "result": 0},
            {"args": [1], "result": 0},
            {"args": [2], "result": 1},
            {"args": [27], "result": 3},
            {"args": [39], "result": 2},
        ],
    },
    "seq_cons": {
        "role": "finite natural-sequence cons",
        "expected_type": "(N -> (N -> N))",
        "tests": [
            {"args": [0, 0], "result": 1},
            {"args": [1, 0], "result": 2},
            {"args": [0, 2], "result": 5},
            {"args": [1, 1], "result": 6},
            {"args": [1, 6], "result": 26},
        ],
    },
    "seq_head": {
        "role": "sequence head with total nil->0 guard",
        "expected_type": "(N -> N)",
        "tests": [
            {"args": [0], "result": 0},
            {"args": [1], "result": 0},
            {"args": [2], "result": 1},
            {"args": [5], "result": 0},
            {"args": [6], "result": 1},
            {"args": [26], "result": 1},
        ],
    },
    "seq_tail": {
        "role": "sequence tail with total nil->0 guard",
        "expected_type": "(N -> N)",
        "tests": [
            {"args": [0], "result": 0},
            {"args": [1], "result": 0},
            {"args": [2], "result": 0},
            {"args": [5], "result": 2},
            {"args": [6], "result": 1},
            {"args": [26], "result": 6},
        ],
    },
}


def generated_artifact() -> dict:
    functions = []
    for name, source in source_terms_5_12b().items():
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
        "schema": "nex-selfhost-meta-sequence",
        "version": "0.1",
        "status": "stage5.12b-experiment-candidate",
        "core_version": "NEX-1 v0.1",
        "meta_representation": "stage5/selfhost/meta-representation-v0.1.json",
        "generator": "stage5/selfhost/build_meta_sequence.py",
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

    expected = generated_artifact()
    if args.write:
        ARTIFACT.write_text(canonical_json(expected), encoding="utf-8")
        print(f"wrote {ARTIFACT.relative_to(ROOT)}")
        return

    actual = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    if actual != expected:
        raise SystemExit(
            "meta-sequence-v0.1.json does not match build_meta_sequence.py; "
            "run with --write and review the diff"
        )
    print("stage5.12b meta-sequence artifact: reproducible")


if __name__ == "__main__":
    main()
