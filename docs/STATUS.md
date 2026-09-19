# Project status

**Date:** 2026-09-19  
**Baseline branch:** `main`  
**Active work:** Post-Stage-5 NEX Core self-sufficiency extension (5.10–5.20)  
**Current state:** `Stages 0–5 complete; 5.10 contract accepted; 5.11 meta-representation candidate committed; Stage 6 remains Planned; NEX-1 v0.1 unchanged`  
**Active decision:** ADR-0018  
**Living dissertation:** `docs/RESEARCH-DISSERTATION.md` / `docs/RESEARCH-DISSERTATION.ru.md`

## Completed stages

- Stage 0 — project/specification/ADR baseline — Complete.
- Stage 1 — canonical wire format — Complete, PR #3.
- Stage 2 — static validation and rank-1 HM inference — Complete, PR #4.
- Stage 3 — weak call-by-name dynamic semantics — Complete, PR #5.
- Stage 4 — empirical validation and benchmarking — Complete, PR #6.
- Stage 5 — independent reconstruction and receiver-conditioned bootstrap evidence — Complete.

Historical Stage 5.0–5.9 remains closed under ADR-0015. The new 5.10–5.20 numbering denotes a **post-Stage-5 extension** and does not rewrite the blind-reconstruction/bootstrap experiment or its negative result.

## Post-Stage-5 research audit

The 2026-09-19 re-audit remains recorded in:

- `docs/RESEARCH-AUDIT-2026-09-19.md`;
- `docs/RESEARCH-AUDIT-2026-09-19.ru.md`;
- `docs/RELATED-WORK.md` / `docs/RELATED-WORK.ru.md`;
- ADR-0016.

No reviewed issue invalidates the NEX-1 v0.1 wire/static/dynamic semantics or frozen Stage 4–5 measurements.

Important corrections remain accepted:

- typed combinatory logic is a legitimate competitor;
- exact total cost is conditional on explicit receiver assumptions and concrete serialization;
- current receiver assumptions use `A1(R)` rather than hiding an executable rule calculus in `A1`;
- `942/942` is strong differential-conformance evidence, not a proof;
- the 98.90% Stage 4 result is an evaluator transition-counter reduction, not wall-clock speedup;
- Lincos, DeVito–Oehrle, Lingua Cosmica, CosmicOS, and exosemiotic work are design inputs for teachability;
- historical novelty is not a project success criterion.

## Stable evidence

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

No new Core constructor, primitive, type former, wire rule, host callback, mutable memory model, or native backend is authorized by the self-sufficiency workstream.

### Stage 4 corpus

```text
programs   17
AST nodes  345
wire bits  1371
```

Constructor attribution remains:

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

Case composition remains:

```text
17   frozen corpus programs
325  valid cases = 25 parameter sets x 13 templates
100  static-error cases = 25 parameter sets x 4 families
500  randomized term shapes tested at wire level
```

Accepted meaning remains strong differential-conformance evidence of reconstructability on the tested surface, not a proof of semantic correctness or specification completeness.

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

The Python/Go host implementations remain engineering controls, not receiver-neutral bootstrap. The post-Stage-5 self-sufficiency experiment does not retroactively change this result.

## Post-Stage-5 Core self-sufficiency extension

ADR-0018 inserts an executable evidence gate before Stage 6 activation:

```text
5.10 contract and gate                 accepted in ADR-0018
5.11 NEX-in-NEX meta-representation   candidate committed / validation in progress
5.12 self wire codec                   planned
5.13 self structural validation        planned
5.14 self HM type inference            planned
5.15 self evaluator                    planned
5.16 integrated NEX-in-NEX toolchain  planned
5.17 self-processing                   planned
5.18 bounded/differential validation   planned
5.19 supporting metatheory             planned
5.20 decision gate                     planned
```

### 5.11 current artifact

The first meta-representation candidate is deliberately austere:

```text
stage5/selfhost/meta-representation-v0.1.json
stage5/selfhost/validate_meta_representation.py
docs/experiments/stage5-selfhost-meta-representation.md
```

Every frozen meta-object uses only NEX mathematical naturals `N` as its physical Core carrier. Finite products and sequences are encoded numerically; no recursive type, list primitive, host AST, host byte array, new Core primitive, or wire change is assumed.

The validator checks Core-dependency closure, tag contracts, bounded pair/sequence injectivity/round trips, and all bit sequences of length 0..5. A local validator execution passed before PR creation; repository CI remains the authoritative branch-level regression gate.

This result is intentionally narrow: it establishes a concrete representation candidate, not a self-hosting claim and not an efficiency claim.

### Required final implementation target

The workstream targets an exact canonical NEX implementation `I` with:

```text
Decode
Encode
Validate
Infer
Evaluate
```

and self-processing checks over `code(I)`.

A native `NEX -> x86/ARM/WASM` compiler is not part of this gate. Such a backend requires a separately declared target/profile.

### Decision outcomes reserved for 5.20

```text
supported
supported_but_impractical
core_limitation_discovered
inconclusive
```

Difficulty during implementation is evidence to record; it does not itself authorize a NEX-1 v0.1 redesign.

## Stage 6 — teaching NEX

ADR-0017 remains Accepted and establishes the teaching/Core boundary:

```text
receiver prior A
    -> NEX Teaching / Bootstrap Message T
    -> reconstructed NEX-1 competence
    -> conformance / self-test
    -> canonical NEX programs P
```

Stage 6 remains **Planned**, not Active, while the 5.10–5.20 gate is unresolved.

### Existing Stage 6 planning artifacts

```text
docs/STAGE-6.md
stage6/curriculum-plan-v0.1.json
stage6/validate_plan.py
docs/adr/0017-separate-teaching-protocol-from-core.md
```

`curriculum-plan-v0.1.json` remains a planning artifact, **not** an accepted teaching message and not a source of `T_bits`.

### Operational competence target retained for Stage 6

When Stage 6 is eventually activated, a receiver experiment is not successful merely because it can execute supplied examples. It must demonstrate:

1. canonical decode;
2. canonical encode;
3. static checking / principal types;
4. evaluation to portable observations;
5. self-test capability;
6. construction of valid NEX programs for held-out tasks.

The final item distinguishes “can run NEX” from “can program in NEX”.

### Initial lesson-order hypothesis retained

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

This remains a Stage 6 hypothesis, not part of NEX-1 semantics.

## Supporting evidence work

The following remain important across the pre-Stage-6 workstream and later Stage 6:

- NEX-specific canonical forms / preservation / progress-or-safety metatheory;
- NEX-specific call-by-need observational-preservation reasoning;
- bounded exhaustive small-term comparison across independent implementations, including function application contexts;
- hold-out and independently specified workloads.

These support confidence in the target Core but do not replace either the self-sufficiency gate or the later teaching experiment.

## Research synthesis status

ADR-0018 is a research-significant decision. Both living dissertation versions must incorporate the pre-Stage-6 self-sufficiency question in this workstream and must be current before the gate is closed. Historical Stage 5 evidence and the post-Stage-5 literature audit remain unchanged.

## Next recommended step

Finish branch-level validation and freeze the 5.11 N-only meta-representation, then implement the derived natural-number/sequence foundation and canonical NEX wire codec for 5.12 without adding Core features.
