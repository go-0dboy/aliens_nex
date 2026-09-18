# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Current stage:** `Stage 3 — Dynamic semantics and evaluator — Complete`  
**Stage 0 completed by:** PR `#1 docs: establish ADRs and project workflow`  
**Research source registry completed by:** PR `#2 docs: add research source registry`  
**Stage 1 completed by:** PR `#3 stage1: implement NEX wire foundation`  
**Stage 1 merge commit:** `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`  
**Stage 2 completed by:** PR `#4 stage2: complete static validation and principal type inference`  
**Stage 2 merge commit:** `cefe889d90a275897de31aa23c4b9742a388ec8f`  
**Stage 3 completed by:** PR `#5 stage3: complete dynamic semantics and reference evaluator`  
**Stage 3 merge commit:** `166cdc03282ea500263fdca7185f006f9b17a702`

## Stage 0 — Complete

Stage 0 established the NEX-1 v0.1 specification, ADR/workflow system, bilingual core documentation, source registry, architecture, testing strategy, and durable project memory.

## Stage 1 — Wire foundation — Complete

Defined and closed in `docs/STAGE-1.md`.

The repository has an executable, CI-verified canonical wire layer for the six v0.1 term constructors, arbitrary-precision `U(n)`, exact/prefix decoding, implementation-independent conformance vectors, and decoder resource limits separated from wire validity.

## Stage 2 — Static validation — Complete

Defined and closed in `docs/STAGE-2.md`.

The reference static pipeline provides:

```text
Term
  -> ValidateClosed
  -> ValidateCorePrimitives
  -> InferClosed
  -> principal TypeScheme
```

`conformance/static-v0.1.json` contains 15 scope vectors and 19 type vectors. The implementation includes substitutions, free type variables, unification with occurs check, primitive type schemes, fresh instantiation, let-generalization, Algorithm-W-style inference, property tests, fuzzing, and clean-checkout CI.

ADR-0007 keeps ordinary term-level type annotations out of canonical v0.1 terms while requiring a future measured comparison against compact explicit/hybrid type information.

## Stage 3 — Dynamic semantics and evaluator — Complete

Defined and closed in `docs/STAGE-3.md`.

Completed functionality:

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

The evaluator implements every NEX-1 v0.1 Core primitive:

```text
fix succ pred ifz pair fst snd inl inr case unit
```

The canonical English `docs/NEX-1-v0.1.md` and informative Russian mirror `docs/NEX-1-v0.1.ru.md` are synchronized for the Stage 3 dynamic contract, including non-strict `Let`, primitive arities and partial application, WHNF categories, primitive forcing rules, divergence/resource refusal, evaluator conformance requirements, and Stage 3 research references.

### Evaluation conformance

`conformance/eval-v0.1.json` records implementation-independent observable WHNF results covering:

- lambda and natural results;
- beta application;
- ignored divergent arguments;
- non-strict `Let`;
- `unit`, `succ`, `pred`, and both `ifz` paths;
- partial primitive application;
- lazy products and projections;
- lazy sums and both `case` branches;
- terminating recursion through `fix`.

The conformance JSON is loaded directly by the Go test suite rather than duplicated in test code.

### Verification evidence

Final PR head before merge:

```text
09f4cb330a8f495996fe253868fd863331fb4d64
```

Final PR clean-checkout CI:

```text
35365175098  success
```

Post-merge `main` clean-checkout CI on merge commit `166cdc03282ea500263fdca7185f006f9b17a702`:

```text
35365823377  success
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

The final Stage 3 diff was reviewed against its scope guard. No human frontend/parser, optimizer, mutable memory/system profile, native/bytecode compiler, or self-hosting implementation entered Stage 3.

## Research basis added for Stage 3

`docs/SOURCES.md` includes:

```text
SRC-0011 Plotkin 1975   call-by-name / call-by-value distinction
SRC-0012 Launchbury 1993 lazy semantics with sharing
SRC-0013 Sestoft 1997   lazy abstract-machine derivation
```

These sources inform evaluation strategy and implementation alternatives; NEX-specific primitive forcing rules remain project decisions documented in the specification and ADRs.

## Remaining project-wide unverified claims

Still intentionally unverified:

- formal/exhaustive proof of decoder, type-inference, or evaluator correctness;
- conformance agreement with a second independent implementation;
- bootstrap/self-hosting feasibility and size;
- total-information-cost comparison against BLC, SKI/Jot, WebAssembly, a typed stack machine, or an explicit-type NEX variant;
- practical cost of call-by-name versus call-by-need for representative NEX programs;
- any claim that NEX is globally optimal or the smallest possible language.

## Next recommended step

Define Stage 4 before implementation. Stage 4 should be chosen based on the project objective rather than implementation convenience: after wire decoding, static validation, and executable Core semantics are complete, the next work should make the current design measurable and independently falsifiable before expanding the language or adding machine-specific features.