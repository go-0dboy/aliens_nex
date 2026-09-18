# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Current stage:** `Stage 2 — Static validation — In progress`  
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

## Stage 2 — Static validation — In progress

Stage 2 is defined in `docs/STAGE-2.md`.

ADR-0007 fixes the v0.1 type-annotation baseline: ordinary canonical Core terms omit type annotations and use inference, while compact explicit/hybrid type information remains a required future total-cost benchmark rather than a rejected alternative.

### 2.1 — de Bruijn scope validation — verified

- `ValidateClosed(term)` enforces closed zero-based de Bruijn scope;
- `Lam` binds its body;
- `Let(value, body)` is non-recursive and binds only `body`;
- language-neutral positive/negative scope vectors exist.

Checkpoint CI `35349955837`: success.

### 2.2 — type/type-scheme representation — verified

- all v0.1 monotype constructors and rank-1 schemes represented;
- malformed in-memory type shapes rejected;
- canonical rendering renames internal variables by first occurrence.

Checkpoint CI `35350348515`: success.

### 2.3 — substitutions and free type variables — verified

- FTV for type/scheme/environment;
- substitution application and composition;
- quantified variables protected;
- substitution cycles rejected;
- composition property fuzz exists.

Checkpoint CI `35350580401`: success.

### 2.4 — unification + occurs check — verified

- structural unification for every v0.1 monotype constructor;
- distinct mismatch and occurs-check diagnostics;
- unification equality property fuzz exists.

Checkpoint CI `35350747002`: success.

### 2.5 — Core primitive table and primitive validity — implemented

- one authoritative table contains IDs `0..10`, names, and type schemes;
- reserved/future/profile IDs are rejected by Core-only validation when no profile is selected;
- an initial CI failure exposed a test expectation that incorrectly treated source-style type-variable names as significant for `inr`; the implementation was retained and the canonicalized expectation was corrected.

### 2.6 — instantiation and generalization — implemented

- each polymorphic scheme use is freshly instantiated;
- instantiation uses direct alpha-renaming rather than general substitution, avoiding false cycles when template IDs and fresh IDs coincide;
- let-generalization quantifies variables free in the inferred type but not the outer environment;
- lambda bindings remain monomorphic.

### 2.7 — Algorithm W style inference — implemented

`InferClosed(term)` performs, in order:

```text
closed-scope validation
  -> Core primitive validity
  -> HM-style inference
  -> top-level generalization
  -> principal type scheme
```

Inference exists for `Var`, `Lam`, `App`, `Let`, `Nat`, and `Prim`. No evaluation is performed.

Tests include identity, constant function, `succ`, products, `fix`, successful polymorphic-let reuse, monomorphic lambda rejection, occurs-check failure, function/type mismatch, scope error preservation, and unknown primitive preservation.

### 2.8 — language-neutral type conformance — implemented

`conformance/static-v0.1.json` now contains:

```text
15 scope vectors
19 type vectors
```

Type vectors include principal types and deterministic static error classes independent of the Go implementation.

Checkpoint CI for the type-conformance state: run `35359948801` — success.

### 2.9 — property/fuzz + final review — in progress

`reference/go/verify.sh` now performs:

```text
gofmt check
go vet ./...
go test ./...
1s substitution-composition fuzz
1s unification-property fuzz
1s inference-stability fuzz
```

The final clean-checkout CI run for this full Stage 2 verification is the remaining gate before the branch can be declared ready for merge.

## Stage 2 scope guard

No evaluator, beta reduction, primitive execution, source parser, optimizer, machine/system profile, bytecode/native compiler, or self-hosting implementation belongs in this stage.

## Remaining project-wide unverified claims

Still intentionally unverified:

- formal/exhaustive proof of decoder or inference correctness;
- conformance with a second independent implementation;
- evaluator behavior;
- self-hosting feasibility;
- total-information-cost comparison against BLC, SKI/Jot, WebAssembly, stack bytecode, or an explicit-type NEX variant;
- any claim that NEX is globally optimal or the smallest possible language.

## Next recommended step

Wait for the final Stage 2 clean-checkout CI gate, perform a complete PR #4 diff review against `docs/STAGE-2.md`, and if both are clean present PR #4 for merge review. Do not begin evaluator/runtime work before Stage 2 is accepted.
