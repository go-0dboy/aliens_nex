# Stage 5.1 conformance-packet completeness audit

**Packet:** `nex1-independent-conformance-packet-v0.1`  
**Frozen NEX source commit:** `4f9c50aed13cdbdf72c9ce6510521477d49c05a5`  
**Audit status:** sufficient to begin an isolated independent implementation after the packet-local observation conventions below are included.

## Method

The audit asks whether an implementer restricted to the frozen packet can reconstruct the portable behavior required by Stage 5 without consulting `reference/go`.

The audit distinguishes:

- **normative semantics** — must come from `docs/NEX-1-v0.1.md` and normative decisions;
- **conformance examples** — machine-readable expected cases;
- **observation formatting** — packet-level representation needed to compare otherwise equivalent host implementations;
- **implementation freedom** — must remain unspecified.

## Coverage matrix

| Area | Packet source | Audit result |
|---|---|---|
| `U(n)` definition | NEX spec §15 + wire vectors | covered |
| six-term AST | NEX spec §4 | covered |
| de Bruijn scope | NEX spec §§5, 14 + static vectors | covered |
| `Let` non-recursive scope | spec §§5, 8 + static vector | covered |
| wire prefixes | NEX spec §16 + wire vectors | covered |
| byte packing / exact bit length | NEX spec §17 | covered |
| arbitrary-precision naturals | NEX spec §§3, 9 | covered |
| primitive IDs / arities / schemes | NEX spec §10 | covered |
| primitive operational semantics | NEX spec §11 | covered |
| weak call-by-name | NEX spec §12 | covered |
| selective forcing | NEX spec §12.2 + eval vectors | covered |
| WHNF classes | NEX spec §12.1 + eval vectors | covered |
| resource refusal vs validity | NEX spec §§12.3, 14 + ADR-0006/0009 | covered |
| HM rank-1 typing | NEX spec §13 + static vectors | covered at semantic-result level |
| occurs check | NEX spec §13.6 + vector | covered |
| primitive validity / profiles | NEX spec §§10, 13.5, 24 | covered for Core-without-profile packet |
| evaluation conformance | eval vectors | covered |

## Finding F1 — principal type text was not fully specified

### Observation

The language specification defines principal type schemes semantically, while `static-v0.1.json` compares text such as:

```text
forall T0 T1. (T0 -> (T1 -> T0))
```

The specification does not make internal fresh-variable numbering observable and does not fully define the conformance text-normalization algorithm.

### Classification

`conformance observation-format omission`, not a Core typing ambiguity.

### Resolution

`OBSERVATIONS.md` defines packet-only alpha-normalization and fully parenthesized rendering. The rule compares principal schemes modulo internal IDs and does not prescribe a type-inference implementation.

### NEX version impact

No NEX-1 v0.1 semantic/wire change.

## Finding F2 — conformance JSON AST shape needed an explicit packet contract

### Observation

The NEX specification defines the abstract `Term` grammar but does not make JSON a Core transport. The conformance files use JSON objects with `kind`, `value`, `a`, and `b` fields.

### Classification

`test-fixture representation omission`, not a Core wire ambiguity.

### Resolution

`OBSERVATIONS.md` explicitly defines the packet JSON mapping solely for reading test fixtures. It is not a NEX wire encoding and does not become normative language syntax.

### NEX version impact

No NEX-1 v0.1 semantic/wire change.

## Finding F3 — Algorithm W implementation details remain intentionally free

### Observation

The spec states the HM rules, generalization/instantiation behavior, unification, and occurs check but does not prescribe substitution-map layout, fresh-ID allocation order, or a literal implementation of Milner's Algorithm W pseudocode.

### Classification

`deliberately unspecified implementation behavior`.

### Resolution

No repair. The independent implementation is required to reproduce normalized principal schemes and error classes, not Go's internal substitutions or fresh IDs.

## Finding F4 — evaluator representation remains intentionally free

### Observation

The spec permits environments, closures, explicit substitution, graph reduction, or call-by-need provided portable behavior agrees with normative weak CBN. ADR-0008 would expose the Go architecture.

### Classification

`deliberately unspecified implementation behavior`.

### Resolution

ADR-0008 is excluded from the packet. The first independent evaluator must choose its own host representation.

## Finding F5 — error precedence outside supplied cases is not yet a portable requirement

### Observation

The packet defines portable error classes for supplied invalid examples, but does not define a total precedence relation for a hypothetical term containing multiple independent static defects.

### Classification

`currently unspecified outside conformance scope`.

### Resolution

Do not invent a global error-precedence rule for Stage 5.2–5.4. Conformance requires the specified class for packet vectors. If differential/generated testing later reveals a practical ambiguity, classify it in Stage 5.6 and add the smallest language-neutral vector if a portable rule is needed.

## Independence conclusion

After adding `OBSERVATIONS.md`, no known missing semantic rule blocks the first independent implementation of:

```text
wire codec
closed-scope validation
HM principal typing
Core primitive validity
normative weak-CBN evaluation
portable conformance observations
```

This conclusion is intentionally provisional. The strongest test of packet completeness is the independent implementation itself. Any place where that implementer must ask "what does Go do?" is evidence of a packet/specification gap and must be recorded rather than answered from the reference code.

## Starting recommendation

Stage 5.0 and Stage 5.1 may proceed to their CI/PR checkpoint. Stage 5.2 implementation should start only in a fresh isolated implementation context as required by ADR-0013.
