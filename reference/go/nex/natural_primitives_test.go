package nex

import (
	"math/big"
	"testing"
)

func TestSuccAndPred(t *testing.T) {
	succ := App(Prim(NaturalUint64(1)), Nat(NaturalUint64(41)))
	value, err := EvaluateClosed(succ, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 42)

	predZero := App(Prim(NaturalUint64(2)), Nat(NaturalUint64(0)))
	value, err = EvaluateClosed(predZero, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 0)

	predFive := App(Prim(NaturalUint64(2)), Nat(NaturalUint64(5)))
	value, err = EvaluateClosed(predFive, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 4)
}

func TestSuccPreservesArbitraryPrecision(t *testing.T) {
	large := new(big.Int).Lsh(big.NewInt(1), 130)
	term := App(Prim(NaturalUint64(1)), Nat(large))
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	want := new(big.Int).Add(new(big.Int).Set(large), big.NewInt(1))
	if value == nil || value.Kind != ValueNat || value.Nat == nil || value.Nat.Cmp(want) != 0 {
		t.Fatalf("succ(2^130) = %#v, want %s", value, want)
	}
}

func TestIfzZeroDoesNotEvaluateNonzeroBranch(t *testing.T) {
	term := App(
		App(
			App(Prim(NaturalUint64(3)), Nat(NaturalUint64(0))),
			Nat(NaturalUint64(42)),
		),
		divergingFixTerm(),
	)
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 42)
}

func TestIfzNonzeroDoesNotEvaluateZeroBranch(t *testing.T) {
	term := App(
		App(
			App(Prim(NaturalUint64(3)), Nat(NaturalUint64(1))),
			divergingFixTerm(),
		),
		Nat(NaturalUint64(9)),
	)
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 9)
}
