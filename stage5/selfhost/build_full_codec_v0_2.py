#!/usr/bin/env python3
"""Build/check Stage 5.12 full Term codec candidate v0.2.

v0.2 preserves the v0.3 data representation, NEX-1 v0.1 canonical wire,
interfaces, errors and frozen resource budgets. Its only algorithmic change is
random-access selection: binary traversal carries a residual query index from
left child to right child instead of first recomputing left subtree size for
every token/bit query.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from build_foundation import FIX, IFZ, PRED, SUCC, app, encode_core, lam, let, lower, nat, v
from build_stream_parser import a_of, b_of, next_of, source_read_head, status_of
from build_full_codec import (
    EXPECTED_TYPE,
    PAIR,
    case6_call,
    codec_result,
    fst,
    literal_finite_bits,
    literal_finite_tokens,
    scan_amount,
    scan_next,
    scan_result,
    scan_status,
    snd,
    source_arithmetic,
    source_case6,
)

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "full-codec-v0.2.json"


def select_result(found, value, remaining, next_offset):
    return app(PAIR, found, app(PAIR, value, app(PAIR, remaining, next_offset)))


def select_found(result):
    return fst(result)


def select_value(result):
    return fst(snd(result))


def select_remaining(result):
    return fst(snd(snd(result)))


def select_next(result):
    return snd(snd(snd(result)))


def source_decode_term_v0_2():
    add, sub, lt, eq, _bitlen, _u_len, _u_bit = source_arithmetic()
    head = source_read_head()
    case6 = source_case6()

    # One validation/count pass remains at top level. This establishes exact
    # structure and token count. It is not used by the per-token selector to
    # pre-count a binary left subtree.
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
                [
                    count_leaf,
                    count_one,
                    count_two,
                    count_two,
                    count_leaf,
                    count_leaf,
                    scan_result(nat(3), nat(0), v("off")),
                ],
            ),
            scan_result(status_of(v("h")), nat(0), next_of(v("h"))),
        ),
    )
    count = app(FIX, lam("self", lam("s", lam("off", count_body))))

    # selectToken(s,off,q) traverses one subtree in preorder. If q lies after
    # the left child, the left result supplies both next wire offset and the
    # residual q for the right child. No count(left) pre-pass occurs here.
    leaf_after_tag = app(
        IFZ,
        v("q1"),
        select_result(nat(1), b_of(v("h")), nat(0), next_of(v("h"))),
        select_result(nat(0), nat(0), app(PRED, v("q1")), next_of(v("h"))),
    )
    unary_after_tag = app(v("self"), v("s"), next_of(v("h")), v("q1"))
    binary_after_tag = let(
        "left",
        app(v("self"), v("s"), next_of(v("h")), v("q1")),
        app(
            IFZ,
            select_found(v("left")),
            app(
                v("self"),
                v("s"),
                select_next(v("left")),
                select_remaining(v("left")),
            ),
            v("left"),
        ),
    )
    selector_after_tag = case6_call(
        a_of(v("h")),
        [
            leaf_after_tag,
            unary_after_tag,
            binary_after_tag,
            binary_after_tag,
            leaf_after_tag,
            leaf_after_tag,
            select_result(nat(0), nat(0), v("q1"), next_of(v("h"))),
        ],
    )
    selector_body = let(
        "h",
        app(v("head"), v("s"), v("off")),
        app(
            IFZ,
            status_of(v("h")),
            app(
                IFZ,
                v("q"),
                select_result(nat(1), a_of(v("h")), nat(0), next_of(v("h"))),
                let("q1", app(PRED, v("q")), selector_after_tag),
            ),
            select_result(nat(0), nat(0), v("q"), next_of(v("h"))),
        ),
    )
    select_token = app(FIX, lam("self", lam("s", lam("off", lam("q", selector_body)))))

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
                                            let(
                                                "selected",
                                                app(v("selectToken"), v("bounded"), nat(0), v("i")),
                                                select_value(v("selected")),
                                            ),
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
                                "selectToken",
                                select_token,
                                let("empty", empty_tokens, lam("bits", decode_body)),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )


def source_encode_term_v0_2():
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
                [
                    leaf_scan(2),
                    one_scan(2),
                    two_scan(2),
                    two_scan(3),
                    leaf_scan(4),
                    leaf_scan(4),
                    scan_result(nat(3), nat(0), v("off")),
                ],
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

    # selectBit(t,length,off,q) consumes prefix/payload/children in canonical
    # order. A missed left child returns residual bit index and next token
    # offset directly to the right child; no wireLen(left) pre-query occurs.
    leaf_select = let(
        "payload",
        app(v("t"), app(SUCC, v("off"))),
        let(
            "ulen",
            app(v("uLen"), v("payload")),
            app(
                IFZ,
                app(v("lt"), v("rem"), v("ulen")),
                select_result(
                    nat(0),
                    nat(0),
                    app(v("sub"), v("rem"), v("ulen")),
                    app(SUCC, app(SUCC, v("off"))),
                ),
                select_result(
                    nat(1),
                    app(v("uBit"), v("payload"), v("rem")),
                    nat(0),
                    app(SUCC, app(SUCC, v("off"))),
                ),
            ),
        ),
    )
    unary_select = app(v("self"), v("t"), v("length"), app(SUCC, v("off")), v("rem"))
    binary_select = let(
        "left",
        app(v("self"), v("t"), v("length"), app(SUCC, v("off")), v("rem")),
        app(
            IFZ,
            select_found(v("left")),
            app(
                v("self"),
                v("t"),
                v("length"),
                select_next(v("left")),
                select_remaining(v("left")),
            ),
            v("left"),
        ),
    )
    after_prefix = let(
        "rem",
        app(v("sub"), v("q"), v("plen")),
        case6_call(
            v("tag"),
            [
                leaf_select,
                unary_select,
                binary_select,
                binary_select,
                leaf_select,
                leaf_select,
                select_result(nat(0), nat(0), v("rem"), app(SUCC, v("off"))),
            ],
        ),
    )
    select_bit_body = let(
        "tag",
        app(v("t"), v("off")),
        let(
            "plen",
            app(v("prefixLen"), v("tag")),
            app(
                IFZ,
                app(v("lt"), v("q"), v("plen")),
                after_prefix,
                select_result(
                    nat(1),
                    app(v("prefixBit"), v("tag"), v("q")),
                    nat(0),
                    v("off"),
                ),
            ),
        ),
    )
    select_bit = app(
        FIX,
        lam("self", lam("t", lam("length", lam("off", lam("q", select_bit_body))))),
    )

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
                                        let(
                                            "selected",
                                            app(v("selectBit"), v("t"), v("length"), nat(0), v("i")),
                                            select_value(v("selected")),
                                        ),
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
                                                "selectBit",
                                                select_bit,
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


def source_terms_full_codec_v0_2():
    return {"decodeTerm": source_decode_term_v0_2(), "encodeTerm": source_encode_term_v0_2()}


def generated_artifact():
    functions = []
    for name, source in source_terms_full_codec_v0_2().items():
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
        "version": "0.2",
        "status": "stage5.12-development-candidate",
        "core_version": "NEX-1 v0.1",
        "contract": "stage5/selfhost/full-codec-contract-v0.2.json",
        "generator": "stage5/selfhost/build_full_codec_v0_2.py",
        "representation": {
            "FiniteBits": "(N -> N) * N",
            "FiniteNatTokens": "(N -> N) * N",
            "CodecResult": "N * ((N -> N) * N)",
        },
        "algorithm": "single-pass preorder selectors carry residual index across binary children; no per-query count(left)/wireLen(left)",
        "functions": functions,
        "development_workload": "stage5/selfhost/full-codec-development-v0.2.json",
        "holdout_workload": "stage5/selfhost/full-codec-holdout-v0.2.json",
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
        raise SystemExit("full-codec-v0.2.json does not match build_full_codec_v0_2.py")
    print("stage5.12 full codec v0.2 artifact: reproducible")


if __name__ == "__main__":
    main()
