package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

type letCase struct {
	SuccChainSteps        int  `json:"succ_chain_steps"`
	Repeats               int  `json:"repeats"`
	PayloadWireBits       int  `json:"payload_wire_bits"`
	DuplicatedWireBits    int  `json:"duplicated_wire_bits"`
	LetWireBits           int  `json:"let_wire_bits"`
	LetMinusDuplicateBits int  `json:"let_minus_duplicate_bits"`
	LetSavesBits          bool `json:"let_saves_bits"`
}

type natCase struct {
	Value                       uint64 `json:"value"`
	LiteralWireBits             int    `json:"literal_wire_bits"`
	SuccChainWireBits           int    `json:"succ_chain_wire_bits"`
	ConstructedMinusLiteralBits int    `json:"constructed_minus_literal_bits"`
}

type report struct {
	Schema         string    `json:"schema"`
	LetExperiments []letCase `json:"let_vs_duplication"`
	NatExperiments []natCase `json:"nat_literal_vs_succ_chain"`
	Interpretation []string  `json:"interpretation_rules"`
}

func main() {
	pretty := flag.Bool("pretty", true, "pretty-print JSON report")
	flag.Parse()

	r := report{
		Schema: "nex-internal-experiments-v0.1",
		Interpretation: []string{
			"negative let_minus_duplicate_bits means Let uses fewer canonical wire bits",
			"positive constructed_minus_literal_bits means direct Nat literal uses fewer canonical wire bits",
			"all measurements use unchanged NEX-1 v0.1 canonical encoding",
		},
	}

	for _, steps := range []int{0, 1, 2, 4, 8} {
		payload := succChain(steps)
		payloadMetrics := mustMeasure(payload)
		for _, repeats := range []int{2, 3, 4, 8} {
			duplicated := repeatedPair(payload, repeats)
			letBound := nex.Let(payload, repeatedPair(nex.Var(nex.NaturalUint64(0)), repeats))
			mustTypecheck(duplicated)
			mustTypecheck(letBound)
			duplicatedMetrics := mustMeasure(duplicated)
			letMetrics := mustMeasure(letBound)
			delta := letMetrics.WireBits - duplicatedMetrics.WireBits
			r.LetExperiments = append(r.LetExperiments, letCase{
				SuccChainSteps:        steps,
				Repeats:               repeats,
				PayloadWireBits:       payloadMetrics.WireBits,
				DuplicatedWireBits:    duplicatedMetrics.WireBits,
				LetWireBits:           letMetrics.WireBits,
				LetMinusDuplicateBits: delta,
				LetSavesBits:          delta < 0,
			})
		}
	}

	for _, value := range []uint64{0, 1, 2, 3, 7, 8, 15, 16, 31, 32, 63, 64, 127, 128, 255} {
		literal := nex.Nat(nex.NaturalUint64(value))
		constructed := succChain(int(value))
		mustTypecheck(literal)
		mustTypecheck(constructed)
		literalMetrics := mustMeasure(literal)
		constructedMetrics := mustMeasure(constructed)
		r.NatExperiments = append(r.NatExperiments, natCase{
			Value:                       value,
			LiteralWireBits:             literalMetrics.WireBits,
			SuccChainWireBits:           constructedMetrics.WireBits,
			ConstructedMinusLiteralBits: constructedMetrics.WireBits - literalMetrics.WireBits,
		})
	}

	var out []byte
	var err error
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

func succChain(steps int) *nex.Term {
	term := nex.Nat(nex.NaturalUint64(0))
	for i := 0; i < steps; i++ {
		term = nex.App(nex.Prim(nex.NaturalUint64(1)), term)
	}
	return term
}

func repeatedPair(item *nex.Term, repeats int) *nex.Term {
	if repeats <= 1 {
		return item
	}
	return nex.App(
		nex.App(nex.Prim(nex.NaturalUint64(4)), item),
		repeatedPair(item, repeats-1),
	)
}

func mustMeasure(term *nex.Term) nex.TermMetrics {
	metrics, err := nex.MeasureTerm(term)
	if err != nil {
		fatalf("measure term: %v", err)
	}
	return metrics
}

func mustTypecheck(term *nex.Term) {
	if _, err := nex.InferClosed(term); err != nil {
		fatalf("typecheck experiment term: %v", err)
	}
}

func fatalf(format string, args ...any) {
	fmt.Fprintf(os.Stderr, "nexexperiment: "+format+"\n", args...)
	os.Exit(1)
}
