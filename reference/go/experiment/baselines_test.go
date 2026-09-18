package experiment

import (
	"errors"
	"testing"

	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

func TestBLCIdentity(t *testing.T) {
	bits, err := BLCBits(nex.Lam(nex.Var(nex.NaturalUint64(0))))
	if err != nil {
		t.Fatal(err)
	}
	if bits != 4 {
		t.Fatalf("BLC identity = %d bits, want 4", bits)
	}
}

func TestBLCRejectsNonLambdaCoreConstructor(t *testing.T) {
	_, err := BLCBits(nex.Nat(nex.NaturalUint64(0)))
	if !errors.Is(err, ErrBaselineUnsupported) {
		t.Fatalf("BLC Nat error = %v, want ErrBaselineUnsupported", err)
	}
}

func TestJotBracketIdentity(t *testing.T) {
	bits, err := JotBitsBracketSK(nex.Lam(nex.Var(nex.NaturalUint64(0))))
	if err != nil {
		t.Fatal(err)
	}
	// Standard bracket abstraction yields I = S K K, then Barker's Jot map.
	if bits != 20 {
		t.Fatalf("canonical bracket-to-Jot identity = %d bits, want 20", bits)
	}
}

func TestTinyStackIdentity(t *testing.T) {
	bits, err := TinyStackBits(nex.Lam(nex.Var(nex.NaturalUint64(0))))
	if err != nil {
		t.Fatal(err)
	}
	// Var(0): 3-bit opcode + U(0), then 3-bit postfix Lam.
	if bits != 7 {
		t.Fatalf("tiny stack identity = %d bits, want 7", bits)
	}
}
