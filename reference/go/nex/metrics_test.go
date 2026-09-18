package nex

import "testing"

func TestMeasureIdentity(t *testing.T) {
	metrics, err := MeasureTerm(Lam(Var(NaturalUint64(0))))
	if err != nil {
		t.Fatal(err)
	}
	if metrics.WireBits != 5 {
		t.Fatalf("wire bits = %d, want 5", metrics.WireBits)
	}
	if metrics.ASTNodes != 2 {
		t.Fatalf("AST nodes = %d, want 2", metrics.ASTNodes)
	}
	want := (ConstructorCounts{Var: 1, Lam: 1})
	if metrics.Constructors != want {
		t.Fatalf("constructors = %#v, want %#v", metrics.Constructors, want)
	}
	if metrics.WireByConstructor.Lam != 2 || metrics.WireByConstructor.Var != 3 {
		t.Fatalf("wire breakdown = %#v", metrics.WireByConstructor)
	}
}

func TestMeasureTermAttributesAllWireBits(t *testing.T) {
	term := App(Lam(Var(NaturalUint64(0))), Nat(NaturalUint64(7)))
	metrics, err := MeasureTerm(term)
	if err != nil {
		t.Fatal(err)
	}
	attributed := metrics.WireByConstructor.Var +
		metrics.WireByConstructor.Lam +
		metrics.WireByConstructor.App +
		metrics.WireByConstructor.Let +
		metrics.WireByConstructor.Nat +
		metrics.WireByConstructor.Prim
	if attributed != metrics.WireBits {
		t.Fatalf("attributed wire bits = %d, total = %d", attributed, metrics.WireBits)
	}
	if metrics.WireByConstructor.App != 2 {
		t.Fatalf("App wire bits = %d, want 2", metrics.WireByConstructor.App)
	}
}

func TestEvaluateClosedWithStatsMatchesEvaluateClosed(t *testing.T) {
	term := App(Lam(Var(NaturalUint64(0))), Nat(NaturalUint64(42)))
	plain, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	measured, stats, err := EvaluateClosedWithStats(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	if plain.Kind != measured.Kind || plain.Nat.Cmp(measured.Nat) != 0 {
		t.Fatalf("measured result differs from ordinary evaluation")
	}
	if stats.Transitions == 0 {
		t.Fatal("expected at least one evaluator transition")
	}
	if stats.MaxDepth == 0 {
		t.Fatal("expected nested evaluation depth")
	}
}
