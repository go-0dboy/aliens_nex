package nex

import "testing"

func terminatingEvalTerm(selector, n byte) *Term {
	value := NaturalUint64(uint64(n))
	switch selector % 8 {
	case 0:
		return Nat(value)
	case 1:
		return App(Lam(Var(NaturalUint64(0))), Nat(value))
	case 2:
		return App(Prim(NaturalUint64(1)), Nat(value))
	case 3:
		return App(Prim(NaturalUint64(2)), Nat(value))
	case 4:
		discriminant := NaturalUint64(uint64(n % 2))
		return App(
			App(
				App(Prim(NaturalUint64(3)), Nat(discriminant)),
				Nat(value),
			),
			Nat(NaturalUint64(uint64(n)+1)),
		)
	case 5:
		return App(Prim(NaturalUint64(5)), pairTerm(Nat(value), Prim(NaturalUint64(10))))
	case 6:
		return App(Prim(NaturalUint64(6)), pairTerm(Prim(NaturalUint64(10)), Nat(value)))
	default:
		return caseTerm(
			inlTerm(Nat(value)),
			Lam(Var(NaturalUint64(0))),
			Lam(Nat(NaturalUint64(0))),
		)
	}
}

func FuzzEvaluationDeterministicObservation(f *testing.F) {
	for _, seed := range [][2]byte{{0, 0}, {1, 42}, {4, 9}, {7, 255}} {
		f.Add(seed[0], seed[1])
	}
	f.Fuzz(func(t *testing.T, selector, n byte) {
		term := terminatingEvalTerm(selector, n)
		first, err := EvaluateClosed(term, DefaultEvalLimits)
		if err != nil {
			t.Fatalf("first EvaluateClosed() failed: %v", err)
		}
		second, err := EvaluateClosed(term, DefaultEvalLimits)
		if err != nil {
			t.Fatalf("second EvaluateClosed() failed: %v", err)
		}
		firstObservation, err := observeValue(first)
		if err != nil {
			t.Fatal(err)
		}
		secondObservation, err := observeValue(second)
		if err != nil {
			t.Fatal(err)
		}
		if firstObservation != secondObservation {
			t.Fatalf("non-deterministic observations: %#v != %#v", firstObservation, secondObservation)
		}
	})
}
