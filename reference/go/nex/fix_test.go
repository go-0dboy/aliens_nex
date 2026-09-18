package nex

import (
	"errors"
	"testing"
)

func TestFixCanIgnoreRecursiveArgument(t *testing.T) {
	term := App(
		Prim(NaturalUint64(0)),
		Lam(Nat(NaturalUint64(7))),
	)
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 7)
}

func TestFixSupportsTerminatingRecursion(t *testing.T) {
	// countdown = fix (\self -> \n -> ifz n 0 (succ (self (pred n))))
	countdownBody := Lam(
		Lam(
			App(
				App(
					App(Prim(NaturalUint64(3)), Var(NaturalUint64(0))),
					Nat(NaturalUint64(0)),
				),
				App(
					Prim(NaturalUint64(1)),
					App(
						Var(NaturalUint64(1)),
						App(Prim(NaturalUint64(2)), Var(NaturalUint64(0))),
					),
				),
			),
		),
	)
	countdown := App(Prim(NaturalUint64(0)), countdownBody)
	term := App(countdown, Nat(NaturalUint64(5)))

	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 5)
}

func TestDivergingFixIsResourceRefusalNotStaticError(t *testing.T) {
	_, err := EvaluateClosed(divergingFixTerm(), EvalLimits{MaxTransitions: 50, MaxDepth: 1_000})
	if !errors.Is(err, ErrEvalResourceLimit) {
		t.Fatalf("EvaluateClosed(diverging fix) error = %v, want ErrEvalResourceLimit", err)
	}
	if errors.Is(err, ErrOutOfScope) || errors.Is(err, ErrTypeMismatch) || errors.Is(err, ErrOccursCheck) {
		t.Fatalf("resource refusal was misclassified as static error: %v", err)
	}
}
