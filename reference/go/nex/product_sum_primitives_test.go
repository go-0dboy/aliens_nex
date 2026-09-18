package nex

import "testing"

func pairTerm(left, right *Term) *Term {
	return App(App(Prim(NaturalUint64(4)), left), right)
}

func inlTerm(payload *Term) *Term {
	return App(Prim(NaturalUint64(7)), payload)
}

func inrTerm(payload *Term) *Term {
	return App(Prim(NaturalUint64(8)), payload)
}

func caseTerm(sum, leftFn, rightFn *Term) *Term {
	return App(App(App(Prim(NaturalUint64(9)), sum), leftFn), rightFn)
}

func TestPairCreationDoesNotForceFields(t *testing.T) {
	term := pairTerm(divergingFixTerm(), divergingFixTerm())
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	if value == nil || value.Kind != ValuePair || value.Left == nil || value.Right == nil {
		t.Fatalf("value = %#v, want lazy pair", value)
	}
}

func TestFstDoesNotForceRightField(t *testing.T) {
	term := App(
		Prim(NaturalUint64(5)),
		pairTerm(Nat(NaturalUint64(1)), divergingFixTerm()),
	)
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 1)
}

func TestSndDoesNotForceLeftField(t *testing.T) {
	term := App(
		Prim(NaturalUint64(6)),
		pairTerm(divergingFixTerm(), Nat(NaturalUint64(2))),
	)
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 2)
}

func TestSumConstructorsDoNotForcePayload(t *testing.T) {
	for _, tc := range []struct {
		name string
		term *Term
		kind ValueKind
	}{
		{"inl", inlTerm(divergingFixTerm()), ValueInl},
		{"inr", inrTerm(divergingFixTerm()), ValueInr},
	} {
		t.Run(tc.name, func(t *testing.T) {
			value, err := EvaluateClosed(tc.term, DefaultEvalLimits)
			if err != nil {
				t.Fatal(err)
			}
			if value == nil || value.Kind != tc.kind || value.Payload == nil {
				t.Fatalf("value = %#v, want lazy sum payload", value)
			}
		})
	}
}

func TestCaseInlDoesNotEvaluateRightFunction(t *testing.T) {
	identity := Lam(Var(NaturalUint64(0)))
	term := caseTerm(
		inlTerm(Nat(NaturalUint64(5))),
		identity,
		divergingFixTerm(),
	)
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 5)
}

func TestCaseInrDoesNotEvaluateLeftFunction(t *testing.T) {
	identity := Lam(Var(NaturalUint64(0)))
	term := caseTerm(
		inrTerm(Nat(NaturalUint64(6))),
		divergingFixTerm(),
		identity,
	)
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 6)
}

func TestCasePassesSelectedPayloadLazily(t *testing.T) {
	ignorePayload := Lam(Nat(NaturalUint64(7)))
	term := caseTerm(
		inlTerm(divergingFixTerm()),
		ignorePayload,
		divergingFixTerm(),
	)
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	requireNatValue(t, value, 7)
}
