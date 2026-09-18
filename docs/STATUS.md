# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Current stage:** `Stage 0 — Complete`  
**Completed by:** PR `#1 docs: establish ADRs and project workflow`  
**Stage 0 merge commit:** `6183546a8fe6a26e6092bd65b87d8916594899ad`

## Stage 0 — Complete

Stage 0 established the project baseline before implementation work begins.

Completed:

- NEX-1 Core v0.1 draft specification exists in `docs/NEX-1-v0.1.md`;
- Russian mirrors exist for the project overview, NEX-1 v0.1 specification, and architecture overview;
- ADR-0001 establishes Architecture Decision Records as durable project memory;
- ADR-0002 records the NEX-1 v0.1 design basis, including accepted, rejected, and deferred alternatives;
- ADR-0003 defines English as canonical documentation and requires maintained Russian mirrors for primary documents;
- `docs/DOMAIN.md` defines shared terminology and project invariants;
- `docs/ARCHITECTURE.md` defines the initial logical architecture and module boundaries;
- `docs/WORKFLOW.md` defines the development feedback loop;
- `docs/TESTING.md` defines testing and conformance strategy;
- `AGENTS.md` defines repository rules for AI-assisted work;
- this `STATUS.md` file defines the continuation checkpoint between work sessions.

No reference implementation was part of Stage 0.

## Current architectural baseline

NEX-1 Core v0.1 currently assumes:

- six term constructors: `Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`;
- zero-based de Bruijn indices;
- Hindley-Milner style rank-1 let-polymorphism;
- direct natural numbers;
- typed general recursion via `fix`;
- canonical prefix binary encoding;
- strict separation of Core from machine/environment profiles.

See ADR-0002 for accepted, rejected, and deferred alternatives.

## Not yet verified

No reference implementation exists yet. Therefore the following remain hypotheses or design intentions rather than verified project results:

- correctness/completeness of every detail of the v0.1 specification;
- practical size of the decoder, type checker, evaluator, or bootstrap;
- comparative encoded size versus BLC, SKI/Jot, WebAssembly, or stack bytecode;
- evaluator performance;
- self-hosting feasibility at a practical size;
- suitability of the current primitive set for the benchmark corpus.

## Stage 1 — Wire foundation

The next stage is deliberately narrow:

```text
U(n) integer codec
  -> Term wire decoder/encoder
  -> fixed conformance vectors
  -> round-trip tests
  -> deterministic malformed-input rejection
```

Stage 1 must not include:

- full evaluator;
- type inference;
- compiler frontend;
- optimizer;
- memory/system profile;
- self-hosting compiler.

The purpose of Stage 1 is to prove that the canonical wire grammar is implementable, deterministic, reversible for valid terms, and testable.

## Next recommended step

Create a dedicated Stage 1 implementation branch and PR for the `U(n)` codec, canonical `Term` encoder/decoder, and initial golden/conformance vectors only.
