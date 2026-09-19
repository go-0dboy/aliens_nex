# Project status

**Date:** 2026-09-19  
**Baseline branch:** `main`  
**Active work:** Post-Stage-5 NEX Core self-sufficiency extension (5.10–5.20)  
**Current state:** `Stages 0–5 complete; 5.10 contract accepted; 5.11 meta-representation active; Stage 6 remains Planned; NEX-1 v0.1 unchanged`  
**Active decision:** ADR-0018  
**Living dissertation:** `docs/RESEARCH-DISSERTATION.md` / `docs/RESEARCH-DISSERTATION.ru.md`

## Completed stages

- Stage 0 — project/specification/ADR baseline — Complete.
- Stage 1 — canonical wire format — Complete, PR #3.
- Stage 2 — static validation and rank-1 HM inference — Complete, PR #4.
- Stage 3 — weak call-by-name dynamic semantics — Complete, PR #5.
- Stage 4 — empirical validation and benchmarking — Complete, PR #6.
- Stage 5 — independent reconstruction and receiver-conditioned bootstrap evidence — Complete.

Historical Stage 5.0–5.9 remains closed under ADR-0015. The new 5.10–5.20 numbering denotes a **post-Stage-5 extension** and does not rewrite the blind-reconstruction/bootstrap experiment.

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

### Stage 5 independent reconstruction

```text
cases total           942
portable matches      942
semantic mismatches     0
resource asymmetries    0
```

Accepted meaning remains strong differential-conformance evidence of reconstructability on the tested surface, not a proof.

### Receiver assumptions / bootstrap status

Current receiver taxonomy remains:

```text
A0        exact binary-frame prior
A1        elementary discrete mathematics only
A1(R)     A1 + exact formal rule calculus R
A2(U)     A1 + exact universal binary machine U and framing
A_host(H) non-neutral terrestrial host control
```

Historical negative bootstrap result remains:

```text
accepted complete bootstrap candidates  0
full B | A known                        false
full SB | A known                       false
total C | A computable                  false
```

The post-Stage-5 self-sufficiency experiment does not retroactively change those results.

## Post-Stage-5 Core self-sufficiency extension

ADR-0018 adds a pre-Stage-6 evidence gate:

```text
5.10 contract and gate                 accepted
5.11 NEX-in-NEX meta-representation   active
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

The target is an exact canonical NEX implementation `I` capable of implementing its own portable wire/static/dynamic semantics and processing `code(I)` without hidden host-language operations.

A native `NEX -> x86/ARM/WASM` compiler is not part of this gate. Such a backend requires a separately declared target/profile.

### Decision outcomes reserved for 5.20

```text
supported
supported_but_impractical
core_limitation_discovered
inconclusive
```

Difficulty during implementation is recorded as evidence; it does not by itself authorize a NEX-1 v0.1 redesign.

## Stage 6 status

Stage 6 remains **Planned**. ADR-0017 and the existing planning artifacts remain valid:

```text
docs/STAGE-6.md
stage6/curriculum-plan-v0.1.json
stage6/validate_plan.py
docs/adr/0017-separate-teaching-protocol-from-core.md
```

The teaching/bootstrap architecture remains:

```text
receiver prior A
    -> NEX Teaching / Bootstrap Message T
    -> reconstructed NEX-1 competence
    -> conformance / self-test
    -> canonical NEX programs P
```

Stage 6 is not activated while the 5.10–5.20 gate is unresolved.

## Research synthesis status

ADR-0018 is a research-significant project decision. The living dissertation pair must incorporate this pre-Stage-6 self-sufficiency question within the same workstream and must be current before 5.20 closeout. Historical Stage 5 evidence and the post-Stage-5 literature audit remain unchanged.

## Next recommended step

Complete and validate the versioned 5.11 meta-representation contract using only existing NEX-1 v0.1 values, then use that frozen representation as the input contract for the 5.12 self wire codec.
