package nex

import (
	"errors"
	"testing"
)

func TestCorePrimitiveTableMatchesSpecification(t *testing.T) {
	want := []struct {
		id     uint64
		name   string
		scheme string
	}{
		{0, "fix", "forall T0. ((T0 -> T0) -> T0)"},
		{1, "succ", "(N -> N)"},
		{2, "pred", "(N -> N)"},
		{3, "ifz", "forall T0. (N -> (T0 -> (T0 -> T0)))"},
		{4, "pair", "forall T0 T1. (T0 -> (T1 -> (T0 * T1)))"},
		{5, "fst", "forall T0 T1. ((T0 * T1) -> T0)"},
		{6, "snd", "forall T0 T1. ((T0 * T1) -> T1)"},
		{7, "inl", "forall T0 T1. (T0 -> (T0 + T1))"},
		{8, "inr", "forall T0 T1. (T0 -> (T1 + T0))"},
		{9, "case", "forall T0 T1 T2. ((T0 + T1) -> ((T0 -> T2) -> ((T1 -> T2) -> T2)))"},
		{10, "unit", "1"},
	}

	got := CorePrimitives()
	if len(got) != len(want) {
		t.Fatalf("CorePrimitives() length = %d, want %d", len(got), len(want))
	}
	for i, expected := range want {
		p := got[i]
		if p.ID != expected.id || p.Name != expected.name {
			t.Fatalf("primitive[%d] = {%d %q}, want {%d %q}", i, p.ID, p.Name, expected.id, expected.name)
		}
		canonical, err := CanonicalSchemeString(p.Scheme)
		if err != nil {
			t.Fatalf("primitive[%d] scheme: %v", i, err)
		}
		if canonical != expected.scheme {
			t.Fatalf("primitive[%d] scheme = %q, want %q", i, canonical, expected.scheme)
		}
	}
}

func TestLookupCorePrimitiveReturnsIndependentScheme(t *testing.T) {
	first, err := LookupCorePrimitive(NaturalUint64(4))
	if err != nil {
		t.Fatal(err)
	}
	first.Scheme.Quantified[0] = 99
	first.Scheme.Body.A = TNat()

	second, err := LookupCorePrimitive(NaturalUint64(4))
	if err != nil {
		t.Fatal(err)
	}
	canonical, err := CanonicalSchemeString(second.Scheme)
	if err != nil {
		t.Fatal(err)
	}
	want := "forall T0 T1. (T0 -> (T1 -> (T0 * T1)))"
	if canonical != want {
		t.Fatalf("second pair scheme = %q, want %q", canonical, want)
	}
}

func TestUnknownCorePrimitiveIDs(t *testing.T) {
	for _, id := range []uint64{11, 31, 32, 1 << 20} {
		_, err := LookupCorePrimitive(NaturalUint64(id))
		if !errors.Is(err, ErrUnknownPrimitive) {
			t.Fatalf("LookupCorePrimitive(%d) error = %v, want ErrUnknownPrimitive", id, err)
		}
	}
}

func TestValidateCorePrimitives(t *testing.T) {
	valid := Let(
		Prim(NaturalUint64(1)),
		App(Prim(NaturalUint64(4)), Prim(NaturalUint64(10))),
	)
	if err := ValidateCorePrimitives(valid); err != nil {
		t.Fatalf("ValidateCorePrimitives(valid) = %v", err)
	}

	invalid := Lam(App(Prim(NaturalUint64(1)), Prim(NaturalUint64(11))))
	if err := ValidateCorePrimitives(invalid); !errors.Is(err, ErrUnknownPrimitive) {
		t.Fatalf("ValidateCorePrimitives(invalid) = %v, want ErrUnknownPrimitive", err)
	}
}
