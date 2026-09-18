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

// TermMetrics are portable exact metrics derived from a canonical in-memory term.
type TermMetrics struct {
	WireBits     int               `json:"wire_bits"`
	ASTNodes     int               `json:"ast_nodes"`
	Constructors ConstructorCounts `json:"constructors"`
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
	case KindLam:
		metrics.Constructors.Lam++
		measureTermNodes(term.A, metrics)
	case KindApp:
		metrics.Constructors.App++
		measureTermNodes(term.A, metrics)
		measureTermNodes(term.B, metrics)
	case KindLet:
		metrics.Constructors.Let++
		measureTermNodes(term.A, metrics)
		measureTermNodes(term.B, metrics)
	case KindNat:
		metrics.Constructors.Nat++
	case KindPrim:
		metrics.Constructors.Prim++
	}
}
