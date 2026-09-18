package nex

import (
	"errors"
	"testing"
)

func TestCanonicalTypeStringRenamesByFirstOccurrence(t *testing.T) {
	typ := TFunc(TVar(42), TFunc(TVar(9), TVar(42)))
	got, err := CanonicalTypeString(typ)
	if err != nil {
		t.Fatal(err)
	}
	want := "(T0 -> (T1 -> T0))"
	if got != want {
		t.Fatalf("CanonicalTypeString() = %q, want %q", got, want)
	}
}

func TestCanonicalTypeStringCoversCoreTypeConstructors(t *testing.T) {
	typ := TProduct(TNat(), TSum(TUnit(), TVar(99)))
	got, err := CanonicalTypeString(typ)
	if err != nil {
		t.Fatal(err)
	}
	want := "(N * (1 + T0))"
	if got != want {
		t.Fatalf("CanonicalTypeString() = %q, want %q", got, want)
	}
}

func TestCanonicalSchemeStringIgnoresInternalIDsAndQuantifierOrder(t *testing.T) {
	body := TFunc(TVar(42), TFunc(TVar(9), TVar(42)))
	first := TypeScheme{Quantified: []TypeVarID{42, 9}, Body: body}
	second := TypeScheme{Quantified: []TypeVarID{9, 42}, Body: body}

	gotFirst, err := CanonicalSchemeString(first)
	if err != nil {
		t.Fatal(err)
	}
	gotSecond, err := CanonicalSchemeString(second)
	if err != nil {
		t.Fatal(err)
	}
	want := "forall T0 T1. (T0 -> (T1 -> T0))"
	if gotFirst != want || gotSecond != want {
		t.Fatalf("canonical schemes = %q and %q, want %q", gotFirst, gotSecond, want)
	}
}

func TestMonoSchemeHasNoForallPrefix(t *testing.T) {
	got, err := CanonicalSchemeString(MonoScheme(TFunc(TVar(7), TVar(7))))
	if err != nil {
		t.Fatal(err)
	}
	want := "(T0 -> T0)"
	if got != want {
		t.Fatalf("CanonicalSchemeString() = %q, want %q", got, want)
	}
}

func TestValidateSchemeRejectsDuplicateQuantifiers(t *testing.T) {
	s := TypeScheme{Quantified: []TypeVarID{1, 1}, Body: TVar(1)}
	if err := ValidateScheme(s); !errors.Is(err, ErrInvalidType) {
		t.Fatalf("ValidateScheme() error = %v, want ErrInvalidType", err)
	}
}

func TestValidateTypeRejectsInvalidShapes(t *testing.T) {
	cases := []*Type{
		nil,
		{Kind: TypeNat, A: TNat()},
		{Kind: TypeUnit, B: TUnit()},
		{Kind: TypeFunc, A: TNat()},
		{Kind: TypeProduct, B: TNat()},
		{Kind: TypeSum, A: TNat()},
		{Kind: TypeKind(255)},
	}

	for i, typ := range cases {
		if err := ValidateType(typ); !errors.Is(err, ErrInvalidType) {
			t.Fatalf("case %d: ValidateType() error = %v, want ErrInvalidType", i, err)
		}
	}
}

func TestEqualType(t *testing.T) {
	a := TFunc(TVar(1), TProduct(TNat(), TVar(1)))
	b := TFunc(TVar(1), TProduct(TNat(), TVar(1)))
	c := TFunc(TVar(2), TProduct(TNat(), TVar(2)))

	if !EqualType(a, b) {
		t.Fatal("EqualType() = false for identical structures")
	}
	if EqualType(a, c) {
		t.Fatal("EqualType() = true for distinct internal variable IDs")
	}
}
