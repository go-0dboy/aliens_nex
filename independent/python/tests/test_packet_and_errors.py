from __future__ import annotations

import unittest

from nex.eval import EvaluationLimits, EvaluationResourceLimitError, evaluate_observed
from nex.scope import OutOfScopeError
from nex.term import App, Lam, Nat, Prim, Var
from nex.typesys import TypeMismatchError, UnknownPrimitiveError, infer_principal
from nex.wire import InvalidBitError, TrailingDataError, TruncatedError, decode_exact


class ClassificationTests(unittest.TestCase):
    def test_wire_error_classes_are_distinct(self) -> None:
        with self.assertRaises(TruncatedError):
            decode_exact("")
        with self.assertRaises(TrailingDataError):
            decode_exact("010011")
        with self.assertRaises(InvalidBitError):
            decode_exact("01x")

    def test_static_error_classes_are_distinct(self) -> None:
        with self.assertRaises(OutOfScopeError):
            infer_principal(Var(0))
        with self.assertRaises(UnknownPrimitiveError):
            infer_principal(Prim(11))
        with self.assertRaises(TypeMismatchError):
            infer_principal(App(Nat(0), Nat(1)))

    def test_evaluation_limit_is_not_static_invalidity(self) -> None:
        looping = App(Prim(0), Lam(Var(0)))
        # Type inference succeeds; only bounded execution refuses.
        infer_principal(looping)
        with self.assertRaises(EvaluationResourceLimitError):
            evaluate_observed(looping, EvaluationLimits(max_steps=50, max_depth=50))


if __name__ == "__main__":
    unittest.main()
