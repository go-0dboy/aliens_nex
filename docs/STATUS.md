# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Documentation work branch:** `docs/adr-workflow`  
**Active pull request:** `#1 docs: establish ADRs and project workflow`

## Proven / present in repository

- NEX-1 Core v0.1 draft specification exists in `docs/NEX-1-v0.1.md`.
- The repository README identifies the total-information-cost design objective.
- ADR process and initial architectural rationale are present on `docs/adr-workflow`.
- Development, testing, domain-language, architecture, AI-agent, and continuation guidance are present on the same branch.
- PR #1 contains documentation/process changes only; it does not modify the NEX-1 v0.1 specification or implementation code.

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

No reference implementation exists yet. Therefore the following are hypotheses or design intentions, not verified project results:

- correctness/completeness of every detail of the v0.1 specification;
- practical size of the decoder, type checker, evaluator, or bootstrap;
- comparative encoded size versus BLC, SKI/Jot, WebAssembly, or stack bytecode;
- evaluator performance;
- self-hosting feasibility at a practical size;
- suitability of the current primitive set for the benchmark corpus.

## Known next feedback loop

The first implementation milestone should be deliberately narrow:

```text
U(n) integer codec
  -> Term wire decoder/encoder
  -> fixed conformance vectors
  -> round-trip tests
```

Do **not** begin with a full evaluator, compiler frontend, optimizer, memory profile, or self-hosting compiler.

The purpose of the first milestone is to prove that the canonical wire grammar is implementable, deterministic, and testable.

## Next recommended step

Review and merge PR #1. Then create one separate implementation PR for the integer codec + term encoder/decoder + initial golden vectors only.
