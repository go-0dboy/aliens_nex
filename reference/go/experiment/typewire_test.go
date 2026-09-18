package experiment

import (
	"testing"

	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

func TestRootTypeEnvelopeIdentity(t *testing.T) {
	scheme := nex.TypeScheme{
		Quantified: []nex.TypeVarID{7},
		Body:       nex.TFunc(nex.TVar(7), nex.TVar(7)),
	}
	bits, err := RootTypeEnvelopeBits(scheme)
	if err != nil {
		t.Fatal(err)
	}
	// U(1)=3 bits, function prefix=3, each T0=00+U(0)=3.
	if bits != 12 {
		t.Fatalf("identity root type envelope = %d bits, want 12", bits)
	}
}

func TestRootTypeEnvelopeNat(t *testing.T) {
	bits, err := RootTypeEnvelopeBits(nex.MonoScheme(nex.TNat()))
	if err != nil {
		t.Fatal(err)
	}
	// U(0)=1 bit plus Nat prefix=3.
	if bits != 4 {
		t.Fatalf("Nat root type envelope = %d bits, want 4", bits)
	}
}

func TestRootTypeEnvelopeRejectsFreeVariable(t *testing.T) {
	_, err := RootTypeEnvelopeBits(nex.MonoScheme(nex.TVar(3)))
	if err == nil {
		t.Fatal("expected free type variable to be rejected")
	}
}
