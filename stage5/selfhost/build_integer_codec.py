#!/usr/bin/env python3
"""Build/check Stage 5.12c NEX-written U(n) codec terms.

Readable names are generator notation only. The research objects are closed,
canonical NEX-1 v0.1 terms frozen in integer-codec-v0.1.json.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_foundation import FIX, IFZ, PRED, SUCC, app, encode_core, lam, let, lower, nat, v, source_terms
from build_meta_sequence import source_terms_5_12b

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "integer-codec-v0.1.json"


def pair_code(a: int, b: int) -> int:
    return (1 << a) * (2 * b + 1) - 1


def seq_code(items: list[int]) -> int:
    result = 0
    for item in reversed(items):
        result = 1 + pair_code(item, result)
    return result


def bits_code(bits: str) -> int:
    return seq_code([int(bit) for bit in bits])


def ok_code(value: int, rest: int) -> int:
    return pair_code(0, pair_code(value, rest))


def error_code(tag: int) -> int:
    return pair_code(tag, 0)


def source_terms_5_12c():
    foundation = source_terms()
    meta = source_terms_5_12b()
    add = foundation["add"]
    odd = foundation["odd"]
    halve = foundation["halve"]
    pair = meta["meta_pair"]
    cons = meta["seq_cons"]
    head = meta["seq_head"]
    tail = meta["seq_tail"]

    length_body = app(
        IFZ,
        v("s"),
        nat(0),
        app(SUCC, app(v("self"), app(v("tail"), v("s")))),
    )
    seq_length = let(
        "tail",
        tail,
        app(FIX, lam("self", lam("s", length_body))),
    )

    reverse_loop = app(
        IFZ,
        v("s"),
        v("acc"),
        app(
            v("self"),
            app(v("tail"), v("s")),
            app(v("cons"), app(v("head"), v("s")), v("acc")),
        ),
    )
    reverse_fn = app(
        FIX,
        lam("self", lam("s", lam("acc", reverse_loop))),
    )
    seq_reverse = let(
        "head",
        head,
        let(
            "tail",
            tail,
            let(
                "cons",
                cons,
                lam("s", app(reverse_fn, v("s"), nat(0))),
            ),
        ),
    )

    binary_rev_body = app(
        IFZ,
        v("m"),
        nat(0),
        app(
            v("cons"),
            app(v("odd"), v("m")),
            app(v("self"), app(v("halve"), v("m"))),
        ),
    )
    binary_rev = let(
        "odd",
        odd,
        let(
            "halve",
            halve,
            let(
                "cons",
                cons,
                app(FIX, lam("self", lam("m", binary_rev_body))),
            ),
        ),
    )

    prepend_body = app(
        IFZ,
        v("k"),
        v("bits"),
        app(
            v("cons"),
            nat(0),
            app(v("self"), app(PRED, v("k")), v("bits")),
        ),
    )
    prepend_zeros = let(
        "cons",
        cons,
        app(FIX, lam("self", lam("k", lam("bits", prepend_body)))),
    )

    encode_body = let(
        "revbits",
        app(v("binary_rev"), app(SUCC, v("n"))),
        let(
            "bits",
            app(v("reverse"), v("revbits")),
            app(
                v("prepend"),
                app(PRED, app(v("length"), v("bits"))),
                v("bits"),
            ),
        ),
    )
    encode_u = let(
        "binary_rev",
        binary_rev,
        let(
            "reverse",
            seq_reverse,
            let(
                "length",
                seq_length,
                let("prepend", prepend_zeros, lam("n", encode_body)),
            ),
        ),
    )

    mk_ok = let(
        "pair",
        pair,
        lam(
            "value",
            lam(
                "rest",
                app(
                    v("pair"),
                    nat(0),
                    app(v("pair"), v("value"), v("rest")),
                ),
            ),
        ),
    )
    mk_error = let(
        "pair",
        pair,
        lam("tag", app(v("pair"), v("tag"), nat(0))),
    )

    read_recurse = app(
        v("self"),
        app(PRED, v("count")),
        app(v("tail"), v("s")),
        app(
            v("add"),
            app(v("add"), v("acc"), v("acc")),
            v("bit"),
        ),
    )
    valid_nonzero = app(
        IFZ,
        app(PRED, v("bit")),
        read_recurse,
        app(v("err"), nat(2)),
    )
    read_nonempty = let(
        "bit",
        app(v("head"), v("s")),
        app(IFZ, v("bit"), read_recurse, valid_nonzero),
    )
    read_body = app(
        IFZ,
        v("count"),
        app(v("ok"), app(PRED, v("acc")), v("s")),
        app(
            IFZ,
            v("s"),
            app(v("err"), nat(1)),
            read_nonempty,
        ),
    )
    reader = let(
        "head",
        head,
        let(
            "tail",
            tail,
            let(
                "add",
                add,
                let(
                    "ok",
                    mk_ok,
                    let(
                        "err",
                        mk_error,
                        app(
                            FIX,
                            lam(
                                "self",
                                lam(
                                    "count",
                                    lam("s", lam("acc", read_body)),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )

    scan_zero = app(
        v("self"),
        app(SUCC, v("zeros")),
        app(v("tail"), v("s")),
    )
    scan_one_or_bad = app(
        IFZ,
        app(PRED, v("bit")),
        app(v("reader"), app(SUCC, v("zeros")), v("s"), nat(0)),
        app(v("err"), nat(2)),
    )
    scan_nonempty = let(
        "bit",
        app(v("head"), v("s")),
        app(IFZ, v("bit"), scan_zero, scan_one_or_bad),
    )
    scan_body = app(
        IFZ,
        v("s"),
        app(v("err"), nat(1)),
        scan_nonempty,
    )
    scan_fn = app(
        FIX,
        lam("self", lam("zeros", lam("s", scan_body))),
    )
    decode_u = let(
        "head",
        head,
        let(
            "tail",
            tail,
            let(
                "reader",
                reader,
                let(
                    "err",
                    mk_error,
                    lam("bits", app(scan_fn, nat(0), v("bits"))),
                ),
            ),
        ),
    )

    return {
        "seq_length": seq_length,
        "seq_reverse": seq_reverse,
        "binary_rev": binary_rev,
        "prepend_zeros": prepend_zeros,
        "encodeU": encode_u,
        "decodeU": decode_u,
    }


CONTRACTS = {
    "seq_length": {
        "expected_type": "(N -> N)",
        "tests": [
            {"args": [0], "result": 0},
            {"args": [bits_code("1")], "result": 1},
            {"args": [bits_code("010")], "result": 3},
        ],
    },
    "seq_reverse": {
        "expected_type": "(N -> N)",
        "tests": [
            {"args": [0], "result": 0},
            {"args": [bits_code("10")], "result": bits_code("01")},
            {"args": [bits_code("010")], "result": bits_code("010")},
        ],
    },
    "binary_rev": {
        "expected_type": "(N -> N)",
        "tests": [
            {"args": [1], "result": bits_code("1")},
            {"args": [2], "result": bits_code("01")},
            {"args": [5], "result": bits_code("101")},
        ],
    },
    "prepend_zeros": {
        "expected_type": "(N -> (N -> N))",
        "tests": [
            {"args": [0, bits_code("1")], "result": bits_code("1")},
            {"args": [2, bits_code("10")], "result": bits_code("0010")},
        ],
    },
    "encodeU": {
        "expected_type": "(N -> N)",
        "tests": [
            {"args": [0], "result": bits_code("1"), "bits": "1"},
            {"args": [1], "result": bits_code("010"), "bits": "010"},
            {"args": [2], "result": bits_code("011"), "bits": "011"},
            {"args": [3], "result": bits_code("00100"), "bits": "00100"},
            {"args": [4], "result": bits_code("00101"), "bits": "00101"},
            {"args": [7], "result": bits_code("0001000"), "bits": "0001000"},
        ],
    },
    "decodeU": {
        "expected_type": "(N -> N)",
        "tests": [
            {"args": [bits_code("1")], "result": ok_code(0, bits_code("")), "bits": "1", "expect": "Ok(0,'')"},
            {"args": [bits_code("010")], "result": ok_code(1, bits_code("")), "bits": "010", "expect": "Ok(1,'')"},
            {"args": [bits_code("0111")], "result": ok_code(2, bits_code("1")), "bits": "0111", "expect": "Ok(2,'1')"},
            {"args": [bits_code("00100")], "result": ok_code(3, bits_code("")), "bits": "00100", "expect": "Ok(3,'')"},
            {"args": [bits_code("")], "result": error_code(1), "bits": "", "expect": "Truncated"},
            {"args": [bits_code("0")], "result": error_code(1), "bits": "0", "expect": "Truncated"},
            {"args": [bits_code("00")], "result": error_code(1), "bits": "00", "expect": "Truncated"},
            {"args": [seq_code([2])], "result": error_code(2), "items": [2], "expect": "MalformedBit"},
        ],
    },
}


def generated_artifact() -> dict:
    functions = []
    for name, source in source_terms_5_12c().items():
        bits = encode_core(lower(source))
        functions.append(
            {
                "name": name,
                "wire_bits": bits,
                "wire_bit_length": len(bits),
                **CONTRACTS[name],
            }
        )
    return {
        "schema": "nex-selfhost-integer-codec",
        "version": "0.1",
        "status": "stage5.12c-candidate",
        "core_version": "NEX-1 v0.1",
        "bits_representation": "nat-sequence-v0.1",
        "decode_result_encoding": {
            "Ok": "pair(0,pair(value,rest_bits))",
            "Truncated": "pair(1,0)",
            "MalformedBit": "pair(2,0)",
        },
        "generator": "stage5/selfhost/build_integer_codec.py",
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
            "integer-codec-v0.1.json does not match build_integer_codec.py; "
            "run with --write and review the diff"
        )
    print("stage5.12c integer codec artifact: reproducible")


if __name__ == "__main__":
    main()
