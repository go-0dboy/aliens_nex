package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"

	"github.com/go-0dboy/aliens_nex/reference/go/bench"
	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

type programCost struct {
	Programs int `json:"programs"`
	Bits     int `json:"bits"`
}

type specificationProxy struct {
	Path        string `json:"path"`
	UTF8Bytes   int    `json:"utf8_bytes"`
	RawUTF8Bits int    `json:"raw_utf8_bits"`
	AcceptedAsS bool   `json:"accepted_as_S"`
}

type referenceProxy struct {
	Files     []string `json:"files"`
	UTF8Bytes int      `json:"utf8_bytes"`
	EqualsB   bool     `json:"equals_B"`
}

type bootstrapCost struct {
	Known  bool   `json:"known"`
	Reason string `json:"reason"`
}

type report struct {
	Schema             string             `json:"schema"`
	Formula            string             `json:"formula"`
	CorpusVersion      string             `json:"corpus_version"`
	P                  programCost        `json:"P_exact_program_cost"`
	SProxy             specificationProxy `json:"S_spec_text_proxy"`
	R                  referenceProxy     `json:"R_reference_go_proxy"`
	B                  bootstrapCost      `json:"B_bootstrap_cost"`
	TotalCComputable   bool               `json:"total_C_computable"`
	InterpretationRule []string           `json:"interpretation_rules"`
}

var referenceManifest = []string{
	"reference/go/nex/term.go",
	"reference/go/nex/codec.go",
	"reference/go/nex/scope.go",
	"reference/go/nex/types.go",
	"reference/go/nex/substitutions.go",
	"reference/go/nex/polymorphism.go",
	"reference/go/nex/unify.go",
	"reference/go/nex/primitives.go",
	"reference/go/nex/infer.go",
	"reference/go/nex/runtime.go",
	"reference/go/nex/eval.go",
}

func main() {
	corpusPath := flag.String("corpus", "", "path to benchmark corpus JSON")
	repoRoot := flag.String("repo-root", "../..", "path to repository root")
	pretty := flag.Bool("pretty", true, "pretty-print JSON report")
	flag.Parse()
	if *corpusPath == "" {
		fatalf("-corpus is required")
	}

	corpus, err := bench.LoadCorpus(*corpusPath)
	if err != nil {
		fatalf("load corpus: %v", err)
	}

	pBits := 0
	for _, program := range corpus.Programs {
		term, err := bench.TermFromJSON(&program.Term)
		if err != nil {
			fatalf("%s: parse term: %v", program.ID, err)
		}
		metrics, err := nex.MeasureTerm(term)
		if err != nil {
			fatalf("%s: measure term: %v", program.ID, err)
		}
		pBits += metrics.WireBits
	}

	root, err := filepath.Abs(*repoRoot)
	if err != nil {
		fatalf("resolve repo root: %v", err)
	}

	specRelative := "docs/NEX-1-v0.1.md"
	specBytes, err := fileBytes(filepath.Join(root, specRelative))
	if err != nil {
		fatalf("read specification proxy: %v", err)
	}

	referenceBytes := 0
	for _, relative := range referenceManifest {
		size, err := fileBytes(filepath.Join(root, relative))
		if err != nil {
			fatalf("read reference proxy file %s: %v", relative, err)
		}
		referenceBytes += size
	}

	result := report{
		Schema:        "nex-total-information-accounting-v0.1",
		Formula:       "C = S + B + P",
		CorpusVersion: corpus.CorpusVersion,
		P: programCost{
			Programs: len(corpus.Programs),
			Bits:     pBits,
		},
		SProxy: specificationProxy{
			Path:        specRelative,
			UTF8Bytes:   specBytes,
			RawUTF8Bits: specBytes * 8,
			AcceptedAsS: false,
		},
		R: referenceProxy{
			Files:     append([]string(nil), referenceManifest...),
			UTF8Bytes: referenceBytes,
			EqualsB:   false,
		},
		B: bootstrapCost{
			Known:  false,
			Reason: "no architecture-neutral bootstrap transmission artifact exists yet",
		},
		TotalCComputable: false,
		InterpretationRule: []string{
			"P is exact only for the selected frozen corpus and canonical NEX-1 v0.1 encoding",
			"raw UTF-8 specification bits are a transparent text-size proxy, not an accepted receiver-neutral S",
			"Go reference source size R is a host implementation proxy and MUST NOT be substituted for B",
			"unknown B is not zero; therefore total C remains numerically unresolved",
			"runtime transition counts are feasibility/performance evidence and are not terms in C",
		},
	}

	var output []byte
	if *pretty {
		output, err = json.MarshalIndent(result, "", "  ")
	} else {
		output, err = json.Marshal(result)
	}
	if err != nil {
		fatalf("encode report: %v", err)
	}
	if _, err := os.Stdout.Write(append(output, '\n')); err != nil {
		fatalf("write report: %v", err)
	}
}

func fileBytes(path string) (int, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return 0, err
	}
	return len(data), nil
}

func fatalf(format string, args ...any) {
	fmt.Fprintf(os.Stderr, "nexaccount: "+format+"\n", args...)
	os.Exit(1)
}
