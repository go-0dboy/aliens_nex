package nex

import (
	"errors"
	"testing"
)

func TestFreeTypeVars(t *testing.T) {
	typ := TFunc(TVar(1), TProduct(TVar(2), TVar(1)))
	vars, err := FreeTypeVars(typ)
	if err != nil {
		t.Fatal(err)
	}
	if len(vars) != 2 || !vars.Has(1) || !vars.Has(2) {
		t.Fatalf("FreeTypeVars() = %#v, want {1,2}", vars)
	}
}

func TestFreeSchemeVarsRemovesQuantifiedVariables(t *testing.T) {
	s := TypeScheme{
		Quantified: []TypeVarID{1},
		Body:       TFunc(TVar(1), TVar(2)),
	}
	vars, err := FreeSchemeVars(s)
	if err != nil {
		t.Fatal(err)
	}
	if len(vars) != 1 || !vars.Has(2) {
		t.Fatalf("FreeSchemeVars() = %#v, want {2}", vars)
	}
}

func TestFreeEnvVars(t *testing.T) {
	env := TypeEnv{
		{Quantified: []TypeVarID{1}, Body: TFunc(TVar(1), TVar(2))},
		MonoScheme(TProduct(TVar(3), TNat())),
	}
	vars, err := FreeEnvVars(env)
	if err != nil {
		t.Fatal(err)
	}
	if len(vars) != 2 || !vars.Has(2) || !vars.Has(3) {
		t.Fatalf("FreeEnvVars() = %#v, want {2,3}", vars)
	}
}

func TestApplyTypeEmptySubstitutionIsIdentity(t *testing.T) {
	typ := TFunc(TVar(1), TSum(TNat(), TProduct(TVar(2), TUnit())))
	got, err := ApplyType(EmptySubstitution(), typ)
	if err != nil {
		t.Fatal(err)
	}
	if !EqualType(got, typ) {
		t.Fatal("empty substitution changed the type")
	}
}

func TestApplyTypeResolvesChains(t *testing.T) {
	sub := Substitution{
		1: TVar(2),
		2: TNat(),
	}
	got, err := ApplyType(sub, TFunc(TVar(1), TVar(3)))
	if err != nil {
		t.Fatal(err)
	}
	want := TFunc(TNat(), TVar(3))
	if !EqualType(got, want) {
		gotText, _ := CanonicalTypeString(got)
		wantText, _ := CanonicalTypeString(want)
		t.Fatalf("ApplyType() = %s, want %s", gotText, wantText)
	}
}

func TestApplySchemeProtectsQuantifiedVariables(t *testing.T) {
	scheme := TypeScheme{
		Quantified: []TypeVarID{1},
		Body:       TFunc(TVar(1), TVar(2)),
	}
	sub := Substitution{
		1: TNat(),
		2: TUnit(),
	}
	got, err := ApplyScheme(sub, scheme)
	if err != nil {
		t.Fatal(err)
	}
	text, err := CanonicalSchemeString(got)
	if err != nil {
		t.Fatal(err)
	}
	want := "forall T0. (T0 -> 1)"
	if text != want {
		t.Fatalf("CanonicalSchemeString(ApplyScheme()) = %q, want %q", text, want)
	}
}

func TestComposeSubstitutions(t *testing.T) {
	older := Substitution{
		0: TVar(2),
		1: TNat(),
	}
	newer := Substitution{
		2: TSum(TUnit(), TVar(4)),
		3: TNat(),
	}
	typ := TFunc(TVar(0), TProduct(TVar(1), TVar(3)))

	composed, err := ComposeSubstitutions(newer, older)
	if err != nil {
		t.Fatal(err)
	}
	left, err := ApplyType(composed, typ)
	if err != nil {
		t.Fatal(err)
	}
	first, err := ApplyType(older, typ)
	if err != nil {
		t.Fatal(err)
	}
	right, err := ApplyType(newer, first)
	if err != nil {
		t.Fatal(err)
	}
	if !EqualType(left, right) {
		leftText, _ := CanonicalTypeString(left)
		rightText, _ := CanonicalTypeString(right)
		t.Fatalf("composition mismatch: %s != %s", leftText, rightText)
	}
}

func TestApplyTypeRejectsSubstitutionCycle(t *testing.T) {
	sub := Substitution{
		1: TVar(2),
		2: TVar(1),
	}
	_, err := ApplyType(sub, TVar(1))
	if !errors.Is(err, ErrInvalidSubstitution) {
		t.Fatalf("ApplyType() error = %v, want ErrInvalidSubstitution", err)
	}
}

func typeFromFuzzBytes(data []byte, pos *int, depth int) *Type {
	if len(data) == 0 {
		return TNat()
	}
	next := func() byte {
		b := data[*pos%len(data)]
		*pos = *pos + 1
		return b
	}
	kind := next() % 6
	if depth >= 5 && kind >= byte(TypeFunc) {
		kind %= 3
	}
	switch TypeKind(kind) {
	case TypeVar:
		return TVar(TypeVarID(next() % 6))
	case TypeUnit:
		return TUnit()
	case TypeNat:
		return TNat()
	case TypeFunc:
		return TFunc(typeFromFuzzBytes(data, pos, depth+1), typeFromFuzzBytes(data, pos, depth+1))
	case TypeProduct:
		return TProduct(typeFromFuzzBytes(data, pos, depth+1), typeFromFuzzBytes(data, pos, depth+1))
	default:
		return TSum(typeFromFuzzBytes(data, pos, depth+1), typeFromFuzzBytes(data, pos, depth+1))
	}
}

func FuzzSubstitutionComposition(f *testing.F) {
	for _, seed := range [][]byte{{0}, {1, 2, 3}, {3, 1, 4, 1, 5, 9}} {
		f.Add(seed)
	}
	f.Fuzz(func(t *testing.T, data []byte) {
		if len(data) == 0 {
			return
		}
		pos := 0
		typ := typeFromFuzzBytes(data, &pos, 0)
		older := Substitution{
			0: TVar(2),
			1: TNat(),
		}
		newer := Substitution{
			2: TSum(TUnit(), TVar(4)),
			3: TNat(),
		}

		composed, err := ComposeSubstitutions(newer, older)
		if err != nil {
			t.Fatal(err)
		}
		left, err := ApplyType(composed, typ)
		if err != nil {
			t.Fatal(err)
		}
		first, err := ApplyType(older, typ)
		if err != nil {
			t.Fatal(err)
		}
		right, err := ApplyType(newer, first)
		if err != nil {
			t.Fatal(err)
		}
		if !EqualType(left, right) {
			t.Fatal("substitution composition property failed")
		}
	})
}
