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
