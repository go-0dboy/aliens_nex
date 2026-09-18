package nex

import "math/big"

type ValueKind uint8

const (
	ValueNat ValueKind = iota
	ValueClosure
	ValueUnit
	ValuePair
	ValueInl
	ValueInr
	ValuePrimitive
)

// Environment is ordered nearest de Bruijn binder first.
type Environment []*Thunk

// Thunk is a non-memoizing suspended computation for the reference call-by-name evaluator.
// Call-by-need sharing is deliberately not part of this first runtime model.
type Thunk struct {
	Term *Term
	Env  Environment
}

type Closure struct {
	Body *Term
	Env  Environment
}

type PrimitiveApplication struct {
	ID   uint64
	Args []*Thunk
}

type Value struct {
	Kind ValueKind
	Nat  *big.Int

	Closure   *Closure
	Left      *Thunk
	Right     *Thunk
	Payload   *Thunk
	Primitive *PrimitiveApplication
}

func natValue(n *big.Int) *Value {
	return &Value{Kind: ValueNat, Nat: cloneNat(n)}
}

func closureValue(body *Term, env Environment) *Value {
	return &Value{Kind: ValueClosure, Closure: &Closure{Body: body, Env: cloneEnvironment(env)}}
}

func primitiveValue(id uint64, args []*Thunk) *Value {
	copied := append([]*Thunk(nil), args...)
	return &Value{Kind: ValuePrimitive, Primitive: &PrimitiveApplication{ID: id, Args: copied}}
}

func cloneEnvironment(env Environment) Environment {
	if len(env) == 0 {
		return nil
	}
	out := make(Environment, len(env))
	copy(out, env)
	return out
}

func extendEnvironment(env Environment, binding *Thunk) Environment {
	out := make(Environment, len(env)+1)
	out[0] = binding
	copy(out[1:], env)
	return out
}
