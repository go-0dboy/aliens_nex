# Stage 4 — Empirical validation and benchmarking

**Status:** Implementation complete; pending merge review  
**Branch:** `stage4/empirical-validation`

Stage 4 starts only after NEX-1 v0.1 has executable wire decoding, static validation, and dynamic semantics. Its purpose is not to add language features. Its purpose is to measure the current design, make the main compactness claims falsifiable, and create evidence for future Core revisions.

The project objective remains:

```text
C = specification + bootstrap + transmitted programs
```

Stage 4 MUST NOT pretend that all three terms are already directly measurable in the same unit. It must separate exact measurements from proxies and unknowns.

## Stage 4.0 — measurement contract

Before optimization or comparison, fix what is measured and what each number means.

### Portable exact metrics

These are properties of a NEX term/wire payload and can be reproduced by independent implementations:

```text
wire_bits
ast_nodes
Var_count
Lam_count
App_count
Let_count
Nat_count
Prim_count
observable_result
```

Where applicable, the benchmark record may also include the inferred principal type as a validation artifact, but internal type-variable IDs are not portable.

### Reference-implementation metrics

These are useful engineering measurements but are not Core observables:

```text
reference_evaluation_transitions
reference_max_evaluation_depth
future: thunk evaluations / allocations / closures / primitive applications
```

They MUST be labelled as reference-only and MUST NOT be used as architecture-neutral performance claims.

### Cost-accounting categories

Stage 4 distinguishes:

```text
P = exact transmitted-program cost
R = reference implementation size/complexity proxy
B = bootstrap transmission cost, currently unknown
S = specification transmission cost, currently not reduced to one accepted scalar
C = S + B + P
```

`R` MUST NOT be silently substituted for `B`. Go source size, binary size, runtime size, or compiler size may be reported as engineering proxies but do not equal the alien bootstrap cost.

### Corpus freeze rule

A benchmark corpus version is immutable after comparative/optimization results are published from it.

If tasks are added, removed, or semantically changed, create a new corpus version. Do not edit an old corpus to make a design look better.

Every benchmark program MUST declare whether it is:

- `direct` — a direct NEX construction of the benchmark meaning;
- `canonical-translation` — produced by a documented translation;
- `hand-optimized` — manually optimized for a representation.

External baselines MUST be labelled by the same distinction where possible.

## Stage 4.1 — canonical benchmark corpus

Create a language-neutral corpus before changing NEX for benchmark results.

The first frozen foundation corpus should cover at least:

```text
identity
constant function
function composition
basic natural arithmetic/control
let reuse
pair construction/projection
sum construction/case
terminating recursion
```

An extended corpus MUST be frozen before Stage 4.3 design experiments and should add representative larger workloads such as addition, multiplication, factorial/Fibonacci, structural traversal, and a small recognizer/interpreter task where expressible without changing Core.

Each record includes:

```text
id
description
classification
Term
expected observable WHNF
```

The term, not prose, is the benchmark source of truth.

## Stage 4.2 — NEX metrics and instrumentation

Build a deterministic tool that consumes the corpus and emits a machine-readable report.

For every benchmark it MUST compute exact wire size and AST structure from the existing reference encoder. For terminating benchmarks it SHOULD also run the Stage 3 evaluator and report labelled reference-only runtime counters.

No metric may be manually copied into the canonical report.

## Stage 4.3 — internal NEX design experiments

Measure current NEX against controlled variants without changing NEX-1 v0.1 first.

Priority questions include:

- when does `Let` pay for its extra wire prefix versus duplicated subterms?;
- when is direct `Nat(n)` cheaper than constructing the value computationally?;
- which constructors dominate transmitted bits across the corpus?;
- how much of the corpus cost comes from application structure?;
- whether obvious local encodings materially change total program cost.

Any proposed v0.2 change must be evaluated against the frozen corpus and recorded separately from v0.1 results.

## Stage 4.4 — erased HM types versus explicit/hybrid type information

ADR-0007 deliberately deferred the global optimality claim for erased annotations.

Build an experimental alternative that can estimate:

```text
NEX-HM:      smaller program payload + larger inference bootstrap
NEX-explicit: larger program payload + potentially smaller checker bootstrap
```

This experiment MUST NOT silently change the normative v0.1 wire format.

Report transmitted-program deltas exactly. Bootstrap deltas may initially require clearly labelled proxies until a real bootstrap representation exists.

## Stage 4.5 — external baselines

Compare against a small set of architecturally different baselines rather than broad general-purpose languages.

Initial baseline families:

```text
Binary Lambda Calculus
SKI/Jot-style combinators
a deliberately tiny typed stack machine
```

Comparison rules:

- use documented translations where possible;
- do not compare a hand-optimized NEX term against an unoptimized baseline without saying so;
- record all baseline assumptions needed to decode/type/evaluate the program;
- keep program bits separate from decoder/interpreter/bootstrap assumptions;
- register new external sources in `docs/SOURCES.md` before relying on them.

## Stage 4.6 — call-by-name versus call-by-need experiment

The Stage 3 reference evaluator remains non-memoizing call-by-name.

Build an experimental memoizing evaluator only as a comparison implementation. It MUST consume the same terms and pass the same language-neutral evaluation conformance corpus.

Compare reference-only quantities such as:

```text
transitions
repeated thunk evaluations
allocations / retained thunks where measurable
```

Do not change the normative observable semantics based only on implementation speed.

## Stage 4.7 — bootstrap accounting model

Define what would count as bootstrap information in the actual NEX communication problem.

Keep at least three distinct quantities:

```text
P exact wire program bits
R host reference implementation proxy
B actual bootstrap transmission cost (unknown until a bootstrap representation is defined)
```

Stage 4 may introduce multiple explicit bootstrap proxies, but MUST NOT collapse them into a false exact `B`.

## Stage 4.8 — reproducible experimental report

Generate a report from repository data and tools, not hand-entered tables.

The report should include:

```text
corpus identity/version
per-program exact wire metrics
aggregate constructor distribution
reference evaluator metrics
internal design experiment deltas
HM versus explicit-type deltas
external baseline program-cost comparisons
CBN versus call-by-need measurements
known unknowns and proxy definitions
```

Every reported number must be traceable to a command, input artifact, or explicitly labelled external measurement.

The implemented consolidated report is generated by `reference/go/cmd/nexreport` and is executed by `reference/go/verify.sh` in clean-checkout CI.

## Stage 4.9 — decision gate

Stage 4 does not automatically lead to a larger language.

Use the measured evidence to record decisions such as:

```text
keep
change in a future Core version
defer pending bootstrap evidence
reject
```

Potential findings such as expensive `App`, costly `Let`, a smaller stack-machine baseline, or a large HM bootstrap are valid experimental outcomes, not project failures.

Any incompatible change to NEX-1 v0.1 requires a new Core version and an ADR.

The completed evidence gate is recorded in ADR-0011. It keeps NEX-1 v0.1 stable, retains direct `Nat`, `Let`, erased HM, and normative weak call-by-name, treats call-by-need as a supported optimization experiment, prioritizes primitive-reference encoding for future compactness research, and leaves total `C` unresolved until a real receiver-neutral bootstrap cost exists.

## Scope guard

Stage 4 MUST NOT add merely because it would make benchmarks easier:

- new NEX-1 v0.1 term constructors;
- mutable memory or system calls;
- source-language frontend/parser as a product feature;
- native/bytecode compiler;
- machine/system profile;
- self-hosting compiler/interpreter.

Experimental baseline translators or comparison encoders are allowed only when isolated from normative v0.1 semantics and clearly labelled.

## Definition of done

Stage 4 is complete when:

- the measurement contract is fixed and documented;
- at least one frozen benchmark corpus is machine-readable;
- exact NEX metrics are generated automatically;
- internal NEX design questions have measured results;
- erased-HM versus explicit/hybrid type transmission has measured program-cost results;
- selected external baseline comparisons are reproducible and assumption-labelled;
- a CBN versus call-by-need experiment exists without changing normative semantics;
- bootstrap costs/proxies are explicitly separated;
- a reproducible report is generated;
- a final decision record states what evidence supports keeping/changing/defering each studied design question;
- no prohibited Stage 5+/system/frontend work entered the stage.

All Definition-of-Done items are implemented on the Stage 4 branch. Final completion is pending merge review and post-merge verification on `main`.
