#!/usr/bin/env python3
"""Build/check Stage 5.12f NEX stream-parser candidate v0.1.

The parser works directly over the accepted functional BitStream=N->N and a
natural-number cursor. It does not materialize a recursive numeric AST.

Readable names below are generator notation only. The research objects are the
generated canonical NEX wire strings frozen in stream-parser-v0.1.json.
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
    prim,
    v,
)

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "stream-parser-v0.1.json"

PAIR = prim(4)
FST = prim(5)
SND = prim(6)

EXPECTED_TYPE = "((N -> N) -> (N -> (N * (N * (N * N)))))"

ROLES = {
    "decodeUAt": "decode Elias gamma U(n) from a functional bit stream at a cursor",
    "readHead": "decode one NEX constructor header and immediate U payload if present",
    "skipTerm": "recursively traverse one complete canonical NEX term and count nodes",
    "exactTerm": "traverse exactly one canonical NEX term and require EOF immediately after it",
}


def result_value(status, a, b, next_offset):
    return app(PAIR, status, app(PAIR, a, app(PAIR, b, next_offset)))


def status_of(result):
    return app(FST, result)


def a_of(result):
    return app(FST, app(SND, result))


def b_of(result):
    return app(FST, app(SND, app(SND, result)))


def next_of(result):
    return app(SND, app(SND, app(SND, result)))


def source_helpers():
    # case3 x zero one eof:
    #   x==0 -> zero
    #   x==1 -> one
    #   otherwise -> eof
    # BitStreams are valid by construction and therefore only return 0,1,2.
    case3 = lam(
        "x",
        lam(
            "zero",
            lam(
                "one",
                lam(
                    "eof",
                    app(
                        IFZ,
                        v("x"),
                        v("zero"),
                        app(IFZ, app(PRED, v("x")), v("one"), v("eof")),
                    ),
                ),
            ),
        ),
    )

    # withbit x ok err:
    #   x==0 or x==1 -> ok
    #   x==2         -> err
    withbit = lam(
        "x",
        lam(
            "ok",
            lam(
                "err",
                app(
                    IFZ,
                    v("x"),
                    v("ok"),
                    app(IFZ, app(PRED, v("x")), v("ok"), v("err")),
                ),
            ),
        ),
    )

    mk = lam(
        "status",
        lam(
            "a",
            lam(
                "b",
                lam(
                    "next",
                    result_value(v("status"), v("a"), v("b"), v("next")),
                ),
            ),
        ),
    )

    add_step = app(SUCC, app(v("self"), v("a"), app(PRED, v("b"))))
    add = app(
        FIX,
        lam(
            "self",
            lam("a", lam("b", app(IFZ, v("b"), v("a"), add_step))),
        ),
    )
    double = let("add", add, lam("n", app(v("add"), v("n"), v("n"))))

    return case3, withbit, mk, add, double


def source_decode_u_at():
    case3, _withbit, mk, _add, double = source_helpers()

    def mk_call(status, a, b, next_offset):
        return app(v("mk"), status, a, b, next_offset)

    def case_call(symbol, zero, one, eof):
        return app(v("case3"), symbol, zero, one, eof)

    payload_body = app(
        IFZ,
        v("rem"),
        mk_call(nat(0), app(PRED, v("value")), nat(0), v("cursor")),
        let(
            "cur",
            app(v("s"), v("cursor")),
            case_call(
                v("cur"),
                app(
                    v("self"),
                    v("s"),
                    app(PRED, v("rem")),
                    app(v("double"), v("value")),
                    app(SUCC, v("cursor")),
                ),
                app(
                    v("self"),
                    v("s"),
                    app(PRED, v("rem")),
                    app(SUCC, app(v("double"), v("value"))),
                    app(SUCC, v("cursor")),
                ),
                mk_call(nat(1), nat(0), nat(0), v("cursor")),
            ),
        ),
    )
    payload = app(
        FIX,
        lam(
            "self",
            lam(
                "s",
                lam(
                    "rem",
                    lam("value", lam("cursor", payload_body)),
                ),
            ),
        ),
    )

    scan_body = let(
        "cur",
        app(v("s"), v("cursor")),
        case_call(
            v("cur"),
            app(
                v("self"),
                v("s"),
                app(SUCC, v("zeros")),
                app(SUCC, v("cursor")),
            ),
            app(
                v("payload"),
                v("s"),
                v("zeros"),
                nat(1),
                app(SUCC, v("cursor")),
            ),
            mk_call(nat(1), nat(0), nat(0), v("cursor")),
        ),
    )
    scan = app(
        FIX,
        lam("self", lam("s", lam("zeros", lam("cursor", scan_body)))),
    )

    return let(
        "case3",
        case3,
        let(
            "mk",
            mk,
            let(
                "double",
                double,
                let(
                    "payload",
                    payload,
                    let(
                        "scan",
                        scan,
                        lam(
                            "s",
                            lam(
                                "offset",
                                app(v("scan"), v("s"), nat(0), v("offset")),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )


def source_read_head():
    case3, withbit, mk, _add, _double = source_helpers()
    decode = source_decode_u_at()

    def mk_call(status, a, b, next_offset):
        return app(v("mk"), status, a, b, next_offset)

    def case_call(symbol, zero, one, eof):
        return app(v("case3"), symbol, zero, one, eof)

    def bit_call(symbol, ok, err):
        return app(v("withbit"), symbol, ok, err)

    def decoded_at(cursor_name: str, kind: int):
        return let(
            "r",
            app(v("decode"), v("s"), v(cursor_name)),
            app(
                IFZ,
                status_of(v("r")),
                mk_call(nat(0), nat(kind), a_of(v("r")), next_of(v("r"))),
                mk_call(nat(1), nat(0), nat(0), next_of(v("r"))),
            ),
        )

    first_zero = app(
        IFZ,
        v("second"),
        decoded_at("cursor2", 0),
        mk_call(nat(0), nat(1), nat(0), v("cursor2")),
    )

    fourth = let(
        "fourth",
        app(v("s"), v("cursor3")),
        let(
            "cursor4",
            app(SUCC, v("cursor3")),
            case_call(
                v("fourth"),
                decoded_at("cursor4", 4),
                decoded_at("cursor4", 5),
                mk_call(nat(1), nat(0), nat(0), v("cursor3")),
            ),
        ),
    )

    third = let(
        "third",
        app(v("s"), v("cursor2")),
        let(
            "cursor3",
            app(SUCC, v("cursor2")),
            case_call(
                v("third"),
                mk_call(nat(0), nat(3), nat(0), v("cursor3")),
                fourth,
                mk_call(nat(1), nat(0), nat(0), v("cursor2")),
            ),
        ),
    )

    first_one = app(
        IFZ,
        v("second"),
        mk_call(nat(0), nat(2), nat(0), v("cursor2")),
        third,
    )

    valid_second = app(IFZ, v("first"), first_zero, first_one)

    valid_first = let(
        "second",
        app(v("s"), v("cursor1")),
        let(
            "cursor2",
            app(SUCC, v("cursor1")),
            bit_call(
                v("second"),
                valid_second,
                mk_call(nat(1), nat(0), nat(0), v("cursor1")),
            ),
        ),
    )

    body = let(
        "first",
        app(v("s"), v("offset")),
        let(
            "cursor1",
            app(SUCC, v("offset")),
            bit_call(
                v("first"),
                valid_first,
                mk_call(nat(1), nat(0), nat(0), v("offset")),
            ),
        ),
    )

    return let(
        "case3",
        case3,
        let(
            "withbit",
            withbit,
            let(
                "mk",
                mk,
                let("decode", decode, lam("s", lam("offset", body))),
            ),
        ),
    )


def source_skip_term():
    _case3, _withbit, mk, add, _double = source_helpers()
    head = source_read_head()

    def mk_call(status, a, b, next_offset):
        return app(v("mk"), status, a, b, next_offset)

    def error_from(result):
        return mk_call(status_of(result), nat(0), nat(0), next_of(result))

    one_child = let(
        "c",
        app(v("self"), v("s"), next_of(v("h"))),
        app(
            IFZ,
            status_of(v("c")),
            mk_call(
                nat(0),
                app(SUCC, a_of(v("c"))),
                nat(0),
                next_of(v("c")),
            ),
            error_from(v("c")),
        ),
    )

    two_children = let(
        "c1",
        app(v("self"), v("s"), next_of(v("h"))),
        app(
            IFZ,
            status_of(v("c1")),
            let(
                "c2",
                app(v("self"), v("s"), next_of(v("c1"))),
                app(
                    IFZ,
                    status_of(v("c2")),
                    mk_call(
                        nat(0),
                        app(
                            SUCC,
                            app(v("add"), a_of(v("c1")), a_of(v("c2"))),
                        ),
                        nat(0),
                        next_of(v("c2")),
                    ),
                    error_from(v("c2")),
                ),
            ),
            error_from(v("c1")),
        ),
    )

    leaf = mk_call(nat(0), nat(1), nat(0), next_of(v("h")))

    # readHead guarantees kind 0..5. Arity:
    # Var=0, Lam=1, App=2, Let=2, Nat=0, Prim=0.
    select_kind = let(
        "k1",
        app(PRED, a_of(v("h"))),
        app(
            IFZ,
            a_of(v("h")),
            leaf,
            let(
                "k2",
                app(PRED, v("k1")),
                app(
                    IFZ,
                    v("k1"),
                    one_child,
                    let(
                        "k3",
                        app(PRED, v("k2")),
                        app(
                            IFZ,
                            v("k2"),
                            two_children,
                            app(IFZ, v("k3"), two_children, leaf),
                        ),
                    ),
                ),
            ),
        ),
    )

    body = let(
        "h",
        app(v("head"), v("s"), v("offset")),
        app(IFZ, status_of(v("h")), select_kind, error_from(v("h"))),
    )

    recursive = app(
        FIX,
        lam("self", lam("s", lam("offset", body))),
    )

    return let(
        "mk",
        mk,
        let("add", add, let("head", head, recursive)),
    )


def source_exact_term():
    _case3, withbit, mk, _add, _double = source_helpers()
    skip = source_skip_term()

    def mk_call(status, a, b, next_offset):
        return app(v("mk"), status, a, b, next_offset)

    def error_from(result):
        return mk_call(status_of(result), nat(0), nat(0), next_of(result))

    body = let(
        "r",
        app(v("skip"), v("s"), v("offset")),
        app(
            IFZ,
            status_of(v("r")),
            let(
                "symbol",
                app(v("s"), next_of(v("r"))),
                app(
                    v("withbit"),
                    v("symbol"),
                    mk_call(
                        nat(2),
                        a_of(v("r")),
                        nat(0),
                        next_of(v("r")),
                    ),
                    mk_call(
                        nat(0),
                        a_of(v("r")),
                        nat(0),
                        next_of(v("r")),
                    ),
                ),
            ),
            error_from(v("r")),
        ),
    )

    return let(
        "withbit",
        withbit,
        let(
            "mk",
            mk,
            let("skip", skip, lam("s", lam("offset", body))),
        ),
    )


def source_terms_parser():
    return {
        "decodeUAt": source_decode_u_at(),
        "readHead": source_read_head(),
        "skipTerm": source_skip_term(),
        "exactTerm": source_exact_term(),
    }


def literal_bit_stream(bits: str):
    """Engineering-only fixed stream term used by development verification."""

    if any(ch not in "01" for ch in bits):
        raise ValueError("literal bit stream accepts only 0/1")

    def pred_n(expression, count: int):
        for _ in range(count):
            expression = app(PRED, expression)
        return expression

    def build(index: int):
        if index >= len(bits):
            return nat(2)
        return app(
            IFZ,
            pred_n(v("i"), index),
            nat(int(bits[index])),
            build(index + 1),
        )

    return lam("i", build(0))


def result_projection(expression, field: int):
    if field == 0:
        return status_of(expression)
    if field == 1:
        return a_of(expression)
    if field == 2:
        return b_of(expression)
    if field == 3:
        return next_of(expression)
    raise ValueError("ParserResult field must be 0..3")


def generated_artifact() -> dict:
    functions = []
    for name, source in source_terms_parser().items():
        bits = encode_core(lower(source))
        functions.append(
            {
                "name": name,
                "wire_bits": bits,
                "wire_bit_length": len(bits),
                "expected_type": EXPECTED_TYPE,
                "role": ROLES[name],
            }
        )
    return {
        "schema": "nex-selfhost-stream-parser-candidate",
        "version": "0.1",
        "status": "stage5.12f-development-candidate",
        "core_version": "NEX-1 v0.1",
        "contract": "stage5/selfhost/parser-contract-v0.1.json",
        "representation": {
            "BitStream": "N -> N",
            "Cursor": "N",
            "ParserResult": "N * (N * (N * N))",
        },
        "generator": "stage5/selfhost/build_stream_parser.py",
        "functions": functions,
        "development_workload": "stage5/selfhost/parser-development-v0.1.json",
        "holdout_workload": "stage5/selfhost/parser-holdout-v0.1.json",
        "holdout_status": "preregistered_unexecuted",
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
            "stream-parser-v0.1.json does not match build_stream_parser.py; "
            "run with --write and review the diff"
        )
    print("stage5.12f stream parser v0.1 artifact: reproducible")


if __name__ == "__main__":
    main()
