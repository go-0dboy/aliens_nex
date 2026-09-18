package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"

	"github.com/go-0dboy/aliens_nex/reference/go/bench"
	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

type request struct {
	ID    string          `json:"id"`
	Level string          `json:"level"`
	Term  *bench.JSONTerm `json:"term,omitempty"`
	Bits  *string         `json:"bits,omitempty"`
}

type response struct {
	ID          string             `json:"id"`
	WireBits    string             `json:"wire_bits,omitempty"`
	WireError   string             `json:"wire_error,omitempty"`
	Type        string             `json:"type,omitempty"`
	StaticError string             `json:"static_error,omitempty"`
	Result      *bench.Observation `json:"result,omitempty"`
	EvalError   string             `json:"eval_error,omitempty"`
}

func main() {
	var requests []request
	if err := json.NewDecoder(os.Stdin).Decode(&requests); err != nil {
		fail(fmt.Errorf("decode requests: %w", err))
	}

	responses := make([]response, 0, len(requests))
	for _, req := range requests {
		responses = append(responses, probe(req))
	}
	enc := json.NewEncoder(os.Stdout)
	enc.SetEscapeHTML(false)
	if err := enc.Encode(responses); err != nil {
		fail(fmt.Errorf("encode responses: %w", err))
	}
}

func probe(req request) response {
	out := response{ID: req.ID}
	term, err := requestTerm(req)
	if err != nil {
		out.WireError = classifyWire(err)
		return out
	}

	bits, err := nex.EncodeTerm(term)
	if err != nil {
		out.WireError = classifyWire(err)
		return out
	}
	out.WireBits = bits.String()
	if req.Level == "wire" {
		return out
	}

	scheme, err := nex.InferClosed(term)
	if err != nil {
		out.StaticError = classifyStatic(err)
		return out
	}
	typeText, err := nex.CanonicalSchemeString(scheme)
	if err != nil {
		out.StaticError = "other"
		return out
	}
	out.Type = typeText
	if req.Level == "static" {
		return out
	}

	value, err := nex.EvaluateClosed(term, nex.DefaultEvalLimits)
	if err != nil {
		out.EvalError = classifyEval(err)
		return out
	}
	observed, err := bench.Observe(value)
	if err != nil {
		out.EvalError = "other"
		return out
	}
	out.Result = &observed
	return out
}

func requestTerm(req request) (*nex.Term, error) {
	if req.Bits != nil {
		bits, err := nex.ParseBits(*req.Bits)
		if err != nil {
			return nil, err
		}
		return nex.DecodeExact(bits, nex.DecodeLimits{})
	}
	if req.Term == nil {
		return nil, fmt.Errorf("request %q has neither term nor bits", req.ID)
	}
	return bench.TermFromJSON(req.Term)
}

func classifyWire(err error) string {
	var limit *nex.ResourceLimitError
	switch {
	case errors.Is(err, nex.ErrTruncated):
		return "truncated"
	case errors.Is(err, nex.ErrTrailingBits):
		return "trailing"
	case errors.Is(err, nex.ErrInvalidBit):
		return "invalid_bit"
	case errors.As(err, &limit):
		return "resource_limit"
	default:
		return "other"
	}
}

func classifyStatic(err error) string {
	switch {
	case errors.Is(err, nex.ErrOutOfScope):
		return "out_of_scope"
	case errors.Is(err, nex.ErrUnknownPrimitive):
		return "unknown_primitive"
	case errors.Is(err, nex.ErrTypeMismatch):
		return "type_mismatch"
	case errors.Is(err, nex.ErrOccursCheck):
		return "occurs_check"
	default:
		return "other"
	}
}

func classifyEval(err error) string {
	if errors.Is(err, nex.ErrEvalResourceLimit) {
		return "resource_limit"
	}
	return classifyStatic(err)
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, err)
	os.Exit(2)
}
