package nex

import (
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
	"testing"
)

type staticTypeConformanceFile struct {
	TypeVectors []struct {
		Name  string   `json:"name"`
		Term  jsonTerm `json:"term"`
		Valid bool     `json:"valid"`
		Type  string   `json:"type,omitempty"`
		Error string   `json:"error,omitempty"`
	} `json:"type_vectors"`
}

func loadStaticTypeConformance(t *testing.T) staticTypeConformanceFile {
	t.Helper()
	path := filepath.Join("..", "..", "..", "conformance", "static-v0.1.json")
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("read static conformance file: %v", err)
	}
	var c staticTypeConformanceFile
	if err := json.Unmarshal(data, &c); err != nil {
		t.Fatalf("parse static conformance file: %v", err)
	}
	return c
}

func TestTypeConformance(t *testing.T) {
	c := loadStaticTypeConformance(t)
	if len(c.TypeVectors) == 0 {
		t.Fatal("static conformance file contains no type vectors")
	}
	for _, tc := range c.TypeVectors {
		t.Run(tc.Name, func(t *testing.T) {
			term := termFromJSON(t, tc.Term)
			scheme, err := InferClosed(term)

			if tc.Valid {
				if err != nil {
					t.Fatalf("InferClosed() error = %v, want nil", err)
				}
				got, err := CanonicalSchemeString(scheme)
				if err != nil {
					t.Fatal(err)
				}
				if got != tc.Type {
					t.Fatalf("principal type = %q, want %q", got, tc.Type)
				}
				return
			}

			if err == nil {
				t.Fatal("InferClosed() error = nil, want failure")
			}
			switch tc.Error {
			case "out_of_scope":
				if !errors.Is(err, ErrOutOfScope) {
					t.Fatalf("error = %v, want ErrOutOfScope", err)
				}
			case "unknown_primitive":
				if !errors.Is(err, ErrUnknownPrimitive) {
					t.Fatalf("error = %v, want ErrUnknownPrimitive", err)
				}
			case "type_mismatch":
				if !errors.Is(err, ErrTypeMismatch) {
					t.Fatalf("error = %v, want ErrTypeMismatch", err)
				}
			case "occurs_check":
				if !errors.Is(err, ErrOccursCheck) {
					t.Fatalf("error = %v, want ErrOccursCheck", err)
				}
			default:
				t.Fatalf("unknown expected error class %q", tc.Error)
			}
		})
	}
}
