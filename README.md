# aliens_nex

[Русская версия](README.ru.md)

Experimental repository for **NEX-1**: a minimal, architecture-neutral, statically typed language for compact transmission of programs between systems that do not share a programming language, processor architecture, ABI, operating system, or textual notation.

## Current status

The project is at the specification stage.

The normative draft is:

- [NEX-1 Core v0.1 specification](docs/NEX-1-v0.1.md)
- [Russian translation of NEX-1 Core v0.1](docs/NEX-1-v0.1.ru.md)

Project working documents:

- [Architecture](docs/ARCHITECTURE.md) / [Russian translation](docs/ARCHITECTURE.ru.md)
- [Domain language and invariants](docs/DOMAIN.md)
- [Development workflow](docs/WORKFLOW.md)
- [Testing and conformance](docs/TESTING.md)
- [Current continuation status](docs/STATUS.md)
- [Architecture Decision Records](docs/adr/README.md)
- [AI agent instructions](AGENTS.md)

English is the canonical documentation language. The project overview, language specification, and architecture overview have maintained Russian mirrors according to ADR-0003.

NEX-1 v0.1 currently defines:

- six Core term constructors: `Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`;
- zero-based de Bruijn indices, so bound variable names are not transmitted;
- Hindley-Milner style rank-1 let-polymorphism;
- natural numbers, functions, products, sums, and unit;
- explicit general recursion through `fix`;
- eleven fixed Core primitives;
- a canonical prefix-free binary wire encoding;
- weak call-by-name reference semantics;
- a strict separation between the universal Core and machine/environment profiles.

## Design goal

NEX does not try to minimize only the interpreter or only source-code syntax. The intended optimization target is the total information cost:

```text
cost = specification + bootstrap implementation + transmitted programs
```

This is why the project does not simply reduce everything to SKI combinators or machine instructions. The hypothesis is that a small typed lambda core with de Bruijn indices and direct binary data representation can provide a better overall trade-off.

## Project memory and decisions

The repository is the project source of truth. Durable architectural reasoning belongs in ADRs, including rejected and deferred alternatives. Chat history is not relied on as architectural memory.

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

## Next milestone

The first implementation milestone is intentionally smaller than a complete interpreter:

1. implement the self-delimiting `U(n)` integer codec;
2. implement canonical `Term` wire encoding/decoding;
3. add fixed conformance/golden vectors;
4. prove round-trip behavior with automated tests;
5. reject malformed encodings deterministically.

Only after that feedback loop is green should the project add de Bruijn validation, Algorithm W type inference, and the evaluator as separate stages.

See `docs/STATUS.md` for the current continuation point.

## Research basis

NEX-1 is an experimental design built from established ideas including:

- de Bruijn indices;
- Binary Lambda Calculus;
- Hindley-Milner type inference;
- PCF-style typed general recursion;
- separation of portable computation from host/environment embedding.

Primary references are listed in the specification.

## Repository policy at this stage

Until measurements exist, claims such as “smallest language”, “smallest compiler”, or fixed bootstrap sizes should be treated as hypotheses, not project facts.
