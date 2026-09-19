#!/usr/bin/env python3
"""Build/check Stage 5.12e functional stream candidate v0.2.

v0.1 is preserved as the failed cons-chain construction. v0.2 keeps the same
Stream=N->N contract and frozen workload but implements repeat by direct indexed
recursion, so querying element i does not first build i nested cons closures.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_foundation import FIX, IFZ, PRED, app, encode_core, lam, let, lower, nat, v
from build_functional_stream import CONTRACTS, as_nat, source_terms_functional_stream

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "functional-stream-v0.2.json"


def source_terms_functional_stream_v0_2():
    terms = dict(source_terms_functional_stream())

    # self bit count i:
    #   count == 0 -> EOF
    #   i == 0     -> bit
    #   otherwise  -> self bit (count-1) (i-1)
    #
    # Partial application to bit/count is still a Stream=N->N. The difference
    # from v0.1 is operational only: no recursive cons-chain is materialized.
    body = app(
        IFZ,
        v("count"),
        nat(2),
        app(
            IFZ,
            v("i"),
            as_nat(v("bit")),
            app(
                v("self"),
                v("bit"),
                app(PRED, v("count")),
                app(PRED, v("i")),
            ),
        ),
    )
    repeat = app(
        FIX,
        lam("self", lam("bit", lam("count", lam("i", body)))),
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
                    as_nat(app(v("repeat"), v("bit"), v("count"), v("i"))),
                ),
            ),
        ),
    )

    terms["stream_repeat"] = repeat
    terms["repeat_query"] = repeat_query
    return terms


def generated_artifact() -> dict:
    functions = []
    for name, source in source_terms_functional_stream_v0_2().items():
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
        "schema": "nex-selfhost-functional-stream-candidate",
        "version": "0.2",
        "status": "stage5.12e-indexed-candidate",
        "core_version": "NEX-1 v0.1",
        "supersedes_candidate": "functional-stream-v0.1.json",
        "representation": {
            "type": "N -> N",
            "data_values": [0, 1],
            "eof": 2,
            "invariant": "indices before EOF contain 0 or 1; EOF and all later indices return 2",
        },
        "claims_under_test": [
            "finite streams have a fixed rank-1 HM type",
            "streams can be constructed dynamically as closures",
            "tail/drop can return streams without recursive types",
            "direct indexed producers avoid numeric tree packing and recursive cons-chain materialization",
        ],
        "repeat_strategy": "direct indexed recursion over (count,index)",
        "generator": "stage5/selfhost/build_functional_stream_v0_2.py",
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
            "functional-stream-v0.2.json does not match build_functional_stream_v0_2.py; "
            "run with --write and review the diff"
        )
    print("stage5.12e functional stream v0.2 artifact: reproducible")


if __name__ == "__main__":
    main()
