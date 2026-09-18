package main

import (
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"os"
	"path/filepath"

	"github.com/go-0dboy/aliens_nex/reference/go/bench"
	"github.com/go-0dboy/aliens_nex/reference/go/experiment"
	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

type wireReport struct {
	Bits              int                     `json:"bits"`
	ASTNodes          int                     `json:"ast_nodes"`
	WireByConstructor nex.ConstructorWireBits `json:"wire_bits_by_constructor"`
}

type typeReport struct {
	RootTypeBits    int     `json:"root_type_bits"`
	HybridTotalBits int     `json:"hybrid_total_bits"`
	OverheadPercent float64 `json:"overhead_percent"`
}

type lambdaBaselineReport struct {
	Programs int `json:"programs"`
	NEXBits  int `json:"nex_bits"`
	BLCBits  int `json:"blc_bits"`
	JotBits  int `json:"jot_bracket_sk_bits"`
}

type stackBaselineReport struct {
	NEXBits           int     `json:"nex_bits"`
	TinyStackBits     int     `json:"tiny_stack_bits"`
	StackMinusNEXBits int     `json:"stack_minus_nex_bits"`
	DeltaPercent      float64 `json:"delta_percent"`
}

type baselineReport struct {
	PureLambda lambdaBaselineReport `json:"pure_lambda_subset"`
	FullCorpus stackBaselineReport  `json:"full_corpus_stack"`
}

type strategyReport struct {
	CBNTransitions           uint64  `json:"cbn_transitions"`
	CallByNeedTransitions    uint64  `json:"call_by_need_transitions"`
	TransitionSavings        int64   `json:"transition_savings"`
	TransitionSavingsPercent float64 `json:"transition_savings_percent"`
	CallByNeedMemoHits       uint64  `json:"call_by_need_memo_hits"`
	ProgramsWithWin          int     `json:"programs_with_transition_win"`
}

type accountingReport struct {
	SpecUTF8Bytes         int  `json:"spec_utf8_bytes_proxy"`
	SpecRawUTF8Bits       int  `json:"spec_raw_utf8_bits_proxy"`
	SpecProxyAcceptedAsS  bool `json:"spec_proxy_accepted_as_S"`
	ReferenceGoUTF8Bytes  int  `json:"reference_go_utf8_bytes_proxy"`
	ReferenceProxyEqualsB bool `json:"reference_proxy_equals_B"`
	BootstrapKnown        bool `json:"bootstrap_known"`
	TotalCComputable      bool `json:"total_C_computable"`
}

type report struct {
	Schema        string           `json:"schema"`
	CorpusVersion string           `json:"corpus_version"`
	Programs      int              `json:"programs"`
	Wire          wireReport       `json:"nex_wire"`
	Types         typeReport       `json:"hybrid_root_type"`
	Baselines     baselineReport   `json:"baselines"`
	Strategy      strategyReport   `json:"evaluation_strategy"`
	Accounting    accountingReport `json:"accounting"`
	Limitations   []string         `json:"limitations"`
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

	result := report{
		Schema:        "nex-stage4-experimental-report-v0.1",
		CorpusVersion: corpus.CorpusVersion,
		Programs:      len(corpus.Programs),
		Limitations: []string{
			"corpus-v0.3 is small and does not establish global optimality",
			"BLC/Jot comparison is restricted to the identical pure-lambda subset",
			"Jot uses one deterministic bracket-abstraction translation, not shortest programs",
			"tiny stack reuses NEX integer/primitive conventions and is not an independent bootstrap",
			"call-by-need counters are Go-reference runtime metrics, not Core transmission costs",
			"S and B lack accepted receiver-neutral transmission artifacts, so total C is unresolved",
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
		result.Wire.Bits += metrics.WireBits
		result.Wire.ASTNodes += metrics.ASTNodes
		addConstructorWire(&result.Wire.WireByConstructor, metrics.WireByConstructor)

		scheme, err := nex.InferClosed(term)
		if err != nil {
			fatalf("%s: infer type: %v", program.ID, err)
		}
		typeBits, err := experiment.RootTypeEnvelopeBits(scheme)
		if err != nil {
			fatalf("%s: measure root type: %v", program.ID, err)
		}
		result.Types.RootTypeBits += typeBits

		stackBits, err := experiment.TinyStackBits(term)
		if err != nil {
			fatalf("%s: tiny stack: %v", program.ID, err)
		}
		result.Baselines.FullCorpus.TinyStackBits += stackBits

		blcBits, blcErr := experiment.BLCBits(term)
		if blcErr == nil {
			jotBits, jotErr := experiment.JotBitsBracketSK(term)
			if jotErr != nil {
				fatalf("%s: Jot translation: %v", program.ID, jotErr)
			}
			result.Baselines.PureLambda.Programs++
			result.Baselines.PureLambda.NEXBits += metrics.WireBits
			result.Baselines.PureLambda.BLCBits += blcBits
			result.Baselines.PureLambda.JotBits += jotBits
		} else if !errors.Is(blcErr, experiment.ErrBaselineUnsupported) {
			fatalf("%s: BLC measurement: %v", program.ID, blcErr)
		}

		cbnValue, cbnStats, err := nex.EvaluateClosedWithStats(term, nex.DefaultEvalLimits)
		if err != nil {
			fatalf("%s: call-by-name: %v", program.ID, err)
		}
		cbnObservation, err := bench.Observe(cbnValue)
		if err != nil || cbnObservation != program.Expected {
			fatalf("%s: call-by-name observation mismatch: %v %#v", program.ID, err, cbnObservation)
		}
		needObservation, needStats, err := experiment.EvaluateCallByNeed(term, nex.DefaultEvalLimits)
		if err != nil {
			fatalf("%s: call-by-need: %v", program.ID, err)
		}
		if needObservation.Kind != program.Expected.Kind || needObservation.Value != program.Expected.Value {
			fatalf("%s: call-by-need observation mismatch", program.ID)
		}
		result.Strategy.CBNTransitions += cbnStats.Transitions
		result.Strategy.CallByNeedTransitions += needStats.Transitions
		result.Strategy.CallByNeedMemoHits += needStats.MemoHits
		if needStats.Transitions < cbnStats.Transitions {
			result.Strategy.ProgramsWithWin++
		}
	}

	result.Types.HybridTotalBits = result.Wire.Bits + result.Types.RootTypeBits
	result.Types.OverheadPercent = percent(result.Types.RootTypeBits, result.Wire.Bits)
	result.Baselines.FullCorpus.NEXBits = result.Wire.Bits
	result.Baselines.FullCorpus.StackMinusNEXBits = result.Baselines.FullCorpus.TinyStackBits - result.Wire.Bits
	result.Baselines.FullCorpus.DeltaPercent = percent(result.Baselines.FullCorpus.StackMinusNEXBits, result.Wire.Bits)
	result.Strategy.TransitionSavings = int64(result.Strategy.CBNTransitions) - int64(result.Strategy.CallByNeedTransitions)
	result.Strategy.TransitionSavingsPercent = percent64(result.Strategy.TransitionSavings, result.Strategy.CBNTransitions)

	root, err := filepath.Abs(*repoRoot)
	if err != nil {
		fatalf("resolve repo root: %v", err)
	}
	specBytes, err := fileBytes(filepath.Join(root, "docs/NEX-1-v0.1.md"))
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
	result.Accounting = accountingReport{
		SpecUTF8Bytes:         specBytes,
		SpecRawUTF8Bits:       specBytes * 8,
		SpecProxyAcceptedAsS:  false,
		ReferenceGoUTF8Bytes:  referenceBytes,
		ReferenceProxyEqualsB: false,
		BootstrapKnown:        false,
		TotalCComputable:      false,
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

func addConstructorWire(dst *nex.ConstructorWireBits, src nex.ConstructorWireBits) {
	dst.Var += src.Var
	dst.Lam += src.Lam
	dst.App += src.App
	dst.Let += src.Let
	dst.Nat += src.Nat
	dst.Prim += src.Prim
}

func percent(delta, base int) float64 {
	if base == 0 {
		return 0
	}
	return 100 * float64(delta) / float64(base)
}

func percent64(delta int64, base uint64) float64 {
	if base == 0 {
		return 0
	}
	return 100 * float64(delta) / float64(base)
}

func fileBytes(path string) (int, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return 0, err
	}
	return len(data), nil
}

func fatalf(format string, args ...any) {
	fmt.Fprintf(os.Stderr, "nexreport: "+format+"\n", args...)
	os.Exit(1)
}
