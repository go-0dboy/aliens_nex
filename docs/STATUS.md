# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Current stage:** `Stage 1 — Wire foundation — In progress`  
**Stage 0 completed by:** PR `#1 docs: establish ADRs and project workflow`  
**Research source registry completed by:** PR `#2 docs: add research source registry`  
**Active Stage 1 branch:** `stage1/wire-foundation`  
**Active Stage 1 pull request:** `#3 stage1: implement NEX wire foundation`

## Stage 0 — Complete

Stage 0 established the project baseline before implementation work began:

- NEX-1 Core v0.1 draft specification;
- Russian mirrors for the project overview, specification, and architecture;
- ADR process and initial design decisions;
- domain vocabulary and invariants;
- architecture, workflow, testing strategy, and AI-agent rules;
- durable continuation status.

PR #2 subsequently added `docs/SOURCES.md`, ADR-0004, and mandatory source-registry maintenance before Stage 1 implementation began.

## Stage 1 — Wire foundation — In progress

Stage 1 is defined in `docs/STAGE-1.md` and is deliberately limited to the canonical wire layer.

Present on the active branch:

- ADR-0005 selects Go for the dependency-free first reference implementation;
- ADR-0006 separates resource-limit refusal from malformed NEX syntax;
- `reference/go/` contains the first executable reference codec;
- `U(n)` supports arbitrary-precision naturals through `math/big.Int`;
- the six canonical constructors `Var`, `Lam`, `App`, `Let`, `Nat`, `Prim` have an in-memory representation;
- `EncodeTerm`, `DecodeOne`, and `DecodeExact` implement the v0.1 constructor prefixes;
- decoder limits cover integer bit length, term depth, and node count;
- `conformance/wire-v0.1.json` contains language-independent integer, term, and invalid-input vectors;
- tests cover golden vectors, large naturals, trailing bits, truncation, invalid bits, resource limits, invalid encoder shapes, decode robustness, and generated round trips.

## Verified in the current work session

The Stage 1 Go code was independently constructed and executed locally before being written to the branch.

From `reference/go/`:

```text
go test ./...   PASS
go vet ./...    PASS
```

A one-second `FuzzTermRoundTrip` run completed more than 30,000 generated executions without a failure in that local run.

These are local verification results for the branch content, not yet CI results.

## Not yet verified / not yet complete

- PR #3 has not been reviewed or merged;
- no CI workflow currently re-runs the Go checks on GitHub;
- no second independent implementation has consumed `conformance/wire-v0.1.json`;
- exhaustive proof of decoder correctness is not claimed;
- de Bruijn scope validity is intentionally not checked in Stage 1;
- primitive/profile semantic validity is intentionally not checked in Stage 1;
- type inference and evaluator behavior remain unimplemented;
- comparative encoded-size claims against BLC, SKI/Jot, WebAssembly, or stack bytecode remain unmeasured hypotheses.

## Stage 1 scope guard

Stage 1 must not add:

- Algorithm W or type inference;
- evaluator semantics;
- human-oriented frontend syntax;
- optimizer passes;
- memory/system profiles;
- self-hosting compiler.

## Stage 1 definition of done

Before Stage 1 can be marked complete:

- `U(n)` conformance vectors must pass;
- canonical term vectors must pass;
- round-trip generated/property tests must pass;
- malformed/truncated input must be rejected deterministically;
- resource-limit errors must remain distinct from malformed syntax;
- conformance vectors must remain implementation-independent;
- reference verification must be repeatable from the repository;
- the final PR diff must contain no Stage 2 functionality;
- the PR must be reviewed before merge.

## Next recommended step

Review PR #3, including the wire error model and conformance vectors. If accepted, add only the minimal repository-level repeatable verification needed for Stage 1, re-run the complete checks, and then decide whether Stage 1 is ready to merge and close.
