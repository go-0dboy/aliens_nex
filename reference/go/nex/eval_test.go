package nex

import (
	"errors"
	"testing"
)

func requireNatValue(t *testing.T, value *Value, want uint64) {
	t.Helper()
	if value == nil || value.Kind != ValueNat || value.Nat == nil {
		t.Fatalf("value = %#v, want Nat(%d)", value, want)
	}
	if value.Nat.Cmp(NaturalUint64(want)) != 0 {
		t.Fatalf("Nat value = %s, want %d", value.Nat, want)
	}
}

func divergingFixTerm() *Term {
	// fix (\self -> self)
	return App(Prim(NaturalUint64(0)), Lam(Var(NaturalUint64(0))))
}

func TestEvaluateClosedNat(t *testing.T) {
	value, err := EvaluateClosed(Nat(NaturalUint64(42)), DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 42)
}

func TestEvaluateIdentityApplication(t *testing.T) {
	term := App(Lam(Var(NaturalUint64(0))), Nat(NaturalUint64(42)))
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 42)
}

func TestEvaluateNestedDeBruijnEnvironment(t *testing.T) {
	// ((\x -> \y -> x) 7) 9 -> 7
	term := App(
		App(
			Lam(Lam(Var(NaturalUint64(1)))),
			Nat(NaturalUint64(7)),
		),
		Nat(NaturalUint64(9)),
	)
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 7)
}

func TestEvaluateLetBinding(t *testing.T) {
	// let id = \x -> x in id 42
	term := Let(
		Lam(Var(NaturalUint64(0))),
		App(Var(NaturalUint64(0)), Nat(NaturalUint64(42))),
	)
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 42)
}

func TestIgnoredLambdaArgumentIsNotEvaluated(t *testing.T) {
	term := App(
		Lam(Nat(NaturalUint64(7))),
		divergingFixTerm(),
	)
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 7)
}

func TestUnusedLetValueIsNotEvaluated(t *testing.T) {
	term := Let(
		divergingFixTerm(),
		Nat(NaturalUint64(7)),
	)
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 7)
}

func TestLambdaBodyIsNotEvaluatedUntilApplication(t *testing.T) {
	term := Lam(divergingFixTerm())
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	if value == nil || value.Kind != ValueClosure || value.Closure == nil {
		t.Fatalf("value = %#v, want closure", value)
	}
}

func TestDemandedDivergingFixHitsResourceLimit(t *testing.T) {
	_, err := EvaluateClosed(divergingFixTerm(), EvalLimits{MaxTransitions: 40, MaxDepth: 1_000})
	if !errors.Is(err, ErrEvalResourceLimit) {
		t.Fatalf("EvaluateClosed(diverging fix) error = %v, want ErrEvalResourceLimit", err)
	}
}

func TestEvaluateClosedPreservesStaticErrors(t *testing.T) {
	_, err := EvaluateClosed(Var(NaturalUint64(0)), DefaultEvalLimits)
	if !errors.Is(err, ErrOutOfScope) {
		t.Fatalf("EvaluateClosed(free Var) error = %v, want ErrOutOfScope", err)
	}
}

func TestEvaluationResourceLimitIsDistinct(t *testing.T) {
	term := App(Lam(Var(NaturalUint64(0))), Nat(NaturalUint64(42)))
	_, err := EvaluateClosed(term, EvalLimits{MaxTransitions: 1, MaxDepth: 100})
	if !errors.Is(err, ErrEvalResourceLimit) {
		t.Fatalf("EvaluateClosed() error = %v, want ErrEvalResourceLimit", err)
	}
}
