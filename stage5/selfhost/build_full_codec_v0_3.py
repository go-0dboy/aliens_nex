#!/usr/bin/env python3
"""Build/check Stage 5.12 full Term codec candidate v0.3.

v0.3 preserves NEX-1 v0.1, canonical wire and the accepted physical carriers.
Unlike v0.1/v0.2 random-access views, recursive parsing constructs functional
fragments once. Parent fragments compose captured child functions and lengths.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from build_foundation import FIX, IFZ, PRED, SUCC, app, encode_core, lam, let, lower, nat, v
from build_stream_parser import a_of, b_of, next_of, source_read_head, status_of
from build_full_codec import (
    EXPECTED_TYPE, PAIR, case6_call, codec_result, fst, snd,
    source_arithmetic, source_case6,
)

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "full-codec-v0.3.json"


def frag_result(status, stream, length, next_offset):
    return app(PAIR, status, app(PAIR, stream, app(PAIR, length, next_offset)))


def frag_status(x): return fst(x)
def frag_stream(x): return fst(snd(x))
def frag_length(x): return fst(snd(snd(x)))
def frag_next(x): return snd(snd(snd(x)))


def source_decode_term_v0_3():
    add, sub, lt, eq, _bitlen, _u_len, _u_bit = source_arithmetic()
    head = source_read_head()
    case6 = source_case6()
    empty = lam("i", nat(0))

    leaf = let(
        "kind", a_of(v("h")),
        let(
            "payload", b_of(v("h")),
            let(
                "out", lam("i", app(IFZ, v("i"), v("kind"), v("payload"))),
                frag_result(nat(0), v("out"), nat(2), next_of(v("h"))),
            ),
        ),
    )

    unary = let(
        "child", app(v("self"), v("s"), next_of(v("h"))),
        app(
            IFZ, frag_status(v("child")),
            let(
                "cs", frag_stream(v("child")),
                let(
                    "cl", frag_length(v("child")),
                    let(
                        "kind", a_of(v("h")),
                        let(
                            "out", lam("i", app(IFZ, v("i"), v("kind"), app(v("cs"), app(PRED, v("i"))))),
                            frag_result(nat(0), v("out"), app(SUCC, v("cl")), frag_next(v("child"))),
                        ),
                    ),
                ),
            ),
            frag_result(frag_status(v("child")), v("empty"), nat(0), frag_next(v("child"))),
        ),
    )

    binary = let(
        "left", app(v("self"), v("s"), next_of(v("h"))),
        app(
            IFZ, frag_status(v("left")),
            let(
                "right", app(v("self"), v("s"), frag_next(v("left"))),
                app(
                    IFZ, frag_status(v("right")),
                    let(
                        "ls", frag_stream(v("left")),
                        let(
                            "ll", frag_length(v("left")),
                            let(
                                "rs", frag_stream(v("right")),
                                let(
                                    "rl", frag_length(v("right")),
                                    let(
                                        "kind", a_of(v("h")),
                                        let(
                                            "out",
                                            lam(
                                                "i",
                                                app(
                                                    IFZ, v("i"), v("kind"),
                                                    let(
                                                        "j", app(PRED, v("i")),
                                                        app(
                                                            IFZ, app(v("lt"), v("j"), v("ll")),
                                                            app(v("rs"), app(v("sub"), v("j"), v("ll"))),
                                                            app(v("ls"), v("j")),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                            frag_result(
                                                nat(0), v("out"),
                                                app(SUCC, app(v("add"), v("ll"), v("rl"))),
                                                frag_next(v("right")),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                    frag_result(frag_status(v("right")), v("empty"), nat(0), frag_next(v("right"))),
                ),
            ),
            frag_result(frag_status(v("left")), v("empty"), nat(0), frag_next(v("left"))),
        ),
    )

    parse_body = let(
        "h", app(v("head"), v("s"), v("off")),
        app(
            IFZ, status_of(v("h")),
            case6_call(
                a_of(v("h")),
                [leaf, unary, binary, binary, leaf, leaf,
                 frag_result(nat(3), v("empty"), nat(0), v("off"))],
            ),
            frag_result(status_of(v("h")), v("empty"), nat(0), next_of(v("h"))),
        ),
    )
    parse = app(FIX, lam("self", lam("s", lam("off", parse_body))))

    decode_body = let(
        "raw", fst(v("bits")),
        let(
            "inputLength", snd(v("bits")),
            let(
                "bounded",
                lam(
                    "i",
                    app(IFZ, app(v("lt"), v("i"), v("inputLength")), nat(2), app(v("raw"), v("i"))),
                ),
                let(
                    "r", app(v("parse"), v("bounded"), nat(0)),
                    app(
                        IFZ, frag_status(v("r")),
                        app(
                            IFZ, app(v("eq"), frag_next(v("r")), v("inputLength")),
                            codec_result(nat(2), v("empty"), nat(0)),
                            let(
                                "inner", frag_stream(v("r")),
                                let(
                                    "outLength", frag_length(v("r")),
                                    let(
                                        "out",
                                        lam(
                                            "i",
                                            app(IFZ, app(v("lt"), v("i"), v("outLength")), nat(0), app(v("inner"), v("i"))),
                                        ),
                                        codec_result(nat(0), v("out"), v("outLength")),
                                    ),
                                ),
                            ),
                        ),
                        codec_result(frag_status(v("r")), v("empty"), nat(0)),
                    ),
                ),
            ),
        ),
    )

    return let(
        "case6", case6,
        let("add", add,
            let("sub", sub,
                let("lt", lt,
                    let("eq", eq,
                        let("head", head,
                            let("empty", empty,
                                let("parse", parse, lam("bits", decode_body))))))))
    )


def source_encode_term_v0_3():
    add, sub, lt, eq, _bitlen, u_len, u_bit = source_arithmetic()
    case6 = source_case6()
    empty = lam("i", nat(2))

    prefix_len = lam("kind", case6_call(v("kind"), [nat(2),nat(2),nat(2),nat(3),nat(4),nat(4),nat(0)]))
    prefix_bit = lam(
        "kind", lam(
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
        )
    )

    malformed = frag_result(nat(3), empty, nat(0), v("off"))

    leaf = app(
        IFZ, app(v("lt"), app(SUCC, v("off")), v("length")),
        malformed,
        let(
            "payload", app(v("t"), app(SUCC, v("off"))),
            let(
                "plen", app(v("prefixLen"), v("tag")),
                let(
                    "ulen", app(v("uLen"), v("payload")),
                    let(
                        "outLen", app(v("add"), v("plen"), v("ulen")),
                        let(
                            "out",
                            lam(
                                "i",
                                app(
                                    IFZ, app(v("lt"), v("i"), v("plen")),
                                    app(v("uBit"), v("payload"), app(v("sub"), v("i"), v("plen"))),
                                    app(v("prefixBit"), v("tag"), v("i")),
                                ),
                            ),
                            frag_result(nat(0), v("out"), v("outLen"), app(SUCC, app(SUCC, v("off")))),
                        ),
                    ),
                ),
            ),
        ),
    )

    unary = let(
        "child", app(v("self"), v("t"), v("length"), app(SUCC, v("off"))),
        app(
            IFZ, frag_status(v("child")),
            let(
                "cs", frag_stream(v("child")),
                let(
                    "cl", frag_length(v("child")),
                    let(
                        "plen", app(v("prefixLen"), v("tag")),
                        let(
                            "outLen", app(v("add"), v("plen"), v("cl")),
                            let(
                                "out",
                                lam(
                                    "i",
                                    app(
                                        IFZ, app(v("lt"), v("i"), v("plen")),
                                        app(v("cs"), app(v("sub"), v("i"), v("plen"))),
                                        app(v("prefixBit"), v("tag"), v("i")),
                                    ),
                                ),
                                frag_result(nat(0), v("out"), v("outLen"), frag_next(v("child"))),
                            ),
                        ),
                    ),
                ),
            ),
            frag_result(frag_status(v("child")), v("empty"), nat(0), frag_next(v("child"))),
        ),
    )

    binary = let(
        "left", app(v("self"), v("t"), v("length"), app(SUCC, v("off"))),
        app(
            IFZ, frag_status(v("left")),
            let(
                "right", app(v("self"), v("t"), v("length"), frag_next(v("left"))),
                app(
                    IFZ, frag_status(v("right")),
                    let(
                        "ls", frag_stream(v("left")),
                        let(
                            "ll", frag_length(v("left")),
                            let(
                                "rs", frag_stream(v("right")),
                                let(
                                    "rl", frag_length(v("right")),
                                    let(
                                        "plen", app(v("prefixLen"), v("tag")),
                                        let(
                                            "leftEnd", app(v("add"), v("plen"), v("ll")),
                                            let(
                                                "outLen", app(v("add"), v("leftEnd"), v("rl")),
                                                let(
                                                    "out",
                                                    lam(
                                                        "i",
                                                        app(
                                                            IFZ, app(v("lt"), v("i"), v("plen")),
                                                            let(
                                                                "j", app(v("sub"), v("i"), v("plen")),
                                                                app(
                                                                    IFZ, app(v("lt"), v("j"), v("ll")),
                                                                    app(v("rs"), app(v("sub"), v("j"), v("ll"))),
                                                                    app(v("ls"), v("j")),
                                                                ),
                                                            ),
                                                            app(v("prefixBit"), v("tag"), v("i")),
                                                        ),
                                                    ),
                                                    frag_result(nat(0), v("out"), v("outLen"), frag_next(v("right"))),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                    frag_result(frag_status(v("right")), v("empty"), nat(0), frag_next(v("right"))),
                ),
            ),
            frag_result(frag_status(v("left")), v("empty"), nat(0), frag_next(v("left"))),
        ),
    )

    parse_body = app(
        IFZ, app(v("lt"), v("off"), v("length")),
        malformed,
        let(
            "tag", app(v("t"), v("off")),
            case6_call(v("tag"), [leaf, unary, binary, binary, leaf, leaf, malformed]),
        ),
    )
    parse = app(FIX, lam("self", lam("t", lam("length", lam("off", parse_body)))))

    encode_body = let(
        "t", fst(v("term")),
        let(
            "inputLength", snd(v("term")),
            let(
                "r", app(v("parse"), v("t"), v("inputLength"), nat(0)),
                app(
                    IFZ, frag_status(v("r")),
                    app(
                        IFZ, app(v("eq"), frag_next(v("r")), v("inputLength")),
                        codec_result(nat(3), v("empty"), nat(0)),
                        let(
                            "inner", frag_stream(v("r")),
                            let(
                                "outLength", frag_length(v("r")),
                                let(
                                    "out",
                                    lam(
                                        "i",
                                        app(IFZ, app(v("lt"), v("i"), v("outLength")), nat(2), app(v("inner"), v("i"))),
                                    ),
                                    codec_result(nat(0), v("out"), v("outLength")),
                                ),
                            ),
                        ),
                    ),
                    codec_result(nat(3), v("empty"), nat(0)),
                ),
            ),
        ),
    )

    return let(
        "case6", case6,
        let("add", add,
            let("sub", sub,
                let("lt", lt,
                    let("eq", eq,
                        let("uLen", u_len,
                            let("uBit", u_bit,
                                let("prefixLen", prefix_len,
                                    let("prefixBit", prefix_bit,
                                        let("empty", empty,
                                            let("parse", parse, lam("term", encode_body)))))))))))
    )


def source_terms_full_codec_v0_3():
    return {"decodeTerm": source_decode_term_v0_3(), "encodeTerm": source_encode_term_v0_3()}


def generated_artifact():
    functions = []
    for name, source in source_terms_full_codec_v0_3().items():
        bits = encode_core(lower(source))
        functions.append({
            "name": name,
            "wire_bit_length": len(bits),
            "wire_sha256": hashlib.sha256(bits.encode("ascii")).hexdigest(),
            "expected_type": EXPECTED_TYPE,
        })
    return {
        "schema": "nex-selfhost-full-codec-candidate",
        "version": "0.3",
        "status": "stage5.12-development-candidate",
        "core_version": "NEX-1 v0.1",
        "contract": "stage5/selfhost/full-codec-contract-v0.3.json",
        "generator": "stage5/selfhost/build_full_codec_v0_3.py",
        "representation": {"FiniteBits":"(N -> N) * N","FiniteNatTokens":"(N -> N) * N","CodecResult":"N * ((N -> N) * N)"},
        "algorithm": "recursive parsing constructs reusable functional token/bit fragments once; parent fragments compose captured child functions and lengths",
        "functions": functions,
        "development_manifest": "stage5/selfhost/full-codec-development-v0.3.json",
        "holdout_workload": "stage5/selfhost/full-codec-holdout-v0.3.json",
        "holdout_status": "preregistered_unexecuted",
    }


def main():
    p = argparse.ArgumentParser(); p.add_argument("--emit", action="store_true"); p.add_argument("--check", action="store_true"); a=p.parse_args()
    if a.emit == a.check: p.error("choose exactly one of --emit or --check")
    expected = generated_artifact()
    if a.emit:
        print(json.dumps(expected, indent=2)); return
    actual = json.loads(ARTIFACT.read_text())
    if actual != expected: raise SystemExit("full-codec-v0.3.json does not match builder")
    print("stage5.12 full codec v0.3 artifact: reproducible")


if __name__ == "__main__": main()
