#!/usr/bin/env python3
"""Build/check the Stage 5.12e functional finite-stream candidate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_foundation import FIX, IFZ, PRED, SUCC, app, encode_core, lam, let, lower, nat, v

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "functional-stream-v0.1.json"
EOF = 2


def as_nat(expr):
    """Identity at runtime; constrains an expression to N statically."""
    return app(IFZ, expr, expr, expr)


def source_terms_functional_stream():
    nil = lam("i", nat(EOF))

    cons = lam(
        "x",
        lam(
            "tail",
            lam(
                "i",
                app(
                    IFZ,
                    v("i"),
                    as_nat(v("x")),
                    as_nat(app(v("tail"), app(PRED, v("i")))),
                ),
            ),
        ),
    )

    head = lam("s", as_nat(app(v("s"), nat(0))))
    tail = lam("s", lam("i", as_nat(app(v("s"), app(SUCC, v("i"))))))

    drop_body = app(
        IFZ,
        v("k"),
        v("s"),
        app(v("self"), app(PRED, v("k")), app(v("tail"), v("s"))),
    )
    drop = let(
        "tail",
        tail,
        app(FIX, lam("self", lam("k", lam("s", drop_body)))),
    )

    dynamic2_query = let(
        "nil",
        nil,
        let(
            "cons",
            cons,
            lam(
                "a",
                lam(
                    "b",
                    lam(
                        "i",
                        app(
                            app(v("cons"), v("a"), app(v("cons"), v("b"), v("nil"))),
                            v("i"),
                        ),
                    ),
                ),
            ),
        ),
    )

    dynamic_tail_query = let(
        "nil",
        nil,
        let(
            "cons",
            cons,
            let(
                "tail",
                tail,
                lam(
                    "a",
                    lam(
                        "b",
                        lam(
                            "i",
                            app(
                                app(
                                    v("tail"),
                                    app(v("cons"), v("a"), app(v("cons"), v("b"), v("nil"))),
                                ),
                                v("i"),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )

    repeat_body = app(
        IFZ,
        v("count"),
        v("nil"),
        app(v("cons"), v("bit"), app(v("self"), v("bit"), app(PRED, v("count")))),
    )
    repeat = let(
        "nil",
        nil,
        let(
            "cons",
            cons,
            app(FIX, lam("self", lam("bit", lam("count", repeat_body)))),
        ),
    )

    repeat_query = let(
        "repeat",
        repeat,
        lam(
            "bit",
            lam(
                "count",
                lam(
                    "i",
                    as_nat(app(app(v("repeat"), v("bit"), v("count")), v("i"))),
                ),
            ),
        ),
    )

    drop_query = let(
        "nil",
        nil,
        let(
            "cons",
            cons,
            let(
                "drop",
                drop,
                lam(
                    "k",
                    lam(
                        "a",
                        lam(
                            "b",
                            lam(
                                "c",
                                lam(
                                    "i",
                                    app(
                                        app(
                                            v("drop"),
                                            v("k"),
                                            app(
                                                v("cons"),
                                                v("a"),
                                                app(
                                                    v("cons"),
                                                    v("b"),
                                                    app(v("cons"), v("c"), v("nil")),
                                                ),
                                            ),
                                        ),
                                        v("i"),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )

    return {
        "stream_nil": nil,
        "stream_cons": cons,
        "stream_head": head,
        "stream_tail": tail,
        "stream_drop": drop,
        "dynamic2_query": dynamic2_query,
        "dynamic_tail_query": dynamic_tail_query,
        "stream_repeat": repeat,
        "repeat_query": repeat_query,
        "drop_query": drop_query,
    }


CONTRACTS = {
    "stream_nil": {
        "expected_type": "(N -> N)",
        "tests": [{"args": [0], "result": 2}, {"args": [7], "result": 2}],
    },
    "stream_cons": {
        "expected_type": "(N -> ((N -> N) -> (N -> N)))",
        "tests": [],
        "static_only": True,
    },
    "stream_head": {
        "expected_type": "((N -> N) -> N)",
        "tests": [],
        "static_only": True,
    },
    "stream_tail": {
        "expected_type": "((N -> N) -> (N -> N))",
        "tests": [],
        "static_only": True,
    },
    "stream_drop": {
        "expected_type": "(N -> ((N -> N) -> (N -> N)))",
        "tests": [],
        "static_only": True,
    },
    "dynamic2_query": {
        "expected_type": "(N -> (N -> (N -> N)))",
        "tests": [
            {"args": [0, 1, 0], "result": 0},
            {"args": [0, 1, 1], "result": 1},
            {"args": [0, 1, 2], "result": 2},
            {"args": [1, 0, 0], "result": 1},
            {"args": [1, 0, 1], "result": 0},
            {"args": [1, 0, 2], "result": 2}
        ],
    },
    "dynamic_tail_query": {
        "expected_type": "(N -> (N -> (N -> N)))",
        "tests": [
            {"args": [0, 1, 0], "result": 1},
            {"args": [0, 1, 1], "result": 2},
            {"args": [1, 0, 0], "result": 0},
            {"args": [1, 0, 1], "result": 2}
        ],
    },
    "stream_repeat": {
        "expected_type": "(N -> (N -> (N -> N)))",
        "tests": [],
        "static_only": True,
    },
    "repeat_query": {
        "expected_type": "(N -> (N -> (N -> N)))",
        "tests": [
            {"args": [0, 0, 0], "result": 2},
            {"args": [0, 1, 0], "result": 0},
            {"args": [0, 1, 1], "result": 2},
            {"args": [1, 8, 7], "result": 1},
            {"args": [1, 8, 8], "result": 2},
            {"args": [0, 32, 31], "result": 0},
            {"args": [0, 32, 32], "result": 2},
            {"args": [1, 128, 127], "result": 1},
            {"args": [1, 128, 128], "result": 2}
        ],
    },
    "drop_query": {
        "expected_type": "(N -> (N -> (N -> (N -> (N -> N)))))",
        "tests": [
            {"args": [0, 0, 1, 0, 0], "result": 0},
            {"args": [1, 0, 1, 0, 0], "result": 1},
            {"args": [2, 0, 1, 0, 0], "result": 0},
            {"args": [3, 0, 1, 0, 0], "result": 2},
            {"args": [1, 0, 1, 0, 1], "result": 0}
        ],
    },
}


def generated_artifact() -> dict:
    functions = []
    for name, source in source_terms_functional_stream().items():
        bits = encode_core(lower(source))
        functions.append({
            "name": name,
            "wire_bits": bits,
            "wire_bit_length": len(bits),
            **CONTRACTS[name],
        })
    return {
        "schema": "nex-selfhost-functional-stream-candidate",
        "version": "0.1",
        "status": "stage5.12e-candidate",
        "core_version": "NEX-1 v0.1",
        "representation": {
            "type": "N -> N",
            "data_values": [0, 1],
            "eof": 2,
            "invariant": "indices before EOF contain 0 or 1; EOF and all later indices return 2"
        },
        "claims_under_test": [
            "finite streams have a fixed rank-1 HM type",
            "streams can be constructed dynamically as closures",
            "tail/drop can return streams without recursive types",
            "runtime cost depends on traversed stream depth rather than packed numeric code magnitude"
        ],
        "generator": "stage5/selfhost/build_functional_stream.py",
        "functions": functions,
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
            "functional-stream-v0.1.json does not match build_functional_stream.py; "
            "run with --write and review the diff"
        )
    print("stage5.12e functional stream artifact: reproducible")


if __name__ == "__main__":
    main()
