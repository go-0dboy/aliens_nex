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
	ID                       string  `json:"id"`
	CBNTransitions           uint64  `json:"cbn_transitions"`
	NeedTransitions          uint64  `json:"call_by_need_transitions"`
	TransitionSavings        int64   `json:"transition_savings"`
	TransitionSavingsPercent float64 `json:"transition_savings_percent"`
	CBNMaxDepth              uint32  `json:"cbn_max_depth"`
	NeedMaxDepth             uint32  `json:"call_by_need_max_depth"`
	NeedThunkForces          uint64  `json:"call_by_need_thunk_forces"`
	NeedThunkEvaluations     uint64  `json:"call_by_need_thunk_evaluations"`
	NeedMemoHits             uint64  `json:"call_by_need_memo_hits"`
}

type aggregateReport struct {
	Programs                  int     `json:"programs"`
	CBNTransitions            uint64  `json:"cbn_transitions"`
	NeedTransitions           uint64  `json:"call_by_need_transitions"`
	TransitionSavings         int64   `json:"transition_savings"`
	TransitionSavingsPercent  float64 `json:"transition_savings_percent"`
	NeedThunkForces           uint64  `json:"call_by_need_thunk_forces"`
	NeedThunkEvaluations      uint64  `json:"call_by_need_thunk_evaluations"`
	NeedMemoHits              uint64  `json:"call_by_need_memo_hits"`
	ProgramsWithTransitionWin int     `json:"programs_with_transition_win"`
}

type report struct {
	Schema        string          `json:"schema"`
	CorpusVersion string          `json:"corpus_version"`
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
		Schema:        "nex-evaluation-strategy-experiment-v0.1",
		CorpusVersion: corpus.CorpusVersion,
		Notes: []string{
			"call-by-name is the normative NEX-1 v0.1 reference evaluator; call-by-need is experimental",
			"every accepted program must have the same observable WHNF under both evaluators",
			"transition/depth/memoization counters are Go-reference implementation metrics, not portable Core costs",
		},
	}

	for _, program := range corpus.Programs {
		term, err := bench.TermFromJSON(&program.Term)
		if err != nil {
			fatalf("%s: parse term: %v", program.ID, err)
		}

		cbnValue, cbnStats, err := nex.EvaluateClosedWithStats(term, nex.DefaultEvalLimits)
		if err != nil {
			fatalf("%s: call-by-name: %v", program.ID, err)
		}
		cbnObservation, err := bench.Observe(cbnValue)
		if err != nil {
			fatalf("%s: observe call-by-name: %v", program.ID, err)
		}
		if cbnObservation != program.Expected {
			fatalf("%s: call-by-name observation %#v != expected %#v", program.ID, cbnObservation, program.Expected)
		}

		needObservation, needStats, err := experiment.EvaluateCallByNeed(term, nex.DefaultEvalLimits)
		if err != nil {
			fatalf("%s: call-by-need: %v", program.ID, err)
		}
		if needObservation.Kind != program.Expected.Kind || needObservation.Value != program.Expected.Value {
			fatalf("%s: call-by-need observation %#v != expected %#v", program.ID, needObservation, program.Expected)
		}

		savings := int64(cbnStats.Transitions) - int64(needStats.Transitions)
		savingsPercent := 0.0
		if cbnStats.Transitions != 0 {
			savingsPercent = 100 * float64(savings) / float64(cbnStats.Transitions)
		}
		entry := programReport{
			ID:                       program.ID,
			CBNTransitions:           cbnStats.Transitions,
			NeedTransitions:          needStats.Transitions,
			TransitionSavings:        savings,
			TransitionSavingsPercent: savingsPercent,
			CBNMaxDepth:              cbnStats.MaxDepth,
			NeedMaxDepth:             needStats.MaxDepth,
			NeedThunkForces:          needStats.ThunkForces,
			NeedThunkEvaluations:     needStats.ThunkEvaluations,
			NeedMemoHits:             needStats.MemoHits,
		}
		result.Programs = append(result.Programs, entry)
		result.Aggregate.Programs++
		result.Aggregate.CBNTransitions += cbnStats.Transitions
		result.Aggregate.NeedTransitions += needStats.Transitions
		result.Aggregate.NeedThunkForces += needStats.ThunkForces
		result.Aggregate.NeedThunkEvaluations += needStats.ThunkEvaluations
		result.Aggregate.NeedMemoHits += needStats.MemoHits
		if savings > 0 {
			result.Aggregate.ProgramsWithTransitionWin++
		}
	}

	result.Aggregate.TransitionSavings = int64(result.Aggregate.CBNTransitions) - int64(result.Aggregate.NeedTransitions)
	if result.Aggregate.CBNTransitions != 0 {
		result.Aggregate.TransitionSavingsPercent = 100 * float64(result.Aggregate.TransitionSavings) / float64(result.Aggregate.CBNTransitions)
	}

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
	fmt.Fprintf(os.Stderr, "nexstrategy: "+format+"\n", args...)
	os.Exit(1)
}
