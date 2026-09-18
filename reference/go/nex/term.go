package nex

import "math/big"

type Kind uint8

const (
	KindVar Kind = iota
	KindLam
	KindApp
	KindLet
	KindNat
	KindPrim
)

type Term struct {
	Kind  Kind
	Value *big.Int
	A     *Term
	B     *Term
}

func cloneNat(n *big.Int) *big.Int {
	if n == nil {
		return nil
	}
	return new(big.Int).Set(n)
}

func Var(index *big.Int) *Term    { return &Term{Kind: KindVar, Value: cloneNat(index)} }
func Lam(body *Term) *Term        { return &Term{Kind: KindLam, A: body} }
func App(fn, arg *Term) *Term     { return &Term{Kind: KindApp, A: fn, B: arg} }
func Let(value, body *Term) *Term { return &Term{Kind: KindLet, A: value, B: body} }
func Nat(value *big.Int) *Term    { return &Term{Kind: KindNat, Value: cloneNat(value)} }
func Prim(id *big.Int) *Term      { return &Term{Kind: KindPrim, Value: cloneNat(id)} }

func NaturalUint64(v uint64) *big.Int { return new(big.Int).SetUint64(v) }

func EqualTerm(x, y *Term) bool {
	if x == nil || y == nil {
		return x == y
	}
	if x.Kind != y.Kind {
		return false
	}
	switch x.Kind {
	case KindVar, KindNat, KindPrim:
		if x.Value == nil || y.Value == nil {
			return x.Value == nil && y.Value == nil
		}
		return x.Value.Cmp(y.Value) == 0
	case KindLam:
		return EqualTerm(x.A, y.A)
	case KindApp, KindLet:
		return EqualTerm(x.A, y.A) && EqualTerm(x.B, y.B)
	default:
		return false
	}
}
