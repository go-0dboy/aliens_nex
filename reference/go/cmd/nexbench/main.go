package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"github.com/go-0dboy/aliens_nex/reference/go/bench"
	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

type portableReport struct {
	WireBits          int                     `json:"wire_bits"`
	ASTNodes          int                     `json:"ast_nodes"`
	Constructors      nex.ConstructorCounts   `json:"constructors"`
	WireByConstructor nex.ConstructorWireBits `json:"wire_bits_by_constructor"`
	Observation       bench.Observation       `json:"observation"`
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
	Programs          int                     `json:"programs"`
	WireBits          int                     `json:"wire_bits"`
	ASTNodes          int                     `json:"ast_nodes"`
	Constructors      nex.ConstructorCounts   `json:"constructors"`
	WireByConstructor nex.ConstructorWireBits `json:"wire_bits_by_constructor"`
	Transitions       uint64                  `json:"reference_evaluation_transitions"`
	MaxEvalDepth      uint32                  `json:"reference_max_evaluation_depth"`
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

	corpus, err := bench.LoadCorpus(*corpusPath)
	if err != nil {
		fatalf("load corpus: %v", err)
	}

	reportValue := report{
		Schema:        "nex-benchmark-report-v0.1",
		CorpusVersion: corpus.CorpusVersion,
		CorpusStatus:  corpus.Status,
		Notes: []string{
			"portable_exact values are architecture-neutral properties of the canonical NEX term/wire encoding",
			"wire_bits_by_constructor attributes each bit to the local constructor encoding that emitted it and sums exactly to wire_bits",
			"reference_only values describe the Go reference evaluator and are not Core performance claims",
			"reference implementation size is not treated as bootstrap transmission cost",
		},
	}

	for _, program := range corpus.Programs {
		term, err := bench.TermFromJSON(&program.Term)
		if err != nil {
			fatalf("%s: parse term: %v", program.ID, err)
		}
		metrics, err := nex.MeasureTerm(term)
		if err != nil {
			fatalf("%s: measure term: %v", program.ID, err)
		}
		value, stats, err := nex.EvaluateClosedWithStats(term, nex.DefaultEvalLimits)
		if err != nil {
			fatalf("%s: evaluate: %v", program.ID, err)
		}
		observed, err := bench.Observe(value)
		if err != nil {
			fatalf("%s: observe: %v", program.ID, err)
		}
		if observed != program.Expected {
			fatalf("%s: observation %#v != expected %#v", program.ID, observed, program.Expected)
		}

		programResult := programReport{
			ID:             program.ID,
			Description:    program.Description,
			Classification: program.Classification,
			Portable: portableReport{
				WireBits:          metrics.WireBits,
				ASTNodes:          metrics.ASTNodes,
				Constructors:      metrics.Constructors,
				WireByConstructor: metrics.WireByConstructor,
				Observation:       observed,
			},
			Reference: referenceReport{
				EvaluationTransitions: stats.Transitions,
				MaxEvaluationDepth:    stats.MaxDepth,
			},
		}
		reportValue.Programs = append(reportValue.Programs, programResult)
		addAggregate(&reportValue.Aggregate, programResult)
	}

	var out []byte
	if *pretty {
		out, err = json.MarshalIndent(reportValue, "", "  ")
	} else {
		out, err = json.Marshal(reportValue)
	}
	if err != nil {
		fatalf("encode report: %v", err)
	}
	if _, err := os.Stdout.Write(append(out, '\n')); err != nil {
		fatalf("write report: %v", err)
	}
}

func addAggregate(aggregate *aggregateReport, program programReport) {
	aggregate.Programs++
	aggregate.WireBits += program.Portable.WireBits
	aggregate.ASTNodes += program.Portable.ASTNodes
	aggregate.Constructors.Var += program.Portable.Constructors.Var
	aggregate.Constructors.Lam += program.Portable.Constructors.Lam
	aggregate.Constructors.App += program.Portable.Constructors.App
	aggregate.Constructors.Let += program.Portable.Constructors.Let
	aggregate.Constructors.Nat += program.Portable.Constructors.Nat
	aggregate.Constructors.Prim += program.Portable.Constructors.Prim
	aggregate.WireByConstructor.Var += program.Portable.WireByConstructor.Var
	aggregate.WireByConstructor.Lam += program.Portable.WireByConstructor.Lam
	aggregate.WireByConstructor.App += program.Portable.WireByConstructor.App
	aggregate.WireByConstructor.Let += program.Portable.WireByConstructor.Let
	aggregate.WireByConstructor.Nat += program.Portable.WireByConstructor.Nat
	aggregate.WireByConstructor.Prim += program.Portable.WireByConstructor.Prim
	aggregate.Transitions += program.Reference.EvaluationTransitions
	if program.Reference.MaxEvaluationDepth > aggregate.MaxEvalDepth {
		aggregate.MaxEvalDepth = program.Reference.MaxEvaluationDepth
	}
}

func fatalf(format string, args ...any) {
	fmt.Fprintf(os.Stderr, "nexbench: "+format+"\n", args...)
	os.Exit(1)
}
