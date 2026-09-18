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
- shared `reference/go/bench` loading/parsing for frozen corpora so later experiments consume the same canonical Terms;
- `reference/go/cmd/nexbench` for inherited frozen corpora and deterministic machine-readable reports;
- `reference/go/verify.sh` clean-checkout reproduction of accepted measurements plus all existing tests/fuzz checks.

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

### Stage 4.3 — internal NEX design experiments — Complete first controlled set

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

### Stage 4.4 — erased HM versus hybrid root type information — First experiment complete

`docs/experiments/stage4-type-information.md` defines an explicitly non-normative hybrid envelope. It leaves the canonical NEX-1 v0.1 term unchanged and appends/transmits only the inferred closed principal top-level `TypeScheme` using an experimental compact prefix code.

This experiment measures only transmitted-program delta `Delta_P`. It does **not** claim that a root type replaces internal HM inference or that bootstrap cost `B` is reduced.

Clean-checkout CI `35370010741` measured the frozen v0.3 corpus:

```text
erased NEX term bits        1371
root principal-type bits     134
hybrid total bits           1505
Delta_P                      134 bits
aggregate overhead           9.77%
```

The overhead is highly workload-dependent:

```text
identity      5 + 12 type bits  = +240%
constant      9 + 20 type bits  = +222.2%
composition  23 + 46 type bits  = +200%
```

Most benchmark programs whose inferred top-level type is simply `N` require only a 4-bit experimental root-type payload, so their relative overhead falls as the term grows (for example `factorial-4`: 239 + 4 bits, about +1.67%).

Measured conclusion: transmitting this particular root principal-type envelope costs +9.77% over erased terms on v0.3. Unmeasured question: whether any explicit/hybrid verification design can save enough real bootstrap information to compensate for that program overhead. A distinct checker/verification design is required before making that claim.

### Stage 4.5 — external / structural baselines — Complete first reproducible set

`docs/experiments/stage4-baselines.md` defines the comparison rules before interpreting results.

BLC and Jot are compared only on the identical pure-lambda subset (`identity`, `constant`, `composition`), so the comparison does not silently charge BLC/Jot for Church encodings of NEX `Nat`/`Prim`. Jot uses one deterministic standard bracket-abstraction path (`lambda -> SK -> Barker Jot`) and is **not** a shortest-program claim. The tiny stack baseline is project-defined, reuses NEX `U(n)` and primitive IDs, and therefore measures a structural encoding alternative rather than an independent bootstrap.

Clean-checkout CI `35372182772` generated:

```text
Pure lambda subset, 3 programs
NEX                         37 bits
BLC                         30 bits
Jot via fixed SK translation 288 bits
```

Per-program pure-lambda values:

```text
identity      NEX 5   BLC 4   Jot 20
constant      NEX 9   BLC 7   Jot 41
composition   NEX 23  BLC 19  Jot 227
```

Measured conclusion: BLC is 7 bits smaller than NEX on this narrow identical pure-lambda subset. The Jot figure demonstrates the cost of the chosen deterministic bracket-abstraction translation only; it is not evidence about optimal Jot encodings.

For the full frozen v0.3 corpus:

```text
NEX canonical wire     1371 bits
tiny postfix stack     1529 bits
delta                   +158 bits
delta percent           +11.52%
```

Measured conclusion: this particular 3-bit postfix structural baseline is larger than NEX on v0.3. Because it reuses NEX integer and primitive conventions, this does not establish a total-information-cost advantage over an independently bootstrapped stack machine.

## Remaining Stage 4 work

Still pending:

- 4.6 call-by-name versus call-by-need comparison;
- 4.7 bootstrap accounting model;
- 4.8 generated final experimental report;
- 4.9 evidence-based decision gate.

## Remaining project-wide unverified claims

Still intentionally unverified:

- formal/exhaustive proof of decoder, type-inference, or evaluator correctness;
- conformance agreement with a second independent implementation;
- bootstrap/self-hosting feasibility and size;
- total-information-cost comparison against external baselines or a real explicit-type checker/bootstrap;
- whether the v0.3 constructor distribution generalizes to other program populations;
- practical CBN-versus-call-by-need cost on the accepted corpus;
- any claim that NEX is globally optimal or the smallest possible language.

## Next recommended step

Proceed to Stage 4.6 without changing normative NEX-1 v0.1 semantics. Implement an explicitly experimental call-by-need evaluator with sharing/memoization, require observable agreement with the reference call-by-name evaluator on the accepted corpus, and compare transitions / repeated thunk forcing as reference-only implementation metrics.
