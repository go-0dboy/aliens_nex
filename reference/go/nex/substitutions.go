package nex

import (
	"errors"
	"fmt"
)

var ErrInvalidSubstitution = errors.New("invalid type substitution")

type TypeVarSet map[TypeVarID]struct{}

type Substitution map[TypeVarID]*Type

// TypeEnv is ordered nearest de Bruijn binder first.
type TypeEnv []TypeScheme

func EmptySubstitution() Substitution { return Substitution{} }

func (s TypeVarSet) Has(id TypeVarID) bool {
	_, ok := s[id]
	return ok
}

func FreeTypeVars(t *Type) (TypeVarSet, error) {
	if err := ValidateType(t); err != nil {
		return nil, err
	}
	out := make(TypeVarSet)
	collectTypeVars(t, out)
	return out, nil
}

func FreeSchemeVars(s TypeScheme) (TypeVarSet, error) {
	if err := ValidateScheme(s); err != nil {
		return nil, err
	}
	out := make(TypeVarSet)
	collectTypeVars(s.Body, out)
	for _, id := range s.Quantified {
		delete(out, id)
	}
	return out, nil
}

func FreeEnvVars(env TypeEnv) (TypeVarSet, error) {
	out := make(TypeVarSet)
	for _, scheme := range env {
		vars, err := FreeSchemeVars(scheme)
		if err != nil {
			return nil, err
		}
		for id := range vars {
			out[id] = struct{}{}
		}
	}
	return out, nil
}

func collectTypeVars(t *Type, out TypeVarSet) {
	switch t.Kind {
	case TypeVar:
		out[t.Var] = struct{}{}
	case TypeUnit, TypeNat:
		return
	case TypeFunc, TypeProduct, TypeSum:
		collectTypeVars(t.A, out)
		collectTypeVars(t.B, out)
	}
}

func ApplyType(sub Substitution, t *Type) (*Type, error) {
	if err := ValidateType(t); err != nil {
		return nil, err
	}
	return applyType(sub, t, make(map[TypeVarID]bool))
}

func applyType(sub Substitution, t *Type, resolving map[TypeVarID]bool) (*Type, error) {
	switch t.Kind {
	case TypeVar:
		replacement, ok := sub[t.Var]
		if !ok {
			return TVar(t.Var), nil
		}
		if replacement == nil {
			return nil, fmt.Errorf("%w: nil replacement for T%d", ErrInvalidSubstitution, t.Var)
		}
		if resolving[t.Var] {
			return nil, fmt.Errorf("%w: cycle involving T%d", ErrInvalidSubstitution, t.Var)
		}
		if err := ValidateType(replacement); err != nil {
			return nil, fmt.Errorf("%w: replacement for T%d: %v", ErrInvalidSubstitution, t.Var, err)
		}
		resolving[t.Var] = true
		out, err := applyType(sub, replacement, resolving)
		delete(resolving, t.Var)
		return out, err
	case TypeUnit:
		return TUnit(), nil
	case TypeNat:
		return TNat(), nil
	case TypeFunc, TypeProduct, TypeSum:
		a, err := applyType(sub, t.A, resolving)
		if err != nil {
			return nil, err
		}
		b, err := applyType(sub, t.B, resolving)
		if err != nil {
			return nil, err
		}
		switch t.Kind {
		case TypeFunc:
			return TFunc(a, b), nil
		case TypeProduct:
			return TProduct(a, b), nil
		default:
			return TSum(a, b), nil
		}
	default:
		return nil, ErrInvalidType
	}
}

func ApplyScheme(sub Substitution, scheme TypeScheme) (TypeScheme, error) {
	if err := ValidateScheme(scheme); err != nil {
		return TypeScheme{}, err
	}
	filtered := make(Substitution, len(sub))
	for id, typ := range sub {
		filtered[id] = typ
	}
	for _, id := range scheme.Quantified {
		delete(filtered, id)
	}
	body, err := ApplyType(filtered, scheme.Body)
	if err != nil {
		return TypeScheme{}, err
	}
	quantified := append([]TypeVarID(nil), scheme.Quantified...)
	return TypeScheme{Quantified: quantified, Body: body}, nil
}

func ApplyEnv(sub Substitution, env TypeEnv) (TypeEnv, error) {
	out := make(TypeEnv, len(env))
	for i, scheme := range env {
		applied, err := ApplyScheme(sub, scheme)
		if err != nil {
			return nil, err
		}
		out[i] = applied
	}
	return out, nil
}

// ComposeSubstitutions returns newer o older: applying the result to a type is
// equivalent to applying older first and newer second.
func ComposeSubstitutions(newer, older Substitution) (Substitution, error) {
	out := make(Substitution, len(older)+len(newer))
	for id, typ := range older {
		applied, err := ApplyType(newer, typ)
		if err != nil {
			return nil, err
		}
		out[id] = applied
	}
	for id, typ := range newer {
		if _, exists := out[id]; exists {
			continue
		}
		applied, err := ApplyType(newer, typ)
		if err != nil {
			return nil, err
		}
		out[id] = applied
	}
	return out, nil
}
