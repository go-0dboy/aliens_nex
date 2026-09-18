package nex

import (
	"errors"
	"fmt"
)

var (
	ErrTypeMismatch = errors.New("types do not unify")
	ErrOccursCheck  = errors.New("occurs check failed")
)

type TypeMismatchError struct {
	Left  *Type
	Right *Type
}

func (e *TypeMismatchError) Error() string {
	left, _ := CanonicalTypeString(e.Left)
	right, _ := CanonicalTypeString(e.Right)
	return fmt.Sprintf("%v: %s vs %s", ErrTypeMismatch, left, right)
}

func (e *TypeMismatchError) Unwrap() error { return ErrTypeMismatch }

type OccursCheckError struct {
	Var  TypeVarID
	Type *Type
}

func (e *OccursCheckError) Error() string {
	typ, _ := CanonicalTypeString(e.Type)
	return fmt.Sprintf("%v: T%d occurs in %s", ErrOccursCheck, e.Var, typ)
}

func (e *OccursCheckError) Unwrap() error { return ErrOccursCheck }

// Unify returns a substitution S such that apply(S, left) == apply(S, right),
// or a deterministic mismatch/occurs-check error.
func Unify(left, right *Type) (Substitution, error) {
	if err := ValidateType(left); err != nil {
		return nil, err
	}
	if err := ValidateType(right); err != nil {
		return nil, err
	}
	return unify(left, right)
}

func unify(left, right *Type) (Substitution, error) {
	if left.Kind == TypeVar && right.Kind == TypeVar && left.Var == right.Var {
		return EmptySubstitution(), nil
	}
	if left.Kind == TypeVar {
		return bindTypeVar(left.Var, right)
	}
	if right.Kind == TypeVar {
		return bindTypeVar(right.Var, left)
	}

	if left.Kind != right.Kind {
		return nil, &TypeMismatchError{Left: left, Right: right}
	}

	switch left.Kind {
	case TypeUnit, TypeNat:
		return EmptySubstitution(), nil
	case TypeFunc, TypeProduct, TypeSum:
		first, err := unify(left.A, right.A)
		if err != nil {
			return nil, err
		}
		leftB, err := ApplyType(first, left.B)
		if err != nil {
			return nil, err
		}
		rightB, err := ApplyType(first, right.B)
		if err != nil {
			return nil, err
		}
		second, err := unify(leftB, rightB)
		if err != nil {
			return nil, err
		}
		return ComposeSubstitutions(second, first)
	default:
		return nil, ErrInvalidType
	}
}

func bindTypeVar(id TypeVarID, typ *Type) (Substitution, error) {
	if typ.Kind == TypeVar && typ.Var == id {
		return EmptySubstitution(), nil
	}
	vars, err := FreeTypeVars(typ)
	if err != nil {
		return nil, err
	}
	if vars.Has(id) {
		return nil, &OccursCheckError{Var: id, Type: typ}
	}
	return Substitution{id: typ}, nil
}
