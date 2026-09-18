# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Current stage:** `Stage 3 — Dynamic semantics and evaluator — Implementation complete; pending merge review`  
**Stage 0 completed by:** PR `#1 docs: establish ADRs and project workflow`  
**Research source registry completed by:** PR `#2 docs: add research source registry`  
**Stage 1 completed by:** PR `#3 stage1: implement NEX wire foundation`  
**Stage 1 merge commit:** `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`  
**Stage 2 completed by:** PR `#4 stage2: complete static validation and principal type inference`  
**Stage 2 merge commit:** `cefe889d90a275897de31aa23c4b9742a388ec8f`  
**Active Stage 3 branch:** `stage3/dynamic-semantics`  
**Active Stage 3 pull request:** `#5 stage3: implement dynamic semantics and reference evaluator`

## Stage 0 — Complete

Stage 0 established the project specification, ADR/workflow system, bilingual core documentation, source registry, architecture, testing strategy, and durable project memory.

## Stage 1 — Wire foundation — Complete

Stage 1 is defined and closed in `docs/STAGE-1.md`. The repository has an executable, tested, CI-verified canonical wire layer for the six v0.1 term constructors, arbitrary-precision `U(n)`, exact/prefix decoding, independent conformance vectors, and implementation resource limits separated from wire validity.

## Stage 2 — Static validation — Complete

Stage 2 is defined and closed in `docs/STAGE-2.md`. The reference static pipeline validates closed de Bruijn scope, Core primitive IDs, and Hindley-Milner principal types. `conformance/static-v0.1.json` contains 15 scope vectors and 19 type vectors.

ADR-0007 keeps ordinary term-level type annotations out of canonical v0.1 terms while requiring a future measured comparison against compact explicit/hybrid type information.

## Stage 3 — Dynamic semantics and evaluator — Implementation complete; pending merge review

Stage 3 is defined in `docs/STAGE-3.md`.

Completed on PR #5:

```text
3.0 dynamic-semantics contract audit and EN/RU specification clarification
3.1 runtime Value / Environment / Thunk / Closure model
3.2 weak call-by-name Var/Lam/App/Let/Nat evaluator
3.3 curried primitive application spine and authoritative runtime arity
3.4 unit/succ/pred/ifz execution with lazy branch selection
3.5 pair/fst/snd/inl/inr/case execution with delayed fields/payloads
3.6 fix and bounded implementation refusal for nontermination tests
3.7 language-neutral evaluation conformance corpus
3.8 evaluator resource controls, property/fuzz testing, clean-checkout CI
3.9 final scope/diff review
```

### Dynamic semantics

ADR-0008 selects the first reference evaluator as:

```text
weak call-by-name
+ environment based
+ closures
+ explicit non-memoizing thunks
```

The runtime environment is ordered nearest de Bruijn binder first. Lambda arguments and `Let` values are delayed. Pair fields and sum payloads remain delayed until selected. Unsaturated primitives are function WHNFs. Call-by-need sharing remains a permitted later optimization rather than the reference behavior.

ADR-0009 separates evaluator resource refusal from NEX validity and semantic results. Finite fuel/depth exhaustion does not prove divergence and does not make a valid program invalid.

### Core primitive runtime

The authoritative primitive table carries ID, name, arity, and type scheme for IDs `0..10`. The evaluator implements all NEX-1 v0.1 Core primitives:

```text
fix succ pred ifz pair fst snd inl inr case unit
```

The forcing contract is tested explicitly: unselected `ifz`/`case` branches and unselected pair fields are not evaluated merely by the selecting primitive; constructor payloads remain delayed.

### Specification synchronization

The canonical English `docs/NEX-1-v0.1.md` and informative Russian mirror `docs/NEX-1-v0.1.ru.md` are synchronized for the Stage 3 dynamic contract, including:

- non-strict `Let`;
- primitive arities and partial application;
- WHNF categories;
- primitive forcing rules;
- divergence versus evaluator resource refusal;
- evaluator conformance requirements;
- Stage 3 research references.

### Evaluation conformance

`conformance/eval-v0.1.json` contains implementation-independent observable-WHNF vectors covering beta application, ignored divergent arguments, non-strict `Let`, natural/unit primitives, both `ifz` paths, partial primitive application, lazy products/sums, both `case` branches, and terminating `fix` recursion.

### Verification evidence

Verified clean-checkout GitHub Actions:

```text
CI 35364644931  success   # dynamic contract/spec checkpoint
CI 35365016780  success   # post-status/final Stage 3 branch checkpoint
```

`reference/go/verify.sh` runs:

```text
gofmt check
go vet ./...
go test ./...
1s FuzzSubstitutionComposition
1s FuzzUnifyProducesEqualAppliedTypes
1s FuzzInferenceSuccessfulSchemeIsClosedAndStable
1s FuzzEvaluationDeterministicObservation
```

### Stage 3.9 final scope review

The complete `main...stage3/dynamic-semantics` diff was reviewed against `docs/STAGE-3.md`.

It contains only:

- Stage 3 planning, ADRs, source/status documentation;
- synchronized EN/RU dynamic-semantics specification changes;
- reference evaluator/runtime implementation;
- language-neutral evaluation conformance;
- evaluator tests/fuzz verification.

It does **not** contain a human frontend/parser, optimizer, mutable memory/system profile, native/bytecode compiler, or self-hosting implementation.

PR #5 is therefore the Stage 3 completion candidate and is ready for merge review.

## Research basis added for Stage 3

`docs/SOURCES.md` includes:

```text
SRC-0011 Plotkin 1975   call-by-name / call-by-value distinction
SRC-0012 Launchbury 1993 lazy semantics with sharing
SRC-0013 Sestoft 1997   lazy abstract-machine derivation
```

These sources inform evaluation strategy and implementation alternatives; NEX-specific primitive forcing rules remain project decisions documented in the specification/ADRs.

## Remaining project-wide unverified claims

Still intentionally unverified:

- formal/exhaustive proof of decoder, inference, or evaluator correctness;
- conformance agreement with a second independent implementation;
- self-hosting feasibility;
- total-information-cost comparison against BLC, SKI/Jot, WebAssembly, stack bytecode, or an explicit-type NEX variant;
- any claim that NEX is globally optimal or the smallest possible language.

## Next recommended step

Review PR #5 as the Stage 3 completion candidate. If accepted, merge it and mark Stage 3 complete on `main` before defining Stage 4. Do not begin frontend, optimizer, machine profiles, compiler, mutable memory, or self-hosting work before that merge decision.