package experiment

import (
	"fmt"
	"math/big"

	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

type NeedStats struct {
	Transitions      uint64 `json:"transitions"`
	MaxDepth         uint32 `json:"max_depth"`
	ThunkForces      uint64 `json:"thunk_forces"`
	ThunkEvaluations uint64 `json:"thunk_evaluations"`
	MemoHits         uint64 `json:"memo_hits"`
}

type NeedObservation struct {
	Kind  string `json:"kind"`
	Value string `json:"value,omitempty"`
}

type needValueKind uint8

const (
	needNat needValueKind = iota
	needClosure
	needUnit
	needPair
	needInl
	needInr
	needPrimitive
)

type needEnv []*needThunk

type needThunk struct {
	term  *nex.Term
	env   needEnv
	ready bool
	value *needValue
}

type needClosureValue struct {
	body *nex.Term
	env  needEnv
}

type needPrimitiveApplication struct {
	id   uint64
	args []*needThunk
}

type needValue struct {
	kind needValueKind
	nat  *big.Int

	closure   *needClosureValue
	left      *needThunk
	right     *needThunk
	payload   *needThunk
	primitive *needPrimitiveApplication
}

type needEvaluator struct {
	limits nex.EvalLimits
	stats  NeedStats
}

// EvaluateCallByNeed is an experimental memoizing evaluator used only for Stage 4
// implementation-cost comparison. It must preserve the observable NEX-1 v0.1 result.
func EvaluateCallByNeed(term *nex.Term, limits nex.EvalLimits) (NeedObservation, NeedStats, error) {
	if _, err := nex.InferClosed(term); err != nil {
		return NeedObservation{}, NeedStats{}, err
	}
	if limits.MaxTransitions == 0 {
		limits.MaxTransitions = nex.DefaultEvalLimits.MaxTransitions
	}
	if limits.MaxDepth == 0 {
		limits.MaxDepth = nex.DefaultEvalLimits.MaxDepth
	}

	e := &needEvaluator{limits: limits}
	value, err := e.eval(term, nil, 0)
	if err != nil {
		return NeedObservation{}, e.stats, err
	}
	observation, err := observeNeed(value)
	return observation, e.stats, err
}

func (e *needEvaluator) step(depth uint32) error {
	if depth > e.stats.MaxDepth {
		e.stats.MaxDepth = depth
	}
	if depth > e.limits.MaxDepth {
		return fmt.Errorf("%w: depth %d > %d", nex.ErrEvalResourceLimit, depth, e.limits.MaxDepth)
	}
	if e.stats.Transitions >= e.limits.MaxTransitions {
		return fmt.Errorf("%w: transitions >= %d", nex.ErrEvalResourceLimit, e.limits.MaxTransitions)
	}
	e.stats.Transitions++
	return nil
}

func (e *needEvaluator) eval(term *nex.Term, env needEnv, depth uint32) (*needValue, error) {
	if err := e.step(depth); err != nil {
		return nil, err
	}
	if term == nil {
		return nil, nex.ErrEvalInvariant
	}

	switch term.Kind {
	case nex.KindVar:
		if term.Value == nil || !term.Value.IsUint64() {
			return nil, nex.ErrEvalInvariant
		}
		index := term.Value.Uint64()
		if index >= uint64(len(env)) {
			return nil, nex.ErrEvalInvariant
		}
		return e.force(env[index], depth+1)

	case nex.KindLam:
		if term.A == nil {
			return nil, nex.ErrEvalInvariant
		}
		return &needValue{kind: needClosure, closure: &needClosureValue{body: term.A, env: cloneNeedEnv(env)}}, nil

	case nex.KindApp:
		if term.A == nil || term.B == nil {
			return nil, nex.ErrEvalInvariant
		}
		fn, err := e.eval(term.A, env, depth+1)
		if err != nil {
			return nil, err
		}
		arg := &needThunk{term: term.B, env: cloneNeedEnv(env)}
		return e.applyValue(fn, arg, depth+1)

	case nex.KindLet:
		if term.A == nil || term.B == nil {
			return nil, nex.ErrEvalInvariant
		}
		binding := &needThunk{term: term.A, env: cloneNeedEnv(env)}
		return e.eval(term.B, extendNeedEnv(env, binding), depth+1)

	case nex.KindNat:
		if term.Value == nil || term.Value.Sign() < 0 {
			return nil, nex.ErrEvalInvariant
		}
		return &needValue{kind: needNat, nat: new(big.Int).Set(term.Value)}, nil

	case nex.KindPrim:
		primitive, err := nex.LookupCorePrimitive(term.Value)
		if err != nil {
			return nil, err
		}
		if primitive.Arity == 0 {
			return e.executePrimitive(primitive.ID, nil, depth+1)
		}
		return &needValue{kind: needPrimitive, primitive: &needPrimitiveApplication{id: primitive.ID}}, nil

	default:
		return nil, nex.ErrEvalInvariant
	}
}

func (e *needEvaluator) force(thunk *needThunk, depth uint32) (*needValue, error) {
	if thunk == nil || thunk.term == nil {
		return nil, nex.ErrEvalInvariant
	}
	e.stats.ThunkForces++
	if thunk.ready {
		e.stats.MemoHits++
		return thunk.value, nil
	}
	e.stats.ThunkEvaluations++
	value, err := e.eval(thunk.term, thunk.env, depth)
	if err != nil {
		return nil, err
	}
	thunk.value = value
	thunk.ready = true
	return value, nil
}

func (e *needEvaluator) applyValue(fn *needValue, arg *needThunk, depth uint32) (*needValue, error) {
	if fn == nil || arg == nil {
		return nil, nex.ErrEvalInvariant
	}
	switch fn.kind {
	case needClosure:
		if fn.closure == nil || fn.closure.body == nil {
			return nil, nex.ErrEvalInvariant
		}
		return e.eval(fn.closure.body, extendNeedEnv(fn.closure.env, arg), depth+1)
	case needPrimitive:
		return e.applyPrimitive(fn.primitive, arg, depth+1)
	default:
		return nil, nex.ErrEvalInvariant
	}
}

func (e *needEvaluator) applyPrimitive(application *needPrimitiveApplication, arg *needThunk, depth uint32) (*needValue, error) {
	if application == nil || arg == nil {
		return nil, nex.ErrEvalInvariant
	}
	primitive, err := nex.LookupCorePrimitive(new(big.Int).SetUint64(application.id))
	if err != nil {
		return nil, err
	}
	if len(application.args) >= int(primitive.Arity) {
		return nil, nex.ErrEvalInvariant
	}
	args := append(append([]*needThunk(nil), application.args...), arg)
	if len(args) < int(primitive.Arity) {
		return &needValue{kind: needPrimitive, primitive: &needPrimitiveApplication{id: application.id, args: args}}, nil
	}
	return e.executePrimitive(application.id, args, depth)
}

func (e *needEvaluator) executePrimitive(id uint64, args []*needThunk, depth uint32) (*needValue, error) {
	switch id {
	case 0: // fix
		fn, err := e.force(args[0], depth+1)
		if err != nil {
			return nil, err
		}
		recursive := &needThunk{
			term: nex.App(nex.Prim(nex.NaturalUint64(0)), args[0].term),
			env:  cloneNeedEnv(args[0].env),
		}
		return e.applyValue(fn, recursive, depth+1)

	case 1: // succ
		n, err := e.forceNat(args[0], depth+1)
		if err != nil {
			return nil, err
		}
		return &needValue{kind: needNat, nat: new(big.Int).Add(n, big.NewInt(1))}, nil

	case 2: // pred
		n, err := e.forceNat(args[0], depth+1)
		if err != nil {
			return nil, err
		}
		if n.Sign() == 0 {
			return &needValue{kind: needNat, nat: n}, nil
		}
		return &needValue{kind: needNat, nat: new(big.Int).Sub(n, big.NewInt(1))}, nil

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
		return &needValue{kind: needPair, left: args[0], right: args[1]}, nil

	case 5: // fst
		pair, err := e.force(args[0], depth+1)
		if err != nil {
			return nil, err
		}
		if pair == nil || pair.kind != needPair || pair.left == nil || pair.right == nil {
			return nil, nex.ErrEvalInvariant
		}
		return e.force(pair.left, depth+1)

	case 6: // snd
		pair, err := e.force(args[0], depth+1)
		if err != nil {
			return nil, err
		}
		if pair == nil || pair.kind != needPair || pair.left == nil || pair.right == nil {
			return nil, nex.ErrEvalInvariant
		}
		return e.force(pair.right, depth+1)

	case 7: // inl
		return &needValue{kind: needInl, payload: args[0]}, nil

	case 8: // inr
		return &needValue{kind: needInr, payload: args[0]}, nil

	case 9: // case
		sum, err := e.force(args[0], depth+1)
		if err != nil {
			return nil, err
		}
		if sum == nil || sum.payload == nil {
			return nil, nex.ErrEvalInvariant
		}
		var selected *needThunk
		switch sum.kind {
		case needInl:
			selected = args[1]
		case needInr:
			selected = args[2]
		default:
			return nil, nex.ErrEvalInvariant
		}
		fn, err := e.force(selected, depth+1)
		if err != nil {
			return nil, err
		}
		return e.applyValue(fn, sum.payload, depth+1)

	case 10: // unit
		return &needValue{kind: needUnit}, nil

	default:
		return nil, nex.ErrEvalInvariant
	}
}

func (e *needEvaluator) forceNat(thunk *needThunk, depth uint32) (*big.Int, error) {
	value, err := e.force(thunk, depth)
	if err != nil {
		return nil, err
	}
	if value == nil || value.kind != needNat || value.nat == nil {
		return nil, nex.ErrEvalInvariant
	}
	return new(big.Int).Set(value.nat), nil
}

func observeNeed(value *needValue) (NeedObservation, error) {
	if value == nil {
		return NeedObservation{}, nex.ErrEvalInvariant
	}
	switch value.kind {
	case needNat:
		if value.nat == nil {
			return NeedObservation{}, nex.ErrEvalInvariant
		}
		return NeedObservation{Kind: "Nat", Value: value.nat.String()}, nil
	case needClosure, needPrimitive:
		return NeedObservation{Kind: "Function"}, nil
	case needUnit:
		return NeedObservation{Kind: "Unit"}, nil
	case needPair:
		return NeedObservation{Kind: "Pair"}, nil
	case needInl:
		return NeedObservation{Kind: "Inl"}, nil
	case needInr:
		return NeedObservation{Kind: "Inr"}, nil
	default:
		return NeedObservation{}, nex.ErrEvalInvariant
	}
}

func cloneNeedEnv(env needEnv) needEnv {
	if len(env) == 0 {
		return nil
	}
	out := make(needEnv, len(env))
	copy(out, env)
	return out
}

func extendNeedEnv(env needEnv, binding *needThunk) needEnv {
	out := make(needEnv, len(env)+1)
	out[0] = binding
	copy(out[1:], env)
	return out
}
