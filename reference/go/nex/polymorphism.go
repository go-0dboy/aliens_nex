package nex

import "sort"

// FreshTypeVars owns the internal identity supply used by one inference run.
// Type variable IDs are implementation details and never appear on the NEX wire.
type FreshTypeVars struct {
	next TypeVarID
}

func NewFreshTypeVars(start TypeVarID) *FreshTypeVars {
	return &FreshTypeVars{next: start}
}

func (f *FreshTypeVars) Fresh() *Type {
	id := f.next
	f.next++
	return TVar(id)
}

func (f *FreshTypeVars) FreshID() TypeVarID {
	id := f.next
	f.next++
	return id
}

// Instantiate alpha-renames every quantified variable to a distinct fresh variable.
// This is intentionally not implemented through general substitution: a scheme may use
// template IDs such as T0 while the fresh supply also starts at T0, and alpha-renaming
// must treat that as a valid identity choice rather than a substitution cycle.
func Instantiate(scheme TypeScheme, fresh *FreshTypeVars) (*Type, error) {
	if err := ValidateScheme(scheme); err != nil {
		return nil, err
	}
	if fresh == nil {
		fresh = NewFreshTypeVars(0)
	}
	renaming := make(map[TypeVarID]TypeVarID, len(scheme.Quantified))
	for _, id := range scheme.Quantified {
		renaming[id] = fresh.FreshID()
	}
	return instantiateType(scheme.Body, renaming), nil
}

func instantiateType(t *Type, renaming map[TypeVarID]TypeVarID) *Type {
	switch t.Kind {
	case TypeVar:
		if id, ok := renaming[t.Var]; ok {
			return TVar(id)
		}
		return TVar(t.Var)
	case TypeUnit:
		return TUnit()
	case TypeNat:
		return TNat()
	case TypeFunc:
		return TFunc(instantiateType(t.A, renaming), instantiateType(t.B, renaming))
	case TypeProduct:
		return TProduct(instantiateType(t.A, renaming), instantiateType(t.B, renaming))
	case TypeSum:
		return TSum(instantiateType(t.A, renaming), instantiateType(t.B, renaming))
	default:
		return cloneType(t)
	}
}

// Generalize quantifies exactly the variables free in typ but not free in env.
// Sorting internal IDs makes the stored scheme deterministic; semantic comparison
// still uses canonicalization rather than relying on these IDs.
func Generalize(env TypeEnv, typ *Type) (TypeScheme, error) {
	if err := ValidateType(typ); err != nil {
		return TypeScheme{}, err
	}
	typeVars, err := FreeTypeVars(typ)
	if err != nil {
		return TypeScheme{}, err
	}
	envVars, err := FreeEnvVars(env)
	if err != nil {
		return TypeScheme{}, err
	}

	quantified := make([]TypeVarID, 0, len(typeVars))
	for id := range typeVars {
		if !envVars.Has(id) {
			quantified = append(quantified, id)
		}
	}
	sort.Slice(quantified, func(i, j int) bool { return quantified[i] < quantified[j] })
	return TypeScheme{Quantified: quantified, Body: cloneType(typ)}, nil
}
