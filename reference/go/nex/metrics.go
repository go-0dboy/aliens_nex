package nex

// ConstructorCounts records exact AST constructor occurrences.
type ConstructorCounts struct {
	Var  int `json:"var"`
	Lam  int `json:"lam"`
	App  int `json:"app"`
	Let  int `json:"let"`
	Nat  int `json:"nat"`
	Prim int `json:"prim"`
}

// ConstructorWireBits attributes each canonical wire bit to the constructor
// whose local prefix/payload encoding emitted it. Child encodings are accounted
// for by their own constructors, so the fields sum exactly to TermMetrics.WireBits.
type ConstructorWireBits struct {
	Var  int `json:"var"`
	Lam  int `json:"lam"`
	App  int `json:"app"`
	Let  int `json:"let"`
	Nat  int `json:"nat"`
	Prim int `json:"prim"`
}

// TermMetrics are portable exact metrics derived from a canonical in-memory term.
type TermMetrics struct {
	WireBits          int                 `json:"wire_bits"`
	ASTNodes          int                 `json:"ast_nodes"`
	Constructors      ConstructorCounts   `json:"constructors"`
	WireByConstructor ConstructorWireBits `json:"wire_bits_by_constructor"`
}

// MeasureTerm derives exact wire and AST metrics without evaluating the term.
func MeasureTerm(term *Term) (TermMetrics, error) {
	bits, err := EncodeTerm(term)
	if err != nil {
		return TermMetrics{}, err
	}
	metrics := TermMetrics{WireBits: len(bits)}
	measureTermNodes(term, &metrics)
	return metrics, nil
}

func measureTermNodes(term *Term, metrics *TermMetrics) {
	metrics.ASTNodes++
	switch term.Kind {
	case KindVar:
		metrics.Constructors.Var++
		encoded, _ := EncodeU(term.Value)
		metrics.WireByConstructor.Var += 2 + len(encoded)
	case KindLam:
		metrics.Constructors.Lam++
		metrics.WireByConstructor.Lam += 2
		measureTermNodes(term.A, metrics)
	case KindApp:
		metrics.Constructors.App++
		metrics.WireByConstructor.App += 2
		measureTermNodes(term.A, metrics)
		measureTermNodes(term.B, metrics)
	case KindLet:
		metrics.Constructors.Let++
		metrics.WireByConstructor.Let += 3
		measureTermNodes(term.A, metrics)
		measureTermNodes(term.B, metrics)
	case KindNat:
		metrics.Constructors.Nat++
		encoded, _ := EncodeU(term.Value)
		metrics.WireByConstructor.Nat += 4 + len(encoded)
	case KindPrim:
		metrics.Constructors.Prim++
		encoded, _ := EncodeU(term.Value)
		metrics.WireByConstructor.Prim += 4 + len(encoded)
	}
}
