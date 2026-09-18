# Project status

**Date:** 2026-09-19  
**Baseline branch:** `main`  
**Active work:** post-Stage-5 research corrections and literature re-audit  
**Current state:** `Stages 0–5 complete; NEX-1 v0.1 unchanged; research claims corrected/narrowed after re-audit`  
**Living dissertation:** `docs/RESEARCH-DISSERTATION.md` / `docs/RESEARCH-DISSERTATION.ru.md`

## Completed stages

- Stage 0 — project/specification/ADR baseline — Complete.
- Stage 1 — canonical wire format — Complete, PR #3.
- Stage 2 — static validation and rank-1 HM inference — Complete, PR #4.
- Stage 3 — weak call-by-name dynamic semantics — Complete, PR #5.
- Stage 4 — empirical validation and benchmarking — Complete, PR #6.
- Stage 5 — independent reconstruction and receiver-conditioned bootstrap evidence — Complete.

## Post-Stage-5 literature re-audit

The 2026-09-19 audit is recorded in:

- `docs/RESEARCH-AUDIT-2026-09-19.md`;
- `docs/RESEARCH-AUDIT-2026-09-19.ru.md`;
- ADR-0016.

### Overall audit judgment

No reviewed issue invalidates NEX-1 v0.1 wire/static/dynamic semantics or the frozen Stage 4–5 measurements.

The audit did identify corrections to the **research interpretation**:

1. typed combinatory logic is a valid static-typing competitor; the old SKI rationale was too strong;
2. `C=S+B+P` is a conditional transmitted-bit ledger, not an unconditional machine-free information scalar;
3. the historical `A1` receiver prior hid too much computational structure and is refined in `assumptions-v0.2.json`;
4. `942/942` is strong differential-conformance evidence but not a correctness/completeness proof;
5. the 98.90% call-by-need result is a reduction in the project evaluator transition counter, not a wall-clock speedup claim;
6. prior interstellar-language work (Lincos, CosmicOS, Lingua Cosmica) materially narrows the novelty claim;
7. NEX-specific type-safety and call-by-need equivalence theorems remain open.

## Stage 5 independent reconstruction

Accepted frozen result:

```text
cases total           942
portable matches      942
semantic mismatches     0
resource asymmetries    0
```

Post-audit case composition:

```text
17   frozen corpus programs
325  valid cases = 25 parameter sets x 13 fixed AST templates
100  static-error cases = 25 parameter sets x 4 fixed error families
500  randomized term shapes tested at wire level
```

Accepted wording:

> strong differential-conformance evidence of reconstructability on the tested surface.

This is not a formal proof and does not exclude correlated errors shared by both implementations.

## Receiver assumptions

Historical Stage 5 evidence remains in:

```text
stage5/receiver-assumptions/assumptions-v0.1.json
```

The current corrected model is:

```text
stage5/receiver-assumptions/assumptions-v0.2.json
```

with:

```text
A0       exact binary-frame prior
A1       elementary discrete mathematics only
A1(R)    A1 + exact formal rule calculus R
A2(U)    A1 + exact universal binary machine U and framing
A_host(H) non-neutral terrestrial host control
```

Exact accounting is stated as:

```text
C | A = |M_A|
```

with disjoint-role decomposition only when defensible:

```text
C | A = (S | A) + (B | A,S) + (P | A,S,B)
```

or joint specification/bootstrap:

```text
C | A = (SB | A) + (P | A,SB)
```

## Stage 5 bootstrap result

The negative Stage 5.8 conclusion remains accepted:

```text
accepted complete bootstrap candidates  0
full B | A known                        false
full SB | A known                       false
total C | A computable                  false
```

Host control only:

```text
Python NEX package source            28,832 bytes
all frozen author-written files      52,859 bytes
```

These values are not bootstrap cost.

## Stage 4 evidence that remains exact

For frozen corpus v0.3:

```text
programs   17
AST nodes  345
wire bits  1371
```

Constructor attribution remains:

```text
Prim  460 bits
Var   286 bits
App   264 bits
Nat   244 bits
Lam    84 bits
Let    33 bits
```

These are corpus-specific measurements, not language-wide frequency estimates.

The call-by-need experiment remains:

```text
CBN transition counter       226151
call-by-need counter           2484
counter reduction             98.90%
```

The metric is an implementation counter, not a direct CPU-time or bootstrap-size measure.

## Current normative state

NEX-1 v0.1 remains unchanged by Stages 4–5 and by the post-Stage-5 audit. No v0.2 wire redesign, new Core primitives, mutable-memory profile, production frontend, native backend, or self-hosting claim has been introduced.

The project now avoids presenting NEX as proven globally minimal. Public research language should use **compact experimental core** unless a particular minimality claim is explicitly proved under stated conditions.

## Highest-priority next evidence

Before an incompatible NEX-1 redesign, prioritize:

1. NEX-specific preservation/canonical-forms/progress-or-safety metatheory;
2. a formal or mechanized argument that an allowed call-by-need implementation preserves NEX observations;
3. bounded exhaustive testing of small closed well-typed terms across independent implementations;
4. hold-out and externally specified workload families beyond the 17-program design corpus;
5. one real dependency-closed bootstrap artifact under `A1(R)` or `A2(U)`.

Only after those gaps are reduced should the project return to claims about total `C | A`, type-information trade-offs, or incompatible compactness redesigns.
