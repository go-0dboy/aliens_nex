package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/go-0dboy/aliens_nex/reference/go/bench"
	"github.com/go-0dboy/aliens_nex/reference/go/experiment"
	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

type request struct {
	ID             string   `json:"id"`
	Level          string   `json:"level"`
	Bits           string   `json:"bits"`
	Args           []uint64 `json:"args,omitempty"`
	MaxTransitions uint64   `json:"max_transitions,omitempty"`
	MaxDepth       uint32   `json:"max_depth,omitempty"`
}

type response struct {
	ID          string                      `json:"id"`
	Type        string                      `json:"type,omitempty"`
	StaticError string                      `json:"static_error,omitempty"`
	CBNResult   *bench.Observation          `json:"cbn_result,omitempty"`
	CBNStats    *nex.EvalStats              `json:"cbn_stats,omitempty"`
	CBNError    string                      `json:"cbn_error,omitempty"`
	NeedResult  *experiment.NeedObservation `json:"need_result,omitempty"`
	NeedStats   *experiment.NeedStats       `json:"need_stats,omitempty"`
	NeedError   string                      `json:"need_error,omitempty"`
}

func main() {
	var requests []request
	if err := json.NewDecoder(os.Stdin).Decode(&requests); err != nil {
		fatalf("decode requests: %v", err)
	}

	responses := make([]response, 0, len(requests))
	for _, req := range requests {
		responses = append(responses, probe(req))
	}
	if err := json.NewEncoder(os.Stdout).Encode(responses); err != nil {
		fatalf("encode responses: %v", err)
	}
}

func probe(req request) response {
	out := response{ID: req.ID}
	bits, err := nex.ParseBits(req.Bits)
	if err != nil {
		out.StaticError = fmt.Sprintf("wire: %v", err)
		return out
	}
	term, err := nex.DecodeExact(bits, nex.DecodeLimits{})
	if err != nil {
		out.StaticError = fmt.Sprintf("wire: %v", err)
		return out
	}
	for _, arg := range req.Args {
		term = nex.App(term, nex.Nat(nex.NaturalUint64(arg)))
	}

	scheme, err := nex.InferClosed(term)
	if err != nil {
		out.StaticError = err.Error()
		return out
	}
	typeText, err := nex.CanonicalSchemeString(scheme)
	if err != nil {
		out.StaticError = err.Error()
		return out
	}
	out.Type = typeText
	if req.Level == "static" {
		return out
	}
	if req.Level != "eval" {
		out.StaticError = "unknown request level"
		return out
	}

	limits := nex.DefaultEvalLimits
	if req.MaxTransitions != 0 {
		limits.MaxTransitions = req.MaxTransitions
	}
	if req.MaxDepth != 0 {
		limits.MaxDepth = req.MaxDepth
	}

	cbnValue, cbnStats, err := nex.EvaluateClosedWithStats(term, limits)
	out.CBNStats = &cbnStats
	if err != nil {
		out.CBNError = err.Error()
	} else {
		observed, observeErr := bench.Observe(cbnValue)
		if observeErr != nil {
			out.CBNError = observeErr.Error()
		} else {
			out.CBNResult = &observed
		}
	}

	needObservation, needStats, err := experiment.EvaluateCallByNeed(term, limits)
	out.NeedStats = &needStats
	if err != nil {
		out.NeedError = err.Error()
	} else {
		out.NeedResult = &needObservation
	}
	return out
}

func fatalf(format string, args ...any) {
	fmt.Fprintf(os.Stderr, "nexselfhostprobe: "+format+"\n", args...)
	os.Exit(2)
}
