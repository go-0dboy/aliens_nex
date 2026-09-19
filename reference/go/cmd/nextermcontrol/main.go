package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"

	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

type request struct {
	ID   string `json:"id"`
	Bits string `json:"bits"`
}

type response struct {
	ID        string   `json:"id"`
	Tokens    []string `json:"tokens,omitempty"`
	Reencoded string   `json:"reencoded,omitempty"`
	Error     string   `json:"error,omitempty"`
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
		out.Error = classify(err)
		return out
	}
	term, err := nex.DecodeExact(bits, nex.DecodeLimits{})
	if err != nil {
		out.Error = classify(err)
		return out
	}
	out.Tokens = make([]string, 0)
	appendTokens(&out.Tokens, term)
	reencoded, err := nex.EncodeTerm(term)
	if err != nil {
		out.Error = classify(err)
		return out
	}
	out.Reencoded = reencoded.String()
	return out
}

func appendTokens(dst *[]string, term *nex.Term) {
	*dst = append(*dst, fmt.Sprintf("%d", term.Kind))
	switch term.Kind {
	case nex.KindVar, nex.KindNat, nex.KindPrim:
		*dst = append(*dst, term.Value.String())
	case nex.KindLam:
		appendTokens(dst, term.A)
	case nex.KindApp, nex.KindLet:
		appendTokens(dst, term.A)
		appendTokens(dst, term.B)
	}
}

func classify(err error) string {
	switch {
	case errors.Is(err, nex.ErrTruncated):
		return "truncated"
	case errors.Is(err, nex.ErrTrailingBits):
		return "trailing"
	case errors.Is(err, nex.ErrInvalidBit):
		return "invalid_bit"
	case errors.Is(err, nex.ErrInvalidTerm):
		return "invalid_term"
	default:
		return "other"
	}
}

func fatalf(format string, args ...any) {
	fmt.Fprintf(os.Stderr, "nextermcontrol: "+format+"\n", args...)
	os.Exit(2)
}
