# Project status

**Date:** 2026-09-19  
**Baseline branch:** `main`  
**Active work:** Stage 6 teaching/bootstrap protocol planning  
**Current state:** `Stages 0–5 complete; Stage 6 protocol checkpoint in preparation; NEX-1 v0.1 unchanged`  
**Living dissertation:** `docs/RESEARCH-DISSERTATION.md` / `docs/RESEARCH-DISSERTATION.ru.md`

## Completed stages

- Stage 0 — project/specification/ADR baseline — Complete.
- Stage 1 — canonical wire format — Complete, PR #3.
- Stage 2 — static validation and rank-1 HM inference — Complete, PR #4.
- Stage 3 — weak call-by-name dynamic semantics — Complete, PR #5.
- Stage 4 — empirical validation and benchmarking — Complete, PR #6.
- Stage 5 — independent reconstruction and receiver-conditioned bootstrap evidence — Complete.

## Post-Stage-5 research audit

The 2026-09-19 re-audit is recorded in:

- `docs/RESEARCH-AUDIT-2026-09-19.md`;
- `docs/RESEARCH-AUDIT-2026-09-19.ru.md`;
- `docs/RELATED-WORK.md` / `docs/RELATED-WORK.ru.md`;
- ADR-0016.

No reviewed issue invalidates the NEX-1 v0.1 wire/static/dynamic semantics or frozen Stage 4–5 measurements.

Important corrections now accepted:

- typed combinatory logic is a legitimate competitor;
- exact total cost is conditional on explicit receiver assumptions and concrete serialization;
- current receiver assumptions use `A1(R)` rather than hiding an executable rule calculus in `A1`;
- `942/942` is strong differential-conformance evidence, not a proof;
- the 98.90% Stage 4 result is an evaluator transition-counter reduction, not wall-clock speedup;
- Lincos, DeVito–Oehrle, Lingua Cosmica, CosmicOS, and exosemiotic work are design inputs for teachability;
- historical novelty is not a project success criterion.

## Stable evidence entering Stage 6

### NEX-1 Core

The normative v0.1 object remains unchanged:

```text
Var Lam App Let Nat Prim
zero-based de Bruijn binding
rank-1 HM Let polymorphism
Core primitives 0..10
weak call-by-name semantics
canonical binary wire
```

### Stage 4 corpus

```text
programs   17
AST nodes  345
wire bits  1371
```

Constructor attribution:

```text
Prim  460
Var   286
App   264
Nat   244
Lam    84
Let    33
```

### Stage 5 independent reconstruction

```text
cases total           942
portable matches      942
semantic mismatches     0
resource asymmetries    0
```

Case composition:

```text
17   frozen corpus programs
325  valid cases = 25 parameter sets x 13 templates
100  static-error cases = 25 parameter sets x 4 families
500  randomized term shapes tested at wire level
```

### Receiver assumptions

Historical Stage 5 evidence remains frozen in `assumptions-v0.1.json`. Current research uses `assumptions-v0.2.json`:

```text
A0        exact binary-frame prior
A1        elementary discrete mathematics only
A1(R)     A1 + exact formal rule calculus R
A2(U)     A1 + exact universal binary machine U and framing
A_host(H) non-neutral terrestrial host control
```

These are experimental conditions, not claims about actual extraterrestrial cognition.

### Bootstrap status

```text
accepted complete bootstrap candidates  0
full B | A known                        false
full SB | A known                       false
total C | A computable                  false
```

The Python/Go host implementations remain engineering controls, not receiver-neutral bootstrap.

## Stage 6 — teaching NEX

ADR-0017 establishes the new architectural boundary:

```text
receiver prior A
    -> NEX Teaching / Bootstrap Message T
    -> reconstructed NEX-1 competence
    -> conformance / self-test
    -> canonical NEX programs P
```

Canonical NEX remains the final target. The teaching representation may be redundant, staged, or pedagogical, but every transmitted convention must be defined and counted unless it is part of the declared prior.

### Stage 6 planning artifacts

```text
docs/STAGE-6.md
stage6/curriculum-plan-v0.1.json
stage6/validate_plan.py
docs/adr/0017-separate-teaching-protocol-from-core.md
```

`curriculum-plan-v0.1.json` is explicitly a planning artifact, **not** an accepted teaching message and not a source of `T_bits`.

### Operational competence target

A receiver experiment is not successful merely because it can execute supplied examples. It must demonstrate:

1. canonical decode;
2. canonical encode;
3. static checking / principal types;
4. evaluation to portable observations;
5. self-test capability;
6. construction of valid NEX programs for held-out tasks.

The final item distinguishes “can run NEX” from “can program in NEX”.

### Initial lesson-order hypothesis

```text
binary/framing
 -> naturals/sequences
 -> self-delimiting integers
 -> structure/trees
 -> primitive equations
 -> application/functions
 -> binding/de Bruijn
 -> products/sums
 -> recursion
 -> types/judgments
 -> principal-type examples
 -> canonical NEX wire
 -> self-tests
 -> held-out construction
```

This sequence is a hypothesis to test, not part of NEX-1 semantics.

## Supporting evidence work during Stage 6

In parallel with the teaching experiment, strengthen:

- NEX-specific canonical forms / preservation / progress-or-safety metatheory;
- NEX-specific call-by-need observational-preservation reasoning;
- bounded exhaustive small-term comparison across independent implementations, including function application contexts;
- hold-out and independently specified workloads.

These workstreams support confidence in the target Core but do not replace the Stage 6 teaching objective.

## Scope guard

Stage 6 does not authorize an incompatible NEX-1 redesign. No new Core constructors, primitive IDs, wire format, mutable memory model, native backend, product frontend, or self-hosting claim enters the stage without a separate evidence-backed ADR/new Core version.

A Core redesign may be discussed only if Stage 6 evidence shows that the stable target itself prevents a defensible teaching/bootstrap construction, rather than merely showing that a particular curriculum is poor.
