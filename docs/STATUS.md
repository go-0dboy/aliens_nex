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

The project explicitly separates:

```text
P  exact transmitted-program cost
R  host/reference implementation proxy
B  actual bootstrap transmission cost (currently unknown)
S  specification transmission cost (not yet one accepted scalar)
```

`R` MUST NOT be substituted for `B`. Benchmark encodings are classified as `direct`, `canonical-translation`, or `hand-optimized`.

### Stage 4.1 — benchmark corpora — Extended corpus frozen

`benchmarks/corpus-v0.1.json` is the immutable 10-program foundation corpus.

An attempted extended `corpus-v0.2.json` is intentionally preserved because it exposed a real reference-runtime cost: `factorial-5` exceeded the default non-memoizing call-by-name budget of 1,000,000 transitions. This is an implementation resource refusal, not a Core validity failure or proof of divergence.

`benchmarks/corpus-v0.3.json` is the accepted extended corpus for Stage 4.3. It inherits v0.1 unchanged and adds seven workloads, for 17 programs total:

```text
right sum/case path
let-polymorphic reuse
small recognizer
recursive multiplication
factorial-4
fibonacci-5
repeated expensive let binding
```

Corpus lineage and the preserved v0.2 result are documented in `benchmarks/README.md`.

Clean-checkout CI `35368707827` successfully parsed, type-checked, evaluated, and measured all accepted v0.3 programs.

### Stage 4.2 — NEX metrics/instrumentation — Complete foundation

Implemented:

- `nex.MeasureTerm` for exact wire-bit, AST-node, constructor-count, and per-constructor wire-bit attribution;
- `EvaluateClosedWithStats` for explicitly reference-only evaluator transition/depth counters;
- `reference/go/cmd/nexbench` for inherited frozen corpora and deterministic machine-readable reports;
- `reference/go/verify.sh` clean-checkout reproduction of v0.1/v0.3 measurement plus all existing tests/fuzz checks.

Portable exact fields include:

```text
wire_bits
ast_nodes
Var/Lam/App/Let/Nat/Prim counts
wire_bits_by_constructor
observable result
```

Reference-only fields include:

```text
evaluation transitions
max evaluation depth
```

### Stage 4.3 — internal NEX design experiments — First controlled experiments complete

`reference/go/cmd/nexexperiment` measures unchanged NEX-1 v0.1 encodings; it does not modify normative semantics.

#### Extended-corpus wire profile

Clean-checkout CI `35369320807` measured v0.3 as:

```text
programs   17
wire_bits  1371
ast_nodes  345
```

Exact wire-bit attribution:

```text
Prim  460 bits  33.6%
Var   286 bits  20.9%
App   264 bits  19.3%
Nat   244 bits  17.8%
Lam    84 bits   6.1%
Let    33 bits   2.4%
```

Therefore the early hypothesis that `App` would dominate transmitted bits is not supported by this corpus. Primitive references are the largest measured contributor in v0.3. This is a corpus result, not a universal claim.

#### Let versus duplication

For a 5-bit closed payload:

```text
2 repeats: Let costs 4 bits more
3 repeats: Let costs 2 bits more
4 repeats: exact tie
8 repeats: Let saves 8 bits
```

For the 14-bit one-`succ` payload, two repeats already make `Let` save 5 bits, and savings increase with payload size/repetition count.

Conclusion: `Let` has a measurable break-even point; it is not intrinsically always smaller or always larger.

#### Direct Nat versus succ-chain construction

For `Nat(0)`, direct literal and zero-step construction tie at 5 bits. For every tested value `1..255`, the direct literal is smaller. Representative endpoint:

```text
Nat(255)          21 bits
succ-chain(255) 2300 bits
saved            2279 bits
```

This strongly supports direct canonical natural literals for the tested construction baseline, while not yet comparing against alternative numeric coding schemes.

Clean-checkout CI `35369168189` verified the internal experiment generator and all prior tests/fuzz properties. CI `35369320807` additionally exposed the full v0.3 aggregate report.

## Remaining Stage 4 work

Still pending:

- 4.4 erased-HM versus explicit/hybrid type-information experiment;
- 4.5 reproducible BLC / SKI-Jot / tiny typed stack baselines;
- 4.6 call-by-name versus call-by-need comparison;
- 4.7 bootstrap accounting model;
- 4.8 generated final experimental report;
- 4.9 evidence-based decision gate.

## Remaining project-wide unverified claims

Still intentionally unverified:

- formal/exhaustive proof of decoder, type-inference, or evaluator correctness;
- conformance agreement with a second independent implementation;
- bootstrap/self-hosting feasibility and size;
- total-information-cost comparison against external baselines or an explicit-type NEX variant;
- whether the v0.3 constructor distribution generalizes to other program populations;
- practical CBN-versus-call-by-need cost on the accepted corpus;
- any claim that NEX is globally optimal or the smallest possible language.

## Next recommended step

Proceed to Stage 4.4 without changing NEX-1 v0.1. Define one or more explicitly experimental type-information envelopes, measure their transmitted-program overhead against erased HM on the frozen v0.3 corpus, and keep any checker/bootstrap simplification as a separately labelled hypothesis until an actual alternative checker exists.
