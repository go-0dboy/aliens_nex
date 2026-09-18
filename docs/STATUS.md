# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Current stage:** `Stage 2 — Static validation — In progress`  
**Stage 0 completed by:** PR `#1 docs: establish ADRs and project workflow`  
**Research source registry completed by:** PR `#2 docs: add research source registry`  
**Stage 1 completed by:** PR `#3 stage1: implement NEX wire foundation`  
**Stage 1 merge commit:** `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`  
**Active Stage 2 branch:** `stage2/static-validation`

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

The repository now has an executable, tested, and CI-verified canonical wire layer for:

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

### Stage 2 design decisions recorded

ADR-0007 fixes the current type-annotation policy:

- NEX-1 v0.1 canonical terms continue to omit ordinary term-level type annotations;
- frontends may accept annotations but erase them when emitting v0.1 Core;
- Stage 2 validates the existing HM-style inferred-type design;
- erased types are **not** claimed globally optimal;
- a future benchmark must compare erased HM inference against compact explicit/hybrid type information using total cost `specification + bootstrap + transmitted programs`.

### Sub-stage 2.1 — de Bruijn scope validation — implemented on active branch

Present on `stage2/static-validation`:

- `ValidateClosed(term)` checks that every `Var(k)` refers to an enclosing `Lam` or `Let` binder;
- validation starts at binder depth `0`, therefore accepted top-level terms are closed;
- `Lam(body)` validates `body` at depth + 1;
- `App(f, x)` validates both children at the same depth;
- `Let(value, body)` validates `value` in the outer depth and `body` at depth + 1;
- this makes v0.1 `Let` explicitly non-recursive at the scope layer;
- `Nat` and `Prim` do not change binder depth;
- out-of-scope variables produce a distinct `ScopeError` / `ErrOutOfScope`;
- invalid in-memory term shapes remain distinct from scope errors;
- `conformance/static-v0.1.json` contains implementation-independent scope vectors;
- Go tests consume those vectors and include direct error-structure and fuzz robustness checks;
- the Go CI workflow now watches all `conformance/*.json` files rather than only wire vectors.

## Verification state for Stage 2.1

The implementation has been committed to the Stage 2 branch and CI has been configured to run the existing `reference/go/verify.sh` suite, which includes all package tests.

Before sub-stage 2.1 is considered accepted, the branch must show a successful clean-checkout CI run and the diff must be reviewed against the Stage 2 scope guard.

## Remaining Stage 2 work

Not yet implemented:

- type AST and schemes;
- substitution application/composition;
- free type variable calculation;
- unification;
- occurs check;
- one authoritative primitive type table;
- instantiation/generalization;
- Algorithm W style inference;
- canonical principal-type normalization;
- positive/negative type conformance vectors.

No evaluator/runtime behavior belongs in this stage.

## Remaining project-wide unverified claims

The following remain intentionally unverified or out of scope:

- formal/exhaustive proof of decoder or type-inference correctness;
- conformance agreement with a second independent implementation;
- evaluator behavior;
- self-hosting feasibility;
- comparative total information cost versus BLC, SKI/Jot, WebAssembly, stack bytecode, or an explicit-type NEX variant;
- any claim that NEX is globally optimal or the smallest possible language.

## Next recommended step

Verify and review sub-stage 2.1 on CI. If green, keep it as the accepted scope-validation foundation and proceed to sub-stage 2.2 only: define the type/type-scheme representation and its canonical test representation without implementing unification yet.
