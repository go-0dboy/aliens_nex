from __future__ import annotations

import json
from pathlib import Path
import unittest

from nex.fixtures import term_from_json
from nex.scope import OutOfScopeError, validate_closed
from nex.term import Lam, Let, Nat, Var

ROOT = Path(__file__).resolve().parents[1]
VECTORS = json.loads((ROOT / "packet/conformance/static-v0.1.json").read_text())


class ScopeConformanceTests(unittest.TestCase):
    def test_scope_vectors(self) -> None:
        for vector in VECTORS["scope_vectors"]:
            term = term_from_json(vector["term"])
            with self.subTest(vector=vector["name"]):
                if vector["valid"]:
                    validate_closed(term)
                else:
                    self.assertEqual(vector["error"], "out_of_scope")
                    with self.assertRaises(OutOfScopeError):
                        validate_closed(term)

    def test_let_value_and_body_have_different_scope(self) -> None:
        with self.assertRaises(OutOfScopeError):
            validate_closed(Let(Var(0), Var(0)))
        validate_closed(Let(Nat(0), Var(0)))
        validate_closed(Lam(Let(Var(0), Var(1))))

    def test_huge_index_is_compared_mathematically(self) -> None:
        with self.assertRaises(OutOfScopeError):
            validate_closed(Lam(Var(10**1000)))


if __name__ == "__main__":
    unittest.main()
