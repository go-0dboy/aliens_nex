# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Current stage:** `Stage 2 — Static validation — Implementation complete; pending merge review`  
**Stage 0 completed by:** PR `#1 docs: establish ADRs and project workflow`  
**Research source registry completed by:** PR `#2 docs: add research source registry`  
**Stage 1 completed by:** PR `#3 stage1: implement NEX wire foundation`  
**Stage 1 merge commit:** `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`  
**Active Stage 2 branch:** `stage2/static-validation`  
**Active Stage 2 pull request:** `#4 stage2: establish static validation foundations`

## Stage 0 — Complete

Stage 0 established the project specification, ADR/workflow system, bilingual core documentation, source registry, architecture, testing strategy, and durable project memory.

## Stage 1 — Wire foundation — Complete

Stage 1 is defined and closed in `docs/STAGE-1.md`. The repository has an executable, tested, and CI-verified canonical wire layer with arbitrary-precision `U(n)`, exact/prefix decoding, independent conformance vectors, and implementation resource limits separated from wire validity.

## Stage 2 — Static validation — Implementation complete; pending merge review

Stage 2 is defined in `docs/STAGE-2.md`.

ADR-0007 fixes the v0.1 type-annotation baseline: ordinary canonical Core terms omit type annotations and use inference, while compact explicit/hybrid type information remains a required future total-cost benchmark rather than a rejected alternative.

Completed on PR #4:

```text
2.1 de Bruijn scope validation
2.2 type AST + type schemes
2.3 substitutions + free type variables
2.4 unification + occurs check
2.5 authoritative Core primitive table + primitive validity
2.6 fresh instantiation + let-generalization
2.7 Algorithm W style inference
2.8 language-neutral principal-type/error conformance
2.9 property fuzzing + clean-checkout CI + diff review
```

### Static-validation pipeline

The reference implementation now provides:

```text
Term
  -> ValidateClosed
  -> ValidateCorePrimitives
  -> InferClosed
  -> principal TypeScheme
```

No evaluation occurs in this pipeline.

### Primitive metadata

One authoritative table contains Core primitive IDs `0..10`, names, and type schemes. Core-only static validation rejects reserved/future/profile primitive IDs when no external profile is selected.

An early 2.5 CI failure exposed an incorrect **test expectation** for canonical `inr` type-variable names. The primitive scheme itself matched the specification; the expected canonical rendering was corrected to respect first occurrence.

### Instantiation/generalization

- quantified variables receive fresh identities on every scheme use;
- instantiation is direct alpha-renaming, avoiding false substitution cycles when template and fresh IDs coincide;
- let-bound inferred types are generalized over variables not free in the outer environment;
- lambda-bound variables remain monomorphic;
- polymorphic recursion is not introduced.

### Algorithm W

Inference covers exactly the six v0.1 Core constructors:

```text
Var
Lam
App
Let
Nat
Prim
```

Tests prove, among other examples:

- identity and constant principal schemes;
- `succ : N -> N` constraints;
- products and `fix`;
- one let-bound identity reused at both `N` and `1`;
- the analogous lambda-bound parameter is rejected as monomorphic;
- `x x` is rejected by occurs check;
- calling a natural as a function is rejected;
- scope and unknown-primitive errors remain distinct from type errors.

### Language-neutral conformance

`conformance/static-v0.1.json` contains:

```text
15 scope vectors
19 type vectors
```

The type vectors record either canonical principal type schemes or deterministic static error classes. They do not depend on Go internal type-variable IDs.

### Verification evidence

Previously verified checkpoints:

```text
2.1 CI 35349955837  success
2.2 CI 35350348515  success
2.3 CI 35350580401  success
2.4 CI 35350747002  success
2.8 CI 35359948801  success
```

Final Stage 2 clean-checkout gate:

```text
CI 35360079519  success
```

That final gate executed:

```text
gofmt check
go vet ./...
go test ./...
1s FuzzSubstitutionComposition
1s FuzzUnifyProducesEqualAppliedTypes
1s FuzzInferenceSuccessfulSchemeIsClosedAndStable
```

The final branch diff was reviewed against `docs/STAGE-2.md`. It contains static-validation code, conformance, tests, CI/documentation, and ADR material only. No evaluator, reduction, primitive execution, source parser, optimizer, system profile, compiler, or self-hosting code is present.

## Remaining project-wide unverified claims

Still intentionally unverified:

- formal/exhaustive proof of decoder or type-inference correctness;
- conformance agreement with a second independent implementation;
- evaluator behavior;
- self-hosting feasibility;
- total-information-cost comparison against BLC, SKI/Jot, WebAssembly, stack bytecode, or an explicit-type NEX variant;
- any claim that NEX is globally optimal or the smallest possible language.

## Next recommended step

Review PR #4 as the Stage 2 completion candidate. If accepted, merge it and mark Stage 2 complete on `main` before defining Stage 3 evaluator semantics. Do not begin evaluator/runtime implementation before that merge decision.
