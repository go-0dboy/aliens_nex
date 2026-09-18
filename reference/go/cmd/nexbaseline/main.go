package main

import (
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"os"

	"github.com/go-0dboy/aliens_nex/reference/go/bench"
	"github.com/go-0dboy/aliens_nex/reference/go/experiment"
	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

type programReport struct {
	ID            string `json:"id"`
	NEXBits       int    `json:"nex_bits"`
	TinyStackBits int    `json:"tiny_stack_bits"`
	BLCBits       *int   `json:"blc_bits,omitempty"`
	JotBits       *int   `json:"jot_bracket_sk_bits,omitempty"`
}

type lambdaSubsetAggregate struct {
	Programs int `json:"programs"`
	NEXBits  int `json:"nex_bits"`
	BLCBits  int `json:"blc_bits"`
	JotBits  int `json:"jot_bracket_sk_bits"`
}

type fullCorpusAggregate struct {
	Programs          int     `json:"programs"`
	NEXBits           int     `json:"nex_bits"`
	TinyStackBits     int     `json:"tiny_stack_bits"`
	StackMinusNEXBits int     `json:"stack_minus_nex_bits"`
	StackDeltaPercent float64 `json:"stack_delta_percent"`
}

type report struct {
	Schema        string                `json:"schema"`
	CorpusVersion string                `json:"corpus_version"`
	Programs      []programReport       `json:"programs"`
	LambdaSubset  lambdaSubsetAggregate `json:"pure_lambda_subset"`
	FullCorpus    fullCorpusAggregate   `json:"full_corpus"`
	Notes         []string              `json:"notes"`
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
		Schema:        "nex-baseline-comparison-v0.1",
		CorpusVersion: corpus.CorpusVersion,
		Notes: []string{
			"BLC is compared only on the identical pure lambda subset; no Church encoding of NEX Nat/Prim is silently introduced",
			"Jot uses deterministic standard SK bracket abstraction followed by Barker's K/S/application mapping; it is not a shortest-Jot-program claim",
			"tiny_stack is a project-defined 3-bit postfix structural encoding that reuses NEX U(n) and primitive IDs; it isolates structural encoding cost and is not an independent bootstrap",
		},
	}

	for _, program := range corpus.Programs {
		term, err := bench.TermFromJSON(&program.Term)
		if err != nil {
			fatalf("%s: parse term: %v", program.ID, err)
		}
		nexMetrics, err := nex.MeasureTerm(term)
		if err != nil {
			fatalf("%s: measure NEX: %v", program.ID, err)
		}
		stackBits, err := experiment.TinyStackBits(term)
		if err != nil {
			fatalf("%s: measure tiny stack: %v", program.ID, err)
		}

		entry := programReport{ID: program.ID, NEXBits: nexMetrics.WireBits, TinyStackBits: stackBits}
		blcBits, blcErr := experiment.BLCBits(term)
		if blcErr == nil {
			jotBits, jotErr := experiment.JotBitsBracketSK(term)
			if jotErr != nil {
				fatalf("%s: Jot translation failed after BLC accepted term: %v", program.ID, jotErr)
			}
			entry.BLCBits = intPointer(blcBits)
			entry.JotBits = intPointer(jotBits)
			result.LambdaSubset.Programs++
			result.LambdaSubset.NEXBits += nexMetrics.WireBits
			result.LambdaSubset.BLCBits += blcBits
			result.LambdaSubset.JotBits += jotBits
		} else if !errors.Is(blcErr, experiment.ErrBaselineUnsupported) {
			fatalf("%s: BLC measurement: %v", program.ID, blcErr)
		}

		result.Programs = append(result.Programs, entry)
		result.FullCorpus.Programs++
		result.FullCorpus.NEXBits += nexMetrics.WireBits
		result.FullCorpus.TinyStackBits += stackBits
	}
	result.FullCorpus.StackMinusNEXBits = result.FullCorpus.TinyStackBits - result.FullCorpus.NEXBits
	result.FullCorpus.StackDeltaPercent = 100 * float64(result.FullCorpus.StackMinusNEXBits) / float64(result.FullCorpus.NEXBits)

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

func intPointer(value int) *int {
	return &value
}

func fatalf(format string, args ...any) {
	fmt.Fprintf(os.Stderr, "nexbaseline: "+format+"\n", args...)
	os.Exit(1)
}
