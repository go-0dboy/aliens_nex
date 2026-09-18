# ADR-0002: NEX-1 Core v0.1 design basis

- **Status:** Accepted
- **Date:** 2026-09-18

## Context

NEX needs a minimal, architecture-neutral, statically typed computational core suitable for compact transmission and eventual self-hosting. The project deliberately optimizes total information cost rather than only interpreter size:

```text
cost = specification + bootstrap implementation + transmitted programs
```

Several minimal computational models are possible, but they have different trade-offs in program size, typing, bootstrap complexity, and data representation.

## Decision drivers

- Architecture independence.
- Static type checking before execution.
- Small canonical wire representation.
- No transmitted bound-variable names.
- Direct and efficient representation of common data such as natural numbers.
- General recursion / computational universality.
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
- The first implementation must include type inference/unification rather than simply executing untyped terms.
- Machine memory, files, networking, text encoding, floating point, threads, and operating-system interaction are outside Core v0.1.
- General recursion means well-typed programs are not guaranteed to terminate.

## Alternatives considered

### Pure SKI combinatory logic

**Rejected for Core v0.1.**

SKI demonstrates an extremely small universal basis, but eliminating lambda binders can enlarge transmitted programs and does not naturally satisfy the project's static-typing objective. Minimal interpreter size alone is not the optimization target.

### Iota / Jot as the canonical language

**Rejected for Core v0.1.**

They provide impressive minimal binary universal encodings, but the same concern applies: the project wants to measure total information cost and retain a practical static type discipline rather than minimize only the universal basis.

### Untyped Binary Lambda Calculus

**Rejected as the complete language; retained as design inspiration.**

BLC strongly motivates de Bruijn indices and compact prefix encoding, but NEX requires static type rejection before execution.

### Church numerals as the only numeric representation

**Rejected.**

They are mathematically sufficient but make ordinary numeric data and arithmetic unnecessarily large or expensive. NEX represents natural numbers directly in binary.

### C-like core with pointers, fixed-width machine integers, and explicit memory

**Rejected for the universal Core.**

Such a core introduces machine assumptions too early and increases the amount of shared platform semantics that must be transmitted. Low-level machine access belongs in explicit profiles.

### Full System F / higher-rank polymorphism

**Rejected for v0.1.**

It offers more expressive polymorphism, but substantially complicates type reconstruction. NEX v0.1 prefers rank-1 let-polymorphism and a small decidable inference procedure.

### Recursive algebraic types

**Deferred.**

They would make lists, trees, and ASTs more direct, but are not required to establish computational universality. They should be added only if measurements show the reduction in program size justifies the extra specification and checker complexity.

### Linear or uniqueness types for memory

**Deferred.**

They are promising for efficient and safe destructive update, but should be evaluated only after Core semantics and the reference type checker are stable.

### DAG/content-addressed program representation

**Deferred to a transport layer.**

Sharing repeated subtrees and known libraries can reduce transmission size, but this does not need to change Core program semantics. First establish an unambiguous canonical tree representation; measure DAG/reference transport separately.

## Evidence and references

The design is informed by established work on de Bruijn indices, Binary Lambda Calculus, Hindley-Milner inference, PCF-style fixed-point recursion, and portable execution formats. The specification contains the current research references.

These references support individual mechanisms; they do **not** prove that NEX is globally optimal. Overall compactness remains a project hypothesis.

## Follow-up validation

ADR-0002 remains accepted only as the v0.1 design baseline. The project must measure it against alternatives.

The reference implementation should report at least:

- encoded bits;
- AST node count;
- type-check success/failure;
- reduction/evaluation work;
- peak implementation memory where practical;
- bootstrap implementation size.

Benchmarks should include identity, arithmetic, recursion, product/sum processing, a recognizer/parser, and eventually a NEX decoder/type checker written in NEX.

If SKI/Jot, stack bytecode, BLC, or another representation produces a materially better total cost, a new ADR may supersede this decision.
