package nex

import (
	"errors"
	"math/big"
	"testing"
)

func TestULargeRoundTrip(t *testing.T) {
	values := []string{
		"18446744073709551616",
		"340282366920938463463374607431768211455",
		"12345678901234567890123456789012345678901234567890",
	}
	for _, s := range values {
		n, _ := new(big.Int).SetString(s, 10)
		bits, err := EncodeU(n)
		if err != nil { t.Fatal(err) }
		got, next, err := DecodeU(bits, 0, DefaultDecodeLimits)
		if err != nil { t.Fatal(err) }
		if next != len(bits) || got.Cmp(n) != 0 {
			t.Fatalf("round trip %s -> %s consumed %d/%d", n, got, next, len(bits))
		}
	}
}

func TestURejectsTruncatedAndLimits(t *testing.T) {
	bits, _ := ParseBits("000")
	_, _, err := DecodeU(bits, 0, DefaultDecodeLimits)
	if !errors.Is(err, ErrTruncated) { t.Fatalf("got %v want ErrTruncated", err) }

	bits, _ = ParseBits("0001000")
	_, _, err = DecodeU(bits, 0, DecodeLimits{MaxIntegerBits: 3})
	var limitErr *ResourceLimitError
	if !errors.As(err, &limitErr) { t.Fatalf("got %v want ResourceLimitError", err) }
}

func TestDecodeOneReportsConsumedBits(t *testing.T) {
	bits, _ := ParseBits("010011")
	term, consumed, err := DecodeOne(bits, DefaultDecodeLimits)
	if err != nil { t.Fatal(err) }
	if !EqualTerm(term, Lam(Var(NaturalUint64(0)))) { t.Fatal("unexpected term") }
	if consumed != 5 { t.Fatalf("consumed=%d want 5", consumed) }

	_, err = DecodeExact(bits, DefaultDecodeLimits)
	if !errors.Is(err, ErrTrailingBits) { t.Fatalf("got %v want ErrTrailingBits", err) }
}

func TestInvalidBitRejected(t *testing.T) {
	_, _, err := DecodeOne(Bits{0, 1, 0, 0, 2}, DefaultDecodeLimits)
	if !errors.Is(err, ErrInvalidBit) { t.Fatalf("got %v want ErrInvalidBit", err) }
}

func TestDecodeResourceLimits(t *testing.T) {
	term := Lam(Lam(Var(NaturalUint64(0))))
	bits, _ := EncodeTerm(term)

	_, err := DecodeExact(bits, DecodeLimits{MaxIntegerBits: 64, MaxTermDepth: 2, MaxNodes: 100})
	var limitErr *ResourceLimitError
	if !errors.As(err, &limitErr) { t.Fatalf("got %v want ResourceLimitError", err) }

	_, err = DecodeExact(bits, DecodeLimits{MaxIntegerBits: 64, MaxTermDepth: 100, MaxNodes: 2})
	if !errors.As(err, &limitErr) { t.Fatalf("got %v want ResourceLimitError", err) }
}

func TestEncodeRejectsInvalidShape(t *testing.T) {
	_, err := EncodeTerm(&Term{Kind: KindLam})
	if !errors.Is(err, ErrInvalidTerm) { t.Fatalf("got %v want ErrInvalidTerm", err) }
}

func FuzzTermDecodeDoesNotPanic(f *testing.F) {
	seeds := []string{"1", "01001", "01101111010001", "11001001001", "000", "1111"}
	for _, s := range seeds { f.Add(s) }
	f.Fuzz(func(t *testing.T, s string) {
		bits, err := ParseBits(s)
		if err != nil { return }
		_, _, _ = DecodeOne(bits, DecodeLimits{MaxIntegerBits: 256, MaxTermDepth: 64, MaxNodes: 1024})
	})
}

func termFromFuzzBytes(data []byte, pos *int, depth int) *Term {
	if len(data) == 0 { return Nat(NaturalUint64(0)) }
	next := func() byte {
		b := data[*pos%len(data)]
		*pos = *pos + 1
		return b
	}
	kind := next() % 6
	if depth >= 6 {
		kind = kind % 3
		if kind == 1 { kind = 4 }
		if kind == 2 { kind = 5 }
	}
	value := func() *big.Int {
		v := uint64(next())<<16 | uint64(next())<<8 | uint64(next())
		return NaturalUint64(v)
	}
	switch Kind(kind) {
	case KindVar:
		return Var(value())
	case KindLam:
		return Lam(termFromFuzzBytes(data, pos, depth+1))
	case KindApp:
		return App(termFromFuzzBytes(data, pos, depth+1), termFromFuzzBytes(data, pos, depth+1))
	case KindLet:
		return Let(termFromFuzzBytes(data, pos, depth+1), termFromFuzzBytes(data, pos, depth+1))
	case KindNat:
		return Nat(value())
	default:
		return Prim(value())
	}
}

func FuzzTermRoundTrip(f *testing.F) {
	for _, seed := range [][]byte{{0}, {1, 2, 3}, {2, 4, 8, 16}, {3, 1, 4, 1, 5, 9}} { f.Add(seed) }
	f.Fuzz(func(t *testing.T, data []byte) {
		if len(data) == 0 { return }
		pos := 0
		term := termFromFuzzBytes(data, &pos, 0)
		bits, err := EncodeTerm(term)
		if err != nil { t.Fatal(err) }
		got, err := DecodeExact(bits, DecodeLimits{MaxIntegerBits: 64, MaxTermDepth: 64, MaxNodes: 4096})
		if err != nil { t.Fatal(err) }
		if !EqualTerm(got, term) { t.Fatal("round-trip term mismatch") }
	})
}
