# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Current stage:** `Stage 4 — Empirical validation and benchmarking — Implementation complete; pending merge review`  
**Stage 0 completed by:** PR `#1 docs: establish ADRs and project workflow`  
**Research source registry completed by:** PR `#2 docs: add research source registry`  
**Stage 1 completed by:** PR `#3 stage1: implement NEX wire foundation`  
**Stage 1 merge commit:** `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`  
**Stage 2 completed by:** PR `#4 stage2: complete static validation and principal type inference`  
**Stage 2 merge commit:** `cefe889d90a275897de31aa23c4b9742a388ec8f`  
**Stage 3 completed by:** PR `#5 stage3: complete dynamic semantics and reference evaluator`  
**Stage 3 merge commit:** `166cdc03282ea500263fdca7185f006f9b17a702`  
**Active Stage 4 branch:** `stage4/empirical-validation`  
**Active Stage 4 pull request:** `#6`  
**Living research dissertation:** `docs/RESEARCH-DISSERTATION.md` / `docs/RESEARCH-DISSERTATION.ru.md` (ADR-0012)

## Stages 0–3 — Complete

Stage 0 established the specification/process baseline. Stage 1 implemented canonical wire encode/decode. Stage 2 implemented closed-scope/static validation and principal HM type inference. Stage 3 implemented the complete weak-call-by-name v0.1 Core evaluator, synchronized EN/RU dynamic semantics, language-neutral evaluation conformance, resource separation, fuzz/property verification, and clean-checkout CI.

Detailed completion records remain in `docs/STAGE-1.md`, `docs/STAGE-2.md`, and `docs/STAGE-3.md`.

## Stage 4 — Implementation complete; pending merge review

Stage 4 is defined in `docs/STAGE-4.md`. ADR-0010 froze the measurement contract/corpus discipline before optimization; ADR-0011 records the evidence-based decision gate.

### 4.0 — measurement contract — Complete

The project separates:

```text
P  exact transmitted-program cost
R  host/reference implementation proxy
B  actual bootstrap transmission cost (unknown)
S  specification transmission cost (no accepted receiver-neutral scalar yet)
C  S + B + P
```

`R` MUST NOT be substituted for `B`.

### 4.1 — frozen benchmark corpora — Complete

- `benchmarks/corpus-v0.1.json`: immutable 10-program foundation corpus.
- `corpus-v0.2.json`: preserved negative checkpoint; `factorial-5` exceeded the default 1,000,000-transition non-memoizing CBN budget. This is resource refusal, not invalidity or proof of divergence.
- `benchmarks/corpus-v0.3.json`: accepted frozen extended corpus, 17 programs total.

Clean-checkout CI `35368707827` parsed, type-checked, evaluated, and measured accepted v0.3.

### 4.2 — instrumentation — Complete

Implemented:

- exact wire/AST/constructor metrics and per-constructor wire-bit attribution;
- reference-only evaluator transition/depth statistics;
- shared frozen-corpus loader/parser;
- deterministic benchmark/report CLIs;
- clean-checkout reproduction in `reference/go/verify.sh`.

### 4.3 — internal NEX experiments — Complete

Frozen v0.3 aggregate:

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

The early hypothesis that `App` would dominate this corpus is not supported; primitive references are the largest measured contributor. This is corpus-specific evidence.

`Let` shows a real break-even point. For a 5-bit payload: 2 repeats cost +4 bits with `Let`, 3 repeats +2, 4 tie, 8 save 8. For the tested 14-bit payload, two repeats already save 5 bits.

Direct natural literals strongly outperform the tested `succ`-chain construction. Representative endpoint:

```text
Nat(255)          21 bits
succ-chain(255) 2300 bits
```

Clean-checkout CI `35369320807` reproduced the full v0.3 profile and experiment outputs.

### 4.4 — erased HM versus hybrid root type — Complete first experiment

The non-normative root-principal-type envelope measured:

```text
erased term bits       1371
root type bits          134
hybrid total           1505
program overhead       +9.77%
```

Small polymorphic functions have large relative overhead (`identity` +240%, `constant` +222.2%, `composition` +200%); most larger `N`-result programs add only 4 type bits.

This measures `Delta P` only. No reduction in receiver-neutral `S+B` has been implemented or measured, and a root principal type does not replace internal HM inference.

Clean-checkout CI `35370010741` reproduced the experiment.

### 4.5 — external / structural baselines — Complete first reproducible set

On the identical pure-lambda subset (`identity`, `constant`, `composition`):

```text
NEX                         37 bits
BLC                         30 bits
Jot via fixed SK translation 288 bits
```

BLC is 7 bits smaller on this narrow shared subset. The Jot number is only for the documented deterministic bracket-abstraction translation and is not a shortest-Jot claim.

On full v0.3:

```text
NEX canonical wire  1371 bits
tiny postfix stack  1529 bits
delta                +158 bits (+11.52%)
```

The tiny-stack baseline reuses NEX integer/primitive conventions and therefore is a structural comparison, not an independent total-bootstrap comparison.

Clean-checkout CI `35372182772` reproduced these values.

### 4.6 — call-by-name versus call-by-need — Complete first experiment

Normative weak CBN was not changed. A separate experimental memoizing evaluator was added and required to match the same observable WHNF on every accepted program.

All 17 v0.3 programs agreed observationally.

Reference-only aggregate:

```text
CBN transitions          226151
call-by-need transitions   2484
saved                    223667
reduction                 98.90%
memo hits                   237
programs with fewer transitions 6/17
```

Representative heavy workloads:

```text
factorial-4         209315 -> 895
fibonacci-5           7424 -> 512
let-reuse-expensive    8710 -> 560
```

This is implementation/runtime evidence, not a transmission-cost result. Call-by-need changes no program bits and may increase bootstrap/runtime machinery.

Clean-checkout CI `35372634610` reproduced the strategy comparison.

### 4.7 — total-information accounting — Complete model

Machine-readable accounting keeps unknowns explicit.

For v0.3:

```text
P exact                         1371 bits
canonical spec Markdown        23440 UTF-8 bytes
raw Markdown proxy            187520 bits
selected Go reference Core     43013 UTF-8 bytes
B bootstrap                    unknown
C total                        not numerically computable
```

The Markdown size is only an `S` proxy; it is not accepted as receiver-neutral specification cost. Go source size is `R`, not `B`. Unknown `B` is not treated as zero.

Clean-checkout CI `35373159387` reproduced the accounting output.

### 4.8 — consolidated reproducible report — Complete

`reference/go/cmd/nexreport` recomputes the principal Stage 4 results from frozen corpus data and experiment/reference functions in one command. It does not copy numbers from documentation.

Clean-checkout CI `35373511054` generated `nex-stage4-experimental-report-v0.1` and also reran all previous tests, experiment CLIs, and fuzz/property checks successfully.

### 4.9 — evidence-based decision gate — Complete

ADR-0011 records the decisions supported by current evidence:

- keep NEX-1 v0.1 wire/Core stable;
- keep direct `Nat`;
- keep `Let` while acknowledging its local break-even behavior;
- keep erased HM for v0.1; explicit/hybrid verification remains deferred until a real alternative checker/bootstrap exists;
- keep weak call-by-name normative; call-by-need remains an allowed optimization when observable results are preserved;
- prioritize primitive-reference/profile encoding in future compactness experiments because `Prim` is the largest measured v0.3 wire contributor;
- do not claim NEX is globally smallest or superior to BLC;
- keep total-information superiority unresolved until an actual receiver-neutral bootstrap artifact makes `B` measurable.

## Living research dissertation — Established

ADR-0012 adds a cumulative dissertation-style research manuscript to the repository:

- canonical English: `docs/RESEARCH-DISSERTATION.md`;
- required Russian mirror: `docs/RESEARCH-DISSERTATION.ru.md`.

The manuscript synthesizes the research problem, object/subject, goal, research questions, hypotheses, theoretical basis, methodology, Stages 0–4, reproducible measurements, negative results, limitations/threats to validity, current contributions, glossary, bibliography, and reproducibility artifacts.

The dissertation is now a mandatory research-synthesis checkpoint. A PR that creates a material new measurement, research-significant decision, external baseline/source, independent conformance result, proof/counterexample, stage-level conclusion, revised `S/B/P/C` evidence, or falsification/qualification of an earlier hypothesis must update the English manuscript and Russian mirror, or explicitly document why no dissertation change is required.

Direct quotations must not be invented; exact quotations may be used only after verifying source wording. Ordinary literature claims should be paraphrased and cited to primary/official sources registered in `docs/SOURCES.md`.

## Stage 4 scope review

Stage 4 did not add new normative NEX-1 v0.1 term constructors, mutable memory/system calls, product frontend/parser work, native/bytecode compiler, machine profile, or self-hosting implementation. Experimental encoders/evaluators remain isolated from normative v0.1 semantics.

The dissertation/process additions are documentation and research-governance work; they do not change normative NEX-1 v0.1 semantics or Stage 4 measurements.

## Remaining project-wide unknowns

Still intentionally unresolved:

- formal/exhaustive proof of decoder, type-inference, or evaluator correctness;
- agreement with a second independent implementation;
- actual receiver-neutral bootstrap artifact and cost `B`;
- receiver-neutral specification transmission cost `S`;
- broader-corpus generalization of v0.3 constructor distribution;
- independent total-cost comparisons against external architectures;
- any claim that NEX is globally optimal or the smallest possible language.

## Next recommended step

Review PR #6 as the completed Stage 4 implementation plus the new living research dissertation/process rule. If accepted, merge it, mark Stage 4 `Complete` on `main`, update the dissertation's Stage 4 evidence status from pending merge to merged, and only then design the next stage around the highest-value unresolved evidence: independent conformance implementation and a receiver-neutral bootstrap experiment. Do not begin a normative NEX-1 v0.2 redesign before that discussion.
