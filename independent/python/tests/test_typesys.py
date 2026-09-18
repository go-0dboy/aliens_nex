from __future__ import annotations

import json
from pathlib import Path
import unittest

from nex.fixtures import term_from_json
from nex.scope import OutOfScopeError
from nex.term import App, Lam, Let, Nat, Prim, Var
from nex.typesys import (
    NAT,
    OccursCheckError,
    TypeMismatchError,
    TyFun,
    TyVar,
    UnknownPrimitiveError,
    infer_principal,
    render_scheme,
    unify,
)

ROOT = Path(__file__).resolve().parents[1]
VECTORS = json.loads((ROOT / "packet/conformance/static-v0.1.json").read_text())

ERRORS = {
    "out_of_scope": OutOfScopeError,
    "unknown_primitive": UnknownPrimitiveError,
    "type_mismatch": TypeMismatchError,
    "occurs_check": OccursCheckError,
}


class TypeConformanceTests(unittest.TestCase):
    def test_type_vectors(self) -> None:
        for vector in VECTORS["type_vectors"]:
            term = term_from_json(vector["term"])
            with self.subTest(vector=vector["name"]):
                if vector["valid"]:
                    self.assertEqual(render_scheme(infer_principal(term)), vector["type"])
                else:
                    with self.assertRaises(ERRORS[vector["error"]]):
                        infer_principal(term)

    def test_occurs_check_directly(self) -> None:
        with self.assertRaises(OccursCheckError):
            unify(TyVar(0), TyFun(TyVar(0), NAT))

    def test_let_polymorphism(self) -> None:
        # let id = (lambda x.x) in pair (id 0) (id unit)
        term = Let(
            Lam(Var(0)),
            App(
                App(Prim(4), App(Var(0), Nat(0))),
                App(Var(0), Prim(10)),
            ),
        )
        self.assertEqual(render_scheme(infer_principal(term)), "(N * 1)")

    def test_lambda_parameter_is_monomorphic(self) -> None:
        term = Lam(
            App(
                App(Prim(4), App(Var(0), Nat(0))),
                App(Var(0), Prim(10)),
            )
        )
        with self.assertRaises(TypeMismatchError):
            infer_principal(term)

    def test_instantiation_is_fresh_per_use(self) -> None:
        # Pairing two polymorphic primitive values should preserve independent type vars.
        term = App(App(Prim(4), Prim(7)), Prim(8))
        text = render_scheme(infer_principal(term))
        self.assertTrue(text.startswith("forall "))
        self.assertIn("*", text)


if __name__ == "__main__":
    unittest.main()
