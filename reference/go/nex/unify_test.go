package nex

import (
	"errors"
	"testing"
)

func TestUnifyVariableWithNatural(t *testing.T) {
	sub, err := Unify(TVar(0), TNat())
	if err != nil {
		t.Fatal(err)
	}
	got, err := ApplyType(sub, TVar(0))
	if err != nil {
		t.Fatal(err)
	}
	if !EqualType(got, TNat()) {
		t.Fatal("unification did not bind variable to N")
	}
}

func TestUnifyFunctionsPropagatesSubstitutions(t *testing.T) {
	left := TFunc(TVar(0), TNat())
	right := TFunc(TNat(), TVar(1))
	sub, err := Unify(left, right)
	if err != nil {
		t.Fatal(err)
	}
	leftApplied, err := ApplyType(sub, left)
	if err != nil {
		t.Fatal(err)
	}
	rightApplied, err := ApplyType(sub, right)
	if err != nil {
		t.Fatal(err)
	}
	want := TFunc(TNat(), TNat())
	if !EqualType(leftApplied, want) || !EqualType(rightApplied, want) {
		leftText, _ := CanonicalTypeString(leftApplied)
		rightText, _ := CanonicalTypeString(rightApplied)
		t.Fatalf("unified types = %s and %s, want (N -> N)", leftText, rightText)
	}
}

func TestUnifyProductsAndSums(t *testing.T) {
	left := TProduct(TVar(0), TSum(TNat(), TVar(1)))
	right := TProduct(TUnit(), TSum(TNat(), TUnit()))
	sub, err := Unify(left, right)
	if err != nil {
		t.Fatal(err)
	}
	leftApplied, err := ApplyType(sub, left)
	if err != nil {
		t.Fatal(err)
	}
	rightApplied, err := ApplyType(sub, right)
	if err != nil {
		t.Fatal(err)
	}
	if !EqualType(leftApplied, rightApplied) {
		t.Fatal("product/sum unification did not produce equal types")
	}
}

func TestUnifyRejectsTypeMismatch(t *testing.T) {
	_, err := Unify(TNat(), TUnit())
	if !errors.Is(err, ErrTypeMismatch) {
		t.Fatalf("Unify() error = %v, want ErrTypeMismatch", err)
	}
}

func TestUnifyRejectsOccursCheck(t *testing.T) {
	_, err := Unify(TVar(0), TFunc(TVar(0), TNat()))
	if !errors.Is(err, ErrOccursCheck) {
		t.Fatalf("Unify() error = %v, want ErrOccursCheck", err)
	}
	var occurs *OccursCheckError
	if !errors.As(err, &occurs) || occurs.Var != 0 {
		t.Fatalf("Unify() error = %v, want OccursCheckError for T0", err)
	}
}

func TestUnifySameVariableNeedsNoBinding(t *testing.T) {
	sub, err := Unify(TVar(7), TVar(7))
	if err != nil {
		t.Fatal(err)
	}
	if len(sub) != 0 {
		t.Fatalf("Unify(T7,T7) substitution = %#v, want empty", sub)
	}
}

func FuzzUnifyProducesEqualAppliedTypes(f *testing.F) {
	for _, seed := range [][]byte{{0}, {1, 2, 3}, {3, 1, 4, 1, 5, 9}} {
		f.Add(seed)
	}
	f.Fuzz(func(t *testing.T, data []byte) {
		if len(data) == 0 {
			return
		}
		pos := 0
		left := typeFromFuzzBytes(data, &pos, 0)
		known := Substitution{
			0: TNat(),
			1: TUnit(),
			2: TProduct(TNat(), TUnit()),
		}
		right, err := ApplyType(known, left)
		if err != nil {
			t.Fatal(err)
		}

		sub, err := Unify(left, right)
		if err != nil {
			t.Fatalf("Unify() unexpectedly failed for constructed unifiable types: %v", err)
		}
		leftApplied, err := ApplyType(sub, left)
		if err != nil {
			t.Fatal(err)
		}
		rightApplied, err := ApplyType(sub, right)
		if err != nil {
			t.Fatal(err)
		}
		if !EqualType(leftApplied, rightApplied) {
			t.Fatal("unification property failed: applied types differ")
		}
	})
}
