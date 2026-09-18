# Domain language

This document defines the shared vocabulary for NEX. Terms here should be used consistently in code, tests, ADRs, and discussion.

## Core terms

### Core

The universal, architecture-neutral semantics defined by the NEX specification. Core must not assume a particular CPU, ABI, operating system, byte order, pointer representation, or text encoding.

### Term

A canonical NEX program expression. In v0.1 a term is one of `Var`, `Lam`, `App`, `Let`, `Nat`, or `Prim`.

### Wire representation

The canonical binary encoding of a Core term. Human-readable syntax is not the wire representation.

### Frontend

Any human- or machine-oriented source notation that translates to canonical NEX terms. Frontends are not part of Core unless explicitly specified.

### Profile

An explicitly defined extension boundary that connects Core to machine- or environment-specific capabilities. A profile must not silently redefine Core semantics.

### Primitive

A Core operation referenced by a stable numeric primitive ID and assigned a normative type and evaluation rule.

### de Bruijn index

A numeric reference to an enclosing binder. Bound variable names are documentation/frontend information and are not transmitted in canonical terms.

### Principal type

The most general type scheme inferred for a term under the v0.1 Hindley-Milner style type system.

### Closed program

A term in which every `Var(k)` refers to an enclosing binder.

### Bootstrap

The minimum implementation or information required for a receiver to decode, validate, type-check, and execute or compile NEX without already possessing the full NEX toolchain.

### Self-hosting

A state in which a NEX implementation is capable of processing its own implementation expressed in NEX or in a NEX-hosted frontend/toolchain.

### Conformance vector

A fixed input with a normative expected decode/type/evaluation result used to compare implementations.

## Project-level distinctions

### Established fact

A claim supported by external theory/specification or directly observed repository evidence.

### Project inference

A conclusion drawn from established facts but not independently demonstrated for NEX.

### Hypothesis

A claim the project intends to test, such as NEX producing a lower total information cost than an alternative representation.

### Verified result

A result produced by a recorded executable test, conformance run, or benchmark with enough information to reproduce it.

## Current key invariants

1. Canonical Core terms contain no bound-variable names.
2. A Core program must type-check before execution.
3. Wire decoding is deterministic and unambiguous.
4. Core semantics do not depend on host machine word size.
5. Machine/environment interaction is outside Core unless introduced by an explicit specification/ADR change.
6. Accepted architectural decisions are not silently changed by implementation convenience.
7. Compactness claims require measurement, not intuition.
