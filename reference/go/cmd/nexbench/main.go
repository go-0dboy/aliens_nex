package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"math/big"
	"os"

	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

type jsonTerm struct {
	Kind  string    `json:"kind"`
	Value string    `json:"value,omitempty"`
	A     *jsonTerm `json:"a,omitempty"`
	B     *jsonTerm `json:"b,omitempty"`
}

type observation struct {
	Kind  string `json:"kind"`
	Value string `json:"value,omitempty"`
}

type corpus struct {
	Schema        string `json:"schema"`
	CorpusVersion string `json:"corpus_version"`
	Status        string `json:"status"`
	Programs      []struct {
		ID             string      `json:"id"`
		Description    string      `json:"description"`
		Classification string      `json:"classification"`
		Term           jsonTerm    `json:"term"`
		Expected       observation `json:"expected"`
	} `json:"programs"`
}

type portableReport struct {
	WireBits     int                   `json:"wire_bits"`
	ASTNodes     int                   `json:"ast_nodes"`
	Constructors nex.ConstructorCounts `json:"constructors"`
	Observation  observation           `json:"observation"`
}

type referenceReport struct {
	EvaluationTransitions uint64 `json:"evaluation_transitions"`
	MaxEvaluationDepth    uint32 `json:"max_evaluation_depth"`
}

type programReport struct {
	ID             string          `json:"id"`
	Description    string          `json:"description"`
	Classification string          `json:"classification"`
	Portable       portableReport  `json:"portable_exact"`
	Reference      referenceReport `json:"reference_only"`
}

type aggregateReport struct {
	Programs      int                   `json:"programs"`
	WireBits      int                   `json:"wire_bits"`
	ASTNodes      int                   `json:"ast_nodes"`
	Constructors  nex.ConstructorCounts `json:"constructors"`
	Transitions   uint64                `json:"reference_evaluation_transitions"`
	MaxEvalDepth  uint32                `json:"reference_max_evaluation_depth"`
}

type report struct {
	Schema        string          `json:"schema"`
	CorpusVersion string          `json:"corpus_version"`
	CorpusStatus  string          `json:"corpus_status"`
	Programs      []programReport `json:"programs"`
	Aggregate     aggregateReport `json:"aggregate"`
	Notes         []string        `json:"notes"`
}

func main() {
	corpusPath := flag.String("corpus", "", "path to benchmark corpus JSON")
	pretty := flag.Bool("pretty", true, "pretty-print JSON report")
	flag.Parse()
	if *corpusPath == "" {
		fatalf("-corpus is required")
	}

	data, err := os.ReadFile(*corpusPath)
	if err != nil {
		fatalf("read corpus: %v", err)
	}
	var c corpus
	if err := json.Unmarshal(data, &c); err != nil {
		fatalf("parse corpus: %v", err)
	}
	if c.Schema != "nex-benchmark-corpus-v0.1" {
		fatalf("unsupported corpus schema %q", c.Schema)
	}
	if len(c.Programs) == 0 {
		fatalf("corpus has no programs")
	}

	r := report{
		Schema:        "nex-benchmark-report-v0.1",
		CorpusVersion: c.CorpusVersion,
		CorpusStatus:  c.Status,
		Notes: []string{
			"portable_exact values are architecture-neutral properties of the canonical NEX term/wire encoding",
			"reference_only values describe the Go reference evaluator and are not Core performance claims",
			"reference implementation size is not treated as bootstrap transmission cost",
		},
	}

	seen := make(map[string]bool)
	for _, p := range c.Programs {
		if p.ID == "" || seen[p.ID] {
			fatalf("invalid or duplicate program id %q", p.ID)
		}
		seen[p.ID] = true
		term, err := termFromJSON(&p.Term)
		if err != nil {
			fatalf("%s: parse term: %v", p.ID, err)
		}
		metrics, err := nex.MeasureTerm(term)
		if err != nil {
			fatalf("%s: measure term: %v", p.ID, err)
		}
		value, stats, err := nex.EvaluateClosedWithStats(term, nex.DefaultEvalLimits)
		if err != nil {
			fatalf("%s: evaluate: %v", p.ID, err)
		}
		observed, err := observe(value)
		if err != nil {
			fatalf("%s: observe: %v", p.ID, err)
		}
		if observed != p.Expected {
			fatalf("%s: observation %#v != expected %#v", p.ID, observed, p.Expected)
		}

		pr := programReport{
			ID:             p.ID,
			Description:    p.Description,
			Classification: p.Classification,
			Portable: portableReport{
				WireBits:     metrics.WireBits,
				ASTNodes:     metrics.ASTNodes,
				Constructors: metrics.Constructors,
				Observation:  observed,
			},
			Reference: referenceReport{
				EvaluationTransitions: stats.Transitions,
				MaxEvaluationDepth:    stats.MaxDepth,
			},
		}
		r.Programs = append(r.Programs, pr)
		addAggregate(&r.Aggregate, pr)
	}

	var out []byte
	if *pretty {
		out, err = json.MarshalIndent(r, "", "  ")
	} else {
		out, err = json.Marshal(r)
	}
	if err != nil {
		fatalf("encode report: %v", err)
	}
	if _, err := os.Stdout.Write(append(out, '\n')); err != nil {
		fatalf("write report: %v", err)
	}
}

func termFromJSON(j *jsonTerm) (*nex.Term, error) {
	if j == nil {
		return nil, fmt.Errorf("missing term")
	}
	switch j.Kind {
	case "Var":
		v, err := natural(j.Value)
		if err != nil {
			return nil, err
		}
		return nex.Var(v), nil
	case "Lam":
		a, err := termFromJSON(j.A)
		if err != nil {
			return nil, err
		}
		return nex.Lam(a), nil
	case "App":
		a, err := termFromJSON(j.A)
		if err != nil {
			return nil, err
		}
		b, err := termFromJSON(j.B)
		if err != nil {
			return nil, err
		}
		return nex.App(a, b), nil
	case "Let":
		a, err := termFromJSON(j.A)
		if err != nil {
			return nil, err
		}
		b, err := termFromJSON(j.B)
		if err != nil {
			return nil, err
		}
		return nex.Let(a, b), nil
	case "Nat":
		v, err := natural(j.Value)
		if err != nil {
			return nil, err
		}
		return nex.Nat(v), nil
	case "Prim":
		v, err := natural(j.Value)
		if err != nil {
			return nil, err
		}
		return nex.Prim(v), nil
	default:
		return nil, fmt.Errorf("unknown term kind %q", j.Kind)
	}
}

func natural(s string) (*big.Int, error) {
	if s == "" {
		return nil, fmt.Errorf("missing natural value")
	}
	v, ok := new(big.Int).SetString(s, 10)
	if !ok || v.Sign() < 0 {
		return nil, fmt.Errorf("invalid natural %q", s)
	}
	return v, nil
}

func observe(value *nex.Value) (observation, error) {
	if value == nil {
		return observation{}, fmt.Errorf("nil runtime value")
	}
	switch value.Kind {
	case nex.ValueNat:
		if value.Nat == nil {
			return observation{}, fmt.Errorf("Nat missing payload")
		}
		return observation{Kind: "Nat", Value: value.Nat.String()}, nil
	case nex.ValueClosure, nex.ValuePrimitive:
		return observation{Kind: "Function"}, nil
	case nex.ValueUnit:
		return observation{Kind: "Unit"}, nil
	case nex.ValuePair:
		return observation{Kind: "Pair"}, nil
	case nex.ValueInl:
		return observation{Kind: "Inl"}, nil
	case nex.ValueInr:
		return observation{Kind: "Inr"}, nil
	default:
		return observation{}, fmt.Errorf("unknown value kind %d", value.Kind)
	}
}

func addAggregate(a *aggregateReport, p programReport) {
	a.Programs++
	a.WireBits += p.Portable.WireBits
	a.ASTNodes += p.Portable.ASTNodes
	a.Constructors.Var += p.Portable.Constructors.Var
	a.Constructors.Lam += p.Portable.Constructors.Lam
	a.Constructors.App += p.Portable.Constructors.App
	a.Constructors.Let += p.Portable.Constructors.Let
	a.Constructors.Nat += p.Portable.Constructors.Nat
	a.Constructors.Prim += p.Portable.Constructors.Prim
	a.Transitions += p.Reference.EvaluationTransitions
	if p.Reference.MaxEvaluationDepth > a.MaxEvalDepth {
		a.MaxEvalDepth = p.Reference.MaxEvaluationDepth
	}
}

func fatalf(format string, args ...any) {
	fmt.Fprintf(os.Stderr, "nexbench: "+format+"\n", args...)
	os.Exit(1)
}
