# aliens_nex

[Русская версия](README.ru.md)

Experimental repository for **NEX-1**: a compact, architecture-neutral, statically typed computational core for studying information-efficient transmission of programs when sender and receiver cannot assume a shared programming language, processor architecture, ABI, operating system, text encoding, or host runtime.

NEX is a research system. **Compact** is a design objective, not a proof of global minimality.

## Current status

Stages 0–5 are complete. NEX-1 v0.1 currently has:

- canonical binary encode/decode and language-neutral wire conformance;
- closed-scope validation and rank-1 Hindley–Milner inference;
- weak call-by-name normative semantics;
- a Go reference implementation;
- an independently produced Python implementation frozen before Go comparison;
- frozen empirical corpora and Stage 4 comparison tooling;
- post-freeze Go/Python differential conformance;
- explicit receiver-assumption and bootstrap-accounting models;
- a negative complete-bootstrap result: no accepted receiver-neutral `B | A` exists yet;
- a living bilingual dissertation and a post-Stage-5 literature re-audit.

Authoritative current state: [docs/STATUS.md](docs/STATUS.md).

The 2026-09-19 full literature re-audit is recorded in:

- [Canonical audit](docs/RESEARCH-AUDIT-2026-09-19.md)
- [Russian mirror](docs/RESEARCH-AUDIT-2026-09-19.ru.md)
- [ADR-0016](docs/adr/0016-post-stage5-literature-reaudit-corrections.md)

## Primary documents

- [NEX-1 Core v0.1 specification](docs/NEX-1-v0.1.md) / [Russian translation](docs/NEX-1-v0.1.ru.md)
- [Architecture](docs/ARCHITECTURE.md) / [Russian translation](docs/ARCHITECTURE.ru.md)
- [Living research dissertation](docs/RESEARCH-DISSERTATION.md) / [Russian translation](docs/RESEARCH-DISSERTATION.ru.md)
- [Post-Stage-5 research audit](docs/RESEARCH-AUDIT-2026-09-19.md) / [Russian mirror](docs/RESEARCH-AUDIT-2026-09-19.ru.md)
- [Research source registry](docs/SOURCES.md)
- [Current continuation status](docs/STATUS.md)
- [Development workflow](docs/WORKFLOW.md)
- [Testing and conformance](docs/TESTING.md)
- [Architecture Decision Records](docs/adr/README.md)
- [AI agent instructions](AGENTS.md)

English is canonical. README, specification, architecture overview, dissertation, and the post-Stage-5 audit maintain Russian mirrors according to the documentation policy.

## NEX-1 v0.1 Core

The current Core defines:

- six term constructors: `Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`;
- zero-based de Bruijn indices;
- rank-1 HM let-polymorphism;
- arbitrary-precision naturals;
- functions, product/sum primitives, and unit;
- explicit general recursion through `fix`;
- eleven fixed Core primitives;
- a canonical prefix binary representation;
- weak call-by-name normative evaluation;
- strict separation between Core and optional machine/environment profiles.

Stages 4–5 and the post-stage audit did **not** change this normative v0.1 object.

## Research objective and accounting

The historical shorthand is:

```text
C = S + B + P
```

but the re-audit makes the exact interpretation explicit. A numerical total is meaningful only for one concrete transmitted object under declared receiver assumptions `A`:

```text
C | A = |M_A|
```

When transmitted roles are defensibly separable:

```text
C | A = (S | A) + (B | A,S) + (P | A,S,B)
```

and if specification/bootstrap are inseparable:

```text
C | A = (SB | A) + (P | A,SB)
```

Every transmitted bit is counted once. Host Go/Python source size is not silently converted into receiver-neutral bootstrap cost.

For frozen corpus v0.3, canonical program payload remains exactly:

```text
17 programs
345 AST nodes
1371 bits
```

This is an exact NEX wire length under the fixed v0.1 contract, not an unconditional machine-free information quantity.

## Stage 5 evidence

The independently produced Python implementation was frozen before access to `reference/go`. Post-freeze comparison yielded:

```text
942 portable matches
0 semantic mismatches
0 resource asymmetries
```

The re-audit narrows the interpretation: this is strong **differential-conformance evidence of reconstructability on the tested surface**, not a proof of semantic correctness or specification completeness.

The 942 cases consist of:

```text
17   frozen corpus programs
325  valid cases from 13 structural templates over 25 parameter sets
100  static-error cases from 4 error families over 25 parameter sets
500  randomized term shapes tested at wire level
```

## Receiver assumptions

Historical Stage 5 evidence is preserved in `assumptions-v0.1.json`. The corrected current model is `stage5/receiver-assumptions/assumptions-v0.2.json`:

```text
A0       exact binary-frame prior
A1       elementary discrete mathematics only
A1(R)    A1 + exact formal rule calculus R
A2(U)    A1 + exact universal binary machine U and framing
A_host(H) terrestrial engineering control only
```

No accepted complete receiver-neutral bootstrap currently exists, so full `B | A` and total `C | A` remain unknown.

## Related work and novelty boundary

NEX does **not** claim to have invented formal interstellar languages, executable interstellar messages, or types in extraterrestrial-message research. The maintained literature now explicitly includes:

- Freudenthal's **Lincos**;
- **CosmicOS**, which bootstraps programs and simulations;
- Lingua Cosmica work using constructive type theory;
- typed combinatory logic;
- MDL/algorithmic-description literature;
- call-by-need equivalence and differential-testing limitations.

The narrower candidate contribution is the combination of compact typed binary Core, exact wire accounting, explicit receiver-conditioned bootstrap accounting, frozen comparative experiments including negative results, and blind independent reconstruction.

## Important current limitations

The project does not yet establish:

- global minimality or global superiority over BLC/other bases;
- formal NEX-specific type safety;
- a formal NEX-specific CBN/call-by-need equivalence theorem;
- representativeness of the 17-program design corpus;
- a complete receiver-neutral bootstrap;
- numerical total `C | A`.

The Stage 4 transition reduction `226151 -> 2484` is an evaluator transition-counter result, not a 98.90% wall-clock speedup claim.

## Next research direction

Before an incompatible NEX-1 redesign, the post-Stage-5 audit recommends:

1. NEX-specific preservation/canonical-forms/progress-or-safety metatheory;
2. formal or mechanized call-by-need observational preservation for the exact Core;
3. bounded exhaustive small-term cross-implementation testing;
4. hold-out and independently specified workload families;
5. one dependency-closed bootstrap under `A1(R)` or `A2(U)`.

The repository remains the source of truth. New measurements, falsifications, formal results, and literature corrections must update the research manuscript and source registry rather than relying on chat history.
