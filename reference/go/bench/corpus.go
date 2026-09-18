package bench

import (
	"encoding/json"
	"fmt"
	"math/big"
	"os"
	"path/filepath"

	"github.com/go-0dboy/aliens_nex/reference/go/nex"
)

type JSONTerm struct {
	Kind  string    `json:"kind"`
	Value string    `json:"value,omitempty"`
	A     *JSONTerm `json:"a,omitempty"`
	B     *JSONTerm `json:"b,omitempty"`
}

type Observation struct {
	Kind  string `json:"kind"`
	Value string `json:"value,omitempty"`
}

type Program struct {
	ID             string      `json:"id"`
	Description    string      `json:"description"`
	Classification string      `json:"classification"`
	Term           JSONTerm    `json:"term"`
	Expected       Observation `json:"expected"`
}

type Corpus struct {
	Schema        string    `json:"schema"`
	CorpusVersion string    `json:"corpus_version"`
	Status        string    `json:"status"`
	Extends       string    `json:"extends,omitempty"`
	Programs      []Program `json:"programs"`
}

func LoadCorpus(path string) (Corpus, error) {
	corpus, err := loadCorpusSeen(path, make(map[string]bool))
	if err != nil {
		return Corpus{}, err
	}
	if len(corpus.Programs) == 0 {
		return Corpus{}, fmt.Errorf("corpus has no programs")
	}
	seenIDs := make(map[string]bool, len(corpus.Programs))
	for _, program := range corpus.Programs {
		if program.ID == "" {
			return Corpus{}, fmt.Errorf("corpus contains empty program id")
		}
		if seenIDs[program.ID] {
			return Corpus{}, fmt.Errorf("duplicate program id %q", program.ID)
		}
		seenIDs[program.ID] = true
	}
	return corpus, nil
}

func loadCorpusSeen(path string, seen map[string]bool) (Corpus, error) {
	absolute, err := filepath.Abs(path)
	if err != nil {
		return Corpus{}, err
	}
	if seen[absolute] {
		return Corpus{}, fmt.Errorf("corpus inheritance cycle at %s", path)
	}
	seen[absolute] = true
	defer delete(seen, absolute)

	data, err := os.ReadFile(path)
	if err != nil {
		return Corpus{}, err
	}
	var corpus Corpus
	if err := json.Unmarshal(data, &corpus); err != nil {
		return Corpus{}, err
	}
	switch corpus.Schema {
	case "nex-benchmark-corpus-v0.1", "nex-benchmark-corpus-v0.2":
	default:
		return Corpus{}, fmt.Errorf("unsupported corpus schema %q", corpus.Schema)
	}
	if corpus.Extends == "" {
		return corpus, nil
	}

	basePath := corpus.Extends
	if !filepath.IsAbs(basePath) {
		basePath = filepath.Join(filepath.Dir(path), basePath)
	}
	base, err := loadCorpusSeen(basePath, seen)
	if err != nil {
		return Corpus{}, fmt.Errorf("load base corpus %q: %w", corpus.Extends, err)
	}
	corpus.Programs = append(base.Programs, corpus.Programs...)
	return corpus, nil
}

func TermFromJSON(j *JSONTerm) (*nex.Term, error) {
	if j == nil {
		return nil, fmt.Errorf("missing term")
	}
	switch j.Kind {
	case "Var":
		value, err := natural(j.Value)
		if err != nil {
			return nil, err
		}
		return nex.Var(value), nil
	case "Lam":
		body, err := TermFromJSON(j.A)
		if err != nil {
			return nil, err
		}
		return nex.Lam(body), nil
	case "App":
		fn, err := TermFromJSON(j.A)
		if err != nil {
			return nil, err
		}
		arg, err := TermFromJSON(j.B)
		if err != nil {
			return nil, err
		}
		return nex.App(fn, arg), nil
	case "Let":
		value, err := TermFromJSON(j.A)
		if err != nil {
			return nil, err
		}
		body, err := TermFromJSON(j.B)
		if err != nil {
			return nil, err
		}
		return nex.Let(value, body), nil
	case "Nat":
		value, err := natural(j.Value)
		if err != nil {
			return nil, err
		}
		return nex.Nat(value), nil
	case "Prim":
		value, err := natural(j.Value)
		if err != nil {
			return nil, err
		}
		return nex.Prim(value), nil
	default:
		return nil, fmt.Errorf("unknown term kind %q", j.Kind)
	}
}

func Observe(value *nex.Value) (Observation, error) {
	if value == nil {
		return Observation{}, fmt.Errorf("nil runtime value")
	}
	switch value.Kind {
	case nex.ValueNat:
		if value.Nat == nil {
			return Observation{}, fmt.Errorf("Nat missing payload")
		}
		return Observation{Kind: "Nat", Value: value.Nat.String()}, nil
	case nex.ValueClosure, nex.ValuePrimitive:
		return Observation{Kind: "Function"}, nil
	case nex.ValueUnit:
		return Observation{Kind: "Unit"}, nil
	case nex.ValuePair:
		return Observation{Kind: "Pair"}, nil
	case nex.ValueInl:
		return Observation{Kind: "Inl"}, nil
	case nex.ValueInr:
		return Observation{Kind: "Inr"}, nil
	default:
		return Observation{}, fmt.Errorf("unknown value kind %d", value.Kind)
	}
}

func natural(s string) (*big.Int, error) {
	if s == "" {
		return nil, fmt.Errorf("missing natural value")
	}
	value, ok := new(big.Int).SetString(s, 10)
	if !ok || value.Sign() < 0 {
		return nil, fmt.Errorf("invalid natural %q", s)
	}
	return value, nil
}
