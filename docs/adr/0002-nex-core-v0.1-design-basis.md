# ADR-0002: NEX-1 Core v0.1 design basis

- **Status:** Accepted
- **Date:** 2026-09-18
- **Post-Stage-5 clarification:** 2026-09-19, see ADR-0016

## Context

NEX needs a compact, architecture-neutral, statically typed computational core suitable for compact transmission and eventual self-hosting. The project deliberately studies total transmitted information rather than only interpreter size:

```text
C = S + B + P
```

This expression is a conceptual ledger. After the Stage 5 literature re-audit, exact claims are conditioned on an explicit receiver profile and concrete transmitted object; see ADR-0016.

Several computational models are possible, with different trade-offs in program size, typing, bootstrap complexity, and data representation.

## Decision drivers

- Architecture independence.
- Static type checking before execution.
- Compact canonical wire representation.
- No transmitted bound-variable names.
- Direct representation of common data such as natural numbers.
- General recursion / general-purpose computational expressiveness.
- A type checker small enough to implement independently.
- Separation of universal computation from machine/environment details.

## Decision

NEX-1 Core v0.1 is based on:

1. unannotated lambda abstraction and application;
2. zero-based de Bruijn indices for bound variables;
3. Hindley-Milner style rank-1 let-polymorphism;
4. arbitrary-precision natural numbers as a primitive type;
5. products and sums exposed through typed primitives;
6. explicit general recursion through a typed `fix` primitive;
7. six term constructors: `Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`;
8. a canonical prefix binary encoding;
9. separation between Core and optional machine/environment profiles.

The normative details live in `docs/NEX-1-v0.1.md`.

## Accepted consequences

- NEX Core is not intended to resemble C, C++, Rust, or another conventional surface language.
- Human-friendly syntax is a frontend concern and is not part of the canonical wire language.
- The first implementation includes type inference/unification rather than simply executing untyped terms.
- Machine memory, files, networking, text encoding, floating point, threads, and operating-system interaction are outside Core v0.1.
- General recursion means well-typed programs are not guaranteed to terminate.
- The word `minimal` in early project prose is not an optimality theorem; the current research terminology is **compact experimental core**.

## Alternatives considered

### Pure SKI / typed combinatory logic

**Rejected for Core v0.1; retained as a serious comparison family.**

The original version of this ADR understated the compatibility of combinatory logic with static typing. That rationale is corrected by ADR-0016 and SRC-0018: Hindley's 1969 work establishes principal type-scheme results directly for combinatory logic. Therefore NEX does **not** reject SK/SKI because it is intrinsically untypable or incompatible with principal types.

The remaining reasons for the v0.1 decision are empirical/design trade-offs:

- eliminating binders through bracket abstraction can enlarge transmitted terms under a given translation;
- NEX wants direct `Let` polymorphism, natural literals, and typed data operations rather than encoding all of them through a tiny basis;
- a smaller primitive basis does not by itself imply smaller total `S+B+P`.

Future typed-combinator baselines remain valuable and may outperform NEX under some workloads or bootstrap assumptions.

### Iota / Jot as the canonical language

**Rejected for Core v0.1; retained as a compact-basis baseline.**

They demonstrate extremely small universal encodings, but basis size alone is not the optimization target. Stage 4 measures one deterministic Jot translation and explicitly does not claim it is shortest.

### Untyped Binary Lambda Calculus

**Rejected as the complete typed language; retained as design inspiration and baseline.**

BLC strongly motivates compact binary de Bruijn syntax and remains a serious bootstrap candidate. NEX separately requires static rejection and direct typed data operations.

### Church numerals as the only numeric representation

**Rejected.**

They are mathematically sufficient but make ordinary numeric data/arithmetic large under the tested representation. NEX represents natural numbers directly. This does not claim Elias gamma or `Nat` is globally optimal among all integer representations.

### C-like core with pointers, fixed-width integers, and explicit memory

**Rejected for the universal Core.**

Such a core introduces machine assumptions too early. Low-level machine access belongs in explicit profiles.

### Full System F / higher-rank polymorphism

**Rejected for v0.1.**

It is more expressive but substantially complicates implicit type reconstruction. NEX v0.1 prefers rank-1 HM and a small decidable inference procedure.

### Recursive algebraic types

**Deferred.**

They would make lists, trees, and ASTs more direct but should be justified by measured total-cost effects.

### Linear or uniqueness types for memory

**Deferred.**

They remain promising for safe destructive update, but a future effectful profile must also revisit ordinary HM generalization; see SRC-0025.

### DAG/content-addressed program representation

**Deferred to a transport layer.**

Sharing repeated subtrees and known libraries can reduce transmission size without changing Core semantics. First establish an unambiguous canonical tree representation; measure DAG/reference transport separately.

## Evidence and references

The design is informed by de Bruijn indices, Binary Lambda Calculus, HM inference, PCF-style recursion, and compact binary languages. SRC-0018 corrects the earlier implication that typed combinatory logic is an unsuitable static-typing competitor.

These sources support individual mechanisms; they do **not** prove that NEX is globally optimal. Overall compactness remains a research hypothesis.

## Follow-up validation

ADR-0002 remains the v0.1 design baseline. Before a Core redesign, the project should prioritize:

- broader and hold-out workload families;
- NEX-specific type-safety metatheory;
- bounded exhaustive cross-implementation testing for small terms;
- a dependency-closed bootstrap artifact under an explicit receiver profile;
- typed combinator and other controlled alternatives where total accounting is possible.

If another representation produces materially better total cost under a declared and comparable accounting model, a new ADR may supersede this design.
