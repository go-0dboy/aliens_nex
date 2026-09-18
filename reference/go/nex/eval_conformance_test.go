package nex

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"testing"
)

type evalObservation struct {
	Kind  string `json:"kind"`
	Value string `json:"value,omitempty"`
}

type evalConformanceFile struct {
	EvaluationVectors []struct {
		Name   string          `json:"name"`
		Term   jsonTerm        `json:"term"`
		Result evalObservation `json:"result"`
	} `json:"evaluation_vectors"`
}

func loadEvalConformance(t *testing.T) evalConformanceFile {
	t.Helper()
	path := filepath.Join("..", "..", "..", "conformance", "eval-v0.1.json")
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("read eval conformance file: %v", err)
	}
	var c evalConformanceFile
	if err := json.Unmarshal(data, &c); err != nil {
		t.Fatalf("parse eval conformance file: %v", err)
	}
	return c
}

func observeValue(value *Value) (evalObservation, error) {
	if value == nil {
		return evalObservation{}, fmt.Errorf("nil runtime value")
	}
	switch value.Kind {
	case ValueNat:
		if value.Nat == nil {
			return evalObservation{}, fmt.Errorf("Nat value missing payload")
		}
		return evalObservation{Kind: "Nat", Value: value.Nat.String()}, nil
	case ValueClosure, ValuePrimitive:
		return evalObservation{Kind: "Function"}, nil
	case ValueUnit:
		return evalObservation{Kind: "Unit"}, nil
	case ValuePair:
		return evalObservation{Kind: "Pair"}, nil
	case ValueInl:
		return evalObservation{Kind: "Inl"}, nil
	case ValueInr:
		return evalObservation{Kind: "Inr"}, nil
	default:
		return evalObservation{}, fmt.Errorf("unknown runtime value kind %d", value.Kind)
	}
}

func TestEvaluationConformance(t *testing.T) {
	c := loadEvalConformance(t)
	if len(c.EvaluationVectors) == 0 {
		t.Fatal("evaluation conformance corpus is empty")
	}
	for _, tc := range c.EvaluationVectors {
		t.Run(tc.Name, func(t *testing.T) {
			term := termFromJSON(t, tc.Term)
			value, err := EvaluateClosed(term, DefaultEvalLimits)
			if err != nil {
				t.Fatalf("EvaluateClosed() error = %v", err)
			}
			got, err := observeValue(value)
			if err != nil {
				t.Fatal(err)
			}
			if got != tc.Result {
				t.Fatalf("observation = %#v, want %#v", got, tc.Result)
			}
		})
	}
}
