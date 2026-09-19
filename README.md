# aliens_nex

[Русская версия](README.ru.md)

Experimental repository for **NEX-1**: a compact, architecture-neutral, statically typed computational core for transmitting executable computational knowledge when sender and receiver cannot assume a shared programming language, processor architecture, ABI, operating system, text encoding, or host runtime.

The project objective is practical and research-oriented: **construct a formal system that an unknown receiver can be taught well enough to decode, type-check, execute, and eventually author programs in it**. Novelty is not a success criterion. Prior work is studied to improve the design.

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

A post-Stage-5 **Core self-sufficiency workstream (5.10–5.20)** is now active under ADR-0018. It tests whether the unchanged NEX-1 v0.1 Core can express a complete implementation of its own portable wire, static, and dynamic semantics before the teaching experiment begins. Stage 6 remains **Planned**.

Authoritative current state: [docs/STATUS.md](docs/STATUS.md).

## Primary documents

- [NEX-1 Core v0.1 specification](docs/NEX-1-v0.1.md) / [Russian translation](docs/NEX-1-v0.1.ru.md)
- [Post-Stage-5 self-sufficiency plan](docs/STAGE-5-EXTENSION.md)
- [Stage 6 teaching plan](docs/STAGE-6.md)
- [Architecture](docs/ARCHITECTURE.md) / [Russian translation](docs/ARCHITECTURE.ru.md)
- [Living research dissertation](docs/RESEARCH-DISSERTATION.md) / [Russian translation](docs/RESEARCH-DISSERTATION.ru.md)
- [Post-Stage-5 research audit](docs/RESEARCH-AUDIT-2026-09-19.md) / [Russian mirror](docs/RESEARCH-AUDIT-2026-09-19.ru.md)
- [Related work: teaching computation to an unknown receiver](docs/RELATED-WORK.md) / [Russian mirror](docs/RELATED-WORK.ru.md)
- [Research source registry](docs/SOURCES.md)
- [Current continuation status](docs/STATUS.md)
- [Development workflow](docs/WORKFLOW.md)
- [Testing and conformance](docs/TESTING.md)
- [Architecture Decision Records](docs/adr/README.md)
- [AI agent instructions](AGENTS.md)

English is canonical. README, specification, architecture overview, dissertation, research audit, and related-work comparison maintain Russian mirrors where required by the documentation policy.

## NEX-1 v0.1 Core

The stable Core defines:

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

Stages 4–5, the post-stage audit, and the current self-sufficiency experiment do **not** change this normative v0.1 object.

## Research objective and accounting

The historical shorthand is:

```text
C = S + B + P
```

The re-audit makes the exact interpretation stricter. A numerical total is meaningful only for one concrete transmitted object under declared receiver assumptions `A`:

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

The accepted interpretation is **strong differential-conformance evidence of reconstructability on the tested surface**, not a proof of semantic correctness or specification completeness.

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

These profiles are experimental conditions, not claims about what an extraterrestrial intelligence necessarily knows. No accepted complete receiver-neutral bootstrap currently exists, so full `B | A` and total `C | A` remain unknown.

## Pre-Stage-6 self-sufficiency gate

ADR-0018 requires executable evidence before Stage 6 activation. The workstream is:

```text
5.10 contract/gate
5.11 NEX-in-NEX meta-representation
5.12 self wire codec
5.13 self structural validation
5.14 self HM inference
5.15 self evaluator
5.16 integrated NEX-in-NEX toolchain
5.17 self-processing
5.18 bounded/differential validation
5.19 supporting metatheory
5.20 decision gate
```

The first 5.11 candidate represents every frozen meta-object through NEX `N`, using numeric encodings for finite products, sequences, terms, types, schemes, and results. This deliberately tests the existing Core before considering recursive types or new primitives.

The target is a canonical NEX implementation `I` that can decode/encode, validate, infer, evaluate, and process its own canonical representation. A native x86/ARM/WASM compiler is not required by this architecture-neutral gate.

## Related work and design lessons

The project explicitly compares itself with Lincos, the DeVito–Oehrle science-based language, Lingua Cosmica, and especially CosmicOS. The purpose is to learn from prior approaches, not to establish priority.

The comparison suggests a two-layer teaching architecture that remains planned after the self-sufficiency gate:

```text
NEX Teaching / Bootstrap Message
        |
        | progressively establishes meaning
        v
NEX-1 Core
        |
        | canonical typed programs
        v
subsequent computation
```

CosmicOS is especially relevant because it already treats the message as an executable curriculum: mathematics and logic are introduced first, then programs and simulations. NEX's complementary strength is the exact final target: a typed binary Core with explicit semantics, conformance tests, independent reconstruction evidence, and bit accounting.

See [docs/RELATED-WORK.md](docs/RELATED-WORK.md) for the full comparison.

## Important current limitations

The project does not yet establish:

- global minimality or global superiority over BLC/other bases;
- formal NEX-specific type safety;
- a formal NEX-specific CBN/call-by-need equivalence theorem;
- representativeness of the 17-program design corpus;
- a complete NEX-in-NEX self-implementation;
- a complete receiver-neutral teaching/bootstrap message;
- numerical total `C | A`.

The Stage 4 transition reduction `226151 -> 2484` is an evaluator transition-counter result, not a 98.90% wall-clock speedup claim.

## Next research direction

The immediate research task is **Core self-sufficiency**, not receiver teaching and not an immediate Core redesign.

The current question is:

> Can the unchanged NEX-1 v0.1 Core implement its own canonical codec, validation, rank-1 HM inference, and weak call-by-name evaluator, and then process that implementation's own canonical representation?

If the 5.20 gate supports the Core, Stage 6 then resumes the already planned question:

> What finite transmitted sequence can take a receiver from an explicit prior profile to demonstrable ability to decode, type-check, execute, and construct NEX programs?

The repository remains the source of truth. New measurements, falsifications, formal results, and literature corrections must update durable project documents rather than relying on chat history.
