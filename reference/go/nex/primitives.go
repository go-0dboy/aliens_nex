package nex

import (
	"errors"
	"fmt"
	"math/big"
)

var ErrUnknownPrimitive = errors.New("unknown Core primitive")

type UnknownPrimitiveError struct {
	ID *big.Int
}

func (e *UnknownPrimitiveError) Error() string {
	if e.ID == nil {
		return ErrUnknownPrimitive.Error()
	}
	return fmt.Sprintf("%v: %s", ErrUnknownPrimitive, e.ID.String())
}

func (e *UnknownPrimitiveError) Unwrap() error { return ErrUnknownPrimitive }

type CorePrimitive struct {
	ID     uint64
	Name   string
	Scheme TypeScheme
}

// corePrimitives is the authoritative NEX-1 v0.1 Core primitive metadata table.
// Type inference and future runtime work must derive primitive metadata from this table
// rather than maintaining independent ID/type definitions.
var corePrimitives = []CorePrimitive{
	{ID: 0, Name: "fix", Scheme: TypeScheme{Quantified: []TypeVarID{0}, Body: TFunc(TFunc(TVar(0), TVar(0)), TVar(0))}},
	{ID: 1, Name: "succ", Scheme: MonoScheme(TFunc(TNat(), TNat()))},
	{ID: 2, Name: "pred", Scheme: MonoScheme(TFunc(TNat(), TNat()))},
	{ID: 3, Name: "ifz", Scheme: TypeScheme{Quantified: []TypeVarID{0}, Body: TFunc(TNat(), TFunc(TVar(0), TFunc(TVar(0), TVar(0))))}},
	{ID: 4, Name: "pair", Scheme: TypeScheme{Quantified: []TypeVarID{0, 1}, Body: TFunc(TVar(0), TFunc(TVar(1), TProduct(TVar(0), TVar(1))))}},
	{ID: 5, Name: "fst", Scheme: TypeScheme{Quantified: []TypeVarID{0, 1}, Body: TFunc(TProduct(TVar(0), TVar(1)), TVar(0))}},
	{ID: 6, Name: "snd", Scheme: TypeScheme{Quantified: []TypeVarID{0, 1}, Body: TFunc(TProduct(TVar(0), TVar(1)), TVar(1))}},
	{ID: 7, Name: "inl", Scheme: TypeScheme{Quantified: []TypeVarID{0, 1}, Body: TFunc(TVar(0), TSum(TVar(0), TVar(1)))}},
	{ID: 8, Name: "inr", Scheme: TypeScheme{Quantified: []TypeVarID{0, 1}, Body: TFunc(TVar(1), TSum(TVar(0), TVar(1)))}},
	{ID: 9, Name: "case", Scheme: TypeScheme{Quantified: []TypeVarID{0, 1, 2}, Body: TFunc(TSum(TVar(0), TVar(1)), TFunc(TFunc(TVar(0), TVar(2)), TFunc(TFunc(TVar(1), TVar(2)), TVar(2))))}},
	{ID: 10, Name: "unit", Scheme: MonoScheme(TUnit())},
}

func CorePrimitives() []CorePrimitive {
	out := make([]CorePrimitive, len(corePrimitives))
	for i, primitive := range corePrimitives {
		out[i] = CorePrimitive{
			ID:     primitive.ID,
			Name:   primitive.Name,
			Scheme: cloneScheme(primitive.Scheme),
		}
	}
	return out
}

func LookupCorePrimitive(id *big.Int) (CorePrimitive, error) {
	if id == nil || id.Sign() < 0 || !id.IsUint64() {
		return CorePrimitive{}, &UnknownPrimitiveError{ID: cloneNat(id)}
	}
	value := id.Uint64()
	if value >= uint64(len(corePrimitives)) {
		return CorePrimitive{}, &UnknownPrimitiveError{ID: cloneNat(id)}
	}
	primitive := corePrimitives[value]
	return CorePrimitive{ID: primitive.ID, Name: primitive.Name, Scheme: cloneScheme(primitive.Scheme)}, nil
}

func ValidateCorePrimitives(term *Term) error {
	if term == nil {
		return ErrInvalidTerm
	}
	switch term.Kind {
	case KindVar, KindNat:
		return validateLeafTermShape(term)
	case KindPrim:
		if err := validateLeafTermShape(term); err != nil {
			return err
		}
		_, err := LookupCorePrimitive(term.Value)
		return err
	case KindLam:
		if term.Value != nil || term.A == nil || term.B != nil {
			return ErrInvalidTerm
		}
		return ValidateCorePrimitives(term.A)
	case KindApp, KindLet:
		if term.Value != nil || term.A == nil || term.B == nil {
			return ErrInvalidTerm
		}
		if err := ValidateCorePrimitives(term.A); err != nil {
			return err
		}
		return ValidateCorePrimitives(term.B)
	default:
		return ErrInvalidTerm
	}
}

func validateLeafTermShape(term *Term) error {
	if term == nil || term.Value == nil || term.Value.Sign() < 0 || term.A != nil || term.B != nil {
		return ErrInvalidTerm
	}
	return nil
}

func cloneScheme(s TypeScheme) TypeScheme {
	quantified := append([]TypeVarID(nil), s.Quantified...)
	return TypeScheme{Quantified: quantified, Body: cloneType(s.Body)}
}

func cloneType(t *Type) *Type {
	if t == nil {
		return nil
	}
	switch t.Kind {
	case TypeVar:
		return TVar(t.Var)
	case TypeUnit:
		return TUnit()
	case TypeNat:
		return TNat()
	case TypeFunc:
		return TFunc(cloneType(t.A), cloneType(t.B))
	case TypeProduct:
		return TProduct(cloneType(t.A), cloneType(t.B))
	case TypeSum:
		return TSum(cloneType(t.A), cloneType(t.B))
	default:
		return &Type{Kind: t.Kind, Var: t.Var, A: cloneType(t.A), B: cloneType(t.B)}
	}
}
