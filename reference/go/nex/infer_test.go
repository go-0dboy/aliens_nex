package nex

import (
	"errors"
	"testing"
)

func inferredSchemeText(t *testing.T, term *Term) string {
	t.Helper()
	scheme, err := InferClosed(term)
	if err != nil {
		t.Fatalf("InferClosed() error = %v", err)
	}
	text, err := CanonicalSchemeString(scheme)
	if err != nil {
		t.Fatalf("CanonicalSchemeString() error = %v", err)
	}
	return text
}

func TestInferIdentity(t *testing.T) {
	got := inferredSchemeText(t, Lam(Var(NaturalUint64(0))))
	want := "forall T0. (T0 -> T0)"
	if got != want {
		t.Fatalf("identity type = %q, want %q", got, want)
	}
}

func TestInferConstantFunction(t *testing.T) {
	term := Lam(Lam(Var(NaturalUint64(1))))
	got := inferredSchemeText(t, term)
	want := "forall T0 T1. (T0 -> (T1 -> T0))"
	if got != want {
		t.Fatalf("constant type = %q, want %q", got, want)
	}
}

func TestInferSuccFunction(t *testing.T) {
	term := Lam(App(Prim(NaturalUint64(1)), Var(NaturalUint64(0))))
	got := inferredSchemeText(t, term)
	want := "(N -> N)"
	if got != want {
		t.Fatalf("succ function type = %q, want %q", got, want)
	}
}

func TestInferPairNatUnit(t *testing.T) {
	term := App(
		App(Prim(NaturalUint64(4)), Nat(NaturalUint64(0))),
		Prim(NaturalUint64(10)),
	)
	got := inferredSchemeText(t, term)
	want := "(N * 1)"
	if got != want {
		t.Fatalf("pair type = %q, want %q", got, want)
	}
}

func TestInferFixPrimitive(t *testing.T) {
	got := inferredSchemeText(t, Prim(NaturalUint64(0)))
	want := "forall T0. ((T0 -> T0) -> T0)"
	if got != want {
		t.Fatalf("fix type = %q, want %q", got, want)
	}
}

func TestInferLetPolymorphismReusesIdentityAtDifferentTypes(t *testing.T) {
	id := Lam(Var(NaturalUint64(0)))
	body := App(
		App(
			Prim(NaturalUint64(4)),
			App(Var(NaturalUint64(0)), Nat(NaturalUint64(0))),
		),
		App(Var(NaturalUint64(0)), Prim(NaturalUint64(10))),
	)
	got := inferredSchemeText(t, Let(id, body))
	want := "(N * 1)"
	if got != want {
		t.Fatalf("let-polymorphic type = %q, want %q", got, want)
	}
}

func TestLambdaBoundVariableRemainsMonomorphic(t *testing.T) {
	body := App(
		App(
			Prim(NaturalUint64(4)),
			App(Var(NaturalUint64(0)), Nat(NaturalUint64(0))),
		),
		App(Var(NaturalUint64(0)), Prim(NaturalUint64(10))),
	)
	_, err := InferClosed(Lam(body))
	if !errors.Is(err, ErrTypeMismatch) {
		t.Fatalf("InferClosed() error = %v, want ErrTypeMismatch", err)
	}
}

func TestInferRejectsSelfApplicationByOccursCheck(t *testing.T) {
	term := Lam(App(Var(NaturalUint64(0)), Var(NaturalUint64(0))))
	_, err := InferClosed(term)
	if !errors.Is(err, ErrOccursCheck) {
		t.Fatalf("InferClosed() error = %v, want ErrOccursCheck", err)
	}
}

func TestInferRejectsCallingNaturalAsFunction(t *testing.T) {
	term := App(Nat(NaturalUint64(0)), Nat(NaturalUint64(1)))
	_, err := InferClosed(term)
	if !errors.Is(err, ErrTypeMismatch) {
		t.Fatalf("InferClosed() error = %v, want ErrTypeMismatch", err)
	}
}

func TestInferPreservesEarlierStaticErrorClasses(t *testing.T) {
	_, err := InferClosed(Var(NaturalUint64(0)))
	if !errors.Is(err, ErrOutOfScope) {
		t.Fatalf("free variable error = %v, want ErrOutOfScope", err)
	}

	_, err = InferClosed(Prim(NaturalUint64(11)))
	if !errors.Is(err, ErrUnknownPrimitive) {
		t.Fatalf("unknown primitive error = %v, want ErrUnknownPrimitive", err)
	}
}

func TestSuccessfulClosedInferenceHasNoFreeSchemeVariables(t *testing.T) {
	terms := []*Term{
		Lam(Var(NaturalUint64(0))),
		Prim(NaturalUint64(0)),
		App(App(Prim(NaturalUint64(4)), Nat(NaturalUint64(0))), Prim(NaturalUint64(10))),
	}
	for i, term := range terms {
		scheme, err := InferClosed(term)
		if err != nil {
			t.Fatalf("case %d: %v", i, err)
		}
		free, err := FreeSchemeVars(scheme)
		if err != nil {
			t.Fatalf("case %d: %v", i, err)
		}
		if len(free) != 0 {
			t.Fatalf("case %d: free vars = %#v, want none", i, free)
		}
	}
}
