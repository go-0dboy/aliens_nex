package nex

import "testing"

func TestCorePrimitiveArities(t *testing.T) {
	want := []uint8{1, 1, 1, 3, 2, 1, 1, 1, 1, 3, 0}
	primitives := CorePrimitives()
	if len(primitives) != len(want) {
		t.Fatalf("CorePrimitives() length = %d, want %d", len(primitives), len(want))
	}
	for i, arity := range want {
		if primitives[i].Arity != arity {
			t.Fatalf("primitive %d arity = %d, want %d", i, primitives[i].Arity, arity)
		}
	}
}

func TestUnsaturatedPrimitiveIsFunctionWHNF(t *testing.T) {
	value, err := EvaluateClosed(Prim(NaturalUint64(1)), DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	if value == nil || value.Kind != ValuePrimitive || value.Primitive == nil {
		t.Fatalf("value = %#v, want primitive function", value)
	}
	if value.Primitive.ID != 1 || len(value.Primitive.Args) != 0 {
		t.Fatalf("primitive = %#v, want succ with no supplied args", value.Primitive)
	}
}

func TestPartialPrimitiveApplicationKeepsArgumentDelayed(t *testing.T) {
	// pair (fix id) is only a partial application. fix execution remains deferred until
	// Stage 3.6, so success proves the stored pair argument was not forced.
	term := App(Prim(NaturalUint64(4)), deferredFixIdentityTerm())
	value, err := EvaluateClosed(term, DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	if value == nil || value.Kind != ValuePrimitive || value.Primitive == nil {
		t.Fatalf("value = %#v, want partially applied pair", value)
	}
	if value.Primitive.ID != 4 || len(value.Primitive.Args) != 1 {
		t.Fatalf("primitive = %#v, want pair with one supplied arg", value.Primitive)
	}
}

func TestZeroArityUnitIsImmediateWHNF(t *testing.T) {
	value, err := EvaluateClosed(Prim(NaturalUint64(10)), DefaultEvalLimits)
	if err != nil {
		t.Fatal(err)
	}
	if value == nil || value.Kind != ValueUnit {
		t.Fatalf("value = %#v, want unit", value)
	}
}
