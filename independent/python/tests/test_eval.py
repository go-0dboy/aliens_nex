from __future__ import annotations

import json
from pathlib import Path
import unittest

from nex.eval import EvaluationLimits, EvaluationResourceLimitError, evaluate_observed
from nex.fixtures import term_from_json
from nex.term import App, Lam, Nat, Prim, Var

ROOT = Path(__file__).resolve().parents[1]
VECTORS = json.loads((ROOT / "packet/conformance/eval-v0.1.json").read_text())


def loop_term():
    return App(Prim(0), Lam(Var(0)))


class EvaluationConformanceTests(unittest.TestCase):
    def test_evaluation_vectors(self) -> None:
        for vector in VECTORS["evaluation_vectors"]:
            with self.subTest(vector=vector["name"]):
                term = term_from_json(vector["term"])
                self.assertEqual(evaluate_observed(term), vector["result"])

    def test_ignored_argument_remains_unforced(self) -> None:
        term = App(Lam(Nat(7)), loop_term())
        self.assertEqual(
            evaluate_observed(term, EvaluationLimits(max_steps=100, max_depth=100)),
            {"kind": "Nat", "value": "7"},
        )

    def test_direct_loop_is_resource_refusal(self) -> None:
        with self.assertRaises(EvaluationResourceLimitError):
            evaluate_observed(loop_term(), EvaluationLimits(max_steps=100, max_depth=100))

    def test_partial_primitives_are_functions(self) -> None:
        self.assertEqual(evaluate_observed(Prim(4)), {"kind": "Function"})
        self.assertEqual(evaluate_observed(App(Prim(4), Nat(1))), {"kind": "Function"})

    def test_pair_observation_does_not_force_fields(self) -> None:
        pair = App(App(Prim(4), loop_term()), loop_term())
        self.assertEqual(
            evaluate_observed(pair, EvaluationLimits(max_steps=100, max_depth=100)),
            {"kind": "Pair"},
        )


if __name__ == "__main__":
    unittest.main()
