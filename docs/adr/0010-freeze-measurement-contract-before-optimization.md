# ADR-0010: Freeze the measurement contract and benchmark corpus before optimization

**Status:** Accepted  
**Date:** 2026-09-18

## Context

NEX is motivated by total information cost rather than by language aesthetics alone:

```text
C = specification + bootstrap + transmitted programs
```

After Stages 1–3, NEX-1 v0.1 can be encoded, statically validated, and evaluated, but the project has not yet measured whether the selected design is competitive for its stated objective.

Benchmark-driven language changes create a serious risk of post-hoc corpus selection, metric mixing, and confusing host implementation details with portable Core properties.

## Decision drivers

- experiments must be reproducible;
- negative results must remain visible;
- program-bit measurements must remain architecture-neutral;
- host implementation metrics must not masquerade as Core semantics;
- the benchmark corpus must not be rewritten after seeing comparison results;
- total bootstrap cost is not currently directly known.

## Decision

Stage 4 will freeze the measurement contract before optimization experiments.

Metrics are split into at least:

1. portable exact NEX metrics such as canonical wire bits and AST structure;
2. reference-only implementation metrics such as evaluator transitions/depth;
3. bootstrap/specification quantities or proxies, each explicitly labelled.

A corpus version becomes immutable once comparative or optimization results are published from it. Semantically changed tasks require a new corpus version.

Reference implementation size `R` is an engineering proxy and MUST NOT be reported as actual bootstrap transmission cost `B`.

Benchmark encodings must state whether they are direct, canonical translations, or hand-optimized. The same distinction applies to external baselines where possible.

NEX-1 v0.1 semantics and wire format remain frozen during measurement. Experimental variants are isolated and labelled rather than silently becoming normative.

## Accepted consequences

- some Stage 4 reports will contain `unknown` rather than a fabricated total-cost scalar;
- corpus versioning adds process overhead;
- benchmark results remain comparable over time;
- unfavorable NEX results are preserved rather than optimized away by changing the tests;
- future v0.2 proposals can be justified against stable evidence.

## Alternatives considered

### Optimize first, benchmark later

Rejected because it allows the benchmark suite to encode the optimization target after the fact.

### Use Go source/binary size as bootstrap cost

Rejected as an exact interpretation. Go source, toolchain, runtime, and host assumptions do not model the information that an unknown receiver must bootstrap.

### Report only total `C`

Rejected until specification and bootstrap terms have defensible representations in compatible units.

### Use only execution speed

Rejected because execution speed is not the primary NEX objective and is strongly host-dependent.

## Evidence / references

This ADR is primarily a project experimental-method decision. Existing baseline sources in `docs/SOURCES.md` remain applicable. New external benchmark/encoding methods must be registered before they materially affect comparisons.

## Follow-up validation

Stage 4 must demonstrate that:

- the corpus is machine-readable and versioned;
- exact wire metrics are reproduced from canonical terms;
- generated reports distinguish portable and reference-only measurements;
- experimental variants do not mutate normative v0.1 semantics;
- changes to a published corpus version are prevented by repository review/tests or equivalent checks.
