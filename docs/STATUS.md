# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Current stage:** `Stage 1 — Wire foundation — Complete`  
**Stage 0 completed by:** PR `#1 docs: establish ADRs and project workflow`  
**Research source registry completed by:** PR `#2 docs: add research source registry`  
**Stage 1 completed by:** PR `#3 stage1: implement NEX wire foundation`  
**Stage 1 merge commit:** `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`

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

Completed:

- ADR-0005 selects Go for the dependency-free first reference implementation;
- ADR-0006 separates resource-limit refusal from malformed NEX syntax;
- `reference/go/` contains the first executable reference codec;
- `U(n)` supports arbitrary-precision naturals through `math/big.Int`;
- the six canonical constructors `Var`, `Lam`, `App`, `Let`, `Nat`, `Prim` have an in-memory representation;
- `EncodeTerm`, `DecodeOne`, and `DecodeExact` implement the v0.1 constructor prefixes;
- decoder limits cover integer bit length, term depth, and node count without redefining wire validity;
- `conformance/wire-v0.1.json` is language-independent;
- `.github/workflows/wire-foundation.yml` repeats repository verification from a clean checkout;
- no Stage 2 functionality was included in the Stage 1 implementation.

## Verified Stage 1 results

Reference verification:

```text
gofmt check    PASS
go vet ./...   PASS
go test ./...  PASS
```

GitHub Actions run `35348259779` completed successfully from a clean checkout.

Final conformance corpus:

```text
17 integer vectors
12 term vectors
15 invalid exact-input vectors
```

A final one-second `FuzzTermRoundTrip` run completed 27,289 generated executions without a failure. This is empirical coverage, not a formal proof.

The final PR diff was reviewed against `docs/STAGE-1.md` and contained no type inference, evaluator, frontend, optimizer, memory/system profile, or self-hosting functionality.

## Remaining unverified claims

The following remain intentionally unverified or out of scope:

- formal/exhaustive proof of decoder correctness;
- conformance agreement with a second independent implementation;
- de Bruijn scope validity;
- primitive/profile semantic validity;
- static type correctness;
- evaluator behavior;
- self-hosting feasibility;
- comparative encoded size versus BLC, SKI/Jot, WebAssembly, or stack bytecode;
- any claim that NEX is globally optimal or the smallest possible language.

## Architectural baseline after Stage 1

NEX-1 Core v0.1 currently has an executable and tested wire layer for:

```text
Var
Lam
App
Let
Nat
Prim
```

with canonical `U(n)` integer coding, exact/prefix decoding, independent conformance vectors, and explicit implementation resource limits.

The project can now begin static semantic validation without changing the established wire foundation unless a new ADR explicitly supersedes an existing decision.

## Next recommended step

Do not begin Stage 2 implementation immediately.

First define and review a dedicated Stage 2 plan covering:

```text
de Bruijn scope validation
  -> type representation
  -> substitutions and free type variables
  -> unification with occurs check
  -> primitive type schemes
  -> Algorithm W / let-generalization
  -> type conformance vectors
```

Any new external theory or implementation baseline used during Stage 2 must be registered in `docs/SOURCES.md` according to ADR-0004.
