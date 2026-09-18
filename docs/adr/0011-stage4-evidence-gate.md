# ADR-0011 — Hold NEX-1 v0.1 stable after the Stage 4 evidence gate

**Status:** Accepted  
**Date:** 2026-09-18

## Context

Stages 1–3 made NEX-1 v0.1 executable and testable. Stage 4 then measured the existing design before changing it.

The goal of this ADR is not to declare NEX globally optimal. It records which design questions now have enough project evidence for a local decision, which should remain unchanged in v0.1, and which remain open because the total-information objective

```text
C = S + B + P
```

still contains unmeasured terms.

All numeric evidence below is scoped to the frozen Stage 4 corpora and documented experimental encodings. It is not a theorem about all program populations.

## Evidence summary

### Canonical program profile

Frozen `corpus-v0.3` contains 17 programs and measures:

```text
1371 canonical NEX wire bits
345 AST nodes
```

Bit attribution is:

```text
Prim  460 bits  33.6%
Var   286 bits  20.9%
App   264 bits  19.3%
Nat   244 bits  17.8%
Lam    84 bits   6.1%
Let    33 bits   2.4%
```

Therefore the earlier possibility that `App` would dominate this corpus was not observed. Primitive references are the largest measured contributor.

### `Let`

`Let` has a measurable break-even point rather than being uniformly smaller or larger.

For the tested 5-bit payload it loses at 2–3 repetitions, ties at 4, and saves bits at 8. For the tested 14-bit payload it already saves bits at 2 repetitions.

### Direct `Nat`

Against the tested repeated-`succ` construction baseline, direct `Nat(n)` is smaller for every tested positive value through 255. At 255:

```text
Nat(255)          21 bits
succ-chain(255) 2300 bits
```

This does not compare all possible numeric representations, but it strongly supports retaining direct natural literals against that baseline.

### Erased HM versus root type transmission

The experimental hybrid root-principal-type envelope adds:

```text
134 bits over 1371 term bits
+9.77% program payload
```

No corresponding receiver-neutral reduction in specification/bootstrap cost has been implemented or measured. A root principal type alone does not replace internal typing judgments or Algorithm W.

### External / structural baselines

On the identical three-program pure-lambda subset:

```text
NEX  37 bits
BLC  30 bits
```

Thus NEX is not smaller than BLC on that subset.

The deterministic bracket-abstraction-to-Jot path measured 288 bits, but this is not a shortest-Jot result.

On all 17 v0.3 programs, the project-defined 3-bit postfix structural baseline measured:

```text
NEX         1371 bits
tiny stack  1529 bits
```

Because this stack baseline reuses NEX integer and primitive conventions, it is not an independent total-information comparison.

### Evaluation strategy

The experimental call-by-need evaluator produced the same observable WHNF as normative call-by-name for all 17 accepted programs.

Reference-only aggregate transition counts were:

```text
CBN        226151
CBNeed       2484
reduction   98.90%
```

Only 6 of 17 programs reduced transition count, but several recursive workloads improved dramatically. This is performance/feasibility evidence only; sharing may increase bootstrap complexity and does not reduce program payload.

### Total-information accounting

For v0.3:

```text
P exact program payload = 1371 bits
```

Transparent proxies measured in clean checkout are:

```text
canonical specification Markdown  23440 UTF-8 bytes
selected Go reference Core        43013 UTF-8 bytes
```

Neither is accepted as a receiver-neutral `S` or `B`. No architecture-neutral bootstrap transmission artifact exists, so:

```text
B is unknown
total C is not numerically computable
```

## Decision

### 1. Keep NEX-1 v0.1 wire and Core semantics stable

Stage 4 does not justify an incompatible v0.1 change. Any later wire/Core change requires a new version and a separate ADR.

### 2. Keep direct `Nat`

Retain direct natural literals in NEX-1 v0.1. The tested computational construction alternative is decisively larger across the measured range.

This does not close future research into other compact integer codes or shared constant tables.

### 3. Keep `Let`

Retain `Let` as a Core constructor. It has demonstrated wire-size break-even behavior and also carries the accepted HM let-polymorphism role.

Do not claim that every local use of `Let` is size-optimal; encoders/frontends may later choose duplication when it is smaller if semantics permit.

### 4. Keep erased HM typing in NEX-1 v0.1

Do not add normative transmitted type annotations to v0.1.

The measured root-type envelope increases `P`, while a compensating reduction in `S+B` remains unmeasured. Explicit/hybrid verification remains a valid future experiment once a real alternative checker/bootstrap exists.

### 5. Keep weak call-by-name as normative semantics; retain call-by-need as an allowed optimization

Do not redefine NEX semantics around memoization.

The call-by-need experiment strongly supports sharing as an implementation optimization for heavier workloads when it preserves observable Core results. Future implementations may use it under the existing equivalence requirement.

### 6. Prioritize primitive-reference encoding as a future compactness question

Do not immediately change primitive IDs/prefixes. However, `Prim` is the largest measured v0.3 wire contributor, so future v0.2 design experiments should investigate primitive/profile coding before assuming `App` is the main optimization target.

Any candidate must be remeasured against a frozen corpus and must include its specification/bootstrap consequences.

### 7. Do not claim NEX is globally smallest or better than BLC

BLC is smaller on the measured identical pure-lambda subset. The external comparisons are intentionally incomplete outside their shared domains.

Project claims must remain conditional on workload, translation, and accounting assumptions.

### 8. Keep total-information superiority unresolved until `B` is real

The project MUST NOT substitute Go source size, compiled binary size, Markdown size, runtime transition counts, or any other convenient proxy for actual bootstrap transmission cost.

A future total-cost claim requires at least one explicit architecture-neutral bootstrap artifact or another defensible receiver-neutral representation of `S+B`.

## Consequences

- NEX-1 v0.1 remains the stable experimental baseline after Stage 4.
- Stage 4 measurements become evidence for future variants, not permission to mutate old corpus/spec results.
- A call-by-need implementation is worth pursuing as an optimization path, but it does not alter the language definition.
- Primitive-reference coding becomes a high-priority future compactness hypothesis.
- Explicit/hybrid typing remains deferred pending actual bootstrap/checker evidence.
- The project explicitly accepts that its central total-information comparison is still unresolved.

## Rejected conclusions

Stage 4 does **not** establish any of the following:

```text
NEX is globally minimal
NEX beats BLC overall
call-by-need has a smaller bootstrap
Go source size equals alien bootstrap size
Markdown byte size equals specification transmission cost
root type transmission replaces HM inference
this 17-program corpus represents all software
```

## Follow-up validation

Before a later Core revision, the project should prioritize:

1. an independent conformance implementation;
2. a receiver-neutral bootstrap representation/experiment so `B` becomes measurable rather than symbolic;
3. broader corpus families before treating constructor distribution as general;
4. controlled primitive-reference/profile encoding variants;
5. only then a renewed `C = S + B + P` comparison across NEX and external alternatives.

## Evidence

Project-generated evidence is reproduced by:

```sh
cd reference/go
sh verify.sh
```

and consolidated by:

```sh
go run ./cmd/nexreport \
  -corpus ../../benchmarks/corpus-v0.3.json \
  -repo-root ../.. \
  -pretty=false
```

External theoretical/baseline sources remain registered in `docs/SOURCES.md`, including BLC, Hindley–Milner, call-by-name/lazy evaluation, and Jot sources used by the corresponding experiments.
