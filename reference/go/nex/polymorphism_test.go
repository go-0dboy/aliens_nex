package nex

import "testing"

func TestInstantiateUsesFreshVariablesPerUse(t *testing.T) {
	scheme := TypeScheme{Quantified: []TypeVarID{0}, Body: TFunc(TVar(0), TVar(0))}
	fresh := NewFreshTypeVars(10)

	first, err := Instantiate(scheme, fresh)
	if err != nil {
		t.Fatal(err)
	}
	second, err := Instantiate(scheme, fresh)
	if err != nil {
		t.Fatal(err)
	}

	if !EqualType(first, TFunc(TVar(10), TVar(10))) {
		t.Fatalf("first instantiation = %#v", first)
	}
	if !EqualType(second, TFunc(TVar(11), TVar(11))) {
		t.Fatalf("second instantiation = %#v", second)
	}
}

func TestInstantiateMayReuseTemplateNumberAsFreshID(t *testing.T) {
	scheme := TypeScheme{Quantified: []TypeVarID{0}, Body: TFunc(TVar(0), TVar(0))}
	got, err := Instantiate(scheme, NewFreshTypeVars(0))
	if err != nil {
		t.Fatal(err)
	}
	want := TFunc(TVar(0), TVar(0))
	if !EqualType(got, want) {
		t.Fatalf("Instantiate() = %#v, want %#v", got, want)
	}
}

func TestInstantiateMonomorphicSchemeClonesType(t *testing.T) {
	scheme := MonoScheme(TFunc(TNat(), TNat()))
	got, err := Instantiate(scheme, NewFreshTypeVars(0))
	if err != nil {
		t.Fatal(err)
	}
	if !EqualType(got, scheme.Body) {
		t.Fatal("monomorphic instantiation changed the type")
	}
	if got == scheme.Body {
		t.Fatal("Instantiate returned the original type pointer")
	}
}

func TestGeneralizeQuantifiesVariablesNotFreeInEnvironment(t *testing.T) {
	env := TypeEnv{MonoScheme(TVar(0))}
	typ := TFunc(TVar(0), TVar(1))

	scheme, err := Generalize(env, typ)
	if err != nil {
		t.Fatal(err)
	}
	if len(scheme.Quantified) != 1 || scheme.Quantified[0] != 1 {
		t.Fatalf("quantified = %#v, want [1]", scheme.Quantified)
	}
	text, err := CanonicalSchemeString(scheme)
	if err != nil {
		t.Fatal(err)
	}
	if text != "forall T1. (T0 -> T1)" {
		t.Fatalf("canonical scheme = %q", text)
	}
}

func TestGeneralizeEmptyEnvironmentProducesPrincipalIdentityScheme(t *testing.T) {
	scheme, err := Generalize(nil, TFunc(TVar(42), TVar(42)))
	if err != nil {
		t.Fatal(err)
	}
	text, err := CanonicalSchemeString(scheme)
	if err != nil {
		t.Fatal(err)
	}
	if text != "forall T0. (T0 -> T0)" {
		t.Fatalf("canonical scheme = %q", text)
	}
}

func TestGeneralizeClosedTypeIsMonomorphic(t *testing.T) {
	scheme, err := Generalize(nil, TProduct(TNat(), TUnit()))
	if err != nil {
		t.Fatal(err)
	}
	if len(scheme.Quantified) != 0 {
		t.Fatalf("quantified = %#v, want none", scheme.Quantified)
	}
}
