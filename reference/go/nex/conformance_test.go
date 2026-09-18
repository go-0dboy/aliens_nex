package nex

import (
	"encoding/json"
	"errors"
	"math/big"
	"os"
	"path/filepath"
	"testing"
)

type conformanceFile struct {
	IntegerVectors []struct {
		Name  string `json:"name"`
		Value string `json:"value"`
		Bits  string `json:"bits"`
	} `json:"integer_vectors"`
	TermVectors []struct {
		Name string   `json:"name"`
		Term jsonTerm `json:"term"`
		Bits string   `json:"bits"`
	} `json:"term_vectors"`
	InvalidExactVectors []struct {
		Name  string `json:"name"`
		Bits  string `json:"bits"`
		Error string `json:"error"`
	} `json:"invalid_exact_vectors"`
}

type jsonTerm struct {
	Kind  string    `json:"kind"`
	Value string    `json:"value,omitempty"`
	A     *jsonTerm `json:"a,omitempty"`
	B     *jsonTerm `json:"b,omitempty"`
}

func loadConformance(t *testing.T) conformanceFile {
	t.Helper()
	path := filepath.Join("..", "..", "..", "conformance", "wire-v0.1.json")
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("read conformance file: %v", err)
	}
	var c conformanceFile
	if err := json.Unmarshal(data, &c); err != nil {
		t.Fatalf("parse conformance file: %v", err)
	}
	return c
}

func naturalFromDecimal(t *testing.T, s string) *big.Int {
	t.Helper()
	n, ok := new(big.Int).SetString(s, 10)
	if !ok || n.Sign() < 0 {
		t.Fatalf("invalid natural %q", s)
	}
	return n
}

func termFromJSON(t *testing.T, j jsonTerm) *Term {
	t.Helper()
	switch j.Kind {
	case "Var":
		return Var(naturalFromDecimal(t, j.Value))
	case "Lam":
		if j.A == nil {
			t.Fatal("Lam missing a")
		}
		return Lam(termFromJSON(t, *j.A))
	case "App":
		if j.A == nil || j.B == nil {
			t.Fatal("App missing child")
		}
		return App(termFromJSON(t, *j.A), termFromJSON(t, *j.B))
	case "Let":
		if j.A == nil || j.B == nil {
			t.Fatal("Let missing child")
		}
		return Let(termFromJSON(t, *j.A), termFromJSON(t, *j.B))
	case "Nat":
		return Nat(naturalFromDecimal(t, j.Value))
	case "Prim":
		return Prim(naturalFromDecimal(t, j.Value))
	default:
		t.Fatalf("unknown term kind %q", j.Kind)
		return nil
	}
}

func TestConformanceIntegerVectors(t *testing.T) {
	c := loadConformance(t)
	for _, tc := range c.IntegerVectors {
		t.Run(tc.Name, func(t *testing.T) {
			n := naturalFromDecimal(t, tc.Value)
			encoded, err := EncodeU(n)
			if err != nil {
				t.Fatal(err)
			}
			if encoded.String() != tc.Bits {
				t.Fatalf("encoded=%s want=%s", encoded.String(), tc.Bits)
			}
			decoded, next, err := DecodeU(encoded, 0, DefaultDecodeLimits)
			if err != nil {
				t.Fatal(err)
			}
			if next != len(encoded) || decoded.Cmp(n) != 0 {
				t.Fatalf("decoded=%s consumed=%d/%d want=%s", decoded, next, len(encoded), n)
			}
		})
	}
}

func TestConformanceTermVectors(t *testing.T) {
	c := loadConformance(t)
	for _, tc := range c.TermVectors {
		t.Run(tc.Name, func(t *testing.T) {
			term := termFromJSON(t, tc.Term)
			encoded, err := EncodeTerm(term)
			if err != nil {
				t.Fatal(err)
			}
			if encoded.String() != tc.Bits {
				t.Fatalf("encoded=%s want=%s", encoded.String(), tc.Bits)
			}
			decoded, err := DecodeExact(encoded, DefaultDecodeLimits)
			if err != nil {
				t.Fatal(err)
			}
			if !EqualTerm(decoded, term) {
				t.Fatal("decoded term differs")
			}
		})
	}
}

func TestConformanceInvalidExactVectors(t *testing.T) {
	c := loadConformance(t)
	for _, tc := range c.InvalidExactVectors {
		t.Run(tc.Name, func(t *testing.T) {
			bits, err := ParseBits(tc.Bits)
			if err != nil {
				t.Fatal(err)
			}
			_, err = DecodeExact(bits, DefaultDecodeLimits)
			switch tc.Error {
			case "truncated":
				if !errors.Is(err, ErrTruncated) {
					t.Fatalf("got %v want truncated", err)
				}
			case "trailing":
				if !errors.Is(err, ErrTrailingBits) {
					t.Fatalf("got %v want trailing", err)
				}
			default:
				t.Fatalf("unknown expected error %q", tc.Error)
			}
		})
	}
}
