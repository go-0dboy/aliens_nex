package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"math/big"
	"os"

	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

type request struct {
	ID   string `json:"id"`
	Op   string `json:"op"`
	N    string `json:"n,omitempty"`
	Bits string `json:"bits,omitempty"`
}

type response struct {
	ID       string `json:"id"`
	Bits     string `json:"bits,omitempty"`
	N        string `json:"n,omitempty"`
	RestBits string `json:"rest_bits,omitempty"`
	Error    string `json:"error,omitempty"`
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
	switch req.Op {
	case "encode":
		n := new(big.Int)
		if _, ok := n.SetString(req.N, 10); !ok || n.Sign() < 0 {
			out.Error = "invalid_n"
			return out
		}
		bits, err := nex.EncodeU(n)
		if err != nil {
			out.Error = classify(err)
			return out
		}
		out.Bits = bits.String()
		return out

	case "decode":
		bits, err := nex.ParseBits(req.Bits)
		if err != nil {
			out.Error = classify(err)
			return out
		}
		n, next, err := nex.DecodeU(bits, 0, nex.DecodeLimits{})
		if err != nil {
			out.Error = classify(err)
			return out
		}
		out.N = n.String()
		out.RestBits = bits[next:].String()
		return out

	default:
		out.Error = "unknown_op"
		return out
	}
}

func classify(err error) string {
	switch {
	case errors.Is(err, nex.ErrTruncated):
		return "truncated"
	case errors.Is(err, nex.ErrInvalidBit):
		return "invalid_bit"
	case errors.Is(err, nex.ErrNegativeNatural):
		return "negative_natural"
	default:
		var limit *nex.ResourceLimitError
		if errors.As(err, &limit) {
			return "resource_limit"
		}
		return "other"
	}
}

func fatalf(format string, args ...any) {
	fmt.Fprintf(os.Stderr, "nexuprobe: "+format+"\n", args...)
	os.Exit(2)
}
