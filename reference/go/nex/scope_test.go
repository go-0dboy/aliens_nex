package nex

import (
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
	"testing"
)

type staticConformanceFile struct {
	ScopeVectors []struct {
		Name  string   `json:"name"`
		Term  jsonTerm `json:"term"`
		Valid bool     `json:"valid"`
		Error string   `json:"error,omitempty"`
	} `json:"scope_vectors"`
}

func loadStaticConformance(t *testing.T) staticConformanceFile {
	t.Helper()
	path := filepath.Join("..", "..", "..", "conformance", "static-v0.1.json")
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("read static conformance file: %v", err)
	}
	var c staticConformanceFile
	if err := json.Unmarshal(data, &c); err != nil {
		t.Fatalf("parse static conformance file: %v", err)
	}
	return c
}

func TestScopeConformance(t *testing.T) {
	c := loadStaticConformance(t)
	for _, tc := range c.ScopeVectors {
		t.Run(tc.Name, func(t *testing.T) {
			term := termFromJSON(t, tc.Term)
			err := ValidateClosed(term)

			if tc.Valid {
				if err != nil {
					t.Fatalf("ValidateClosed() error = %v, want nil", err)
				}
				return
			}

			if err == nil {
				t.Fatal("ValidateClosed() error = nil, want failure")
			}
			switch tc.Error {
			case "out_of_scope":
				if !errors.Is(err, ErrOutOfScope) {
					t.Fatalf("ValidateClosed() error = %v, want ErrOutOfScope", err)
				}
			default:
				t.Fatalf("unknown expected error class %q", tc.Error)
			}
		})
	}
}

func TestScopeErrorCarriesIndexAndDepth(t *testing.T) {
	err := ValidateClosed(Lam(Var(NaturalUint64(1))))
	var scopeErr *ScopeError
	if !errors.As(err, &scopeErr) {
		t.Fatalf("ValidateClosed() error = %v, want *ScopeError", err)
	}
	if scopeErr.Index.Cmp(NaturalUint64(1)) != 0 {
		t.Fatalf("ScopeError.Index = %s, want 1", scopeErr.Index)
	}
	if scopeErr.Depth != 1 {
		t.Fatalf("ScopeError.Depth = %d, want 1", scopeErr.Depth)
	}
}

func TestScopeRejectsInvalidInMemoryShape(t *testing.T) {
	cases := []*Term{
		nil,
		{Kind: KindVar},
		{Kind: KindLam},
		{Kind: KindNat},
		{Kind: KindPrim},
		{Kind: KindApp, A: Nat(NaturalUint64(0))},
		{Kind: KindLet, B: Nat(NaturalUint64(0))},
	}

	for i, term := range cases {
		if err := ValidateClosed(term); !errors.Is(err, ErrInvalidTerm) {
			t.Fatalf("case %d: ValidateClosed() error = %v, want ErrInvalidTerm", i, err)
		}
	}
}

func FuzzScopeValidationDoesNotPanic(f *testing.F) {
	for _, seed := range [][]byte{{0}, {1, 2, 3}, {3, 1, 4, 1, 5, 9}} {
		f.Add(seed)
	}
	f.Fuzz(func(t *testing.T, data []byte) {
		if len(data) == 0 {
			return
		}
		pos := 0
		term := termFromFuzzBytes(data, &pos, 0)
		_ = ValidateClosed(term)
	})
}
