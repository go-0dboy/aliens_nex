package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"github.com/go-0dboy/aliens_nex/reference/go/bench"
	"github.com/go-0dboy/aliens_nex/reference/go/experiment"
	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

type programReport struct {
	ID               string  `json:"id"`
	PrincipalType    string  `json:"principal_type"`
	ErasedTermBits   int     `json:"erased_term_bits"`
	RootTypeBits     int     `json:"root_type_bits"`
	HybridTotalBits  int     `json:"hybrid_total_bits"`
	OverheadBits     int     `json:"overhead_bits"`
	OverheadPercent  float64 `json:"overhead_percent"`
}

type aggregateReport struct {
	Programs          int     `json:"programs"`
	ErasedTermBits    int     `json:"erased_term_bits"`
	RootTypeBits      int     `json:"root_type_bits"`
	HybridTotalBits   int     `json:"hybrid_total_bits"`
	OverheadBits      int     `json:"overhead_bits"`
	OverheadPercent   float64 `json:"overhead_percent"`
}

type report struct {
	Schema        string          `json:"schema"`
	CorpusVersion string          `json:"corpus_version"`
	Envelope      string          `json:"experimental_envelope"`
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

	result := report{
		Schema:        "nex-type-information-experiment-v0.1",
		CorpusVersion: corpus.CorpusVersion,
		Envelope:      "hybrid-root-principal-type-v0.1",
		Notes: []string{
			"NEX-1 v0.1 canonical term encoding remains unchanged and type-erased",
			"root_type_bits encode only the inferred closed principal top-level type scheme",
			"this measures exact transmission overhead of one hybrid envelope, not a complete explicit-typing replacement",
			"no bootstrap/checker reduction is claimed until an alternative checker is implemented and measured",
		},
	}

	for _, program := range corpus.Programs {
		term, err := bench.TermFromJSON(&program.Term)
		if err != nil {
			fatalf("%s: parse term: %v", program.ID, err)
		}
		termMetrics, err := nex.MeasureTerm(term)
		if err != nil {
			fatalf("%s: measure term: %v", program.ID, err)
		}
		scheme, err := nex.InferClosed(term)
		if err != nil {
			fatalf("%s: infer type: %v", program.ID, err)
		}
		typeBits, err := experiment.RootTypeEnvelopeBits(scheme)
		if err != nil {
			fatalf("%s: encode root type: %v", program.ID, err)
		}
		principal, err := nex.CanonicalSchemeString(scheme)
		if err != nil {
			fatalf("%s: canonical type: %v", program.ID, err)
		}
		hybridBits := termMetrics.WireBits + typeBits
		overheadPercent := 100 * float64(typeBits) / float64(termMetrics.WireBits)
		entry := programReport{
			ID:              program.ID,
			PrincipalType:   principal,
			ErasedTermBits:  termMetrics.WireBits,
			RootTypeBits:    typeBits,
			HybridTotalBits: hybridBits,
			OverheadBits:    typeBits,
			OverheadPercent: overheadPercent,
		}
		result.Programs = append(result.Programs, entry)
		result.Aggregate.Programs++
		result.Aggregate.ErasedTermBits += termMetrics.WireBits
		result.Aggregate.RootTypeBits += typeBits
		result.Aggregate.HybridTotalBits += hybridBits
	}
	result.Aggregate.OverheadBits = result.Aggregate.RootTypeBits
	result.Aggregate.OverheadPercent = 100 * float64(result.Aggregate.RootTypeBits) / float64(result.Aggregate.ErasedTermBits)

	var out []byte
	if *pretty {
		out, err = json.MarshalIndent(result, "", "  ")
	} else {
		out, err = json.Marshal(result)
	}
	if err != nil {
		fatalf("encode report: %v", err)
	}
	if _, err := os.Stdout.Write(append(out, '\n')); err != nil {
		fatalf("write report: %v", err)
	}
}

func fatalf(format string, args ...any) {
	fmt.Fprintf(os.Stderr, "nextypeexperiment: "+format+"\n", args...)
	os.Exit(1)
}
