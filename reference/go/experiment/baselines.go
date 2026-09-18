package experiment

import (
	"errors"
	"fmt"
	"math"

	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

var ErrBaselineUnsupported = errors.New("term unsupported by baseline")

// BLCBits measures John Tromp's Binary Lambda Calculus encoding for the same
// pure lambda term. NEX zero-based Var(k) corresponds to BLC's one-based index k+1.
func BLCBits(term *nex.Term) (int, error) {
	if term == nil {
		return 0, nex.ErrInvalidTerm
	}
	switch term.Kind {
	case nex.KindVar:
		if term.Value == nil || term.Value.Sign() < 0 || !term.Value.IsUint64() {
			return 0, nex.ErrInvalidTerm
		}
		index := term.Value.Uint64()
		if index > uint64(math.MaxInt-2) {
			return 0, fmt.Errorf("BLC variable index too large for measurement")
		}
		return int(index) + 2, nil
	case nex.KindLam:
		body, err := BLCBits(term.A)
		if err != nil {
			return 0, err
		}
		return 2 + body, nil
	case nex.KindApp:
		left, err := BLCBits(term.A)
		if err != nil {
			return 0, err
		}
		right, err := BLCBits(term.B)
		if err != nil {
			return 0, err
		}
		return 2 + left + right, nil
	default:
		return 0, ErrBaselineUnsupported
	}
}

// TinyStackBits measures the project-defined postfix structural stack baseline.
// Leaf instructions are 3-bit opcodes plus NEX U(n); Lam/App/Let are 3-bit
// postfix operators. Exact transport bit length delimits the whole program.
func TinyStackBits(term *nex.Term) (int, error) {
	if term == nil {
		return 0, nex.ErrInvalidTerm
	}
	switch term.Kind {
	case nex.KindVar, nex.KindNat, nex.KindPrim:
		if term.Value == nil || term.Value.Sign() < 0 {
			return 0, nex.ErrInvalidTerm
		}
		payload, err := nex.EncodeU(term.Value)
		if err != nil {
			return 0, err
		}
		return 3 + len(payload), nil
	case nex.KindLam:
		body, err := TinyStackBits(term.A)
		if err != nil {
			return 0, err
		}
		return body + 3, nil
	case nex.KindApp, nex.KindLet:
		left, err := TinyStackBits(term.A)
		if err != nil {
			return 0, err
		}
		right, err := TinyStackBits(term.B)
		if err != nil {
			return 0, err
		}
		return left + right + 3, nil
	default:
		return 0, nex.ErrInvalidTerm
	}
}

// JotBitsBracketSK measures a deterministic translation of a closed pure lambda
// term: de Bruijn -> named lambda -> standard SK bracket abstraction -> Barker Jot.
// It is a canonical project translation, not a shortest-Jot-program claim.
func JotBitsBracketSK(term *nex.Term) (int, error) {
	nextID := 0
	named, err := toNamedLambda(term, nil, &nextID)
	if err != nil {
		return 0, err
	}
	cl := lambdaToCL(named)
	if containsAnyCLVar(cl) {
		return 0, fmt.Errorf("%w: translated combinator term still has free variables", ErrBaselineUnsupported)
	}
	return jotCLBits(cl), nil
}

type namedKind uint8

const (
	namedVar namedKind = iota
	namedLam
	namedApp
)

type namedTerm struct {
	kind   namedKind
	binder int
	a      *namedTerm
	b      *namedTerm
}

func toNamedLambda(term *nex.Term, env []int, nextID *int) (*namedTerm, error) {
	if term == nil {
		return nil, nex.ErrInvalidTerm
	}
	switch term.Kind {
	case nex.KindVar:
		if term.Value == nil || !term.Value.IsUint64() {
			return nil, nex.ErrInvalidTerm
		}
		index := term.Value.Uint64()
		if index >= uint64(len(env)) {
			return nil, fmt.Errorf("%w: free de Bruijn variable", ErrBaselineUnsupported)
		}
		return &namedTerm{kind: namedVar, binder: env[index]}, nil
	case nex.KindLam:
		id := *nextID
		*nextID = *nextID + 1
		bodyEnv := make([]int, 0, len(env)+1)
		bodyEnv = append(bodyEnv, id)
		bodyEnv = append(bodyEnv, env...)
		body, err := toNamedLambda(term.A, bodyEnv, nextID)
		if err != nil {
			return nil, err
		}
		return &namedTerm{kind: namedLam, binder: id, a: body}, nil
	case nex.KindApp:
		left, err := toNamedLambda(term.A, env, nextID)
		if err != nil {
			return nil, err
		}
		right, err := toNamedLambda(term.B, env, nextID)
		if err != nil {
			return nil, err
		}
		return &namedTerm{kind: namedApp, a: left, b: right}, nil
	default:
		return nil, ErrBaselineUnsupported
	}
}

type clKind uint8

const (
	clVar clKind = iota
	clS
	clK
	clApp
)

type clTerm struct {
	kind clKind
	id   int
	a    *clTerm
	b    *clTerm
}

func lambdaToCL(term *namedTerm) *clTerm {
	switch term.kind {
	case namedVar:
		return &clTerm{kind: clVar, id: term.binder}
	case namedApp:
		return clApply(lambdaToCL(term.a), lambdaToCL(term.b))
	case namedLam:
		return bracketAbstract(term.binder, lambdaToCL(term.a))
	default:
		panic("unknown named lambda kind")
	}
}

func bracketAbstract(id int, term *clTerm) *clTerm {
	if term.kind == clVar && term.id == id {
		return clIdentity()
	}
	if !containsCLVar(term, id) {
		return clApply(&clTerm{kind: clK}, term)
	}
	if term.kind == clApp {
		return clApply(
			clApply(&clTerm{kind: clS}, bracketAbstract(id, term.a)),
			bracketAbstract(id, term.b),
		)
	}
	panic("bracket abstraction invariant violated")
}

func clIdentity() *clTerm {
	return clApply(clApply(&clTerm{kind: clS}, &clTerm{kind: clK}), &clTerm{kind: clK})
}

func clApply(a, b *clTerm) *clTerm {
	return &clTerm{kind: clApp, a: a, b: b}
}

func containsCLVar(term *clTerm, id int) bool {
	if term == nil {
		return false
	}
	switch term.kind {
	case clVar:
		return term.id == id
	case clApp:
		return containsCLVar(term.a, id) || containsCLVar(term.b, id)
	default:
		return false
	}
}

func containsAnyCLVar(term *clTerm) bool {
	if term == nil {
		return false
	}
	switch term.kind {
	case clVar:
		return true
	case clApp:
		return containsAnyCLVar(term.a) || containsAnyCLVar(term.b)
	default:
		return false
	}
}

func jotCLBits(term *clTerm) int {
	switch term.kind {
	case clK:
		return 5
	case clS:
		return 8
	case clApp:
		return 1 + jotCLBits(term.a) + jotCLBits(term.b)
	default:
		panic("Jot encoding requires closed S/K term")
	}
}
