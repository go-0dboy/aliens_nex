# aliens_nex

[Русская версия](README.ru.md)

Experimental repository for **NEX-1**: a minimal, architecture-neutral, statically typed language for compact transmission of programs between systems that do not share a programming language, processor architecture, ABI, operating system, or textual notation.

## Current status

NEX-1 v0.1 now has an executable research baseline covering canonical wire encoding, static validation/type inference, dynamic semantics, language-neutral conformance artifacts, frozen benchmark corpora, and empirical comparison tooling.

Stages 0–3 are complete. Stage 4 — empirical validation and benchmarking — is implementation-complete on PR #6 and pending merge review. See [Current continuation status](docs/STATUS.md) for the authoritative checkpoint.

Primary documents:

- [NEX-1 Core v0.1 specification](docs/NEX-1-v0.1.md) / [Russian translation](docs/NEX-1-v0.1.ru.md)
- [Architecture](docs/ARCHITECTURE.md) / [Russian translation](docs/ARCHITECTURE.ru.md)
- [Living research dissertation](docs/RESEARCH-DISSERTATION.md) / [Russian translation](docs/RESEARCH-DISSERTATION.ru.md)
- [Domain language and invariants](docs/DOMAIN.md)
- [Development workflow](docs/WORKFLOW.md)
- [Testing and conformance](docs/TESTING.md)
- [Research sources registry](docs/SOURCES.md)
- [Current continuation status](docs/STATUS.md)
- [Architecture Decision Records](docs/adr/README.md)
- [AI agent instructions](AGENTS.md)

English is the canonical documentation language. The project overview, language specification, architecture overview, and research dissertation have maintained Russian mirrors according to ADR-0003 and ADR-0012.

NEX-1 v0.1 currently defines:

- six Core term constructors: `Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`;
- zero-based de Bruijn indices, so bound variable names are not transmitted;
- Hindley-Milner style rank-1 let-polymorphism;
- natural numbers, functions, products, sums, and unit;
- explicit general recursion through `fix`;
- eleven fixed Core primitives;
- a canonical prefix-free binary wire encoding;
- weak call-by-name normative reference semantics;
- a strict separation between the universal Core and machine/environment profiles.

## Design and research goal

NEX does not try to minimize only the interpreter or only source-code syntax. The intended optimization target is the total information cost:

```text
C = S + B + P
```

where `S` is receiver-neutral specification cost, `B` is receiver-neutral bootstrap cost, and `P` is transmitted program cost.

Stage 4 establishes that `P` can be measured exactly for frozen corpora, while a defensible receiver-neutral `S` and especially `B` are still unresolved. Therefore the project does **not** claim that NEX is globally smallest, globally better than Binary Lambda Calculus, or already optimal under total information cost.

The current research manuscript synthesizes the project from its initial problem statement through Stages 0–4, including positive, negative, and unresolved findings:

- [Canonical research dissertation](docs/RESEARCH-DISSERTATION.md)
- [Russian mirror](docs/RESEARCH-DISSERTATION.ru.md)

Per ADR-0012, the dissertation is a living research record and must be enriched when new reproducible measurements, significant architectural conclusions, independent conformance results, falsifications, or `S/B/P/C` evidence become available.

## Project memory and decisions

The repository is the project source of truth. Durable architectural reasoning belongs in ADRs, including rejected and deferred alternatives. Chat history is not relied on as architectural memory.

External technical sources that materially influence specifications, ADRs, algorithms, standards choices, or benchmark baselines are tracked in `docs/SOURCES.md` under ADR-0004.

Implementation work follows the feedback loop defined in `docs/WORKFLOW.md`:

```text
Problem
  -> Contract
  -> Invariant
  -> Failing test / executable example
  -> Implementation
  -> Verification
  -> Diff review
  -> Status checkpoint
  -> Research synthesis checkpoint when evidence changed
```

## Important non-goals for v0.1

Core v0.1 intentionally does not define:

- pointers or mutable machine memory;
- files, sockets, display, keyboard, or operating-system calls;
- Unicode or strings;
- floating point;
- threads or atomics;
- exceptions, objects, classes, or modules;
- a human-oriented source language.

These belong in libraries, frontends, or explicit execution profiles rather than the universal Core.

## Evidence accumulated so far

The current repository contains:

- canonical wire encode/decode with golden/conformance vectors;
- closed-scope validation and HM principal type inference;
- a weak call-by-name Core evaluator and evaluation conformance;
- experimental call-by-need comparison preserving the tested observable results;
- frozen benchmark corpora and constructor-level wire accounting;
- internal `Let` and `Nat` experiments;
- an experimental type-information envelope;
- BLC, Jot-translation, and structural stack baselines with explicit comparison limits;
- machine-readable total-information accounting that keeps unknown bootstrap cost unknown;
- a consolidated reproducible Stage 4 report.

The latest measured conclusions and limitations are maintained in `docs/STATUS.md` and synthesized in the research dissertation.

## Research basis

NEX-1 is an experimental design built from established ideas including:

- de Bruijn indices;
- Binary Lambda Calculus;
- Hindley-Milner type inference and principal type schemes;
- PCF-style typed general recursion;
- universal/self-delimiting integer coding;
- call-by-name and lazy evaluation research;
- separation of portable computation from host/environment embedding.

The maintained research bibliography and usage notes are in [docs/SOURCES.md](docs/SOURCES.md). Primary references are cited in the dissertation, specification, and ADRs where relevant.

## Next research direction

After Stage 4 is reviewed and merged, the highest-value unresolved evidence is not another immediate Core expansion. The next design discussion should focus on:

1. an independent conformance implementation built from the specification rather than the Go implementation; and
2. a genuinely receiver-neutral bootstrap/specification experiment capable of making `B`, and eventually total `C`, measurable.

Any incompatible NEX-1 redesign should remain deferred until that evidence is considered.
