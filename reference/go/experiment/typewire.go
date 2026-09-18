package experiment

import (
	"fmt"
	"math/big"

	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

// RootTypeEnvelopeBits measures an explicitly non-normative hybrid envelope:
// U(number of quantified variables) followed by one compact principal monotype.
// It is an experiment only; NEX-1 v0.1 canonical terms remain type-erased.
func RootTypeEnvelopeBits(scheme nex.TypeScheme) (int, error) {
	if err := nex.ValidateScheme(scheme); err != nil {
		return 0, err
	}

	quantified := make(map[nex.TypeVarID]struct{}, len(scheme.Quantified))
	for _, id := range scheme.Quantified {
		quantified[id] = struct{}{}
	}

	indices := make(map[nex.TypeVarID]uint64, len(scheme.Quantified))
	if err := assignTypeVarIndices(scheme.Body, quantified, indices); err != nil {
		return 0, err
	}
	for _, id := range scheme.Quantified {
		if _, ok := indices[id]; !ok {
			indices[id] = uint64(len(indices))
		}
	}

	quantifierBits, err := nex.EncodeU(new(big.Int).SetUint64(uint64(len(scheme.Quantified))))
	if err != nil {
		return 0, err
	}
	bodyBits, err := typeBits(scheme.Body, indices)
	if err != nil {
		return 0, err
	}
	return len(quantifierBits) + bodyBits, nil
}

func assignTypeVarIndices(t *nex.Type, quantified map[nex.TypeVarID]struct{}, indices map[nex.TypeVarID]uint64) error {
	if t == nil {
		return nex.ErrInvalidType
	}
	switch t.Kind {
	case nex.TypeVar:
		if _, ok := quantified[t.Var]; !ok {
			return fmt.Errorf("experimental root type envelope requires a closed scheme: free type variable %d", t.Var)
		}
		if _, ok := indices[t.Var]; !ok {
			indices[t.Var] = uint64(len(indices))
		}
	case nex.TypeUnit, nex.TypeNat:
		return nil
	case nex.TypeFunc, nex.TypeProduct, nex.TypeSum:
		if err := assignTypeVarIndices(t.A, quantified, indices); err != nil {
			return err
		}
		return assignTypeVarIndices(t.B, quantified, indices)
	default:
		return nex.ErrInvalidType
	}
	return nil
}

func typeBits(t *nex.Type, indices map[nex.TypeVarID]uint64) (int, error) {
	if t == nil {
		return 0, nex.ErrInvalidType
	}
	switch t.Kind {
	case nex.TypeVar:
		index, ok := indices[t.Var]
		if !ok {
			return 0, fmt.Errorf("missing canonical type-variable index for %d", t.Var)
		}
		encoded, err := nex.EncodeU(new(big.Int).SetUint64(index))
		if err != nil {
			return 0, err
		}
		return 2 + len(encoded), nil // 00 U(index)
	case nex.TypeUnit:
		return 3, nil // 010
	case nex.TypeNat:
		return 3, nil // 011
	case nex.TypeFunc, nex.TypeProduct, nex.TypeSum:
		left, err := typeBits(t.A, indices)
		if err != nil {
			return 0, err
		}
		right, err := typeBits(t.B, indices)
		if err != nil {
			return 0, err
		}
		return 3 + left + right, nil // 100 / 101 / 110
	default:
		return 0, nex.ErrInvalidType
	}
}
