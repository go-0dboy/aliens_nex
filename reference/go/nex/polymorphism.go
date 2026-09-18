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

// Instantiate replaces each quantified variable in a type scheme with a distinct
// fresh monotype variable. Every scheme use must be instantiated independently.
func Instantiate(scheme TypeScheme, fresh *FreshTypeVars) (*Type, error) {
	if err := ValidateScheme(scheme); err != nil {
		return nil, err
	}
	if fresh == nil {
		fresh = NewFreshTypeVars(0)
	}
	sub := make(Substitution, len(scheme.Quantified))
	for _, id := range scheme.Quantified {
		sub[id] = fresh.Fresh()
	}
	return ApplyType(sub, scheme.Body)
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
