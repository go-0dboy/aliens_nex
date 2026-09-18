# Architecture

This document describes the current logical architecture of the NEX project. It is a living view of the accepted ADRs and specification; it does not replace them.

## Layers

```text
Human / machine frontend syntax
            |
            v
      Canonical NEX terms
            |
     +------+------+
     |             |
     v             v
 Type inference   Wire codec
     |             |
     +------+------+
            |
            v
        Core evaluator
            |
            v
   Optional execution profiles
            |
            v
      Host / target machine
```

## Core model

NEX-1 Core v0.1 has six canonical term constructors:

```text
Var
Lam
App
Let
Nat
Prim
```

The type system provides natural numbers, unit, functions, products, sums, and rank-1 let-polymorphism.

General recursion is explicit through the `fix` primitive.

## Module boundaries for the reference implementation

The first implementation should be split into modules with narrow contracts.

### `term`

Owns the canonical in-memory term representation and de Bruijn scope rules.

Must not know about parsing a human source language.

### `wire`

Owns canonical bit encoding/decoding and self-delimiting natural-number encoding.

Contract:

```text
encode : Term -> Bits
decode : Bits -> Result<Term, DecodeError>
```

The decoder must reject malformed or trailing-invalid representations according to the specification.

### `types`

Owns type terms, type schemes, substitutions, free-type-variable operations, and unification.

### `infer`

Owns Algorithm-W-style inference over NEX terms and the primitive type environment.

Contract:

```text
infer : Term -> Result<TypeScheme, TypeError>
```

### `eval`

Owns the reference evaluation semantics.

It must implement the specified observable semantics, not an unrelated optimization model.

### `primitives`

Owns the stable Core primitive ID table, type schemes, and primitive reduction rules.

There must be one authoritative primitive table conceptually; type inference and evaluation must not drift into separately maintained incompatible definitions.

### `conformance`

Owns normative/golden vectors that exercise decode, encode, type inference, rejection, and evaluation.

### `bench`

Owns reproducible measurements. Benchmarks must not be mixed with conformance claims.

## Dependency direction

Preferred dependency direction:

```text
term <- wire
term <- infer <- types
term <- eval
infer <- primitives -> eval
conformance -> all public contracts
bench -> public contracts
```

Avoid circular dependencies between evaluator, type inference, and wire codec.

## Out of scope for the first reference implementation

The first implementation should not add unless an ADR explicitly changes scope:

- a C-like or Rust-like frontend;
- native code generation;
- mutable host memory model;
- operating-system bindings;
- recursive algebraic types;
- linear types;
- DAG/content-addressed transport;
- optimizer passes.

These may be useful later, but they would weaken the first feedback loop: prove the Core specification first.
