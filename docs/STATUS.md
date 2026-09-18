# Project status

**Date:** 2026-09-19  
**Baseline branch:** `main`  
**Active work:** post-Stage-5 research corrections and preparation for Stage 6  
**Current state:** `Stages 0–5 complete; NEX-1 v0.1 unchanged; next stage targets teachability/bootstrap`  
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
- ADR-0016;
- `docs/RELATED-WORK.md` / `docs/RELATED-WORK.ru.md`.

### Overall audit judgment

No reviewed issue invalidates NEX-1 v0.1 wire/static/dynamic semantics or the frozen Stage 4–5 measurements.

The audit corrected the research interpretation:

1. typed combinatory logic is a valid static-typing competitor; the old SKI rationale was too strong and remains preserved only in the frozen historical ADR-0002 snapshot;
2. `C=S+B+P` is a conditional transmitted-bit ledger, not an unconditional machine-free information scalar;
3. the historical `A1` receiver prior hid too much computational structure and is refined in `assumptions-v0.2.json`;
4. `942/942` is strong differential-conformance evidence but not a correctness/completeness proof;
5. the 98.90% call-by-need result is a reduction in the project evaluator transition counter, not a wall-clock speedup claim;
6. Lincos, DeVito–Oehrle, Lingua Cosmica, CosmicOS, and exosemiotic work are now used as design evidence for how an unknown receiver may be taught;
7. NEX-specific type-safety and call-by-need equivalence theorems remain open.

Historical novelty is **not** a success criterion. The project succeeds if it can construct and validate a finite formal teaching/transmission system for an unknown receiver.

## Stage 5 independent reconstruction

Accepted frozen result:

```text
cases total           942
portable matches      942
semantic mismatches     0
resource asymmetries    0
```

Case composition:

```text
17   frozen corpus programs
325  valid cases = 25 parameter sets x 13 fixed AST templates
100  static-error cases = 25 parameter sets x 4 fixed error families
500  randomized term shapes tested at wire level
```

Accepted wording:

> strong differential-conformance evidence of reconstructability on the tested surface.

This is not a formal proof and does not exclude correlated errors shared by both implementations. The top-level `Function` observation is also intentionally coarse; future exhaustive work should exercise functions through application contexts.

## Receiver assumptions

Historical Stage 5 evidence remains frozen in:

```text
stage5/receiver-assumptions/assumptions-v0.1.json
```

The current corrected model is:

```text
stage5/receiver-assumptions/assumptions-v0.2.json
```

with:

```text
A0        exact binary-frame prior
A1        elementary discrete mathematics only
A1(R)     A1 + exact formal rule calculus R
A2(U)     A1 + exact universal binary machine U and framing
A_host(H) non-neutral terrestrial host control
```

These are experimental assumptions, not claims about actual extraterrestrial cognition.

Exact accounting is:

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

These values are not receiver-neutral bootstrap cost.

## Stage 4 evidence that remains exact

For frozen corpus v0.3:

```text
programs   17
AST nodes  345
wire bits  1371
```

Constructor attribution:

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

The stable Core is now explicitly separated conceptually from the next teaching layer:

```text
receiver prior A
    -> NEX teaching/bootstrap message T
    -> reconstructed NEX-1 competence
    -> conformance/self-test
    -> canonical NEX program transmission P
```

A pedagogical representation may be redundant and may differ from the canonical wire. The Core MUST NOT be redesigned merely because its canonical representation is not the easiest first lesson.

## Next stage: Stage 6 — teaching NEX

Stage 6 should answer:

> What finite transmitted teaching/bootstrap sequence is sufficient to take a receiver from an explicit prior profile to demonstrable ability to decode, type-check, execute, and construct NEX programs?

Primary workstreams:

1. define the teaching/bootstrap layer and its exact boundary from the stable Core;
2. design a progressive lesson sequence informed by Lincos and CosmicOS;
3. define an operational competence criterion and transmitted self-tests;
4. require held-out program-construction tasks, not only interpretation of examples;
5. build a finite machine-readable teaching artifact and measure its exact transmitted bits;
6. record every additional receiver assumption discovered during construction.

Supporting evidence work should continue in parallel:

- NEX-specific preservation/canonical-forms/progress-or-safety metatheory;
- a formal or mechanized call-by-need observational-preservation argument;
- bounded exhaustive testing of small closed well-typed terms, including function application contexts;
- hold-out and independently specified workload families.

An incompatible Core redesign remains out of scope unless Stage 6 evidence directly demonstrates that the stable Core prevents a defensible teaching/bootstrap construction.
