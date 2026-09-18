from __future__ import annotations

import json
from pathlib import Path
import random
import unittest

from nex.fixtures import term_from_json
from nex.term import App, Lam, Let, Nat, Prim, Var
from nex.wire import (
    DecodeLimits,
    ResourceLimitError,
    TrailingDataError,
    TruncatedError,
    decode_exact,
    decode_one,
    decode_u,
    encode_term,
    encode_u,
)

ROOT = Path(__file__).resolve().parents[1]
VECTORS = json.loads((ROOT / "packet/conformance/wire-v0.1.json").read_text())


class WireConformanceTests(unittest.TestCase):
    def test_integer_vectors(self) -> None:
        for vector in VECTORS["integer_vectors"]:
            with self.subTest(vector=vector["name"]):
                n = int(vector["value"])
                self.assertEqual(encode_u(n), vector["bits"])
                value, used = decode_u(vector["bits"])
                self.assertEqual(value, n)
                self.assertEqual(used, len(vector["bits"]))

    def test_term_vectors(self) -> None:
        for vector in VECTORS["term_vectors"]:
            with self.subTest(vector=vector["name"]):
                term = term_from_json(vector["term"])
                self.assertEqual(encode_term(term), vector["bits"])
                decoded, consumed = decode_one(vector["bits"] + "101010")
                self.assertEqual(decoded, term)
                self.assertEqual(consumed, len(vector["bits"]))
                self.assertEqual(decode_exact(vector["bits"]), term)

    def test_invalid_exact_vectors(self) -> None:
        for vector in VECTORS["invalid_exact_vectors"]:
            with self.subTest(vector=vector["name"]):
                if vector["error"] == "truncated":
                    with self.assertRaises(TruncatedError):
                        decode_exact(vector["bits"])
                elif vector["error"] == "trailing":
                    with self.assertRaises(TrailingDataError):
                        decode_exact(vector["bits"])
                else:
                    self.fail(f"unknown expected error {vector['error']}")

    def test_huge_integer_round_trip(self) -> None:
        n = (1 << 4096) + 123456789
        bits = encode_u(n)
        self.assertEqual(decode_u(bits), (n, len(bits)))
        term = Nat(n)
        self.assertEqual(decode_exact(encode_term(term)), term)

    def test_resource_limits_are_not_syntax_errors(self) -> None:
        bits = encode_term(Nat(1 << 200))
        with self.assertRaises(ResourceLimitError):
            decode_exact(bits, DecodeLimits(max_integer_bits=64))
        self.assertEqual(decode_exact(bits, DecodeLimits(max_integer_bits=512)), Nat(1 << 200))

        deep = Lam(Lam(Lam(Var(0))))
        with self.assertRaises(ResourceLimitError):
            decode_exact(encode_term(deep), DecodeLimits(max_depth=3))
        self.assertEqual(decode_exact(encode_term(deep), DecodeLimits(max_depth=4)), deep)

        tree = App(Nat(0), Nat(1))
        with self.assertRaises(ResourceLimitError):
            decode_exact(encode_term(tree), DecodeLimits(max_nodes=2))
        self.assertEqual(decode_exact(encode_term(tree), DecodeLimits(max_nodes=3)), tree)

    def test_host_decoder_recursion_exhaustion_is_resource_refusal(self) -> None:
        # A deeply nested but otherwise canonical term must never be relabeled malformed.
        bits = "01" * 5000 + "11101"
        with self.assertRaises(ResourceLimitError):
            decode_exact(bits)

    def test_deterministic_generated_round_trips(self) -> None:
        rng = random.Random(20260918)

        def gen(depth: int):
            if depth <= 0:
                leaf = rng.randrange(3)
                if leaf == 0:
                    return Var(rng.randrange(0, 1 << 80))
                if leaf == 1:
                    return Nat(rng.randrange(0, 1 << 160))
                return Prim(rng.randrange(0, 1 << 80))
            kind = rng.randrange(6)
            if kind == 0:
                return Var(rng.randrange(0, 1 << 80))
            if kind == 1:
                return Lam(gen(depth - 1))
            if kind == 2:
                return App(gen(depth - 1), gen(depth - 1))
            if kind == 3:
                return Let(gen(depth - 1), gen(depth - 1))
            if kind == 4:
                return Nat(rng.randrange(0, 1 << 160))
            return Prim(rng.randrange(0, 1 << 80))

        for _ in range(250):
            term = gen(5)
            bits = encode_term(term)
            self.assertEqual(decode_exact(bits), term)
            decoded, used = decode_one(bits + "1")
            self.assertEqual((decoded, used), (term, len(bits)))


if __name__ == "__main__":
    unittest.main()
