package nex

import (
	"errors"
	"testing"
)

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
	// pair unit is only a partial application. unit execution is still deferred at this
	// checkpoint, so success proves the first pair argument was stored without forcing it.
	term := App(Prim(NaturalUint64(4)), Prim(NaturalUint64(10)))
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

func TestSaturatedPrimitiveExecutionStillDeferred(t *testing.T) {
	term := App(Prim(NaturalUint64(1)), Nat(NaturalUint64(0)))
	_, err := EvaluateClosed(term, DefaultEvalLimits)
	if !errors.Is(err, ErrPrimitiveExecutionDeferred) {
		t.Fatalf("EvaluateClosed(succ 0) error = %v, want ErrPrimitiveExecutionDeferred", err)
	}
}

func TestZeroArityUnitExecutionStillDeferred(t *testing.T) {
	_, err := EvaluateClosed(Prim(NaturalUint64(10)), DefaultEvalLimits)
	if !errors.Is(err, ErrPrimitiveExecutionDeferred) {
		t.Fatalf("EvaluateClosed(unit) error = %v, want ErrPrimitiveExecutionDeferred", err)
	}
}
