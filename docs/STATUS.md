# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Current stage:** `Stage 3 — Dynamic semantics and evaluator — In progress`  
**Stage 0 completed by:** PR `#1 docs: establish ADRs and project workflow`  
**Research source registry completed by:** PR `#2 docs: add research source registry`  
**Stage 1 completed by:** PR `#3 stage1: implement NEX wire foundation`  
**Stage 1 merge commit:** `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`  
**Stage 2 completed by:** PR `#4 stage2: complete static validation and principal type inference`  
**Stage 2 merge commit:** `cefe889d90a275897de31aa23c4b9742a388ec8f`  
**Active Stage 3 branch:** `stage3/dynamic-semantics`

## Stage 0 — Complete

Stage 0 established the project specification, ADR/workflow system, bilingual core documentation, source registry, architecture, testing strategy, and durable project memory.

## Stage 1 — Wire foundation — Complete

Stage 1 is defined and closed in `docs/STAGE-1.md`. The repository has an executable, tested, CI-verified canonical wire layer for the six v0.1 term constructors, arbitrary-precision `U(n)`, exact/prefix decoding, independent conformance vectors, and implementation resource limits separated from wire validity.

## Stage 2 — Static validation — Complete

Stage 2 is defined and closed in `docs/STAGE-2.md`.

The reference pipeline now provides:

```text
Term
  -> ValidateClosed
  -> ValidateCorePrimitives
  -> InferClosed
  -> principal TypeScheme
```

`conformance/static-v0.1.json` contains 15 scope vectors and 19 type vectors. Stage 2's final clean-checkout/fuzz verification passed before and after merge.

ADR-0007 keeps ordinary term-level type annotations out of canonical v0.1 terms while requiring a future measured comparison against compact explicit/hybrid type information.

## Stage 3 — Dynamic semantics and evaluator — In progress

Stage 3 is defined in `docs/STAGE-3.md`.

Accepted work order:

```text
3.0 dynamic-semantics contract audit and specification clarification
3.1 runtime Value / Environment / Thunk / Closure model
3.2 weak call-by-name Var/Lam/App/Let/Nat evaluator
3.3 primitive application spine and authoritative runtime arity
3.4 unit/natural primitive execution
3.5 product/sum primitive execution
3.6 fix and bounded handling of nontermination in tests
3.7 language-neutral evaluation conformance
3.8 resource controls, properties/fuzzing, clean-checkout CI
3.9 final scope/diff review and completion
```

### Stage 3.0 findings

The existing v0.1 text already selects weak call-by-name, but four details were insufficiently explicit for an executable oracle:

1. `Let(value, body)` had typing rules but no explicit dynamic rule;
2. WHNF/result categories and partially applied primitives were not formalized;
3. primitive argument-forcing behavior was only partly stated (`ifz` selected branch) rather than complete for products/sums/partial application;
4. evaluator resource exhaustion was not explicitly separated from divergence and Core validity.

The Stage 3 branch now records the proposed/accepted clarifications in `docs/STAGE-3.md`, ADR-0008, and ADR-0009. The canonical English specification and Russian mirror MUST be synchronized with this contract before Stage 3 is merged.

### Stage 3 runtime decision

ADR-0008 selects a first reference evaluator that is:

```text
weak call-by-name
+ environment based
+ closure based
+ explicit non-memoizing thunks
```

The runtime environment is ordered nearest de Bruijn binder first. `Let` and lambda arguments are delayed. Pair fields and sum payloads are delayed. Call-by-need sharing remains a permitted later optimization, not the first oracle.

### Stage 3 resource decision

ADR-0009 separates evaluator fuel/depth/memory refusal from language validity and semantic results. A finite resource refusal cannot prove divergence, and cross-implementation conformance will not depend on an exact internal step count.

### Stage 3 research basis

The source registry now includes:

```text
SRC-0011 Plotkin 1975   call-by-name / call-by-value distinction
SRC-0012 Launchbury 1993 lazy semantics with sharing
SRC-0013 Sestoft 1997  lazy abstract-machine derivation
```

These sources inform evaluation strategy/implementation alternatives; they do not define NEX-specific primitive forcing rules.

## Remaining project-wide unverified claims

Still intentionally unverified:

- formal/exhaustive proof of decoder, inference, or evaluator correctness;
- conformance agreement with a second independent implementation;
- Stage 3 runtime implementation and evaluation conformance;
- self-hosting feasibility;
- total-information-cost comparison against BLC, SKI/Jot, WebAssembly, stack bytecode, or an explicit-type NEX variant;
- any claim that NEX is globally optimal or the smallest possible language.

## Next recommended step

Finish Stage 3.0 by synchronizing the canonical English and Russian v0.1 evaluation sections with the accepted forcing/WHNF/resource contract. Then implement only Stage 3.1 and 3.2 first: runtime values/environments/thunks/closures and the lambda/let evaluator core. Do not add primitive execution until those layers have independent tests and clean CI.
