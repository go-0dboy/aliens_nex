package experiment

import (
	"testing"

	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

func TestCallByNeedMemoizesRepeatedLetForce(t *testing.T) {
	term := nex.Let(
		nex.Nat(nex.NaturalUint64(0)),
		nex.App(
			nex.App(
				nex.App(nex.Prim(nex.NaturalUint64(3)), nex.Var(nex.NaturalUint64(0))),
				nex.Var(nex.NaturalUint64(0)),
			),
			nex.Nat(nex.NaturalUint64(1)),
		),
	)

	observation, stats, err := EvaluateCallByNeed(term, nex.DefaultEvalLimits)
	if err != nil {
		t.Fatalf("EvaluateCallByNeed: %v", err)
	}
	if observation.Kind != "Nat" || observation.Value != "0" {
		t.Fatalf("observation = %#v, want Nat(0)", observation)
	}
	if stats.MemoHits == 0 {
		t.Fatalf("expected at least one memo hit, stats = %#v", stats)
	}
	if stats.ThunkEvaluations >= stats.ThunkForces {
		t.Fatalf("expected sharing to avoid at least one thunk evaluation, stats = %#v", stats)
	}
}

func TestCallByNeedAgreesWithReferenceOnBasicTerm(t *testing.T) {
	term := nex.App(nex.Lam(nex.Var(nex.NaturalUint64(0))), nex.Nat(nex.NaturalUint64(42)))

	referenceValue, _, err := nex.EvaluateClosedWithStats(term, nex.DefaultEvalLimits)
	if err != nil {
		t.Fatalf("EvaluateClosedWithStats: %v", err)
	}
	if referenceValue.Kind != nex.ValueNat || referenceValue.Nat.String() != "42" {
		t.Fatalf("reference result = %#v", referenceValue)
	}

	observation, _, err := EvaluateCallByNeed(term, nex.DefaultEvalLimits)
	if err != nil {
		t.Fatalf("EvaluateCallByNeed: %v", err)
	}
	if observation.Kind != "Nat" || observation.Value != "42" {
		t.Fatalf("call-by-need observation = %#v", observation)
	}
}
