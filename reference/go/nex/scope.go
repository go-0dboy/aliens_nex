package nex

import (
	"errors"
	"fmt"
	"math/big"
)

var ErrOutOfScope = errors.New("de Bruijn index out of scope")

// ScopeError reports a Var(index) that has no enclosing Lam or Let binder.
// Depth is the number of binders visible at the offending variable.
type ScopeError struct {
	Index *big.Int
	Depth int
}

func (e *ScopeError) Error() string {
	return fmt.Sprintf("%v: index %s at binder depth %d", ErrOutOfScope, e.Index.String(), e.Depth)
}

func (e *ScopeError) Unwrap() error { return ErrOutOfScope }

// ValidateClosed verifies the NEX-1 v0.1 de Bruijn scope rules for a top-level Core term.
//
// A top-level program starts with binder depth 0. Lam introduces one binder for its body.
// Let introduces one binder for its body only; the let value is checked in the outer scope.
func ValidateClosed(term *Term) error {
	return validateScope(term, 0)
}

func validateScope(term *Term, depth int) error {
	if term == nil {
		return ErrInvalidTerm
	}

	switch term.Kind {
	case KindVar:
		if term.Value == nil || term.Value.Sign() < 0 || term.A != nil || term.B != nil {
			return ErrInvalidTerm
		}
		if !indexInScope(term.Value, depth) {
			return &ScopeError{Index: cloneNat(term.Value), Depth: depth}
		}
		return nil

	case KindLam:
		if term.A == nil || term.Value != nil || term.B != nil {
			return ErrInvalidTerm
		}
		return validateScope(term.A, depth+1)

	case KindApp:
		if term.A == nil || term.B == nil || term.Value != nil {
			return ErrInvalidTerm
		}
		if err := validateScope(term.A, depth); err != nil {
			return err
		}
		return validateScope(term.B, depth)

	case KindLet:
		if term.A == nil || term.B == nil || term.Value != nil {
			return ErrInvalidTerm
		}
		// NEX-1 v0.1 Let is non-recursive: its binder is not visible in value.
		if err := validateScope(term.A, depth); err != nil {
			return err
		}
		return validateScope(term.B, depth+1)

	case KindNat, KindPrim:
		if term.Value == nil || term.Value.Sign() < 0 || term.A != nil || term.B != nil {
			return ErrInvalidTerm
		}
		return nil

	default:
		return ErrInvalidTerm
	}
}

func indexInScope(index *big.Int, depth int) bool {
	if index == nil || index.Sign() < 0 || depth <= 0 {
		return false
	}
	// depth is an in-memory tree depth and therefore bounded by the host int.
	// Any non-negative index that does not fit uint64 is necessarily >= depth.
	if !index.IsUint64() {
		return false
	}
	return index.Uint64() < uint64(depth)
}
