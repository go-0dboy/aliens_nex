# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Current stage:** `Stage 2 — Static validation — Complete`  
**Stage 0 completed by:** PR `#1 docs: establish ADRs and project workflow`  
**Research source registry completed by:** PR `#2 docs: add research source registry`  
**Stage 1 completed by:** PR `#3 stage1: implement NEX wire foundation`  
**Stage 1 merge commit:** `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`  
**Stage 2 completed by:** PR `#4 stage2: complete static validation and principal type inference`  
**Stage 2 merge commit:** `cefe889d90a275897de31aa23c4b9742a388ec8f`

## Stage 0 — Complete

Stage 0 established the project specification, ADR/workflow system, bilingual core documentation, source registry, architecture, testing strategy, and durable project memory.

## Stage 1 — Wire foundation — Complete

Stage 1 is defined and closed in `docs/STAGE-1.md`.

The repository has an executable, tested, and CI-verified canonical wire layer for the six v0.1 term constructors, arbitrary-precision `U(n)`, exact/prefix decoding, implementation-independent conformance vectors, and implementation resource limits separated from wire validity.

## Stage 2 — Static validation — Complete

Stage 2 is defined and closed in `docs/STAGE-2.md`.

Completed functionality:

```text
2.1 de Bruijn scope validation
2.2 type AST + type schemes
2.3 substitutions + free type variables
2.4 unification + occurs check
2.5 authoritative Core primitive table + primitive validity
2.6 fresh instantiation + let-generalization
2.7 Algorithm W style principal type inference
2.8 language-neutral static conformance
2.9 property fuzzing + clean-checkout CI + final diff review
```

The reference static-validation pipeline is now:

```text
Term
  -> ValidateClosed
  -> ValidateCorePrimitives
  -> InferClosed
  -> principal TypeScheme
```

No evaluation occurs in this pipeline.

### Type annotations decision

ADR-0007 keeps ordinary term-level type annotations out of canonical NEX-1 v0.1 terms. Frontends may accept annotations but erase them before canonical Core output.

This is not claimed globally optimal. A future experiment must compare erased HM inference against compact explicit/hybrid type information using total information cost:

```text
specification + bootstrap implementation + transmitted programs
```

### Conformance state

`conformance/static-v0.1.json` contains:

```text
15 scope vectors
19 type vectors
```

The type vectors record canonical principal schemes or deterministic static error classes independently of Go internal type-variable IDs.

### Stage 2 verification evidence

Verified clean-checkout checkpoints include:

```text
2.1 CI 35349955837  success
2.2 CI 35350348515  success
2.3 CI 35350580401  success
2.4 CI 35350747002  success
2.8 CI 35359948801  success
final gate 35360079519  success
final PR head 35360245915  success
```

The final verification runs:

```text
gofmt check
go vet ./...
go test ./...
1s FuzzSubstitutionComposition
1s FuzzUnifyProducesEqualAppliedTypes
1s FuzzInferenceSuccessfulSchemeIsClosedAndStable
```

The final Stage 2 diff was reviewed against the stage scope guard. No evaluator, reduction, primitive execution, source parser, optimizer, system profile, compiler, or self-hosting code entered Stage 2.

## Remaining project-wide unverified claims

Still intentionally unverified:

- formal/exhaustive proof of decoder or type-inference correctness;
- conformance agreement with a second independent implementation;
- evaluator semantics and runtime behavior;
- self-hosting feasibility;
- total-information-cost comparison against BLC, SKI/Jot, WebAssembly, stack bytecode, or an explicit-type NEX variant;
- any claim that NEX is globally optimal or the smallest possible language.

## Next recommended step

Design Stage 3 before implementation. Stage 3 should define and verify evaluator semantics for already validated v0.1 Core terms, beginning with evaluation strategy, runtime value/thunk/environment representation, primitive forcing rules, deterministic execution/error/resource behavior, and implementation-independent evaluation conformance vectors.

Do not begin frontend, optimizer, machine profiles, compiler, or self-hosting work until the Stage 3 evaluator boundary is explicitly defined.