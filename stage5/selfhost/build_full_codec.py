#!/usr/bin/env python3
"""Build/check the Stage 5.12 full Term codec candidate v0.1.

The research objects are two closed canonical NEX-1 v0.1 terms. The generator
uses readable engineering names only. Runtime candidate execution is performed
by a separate development verifier after the candidate identity is frozen.
"""
from __future__ import annotations

import argparse
import hashlib
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
    source_terms,
    v,
)
from build_stream_parser import a_of, b_of, next_of, source_read_head, status_of

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "full-codec-v0.1.json"

PAIR = prim(4)
FST = prim(5)
SND = prim(6)
EXPECTED_TYPE = "(((N -> N) * N) -> (N * ((N -> N) * N)))"


def fst(x):
    return app(FST, x)


def snd(x):
    return app(SND, x)


def codec_result(status, stream, length):
    return app(PAIR, status, app(PAIR, stream, length))


def codec_status(result):
    return fst(result)


def codec_stream(result):
    return fst(snd(result))


def codec_length(result):
    return snd(snd(result))


def scan_result(status, amount, next_offset):
    return app(PAIR, status, app(PAIR, amount, next_offset))


def scan_status(result):
    return fst(result)


def scan_amount(result):
    return fst(snd(result))


def scan_next(result):
    return snd(snd(result))


def source_case6():
    body = app(
        IFZ,
        v("k"),
        v("b0"),
        let(
            "k1",
            app(PRED, v("k")),
            app(
                IFZ,
                v("k1"),
                v("b1"),
                let(
                    "k2",
                    app(PRED, v("k1")),
                    app(
                        IFZ,
                        v("k2"),
                        v("b2"),
                        let(
                            "k3",
                            app(PRED, v("k2")),
                            app(
                                IFZ,
                                v("k3"),
                                v("b3"),
                                let(
                                    "k4",
                                    app(PRED, v("k3")),
                                    app(
                                        IFZ,
                                        v("k4"),
                                        v("b4"),
                                        let(
                                            "k5",
                                            app(PRED, v("k4")),
                                            app(IFZ, v("k5"), v("b5"), v("bad")),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )
    result = body
    for name in reversed(("bad", "b5", "b4", "b3", "b2", "b1", "b0", "k")):
        result = lam(name, result)
    return result


def source_arithmetic():
    foundation = source_terms()
    add = foundation["add"]
    halve = foundation["halve"]
    odd = foundation["odd"]
    shift_right = foundation["shift_right"]

    sub_body = app(
        IFZ,
        v("b"),
        v("a"),
        app(v("self"), app(PRED, v("a")), app(PRED, v("b"))),
    )
    sub = app(FIX, lam("self", lam("a", lam("b", sub_body))))

    lt_body = app(
        IFZ,
        v("b"),
        nat(0),
        app(
            IFZ,
            v("a"),
            nat(1),
            app(v("self"), app(PRED, v("a")), app(PRED, v("b"))),
        ),
    )
    lt = app(FIX, lam("self", lam("a", lam("b", lt_body))))

    eq_body = app(
        IFZ,
        v("a"),
        app(IFZ, v("b"), nat(1), nat(0)),
        app(
            IFZ,
            v("b"),
            nat(0),
            app(v("self"), app(PRED, v("a")), app(PRED, v("b"))),
        ),
    )
    eq = app(FIX, lam("self", lam("a", lam("b", eq_body))))

    bitlen = let(
        "halve",
        halve,
        app(
            FIX,
            lam(
                "self",
                lam(
                    "m",
                    app(
                        IFZ,
                        v("m"),
                        nat(0),
                        app(SUCC, app(v("self"), app(v("halve"), v("m")))),
                    ),
                ),
            ),
        ),
    )

    u_len = let(
        "bitlen",
        bitlen,
        let(
            "add",
            add,
            lam(
                "n",
                let(
                    "l",
                    app(v("bitlen"), app(SUCC, v("n"))),
                    app(PRED, app(v("add"), v("l"), v("l"))),
                ),
            ),
        ),
    )

    u_bit = let(
        "bitlen",
        bitlen,
        let(
            "lt",
            lt,
            let(
                "sub",
                sub,
                let(
                    "odd",
                    odd,
                    let(
                        "shift",
                        shift_right,
                        lam(
                            "n",
                            lam(
                                "q",
                                let(
                                    "m",
                                    app(SUCC, v("n")),
                                    let(
                                        "l",
                                        app(v("bitlen"), v("m")),
                                        let(
                                            "zeros",
                                            app(PRED, v("l")),
                                            app(
                                                IFZ,
                                                app(v("lt"), v("q"), v("zeros")),
                                                let(
                                                    "pos",
                                                    app(v("sub"), v("q"), v("zeros")),
                                                    let(
                                                        "exp",
                                                        app(v("sub"), v("zeros"), v("pos")),
                                                        app(v("odd"), app(v("shift"), v("m"), v("exp"))),
                                                    ),
                                                ),
                                                nat(0),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )

    return add, sub, lt, eq, bitlen, u_len, u_bit


def case6_call(kind, branches):
    if len(branches) != 7:
        raise ValueError("case6 requires six branches plus bad")
    return app(v("case6"), kind, *branches)


def source_decode_term():
    add, sub, lt, eq, _bitlen, _u_len, _u_bit = source_arithmetic()
    head = source_read_head()
    case6 = source_case6()

    count_leaf = scan_result(nat(0), nat(2), next_of(v("h")))
    count_one = let(
        "c",
        app(v("self"), v("s"), next_of(v("h"))),
        app(
            IFZ,
            scan_status(v("c")),
            scan_result(nat(0), app(SUCC, scan_amount(v("c"))), scan_next(v("c"))),
            scan_result(scan_status(v("c")), nat(0), scan_next(v("c"))),
        ),
    )
    count_two = let(
        "c1",
        app(v("self"), v("s"), next_of(v("h"))),
        app(
            IFZ,
            scan_status(v("c1")),
            let(
                "c2",
                app(v("self"), v("s"), scan_next(v("c1"))),
                app(
                    IFZ,
                    scan_status(v("c2")),
                    scan_result(
                        nat(0),
                        app(SUCC, app(v("add"), scan_amount(v("c1")), scan_amount(v("c2")))),
                        scan_next(v("c2")),
                    ),
                    scan_result(scan_status(v("c2")), nat(0), scan_next(v("c2"))),
                ),
            ),
            scan_result(scan_status(v("c1")), nat(0), scan_next(v("c1"))),
        ),
    )
    count_body = let(
        "h",
        app(v("head"), v("s"), v("off")),
        app(
            IFZ,
            status_of(v("h")),
            case6_call(
                a_of(v("h")),
                [count_leaf, count_one, count_two, count_two, count_leaf, count_leaf, scan_result(nat(3), nat(0), v("off"))],
            ),
            scan_result(status_of(v("h")), nat(0), next_of(v("h"))),
        ),
    )
    count = app(FIX, lam("self", lam("s", lam("off", count_body))))

    leaf_token = b_of(v("h"))
    unary_token = app(v("self"), v("s"), next_of(v("h")), v("q1"))
    binary_token = let(
        "left",
        app(v("count"), v("s"), next_of(v("h"))),
        app(
            IFZ,
            app(v("lt"), v("q1"), scan_amount(v("left"))),
            app(
                v("self"),
                v("s"),
                scan_next(v("left")),
                app(v("sub"), v("q1"), scan_amount(v("left"))),
            ),
            app(v("self"), v("s"), next_of(v("h")), v("q1")),
        ),
    )
    token_body = let(
        "h",
        app(v("head"), v("s"), v("off")),
        app(
            IFZ,
            v("q"),
            a_of(v("h")),
            let(
                "q1",
                app(PRED, v("q")),
                case6_call(
                    a_of(v("h")),
                    [leaf_token, unary_token, binary_token, binary_token, leaf_token, leaf_token, nat(0)],
                ),
            ),
        ),
    )
    token_at = app(FIX, lam("self", lam("s", lam("off", lam("q", token_body)))))

    empty_tokens = app(PAIR, lam("i", nat(0)), nat(0))
    decode_body = let(
        "raw",
        fst(v("bits")),
        let(
            "length",
            snd(v("bits")),
            let(
                "bounded",
                lam(
                    "i",
                    app(
                        IFZ,
                        app(v("lt"), v("i"), v("length")),
                        nat(2),
                        app(v("raw"), v("i")),
                    ),
                ),
                let(
                    "r",
                    app(v("count"), v("bounded"), nat(0)),
                    app(
                        IFZ,
                        scan_status(v("r")),
                        app(
                            IFZ,
                            app(v("eq"), scan_next(v("r")), v("length")),
                            codec_result(nat(2), fst(v("empty")), snd(v("empty"))),
                            let(
                                "tokenCount",
                                scan_amount(v("r")),
                                let(
                                    "out",
                                    lam(
                                        "i",
                                        app(
                                            IFZ,
                                            app(v("lt"), v("i"), v("tokenCount")),
                                            nat(0),
                                            app(v("tokenAt"), v("bounded"), nat(0), v("i")),
                                        ),
                                    ),
                                    codec_result(nat(0), v("out"), v("tokenCount")),
                                ),
                            ),
                        ),
                        codec_result(scan_status(v("r")), fst(v("empty")), snd(v("empty"))),
                    ),
                ),
            ),
        ),
    )

    return let(
        "case6",
        case6,
        let(
            "add",
            add,
            let(
                "sub",
                sub,
                let(
                    "lt",
                    lt,
                    let(
                        "eq",
                        eq,
                        let(
                            "head",
                            head,
                            let(
                                "count",
                                count,
                                let(
                                    "tokenAt",
                                    token_at,
                                    let("empty", empty_tokens, lam("bits", decode_body)),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )


def source_encode_term():
    add, sub, lt, eq, _bitlen, u_len, u_bit = source_arithmetic()
    case6 = source_case6()

    leaf_len = lambda prefix: app(v("add"), nat(prefix), app(v("uLen"), app(v("t"), app(SUCC, v("off")))))

    def leaf_scan(prefix: int):
        return app(
            IFZ,
            app(v("lt"), app(SUCC, v("off")), v("length")),
            scan_result(nat(3), nat(0), v("off")),
            scan_result(nat(0), leaf_len(prefix), app(SUCC, app(SUCC, v("off")))),
        )

    def one_scan(prefix: int):
        return let(
            "c",
            app(v("self"), v("t"), v("length"), app(SUCC, v("off"))),
            app(
                IFZ,
                scan_status(v("c")),
                scan_result(nat(0), app(v("add"), nat(prefix), scan_amount(v("c"))), scan_next(v("c"))),
                scan_result(nat(3), nat(0), scan_next(v("c"))),
            ),
        )

    def two_scan(prefix: int):
        return let(
            "c1",
            app(v("self"), v("t"), v("length"), app(SUCC, v("off"))),
            app(
                IFZ,
                scan_status(v("c1")),
                let(
                    "c2",
                    app(v("self"), v("t"), v("length"), scan_next(v("c1"))),
                    app(
                        IFZ,
                        scan_status(v("c2")),
                        scan_result(
                            nat(0),
                            app(v("add"), nat(prefix), app(v("add"), scan_amount(v("c1")), scan_amount(v("c2")))),
                            scan_next(v("c2")),
                        ),
                        scan_result(nat(3), nat(0), scan_next(v("c2"))),
                    ),
                ),
                scan_result(nat(3), nat(0), scan_next(v("c1"))),
            ),
        )

    wire_len_body = app(
        IFZ,
        app(v("lt"), v("off"), v("length")),
        scan_result(nat(3), nat(0), v("off")),
        let(
            "tag",
            app(v("t"), v("off")),
            case6_call(
                v("tag"),
                [leaf_scan(2), one_scan(2), two_scan(2), two_scan(3), leaf_scan(4), leaf_scan(4), scan_result(nat(3), nat(0), v("off"))],
            ),
        ),
    )
    wire_len = app(FIX, lam("self", lam("t", lam("length", lam("off", wire_len_body)))))

    prefix_len = lam(
        "kind",
        case6_call(v("kind"), [nat(2), nat(2), nat(2), nat(3), nat(4), nat(4), nat(0)]),
    )
    prefix_bit = lam(
        "kind",
        lam(
            "q",
            case6_call(
                v("kind"),
                [
                    nat(0),
                    app(IFZ, v("q"), nat(0), nat(1)),
                    app(IFZ, v("q"), nat(1), nat(0)),
                    app(IFZ, v("q"), nat(1), app(IFZ, app(PRED, v("q")), nat(1), nat(0))),
                    app(IFZ, app(v("eq"), v("q"), nat(3)), nat(1), nat(0)),
                    nat(1),
                    nat(0),
                ],
            ),
        ),
    )

    leaf_bit = app(v("uBit"), app(v("t"), app(SUCC, v("off"))), v("rem"))
    unary_bit = app(v("self"), v("t"), v("length"), app(SUCC, v("off")), v("rem"))
    binary_bit = let(
        "left",
        app(v("wireLen"), v("t"), v("length"), app(SUCC, v("off"))),
        app(
            IFZ,
            app(v("lt"), v("rem"), scan_amount(v("left"))),
            app(
                v("self"),
                v("t"),
                v("length"),
                scan_next(v("left")),
                app(v("sub"), v("rem"), scan_amount(v("left"))),
            ),
            app(v("self"), v("t"), v("length"), app(SUCC, v("off")), v("rem")),
        ),
    )
    wire_bit_body = let(
        "tag",
        app(v("t"), v("off")),
        let(
            "plen",
            app(v("prefixLen"), v("tag")),
            app(
                IFZ,
                app(v("lt"), v("q"), v("plen")),
                let(
                    "rem",
                    app(v("sub"), v("q"), v("plen")),
                    case6_call(v("tag"), [leaf_bit, unary_bit, binary_bit, binary_bit, leaf_bit, leaf_bit, nat(0)]),
                ),
                app(v("prefixBit"), v("tag"), v("q")),
            ),
        ),
    )
    wire_bit = app(FIX, lam("self", lam("t", lam("length", lam("off", lam("q", wire_bit_body))))))

    empty_bits = app(PAIR, lam("i", nat(2)), nat(0))
    encode_body = let(
        "t",
        fst(v("term")),
        let(
            "length",
            snd(v("term")),
            let(
                "r",
                app(v("wireLen"), v("t"), v("length"), nat(0)),
                app(
                    IFZ,
                    scan_status(v("r")),
                    app(
                        IFZ,
                        app(v("eq"), scan_next(v("r")), v("length")),
                        codec_result(nat(3), fst(v("empty")), snd(v("empty"))),
                        let(
                            "bitLength",
                            scan_amount(v("r")),
                            let(
                                "out",
                                lam(
                                    "i",
                                    app(
                                        IFZ,
                                        app(v("lt"), v("i"), v("bitLength")),
                                        nat(2),
                                        app(v("wireBit"), v("t"), v("length"), nat(0), v("i")),
                                    ),
                                ),
                                codec_result(nat(0), v("out"), v("bitLength")),
                            ),
                        ),
                    ),
                    codec_result(nat(3), fst(v("empty")), snd(v("empty"))),
                ),
            ),
        ),
    )

    return let(
        "case6",
        case6,
        let(
            "add",
            add,
            let(
                "sub",
                sub,
                let(
                    "lt",
                    lt,
                    let(
                        "eq",
                        eq,
                        let(
                            "uLen",
                            u_len,
                            let(
                                "uBit",
                                u_bit,
                                let(
                                    "wireLen",
                                    wire_len,
                                    let(
                                        "prefixLen",
                                        prefix_len,
                                        let(
                                            "prefixBit",
                                            prefix_bit,
                                            let(
                                                "wireBit",
                                                wire_bit,
                                                let("empty", empty_bits, lam("term", encode_body)),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )


def source_terms_full_codec():
    return {"decodeTerm": source_decode_term(), "encodeTerm": source_encode_term()}


def pred_n(expression, count: int):
    for _ in range(count):
        expression = app(PRED, expression)
    return expression


def literal_nat_stream(values: list[int], eof_value: int):
    if any((not isinstance(value, int)) or value < 0 for value in values):
        raise ValueError("literal stream values must be naturals")

    def build(index: int):
        if index >= len(values):
            return nat(eof_value)
        return app(IFZ, pred_n(v("i"), index), nat(values[index]), build(index + 1))

    return lam("i", build(0))


def literal_finite_bits(bits: str):
    if any(ch not in "01" for ch in bits):
        raise ValueError("literal bits must contain only 0/1")
    return app(PAIR, literal_nat_stream([int(ch) for ch in bits], 2), nat(len(bits)))


def literal_finite_tokens(tokens: list[int]):
    return app(PAIR, literal_nat_stream(tokens, 0), nat(len(tokens)))


def generated_artifact():
    functions = []
    for name, source in source_terms_full_codec().items():
        bits = encode_core(lower(source))
        functions.append(
            {
                "name": name,
                "wire_bit_length": len(bits),
                "wire_sha256": hashlib.sha256(bits.encode("ascii")).hexdigest(),
                "expected_type": EXPECTED_TYPE,
            }
        )
    return {
        "schema": "nex-selfhost-full-codec-candidate",
        "version": "0.1",
        "status": "stage5.12-development-candidate",
        "core_version": "NEX-1 v0.1",
        "contract": "stage5/selfhost/full-codec-contract-v0.1.json",
        "generator": "stage5/selfhost/build_full_codec.py",
        "representation": {
            "FiniteBits": "(N -> N) * N",
            "FiniteNatTokens": "(N -> N) * N",
            "CodecResult": "N * ((N -> N) * N)",
        },
        "functions": functions,
        "development_workload": "stage5/selfhost/full-codec-development-v0.1.json",
        "holdout_workload": "stage5/selfhost/full-codec-holdout-v0.1.json",
        "holdout_status": "preregistered_unexecuted",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.emit == args.check:
        parser.error("choose exactly one of --emit or --check")
    expected = generated_artifact()
    if args.emit:
        print(json.dumps(expected, indent=2))
        return
    actual = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    if actual != expected:
        raise SystemExit("full-codec-v0.1.json does not match build_full_codec.py")
    print("stage5.12 full codec v0.1 artifact: reproducible")


if __name__ == "__main__":
    main()
