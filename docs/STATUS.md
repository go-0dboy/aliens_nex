# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Current stage:** `Stage 4 — Empirical validation and benchmarking — In progress`  
**Stage 0 completed by:** PR `#1 docs: establish ADRs and project workflow`  
**Research source registry completed by:** PR `#2 docs: add research source registry`  
**Stage 1 completed by:** PR `#3 stage1: implement NEX wire foundation`  
**Stage 1 merge commit:** `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`  
**Stage 2 completed by:** PR `#4 stage2: complete static validation and principal type inference`  
**Stage 2 merge commit:** `cefe889d90a275897de31aa23c4b9742a388ec8f`  
**Stage 3 completed by:** PR `#5 stage3: complete dynamic semantics and reference evaluator`  
**Stage 3 merge commit:** `166cdc03282ea500263fdca7185f006f9b17a702`  
**Active Stage 4 branch:** `stage4/empirical-validation`  
**Active Stage 4 pull request:** `#6 stage4: establish empirical measurement foundation`

## Stages 0–3 — Complete

Stage 0 established the specification/process baseline. Stage 1 implemented canonical wire encode/decode. Stage 2 implemented closed-scope/static validation and principal HM type inference. Stage 3 implemented the complete weak-call-by-name v0.1 Core evaluator, synchronized EN/RU dynamic semantics, language-neutral evaluation conformance, resource separation, fuzz/property verification, and clean-checkout CI.

Detailed completion records remain in `docs/STAGE-1.md`, `docs/STAGE-2.md`, and `docs/STAGE-3.md`.

## Stage 4 — Empirical validation and benchmarking — In progress

Stage 4 is defined in `docs/STAGE-4.md`.

Accepted work order:

```text
4.0 measurement contract
4.1 frozen canonical benchmark corpus
4.2 NEX metrics/instrumentation
4.3 internal NEX design experiments
4.4 erased-HM versus explicit/hybrid type-information experiment
4.5 external baselines
4.6 call-by-name versus call-by-need experiment
4.7 bootstrap accounting model
4.8 reproducible experimental report
4.9 evidence-based decision gate
```

ADR-0010 requires the measurement contract and corpus to be fixed before optimization comparisons. Portable exact metrics, reference-only runtime metrics, and bootstrap/specification proxies remain separately labelled.

### Stage 4.0 — measurement contract — Complete

The project now explicitly separates:

```text
P  exact transmitted-program cost
R  host/reference implementation proxy
B  actual bootstrap transmission cost (currently unknown)
S  specification transmission cost (not yet one accepted scalar)
```

`R` MUST NOT be substituted for `B`. Benchmark encodings are classified as `direct`, `canonical-translation`, or `hand-optimized`, and corpus versions become immutable after publication of comparative/optimization results.

### Stage 4.1 — benchmark corpus — Foundation frozen

`benchmarks/corpus-v0.1.json` is the first frozen foundation corpus. It contains 10 direct NEX programs covering:

```text
identity
constant function
composition
succ / ifz
let binding
pair projection
sum/case
terminating fix recursion
recursive addition
```

Every record contains the canonical `Term` and expected observable WHNF. The corpus is consumed directly by the benchmark tool; results are not copied manually into tests.

An extended corpus version is still required before Stage 4.3 design experiments. Existing v0.1 records MUST NOT be edited in place to accommodate later benchmark results.

### Stage 4.2 — NEX metrics/instrumentation — Foundation implemented

Implemented:

- `nex.MeasureTerm` for exact wire-bit, AST-node, and constructor-count measurements;
- `EvaluateClosedWithStats` for explicitly reference-only evaluator transition/depth counters;
- `reference/go/cmd/nexbench` to parse the frozen corpus, measure terms, evaluate them, validate expected results, aggregate metrics, and emit deterministic machine-readable JSON;
- clean-checkout verification of the corpus/tool from `reference/go/verify.sh`.

Portable exact report fields:

```text
wire_bits
ast_nodes
Var/Lam/App/Let/Nat/Prim counts
observable result
```

Reference-only report fields:

```text
evaluation transitions
max evaluation depth
```

The first CI attempt (`35367316312`) failed only because the new CLI had not been gofmt-formatted. After formatting, clean-checkout CI `35367555762` completed successfully, including parsing, type-checking, evaluating, and measuring all 10 corpus programs.

## Remaining Stage 4 work

Still pending:

- freeze an extended corpus before Stage 4.3 comparisons;
- internal NEX encoding experiments;
- erased-HM versus explicit/hybrid type-information experiment;
- reproducible BLC / SKI-Jot / tiny typed stack baselines;
- call-by-name versus call-by-need comparison;
- bootstrap accounting model;
- generated final experimental report;
- evidence-based decision gate.

## Remaining project-wide unverified claims

Still intentionally unverified:

- formal/exhaustive proof of decoder, type-inference, or evaluator correctness;
- conformance agreement with a second independent implementation;
- bootstrap/self-hosting feasibility and size;
- total-information-cost comparison against BLC, SKI/Jot, a typed stack machine, or an explicit-type NEX variant;
- practical cost of call-by-name versus call-by-need for representative NEX programs;
- any claim that NEX is globally optimal or the smallest possible language.

## Next recommended step

Complete Stage 4.1 before any design optimization: create and freeze the extended corpus version with larger representative programs, then use the already verified `nexbench` path as the single source for Stage 4.3 measurements. Do not change NEX-1 v0.1 semantics or wire encoding in response to early benchmark numbers.
