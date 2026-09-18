package nex

import (
	"errors"
	"fmt"
	"strings"
)

var ErrInvalidType = errors.New("invalid in-memory type")

type TypeVarID uint64

type TypeKind uint8

const (
	TypeVar TypeKind = iota
	TypeUnit
	TypeNat
	TypeFunc
	TypeProduct
	TypeSum
)

// Type is the reference in-memory representation of the NEX-1 v0.1 monotype grammar.
// Human-readable variable names are intentionally absent; variables use internal IDs.
type Type struct {
	Kind TypeKind
	Var  TypeVarID
	A    *Type
	B    *Type
}

// TypeScheme represents forall Quantified. Body.
// Quantified variables are internal IDs, not transmitted names.
type TypeScheme struct {
	Quantified []TypeVarID
	Body       *Type
}

func TVar(id TypeVarID) *Type          { return &Type{Kind: TypeVar, Var: id} }
func TUnit() *Type                     { return &Type{Kind: TypeUnit} }
func TNat() *Type                      { return &Type{Kind: TypeNat} }
func TFunc(a, b *Type) *Type           { return &Type{Kind: TypeFunc, A: a, B: b} }
func TProduct(a, b *Type) *Type        { return &Type{Kind: TypeProduct, A: a, B: b} }
func TSum(a, b *Type) *Type            { return &Type{Kind: TypeSum, A: a, B: b} }
func MonoScheme(body *Type) TypeScheme { return TypeScheme{Body: body} }

func EqualType(x, y *Type) bool {
	if x == nil || y == nil {
		return x == y
	}
	if x.Kind != y.Kind {
		return false
	}
	switch x.Kind {
	case TypeVar:
		return x.Var == y.Var && x.A == nil && x.B == nil && y.A == nil && y.B == nil
	case TypeUnit, TypeNat:
		return x.A == nil && x.B == nil && y.A == nil && y.B == nil
	case TypeFunc, TypeProduct, TypeSum:
		return EqualType(x.A, y.A) && EqualType(x.B, y.B)
	default:
		return false
	}
}

func ValidateType(t *Type) error {
	if t == nil {
		return ErrInvalidType
	}
	switch t.Kind {
	case TypeVar:
		if t.A != nil || t.B != nil {
			return ErrInvalidType
		}
		return nil
	case TypeUnit, TypeNat:
		if t.Var != 0 || t.A != nil || t.B != nil {
			return ErrInvalidType
		}
		return nil
	case TypeFunc, TypeProduct, TypeSum:
		if t.Var != 0 || t.A == nil || t.B == nil {
			return ErrInvalidType
		}
		if err := ValidateType(t.A); err != nil {
			return err
		}
		return ValidateType(t.B)
	default:
		return ErrInvalidType
	}
}

func ValidateScheme(s TypeScheme) error {
	if err := ValidateType(s.Body); err != nil {
		return err
	}
	seen := make(map[TypeVarID]struct{}, len(s.Quantified))
	for _, id := range s.Quantified {
		if _, exists := seen[id]; exists {
			return fmt.Errorf("%w: duplicate quantified variable %d", ErrInvalidType, id)
		}
		seen[id] = struct{}{}
	}
	return nil
}

// CanonicalTypeString gives types a stable test/debug representation independent of
// internal type-variable IDs. Variables are renamed T0, T1, ... by first occurrence.
func CanonicalTypeString(t *Type) (string, error) {
	if err := ValidateType(t); err != nil {
		return "", err
	}
	n := newTypeCanonicalizer()
	return n.format(t), nil
}

// CanonicalSchemeString canonicalizes both quantified-variable ordering and variable IDs.
// Quantified variables that occur in the body are listed by first occurrence in the body.
func CanonicalSchemeString(s TypeScheme) (string, error) {
	if err := ValidateScheme(s); err != nil {
		return "", err
	}

	quantified := make(map[TypeVarID]struct{}, len(s.Quantified))
	for _, id := range s.Quantified {
		quantified[id] = struct{}{}
	}

	c := newTypeCanonicalizer()
	body := c.format(s.Body)

	ordered := make([]string, 0, len(s.Quantified))
	for _, id := range c.order {
		if _, ok := quantified[id]; ok {
			ordered = append(ordered, c.names[id])
		}
	}
	// Vacuous quantified variables are uncommon in principal schemes, but keeping them
	// deterministic makes the representation total for any validated TypeScheme.
	for _, id := range s.Quantified {
		if _, alreadyNamed := c.names[id]; !alreadyNamed {
			ordered = append(ordered, c.name(id))
		}
	}

	if len(ordered) == 0 {
		return body, nil
	}
	return "forall " + strings.Join(ordered, " ") + ". " + body, nil
}

type typeCanonicalizer struct {
	names map[TypeVarID]string
	order []TypeVarID
}

func newTypeCanonicalizer() *typeCanonicalizer {
	return &typeCanonicalizer{names: make(map[TypeVarID]string)}
}

func (c *typeCanonicalizer) name(id TypeVarID) string {
	if name, ok := c.names[id]; ok {
		return name
	}
	name := fmt.Sprintf("T%d", len(c.names))
	c.names[id] = name
	c.order = append(c.order, id)
	return name
}

func (c *typeCanonicalizer) format(t *Type) string {
	switch t.Kind {
	case TypeVar:
		return c.name(t.Var)
	case TypeUnit:
		return "1"
	case TypeNat:
		return "N"
	case TypeFunc:
		return "(" + c.format(t.A) + " -> " + c.format(t.B) + ")"
	case TypeProduct:
		return "(" + c.format(t.A) + " * " + c.format(t.B) + ")"
	case TypeSum:
		return "(" + c.format(t.A) + " + " + c.format(t.B) + ")"
	default:
		panic("format called after ValidateType accepted an unknown TypeKind")
	}
}
