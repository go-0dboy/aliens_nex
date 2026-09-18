package nex

import (
	"errors"
	"fmt"
	"math/big"
)

var (
	ErrEvalResourceLimit = errors.New("evaluation resource limit exceeded")
	ErrEvalInvariant     = errors.New("invalid evaluator state")
)

type EvalLimits struct {
	MaxTransitions uint64
	MaxDepth       uint32
}

var DefaultEvalLimits = EvalLimits{
	MaxTransitions: 1_000_000,
	MaxDepth:       10_000,
}

type evaluator struct {
	limits      EvalLimits
	transitions uint64
}

// EvaluateClosed evaluates a statically valid closed Core term to weak-head form.
func EvaluateClosed(term *Term, limits EvalLimits) (*Value, error) {
	if _, err := InferClosed(term); err != nil {
		return nil, err
	}
	if limits.MaxTransitions == 0 {
		limits.MaxTransitions = DefaultEvalLimits.MaxTransitions
	}
	if limits.MaxDepth == 0 {
		limits.MaxDepth = DefaultEvalLimits.MaxDepth
	}
	e := &evaluator{limits: limits}
	return e.eval(term, nil, 0)
}

func (e *evaluator) step(depth uint32) error {
	if depth > e.limits.MaxDepth {
		return fmt.Errorf("%w: depth %d > %d", ErrEvalResourceLimit, depth, e.limits.MaxDepth)
	}
	if e.transitions >= e.limits.MaxTransitions {
		return fmt.Errorf("%w: transitions >= %d", ErrEvalResourceLimit, e.limits.MaxTransitions)
	}
	e.transitions++
	return nil
}

func (e *evaluator) eval(term *Term, env Environment, depth uint32) (*Value, error) {
	if err := e.step(depth); err != nil {
		return nil, err
	}
	if term == nil {
		return nil, ErrEvalInvariant
	}

	switch term.Kind {
	case KindVar:
		if term.Value == nil || !term.Value.IsUint64() {
			return nil, ErrEvalInvariant
		}
		index := term.Value.Uint64()
		if index >= uint64(len(env)) {
			return nil, ErrEvalInvariant
		}
		return e.force(env[index], depth+1)

	case KindLam:
		if term.A == nil {
			return nil, ErrEvalInvariant
		}
		return closureValue(term.A, env), nil

	case KindApp:
		if term.A == nil || term.B == nil {
			return nil, ErrEvalInvariant
		}
		fn, err := e.eval(term.A, env, depth+1)
		if err != nil {
			return nil, err
		}
		arg := &Thunk{Term: term.B, Env: cloneEnvironment(env)}
		return e.applyValue(fn, arg, depth+1)

	case KindLet:
		if term.A == nil || term.B == nil {
			return nil, ErrEvalInvariant
		}
		binding := &Thunk{Term: term.A, Env: cloneEnvironment(env)}
		bodyEnv := extendEnvironment(env, binding)
		return e.eval(term.B, bodyEnv, depth+1)

	case KindNat:
		if term.Value == nil || term.Value.Sign() < 0 {
			return nil, ErrEvalInvariant
		}
		return natValue(term.Value), nil

	case KindPrim:
		primitive, err := LookupCorePrimitive(term.Value)
		if err != nil {
			return nil, err
		}
		if primitive.Arity == 0 {
			return e.executePrimitive(primitive.ID, nil, depth+1)
		}
		return primitiveValue(primitive.ID, nil), nil

	default:
		return nil, ErrEvalInvariant
	}
}

func (e *evaluator) force(thunk *Thunk, depth uint32) (*Value, error) {
	if thunk == nil || thunk.Term == nil {
		return nil, ErrEvalInvariant
	}
	return e.eval(thunk.Term, thunk.Env, depth)
}

func (e *evaluator) applyValue(fn *Value, arg *Thunk, depth uint32) (*Value, error) {
	if fn == nil || arg == nil {
		return nil, ErrEvalInvariant
	}
	switch fn.Kind {
	case ValueClosure:
		if fn.Closure == nil || fn.Closure.Body == nil {
			return nil, ErrEvalInvariant
		}
		bodyEnv := extendEnvironment(fn.Closure.Env, arg)
		return e.eval(fn.Closure.Body, bodyEnv, depth+1)
	case ValuePrimitive:
		return e.applyPrimitive(fn.Primitive, arg, depth+1)
	default:
		return nil, ErrEvalInvariant
	}
}

func (e *evaluator) applyPrimitive(application *PrimitiveApplication, arg *Thunk, depth uint32) (*Value, error) {
	if application == nil || arg == nil {
		return nil, ErrEvalInvariant
	}
	primitive, err := LookupCorePrimitive(NaturalUint64(application.ID))
	if err != nil {
		return nil, err
	}
	if len(application.Args) >= int(primitive.Arity) {
		return nil, ErrEvalInvariant
	}
	args := append(append([]*Thunk(nil), application.Args...), arg)
	if len(args) < int(primitive.Arity) {
		return primitiveValue(application.ID, args), nil
	}
	return e.executePrimitive(application.ID, args, depth)
}

func (e *evaluator) executePrimitive(id uint64, args []*Thunk, depth uint32) (*Value, error) {
	switch id {
	case 0: // fix
		fn, err := e.force(args[0], depth+1)
		if err != nil {
			return nil, err
		}
		recursive := &Thunk{
			Term: App(Prim(NaturalUint64(0)), args[0].Term),
			Env:  cloneEnvironment(args[0].Env),
		}
		return e.applyValue(fn, recursive, depth+1)

	case 1: // succ
		n, err := e.forceNat(args[0], depth+1)
		if err != nil {
			return nil, err
		}
		return natValue(new(big.Int).Add(n, NaturalUint64(1))), nil

	case 2: // pred
		n, err := e.forceNat(args[0], depth+1)
		if err != nil {
			return nil, err
		}
		if n.Sign() == 0 {
			return natValue(n), nil
		}
		return natValue(new(big.Int).Sub(n, NaturalUint64(1))), nil

	case 3: // ifz
		n, err := e.forceNat(args[0], depth+1)
		if err != nil {
			return nil, err
		}
		if n.Sign() == 0 {
			return e.force(args[1], depth+1)
		}
		return e.force(args[2], depth+1)

	case 4: // pair
		return pairValue(args[0], args[1]), nil

	case 5: // fst
		pair, err := e.force(args[0], depth+1)
		if err != nil {
			return nil, err
		}
		if pair == nil || pair.Kind != ValuePair || pair.Left == nil || pair.Right == nil {
			return nil, ErrEvalInvariant
		}
		return e.force(pair.Left, depth+1)

	case 6: // snd
		pair, err := e.force(args[0], depth+1)
		if err != nil {
			return nil, err
		}
		if pair == nil || pair.Kind != ValuePair || pair.Left == nil || pair.Right == nil {
			return nil, ErrEvalInvariant
		}
		return e.force(pair.Right, depth+1)

	case 7: // inl
		return inlValue(args[0]), nil

	case 8: // inr
		return inrValue(args[0]), nil

	case 9: // case
		sum, err := e.force(args[0], depth+1)
		if err != nil {
			return nil, err
		}
		if sum == nil || sum.Payload == nil {
			return nil, ErrEvalInvariant
		}

		var selected *Thunk
		switch sum.Kind {
		case ValueInl:
			selected = args[1]
		case ValueInr:
			selected = args[2]
		default:
			return nil, ErrEvalInvariant
		}

		fn, err := e.force(selected, depth+1)
		if err != nil {
			return nil, err
		}
		return e.applyValue(fn, sum.Payload, depth+1)

	case 10: // unit
		return unitValue(), nil

	default:
		return nil, ErrEvalInvariant
	}
}

func (e *evaluator) forceNat(thunk *Thunk, depth uint32) (*big.Int, error) {
	value, err := e.force(thunk, depth)
	if err != nil {
		return nil, err
	}
	if value == nil || value.Kind != ValueNat || value.Nat == nil {
		return nil, ErrEvalInvariant
	}
	return cloneNat(value.Nat), nil
}
