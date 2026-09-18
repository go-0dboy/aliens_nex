package nex

import (
	"errors"
	"fmt"
	"math/big"
	"strings"
)

// Bits is the reference representation of a NEX bit string.
// Each element MUST be either 0 or 1.
type Bits []byte

var (
	ErrTruncated       = errors.New("truncated bit string")
	ErrTrailingBits    = errors.New("trailing bits after complete term")
	ErrInvalidBit      = errors.New("bit string contains value other than 0 or 1")
	ErrInvalidTerm     = errors.New("invalid in-memory term")
	ErrNegativeNatural = errors.New("natural number must be non-negative")
)

type ResourceLimitError struct {
	Resource string
	Limit    int
}

func (e *ResourceLimitError) Error() string {
	return fmt.Sprintf("resource limit exceeded: %s > %d", e.Resource, e.Limit)
}

func ParseBits(s string) (Bits, error) {
	out := make(Bits, len(s))
	for i := range s {
		switch s[i] {
		case '0':
			out[i] = 0
		case '1':
			out[i] = 1
		default:
			return nil, fmt.Errorf("%w at character %d", ErrInvalidBit, i)
		}
	}
	return out, nil
}

func (b Bits) String() string {
	var sb strings.Builder
	sb.Grow(len(b))
	for _, bit := range b {
		if bit == 0 {
			sb.WriteByte('0')
		} else if bit == 1 {
			sb.WriteByte('1')
		} else {
			sb.WriteByte('?')
		}
	}
	return sb.String()
}

func appendBits(dst Bits, values ...byte) Bits {
	return append(dst, values...)
}

func readBit(bits Bits, pos int) (byte, int, error) {
	if pos >= len(bits) {
		return 0, pos, ErrTruncated
	}
	bit := bits[pos]
	if bit != 0 && bit != 1 {
		return 0, pos, fmt.Errorf("%w at bit %d", ErrInvalidBit, pos)
	}
	return bit, pos + 1, nil
}

// DecodeLimits are implementation safety limits, not NEX wire validity rules.
// A zero field means unlimited for that resource.
type DecodeLimits struct {
	MaxIntegerBits int
	MaxTermDepth   int
	MaxNodes       int
}

var DefaultDecodeLimits = DecodeLimits{
	MaxIntegerBits: 1 << 20,
	MaxTermDepth:   2048,
	MaxNodes:       1 << 18,
}

// EncodeU encodes a non-negative integer as Elias gamma(n+1), as specified by NEX U(n).
func EncodeU(n *big.Int) (Bits, error) {
	if n == nil || n.Sign() < 0 {
		return nil, ErrNegativeNatural
	}

	m := new(big.Int).Add(n, big.NewInt(1))
	binary := m.Text(2)
	out := make(Bits, 0, 2*len(binary)-1)
	for i := 1; i < len(binary); i++ {
		out = append(out, 0)
	}
	for i := range binary {
		if binary[i] == '0' {
			out = append(out, 0)
		} else {
			out = append(out, 1)
		}
	}
	return out, nil
}

// DecodeU decodes one U(n) value starting at offset and returns the next unread bit offset.
func DecodeU(bits Bits, offset int, limits DecodeLimits) (*big.Int, int, error) {
	if offset < 0 || offset > len(bits) {
		return nil, offset, fmt.Errorf("invalid offset %d", offset)
	}

	pos := offset
	zeroCount := 0
	for {
		bit, next, err := readBit(bits, pos)
		if err != nil {
			return nil, pos, err
		}
		pos = next
		if bit == 1 {
			break
		}
		zeroCount++
		if limits.MaxIntegerBits > 0 && zeroCount+1 > limits.MaxIntegerBits {
			return nil, pos, &ResourceLimitError{Resource: "integer bits", Limit: limits.MaxIntegerBits}
		}
	}

	bitLen := zeroCount + 1
	if limits.MaxIntegerBits > 0 && bitLen > limits.MaxIntegerBits {
		return nil, pos, &ResourceLimitError{Resource: "integer bits", Limit: limits.MaxIntegerBits}
	}

	m := big.NewInt(1)
	for i := 1; i < bitLen; i++ {
		bit, next, err := readBit(bits, pos)
		if err != nil {
			return nil, pos, err
		}
		pos = next
		m.Lsh(m, 1)
		if bit == 1 {
			m.Add(m, big.NewInt(1))
		}
	}

	return new(big.Int).Sub(m, big.NewInt(1)), pos, nil
}

func EncodeTerm(term *Term) (Bits, error) {
	var out Bits
	if err := encodeTermInto(&out, term); err != nil {
		return nil, err
	}
	return out, nil
}

func encodeTermInto(out *Bits, term *Term) error {
	if term == nil {
		return ErrInvalidTerm
	}

	switch term.Kind {
	case KindVar:
		if term.Value == nil || term.Value.Sign() < 0 || term.A != nil || term.B != nil {
			return ErrInvalidTerm
		}
		*out = appendBits(*out, 0, 0)
		encoded, err := EncodeU(term.Value)
		if err != nil {
			return err
		}
		*out = append(*out, encoded...)
		return nil

	case KindLam:
		if term.A == nil || term.Value != nil || term.B != nil {
			return ErrInvalidTerm
		}
		*out = appendBits(*out, 0, 1)
		return encodeTermInto(out, term.A)

	case KindApp:
		if term.A == nil || term.B == nil || term.Value != nil {
			return ErrInvalidTerm
		}
		*out = appendBits(*out, 1, 0)
		if err := encodeTermInto(out, term.A); err != nil {
			return err
		}
		return encodeTermInto(out, term.B)

	case KindLet:
		if term.A == nil || term.B == nil || term.Value != nil {
			return ErrInvalidTerm
		}
		*out = appendBits(*out, 1, 1, 0)
		if err := encodeTermInto(out, term.A); err != nil {
			return err
		}
		return encodeTermInto(out, term.B)

	case KindNat:
		if term.Value == nil || term.Value.Sign() < 0 || term.A != nil || term.B != nil {
			return ErrInvalidTerm
		}
		*out = appendBits(*out, 1, 1, 1, 0)
		encoded, err := EncodeU(term.Value)
		if err != nil {
			return err
		}
		*out = append(*out, encoded...)
		return nil

	case KindPrim:
		if term.Value == nil || term.Value.Sign() < 0 || term.A != nil || term.B != nil {
			return ErrInvalidTerm
		}
		*out = appendBits(*out, 1, 1, 1, 1)
		encoded, err := EncodeU(term.Value)
		if err != nil {
			return err
		}
		*out = append(*out, encoded...)
		return nil

	default:
		return ErrInvalidTerm
	}
}

type decodeState struct {
	bits   Bits
	limits DecodeLimits
	nodes  int
}

func DecodeOne(bits Bits, limits DecodeLimits) (*Term, int, error) {
	s := &decodeState{bits: bits, limits: limits}
	return s.term(0, 1)
}

func DecodeExact(bits Bits, limits DecodeLimits) (*Term, error) {
	term, consumed, err := DecodeOne(bits, limits)
	if err != nil {
		return nil, err
	}
	if consumed != len(bits) {
		return nil, fmt.Errorf("%w: consumed %d of %d", ErrTrailingBits, consumed, len(bits))
	}
	return term, nil
}

func (s *decodeState) countNode(depth int) error {
	if s.limits.MaxTermDepth > 0 && depth > s.limits.MaxTermDepth {
		return &ResourceLimitError{Resource: "term depth", Limit: s.limits.MaxTermDepth}
	}
	s.nodes++
	if s.limits.MaxNodes > 0 && s.nodes > s.limits.MaxNodes {
		return &ResourceLimitError{Resource: "term nodes", Limit: s.limits.MaxNodes}
	}
	return nil
}

func (s *decodeState) term(pos int, depth int) (*Term, int, error) {
	if err := s.countNode(depth); err != nil {
		return nil, pos, err
	}

	first, pos, err := readBit(s.bits, pos)
	if err != nil {
		return nil, pos, err
	}
	second, pos, err := readBit(s.bits, pos)
	if err != nil {
		return nil, pos, err
	}

	if first == 0 {
		if second == 0 {
			value, next, err := DecodeU(s.bits, pos, s.limits)
			if err != nil {
				return nil, next, err
			}
			return Var(value), next, nil
		}
		body, next, err := s.term(pos, depth+1)
		if err != nil {
			return nil, next, err
		}
		return Lam(body), next, nil
	}

	if second == 0 {
		fn, next, err := s.term(pos, depth+1)
		if err != nil {
			return nil, next, err
		}
		arg, next2, err := s.term(next, depth+1)
		if err != nil {
			return nil, next2, err
		}
		return App(fn, arg), next2, nil
	}

	third, pos, err := readBit(s.bits, pos)
	if err != nil {
		return nil, pos, err
	}
	if third == 0 {
		value, next, err := s.term(pos, depth+1)
		if err != nil {
			return nil, next, err
		}
		body, next2, err := s.term(next, depth+1)
		if err != nil {
			return nil, next2, err
		}
		return Let(value, body), next2, nil
	}

	fourth, pos, err := readBit(s.bits, pos)
	if err != nil {
		return nil, pos, err
	}
	value, next, err := DecodeU(s.bits, pos, s.limits)
	if err != nil {
		return nil, next, err
	}
	if fourth == 0 {
		return Nat(value), next, nil
	}
	return Prim(value), next, nil
}
