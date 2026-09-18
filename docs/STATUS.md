# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Current stage:** `Stage 2 — Static validation — In progress`  
**Stage 0 completed by:** PR `#1 docs: establish ADRs and project workflow`  
**Research source registry completed by:** PR `#2 docs: add research source registry`  
**Stage 1 completed by:** PR `#3 stage1: implement NEX wire foundation`  
**Stage 1 merge commit:** `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`  
**Active Stage 2 branch:** `stage2/static-validation`  
**Active Stage 2 pull request:** `#4 stage2: static validation foundations`

## Stage 0 — Complete

Stage 0 established the project baseline before implementation work began:

- NEX-1 Core v0.1 draft specification;
- Russian mirrors for the project overview, specification, and architecture;
- ADR process and initial design decisions;
- domain vocabulary and invariants;
- architecture, workflow, testing strategy, and AI-agent rules;
- durable continuation status.

PR #2 subsequently added `docs/SOURCES.md`, ADR-0004, and mandatory source-registry maintenance before Stage 1 implementation began.

## Stage 1 — Wire foundation — Complete

Stage 1 is defined and closed in `docs/STAGE-1.md`.

The repository has an executable, tested, and CI-verified canonical wire layer for:

```text
Var
Lam
App
Let
Nat
Prim
```

including arbitrary-precision `U(n)`, exact/prefix decode APIs, independent conformance vectors, and implementation resource limits separated from wire validity.

## Stage 2 — Static validation — In progress

Stage 2 is defined in `docs/STAGE-2.md`.

Accepted work order:

```text
2.1 de Bruijn scope validation
2.2 type AST + type schemes
2.3 substitutions + free type variables
2.4 unification + occurs check
2.5 primitive type schemes and primitive validity
2.6 instantiation + generalization
2.7 Algorithm W style inference
2.8 language-neutral type conformance
2.9 property/fuzz tests, CI, and completion review
```

### Stage 2 design decision

ADR-0007 fixes the v0.1 type-annotation policy:

- canonical v0.1 Core terms omit ordinary term-level type annotations;
- frontends may accept annotations but erase them when emitting canonical v0.1 Core;
- Stage 2 implements inference for the existing erased-type representation;
- erased types are **not** claimed globally optimal;
- a future benchmark must compare erased HM inference against compact explicit/hybrid type information using total cost `specification + bootstrap + transmitted programs`.

## Completed Stage 2 checkpoints on the active branch

### 2.1 — de Bruijn scope validation

Implemented and clean-checkout CI verified:

- `ValidateClosed(term)` enforces zero-based de Bruijn scope;
- top-level validation starts at binder depth `0`, so accepted programs are closed;
- `Lam` introduces one binder for its body;
- `Let(value, body)` is non-recursive: its binder is visible only in `body`;
- `App` validates both children in the same outer scope;
- `Nat` and `Prim` do not affect binder depth;
- out-of-scope variables produce distinct `ScopeError` / `ErrOutOfScope` diagnostics;
- `conformance/static-v0.1.json` contains implementation-independent scope vectors.

Checkpoint CI: run `35349955837` — success.

### 2.2 — type and type-scheme representation

Implemented and clean-checkout CI verified:

- internal `TypeVarID` is independent of human-readable variable names;
- monotypes represent type variable, `1`, `N`, function, product, and sum;
- `TypeScheme` represents `forall` schemes;
- malformed in-memory type/scheme shapes are rejected;
- canonical test/debug rendering renames variables `T0`, `T1`, ... by first occurrence;
- canonical scheme rendering is independent of internal type-variable IDs and ordinary quantified-list ordering for variables occurring in the body.

Checkpoint CI: run `35350348515` — success.

### 2.3 — substitutions and free type variables

Implemented and clean-checkout CI verified:

- free type variables for monotypes, schemes, and type environments;
- substitution application to types, schemes, and environments;
- quantified scheme variables are protected from substitution;
- substitution chains are resolved;
- cyclic substitutions are rejected separately;
- substitution composition implements `newer o older`;
- property/fuzz test checks:

```text
apply(compose(S2, S1), T)
==
apply(S2, apply(S1, T))
```

A local one-second property fuzz run completed 34,311 executions without failure.

Checkpoint CI: run `35350580401` — success.

### 2.4 — unification and occurs check

Implemented and clean-checkout CI verified:

- structural unification for type variables, `1`, `N`, functions, products, and sums;
- deterministic type-mismatch diagnostics;
- mandatory occurs check with distinct `ErrOccursCheck` / `OccursCheckError`;
- substitutions produced by unification are composed through the Stage 2.3 machinery;
- property/fuzz test constructs unifiable type pairs and checks:

```text
if Unify(A, B) = S
then apply(S, A) == apply(S, B)
```

A local one-second unification fuzz run completed 38,212 executions without failure.

Checkpoint CI: run `35350747002` — success.

## Current Stage 2 boundary

The project deliberately stops here before primitive typing and Algorithm W.

Not yet implemented:

- authoritative primitive type-scheme table;
- primitive/profile validity checking;
- fresh type-variable generator for inference;
- instantiation/generalization;
- Algorithm W style inference;
- principal type conformance vectors;
- positive/negative complete static-validation corpus.

No evaluator/runtime behavior has been added.

## Remaining project-wide unverified claims

The following remain intentionally unverified or out of scope:

- formal/exhaustive proof of decoder, substitution, unification, or future inference correctness;
- conformance agreement with a second independent implementation;
- evaluator behavior;
- self-hosting feasibility;
- comparative total information cost versus BLC, SKI/Jot, WebAssembly, stack bytecode, or an explicit-type NEX variant;
- any claim that NEX is globally optimal or the smallest possible language.

## Next recommended step

Review the Stage 2.1–2.4 foundation in PR #4. If accepted, continue with sub-stage 2.5 only: define one authoritative Core primitive table containing IDs, names, and type schemes, then add primitive validity tests before any Algorithm W implementation.
