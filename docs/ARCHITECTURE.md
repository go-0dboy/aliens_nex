# Architecture

This document describes the current logical architecture of NEX. It is a living view of accepted ADRs and the normative specification; it does not replace them.

## Communication architecture

ADR-0017 separates the protocol used to **teach** NEX from the stable computational Core that the receiver is ultimately expected to use.

```text
Declared receiver prior A
            |
            v
NEX Teaching / Bootstrap Message T
            |
            | establishes meaning progressively
            v
 Reconstructed NEX-1 competence
            |
       self-test gate
            |
            v
      NEX-1 Core v0.1
            |
     canonical programs P
```

The teaching representation and the canonical Core representation are intentionally different architectural layers.

A teaching lesson may use redundancy, examples, temporary pedagogical notation, or staged encodings. None of those conventions are free: if the receiver is expected to interpret them and they are not part of the declared prior, their definition belongs to transmitted teaching material.

The canonical NEX-1 Core remains unchanged unless a later evidence-backed Core-version ADR explicitly changes it.

## Pre-Stage-6 Core self-sufficiency gate

ADR-0018 inserts the post-Stage-5 extension 5.10–5.20 before Stage 6 may become Active. This experimental layer tests self-implementation while preserving the normative NEX-1 v0.1 Core. The current boundary is: 5.10–5.12 Complete, 5.13 structural validation Planned, and Stage 6 Planned until the 5.20 decision gate. Accepted Stage 5.11/5.12 operational representations and codec programs are research/self-implementation artifacts, not new Core constructors, primitives, types, or wire rules.


## Core execution layers

```text
Optional human / machine frontend
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

Human-friendly syntax is not canonical NEX wire and is not assumed in receiver-neutral communication.

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

The type system provides natural numbers, unit, functions, products, sums, and rank-1 `Let` polymorphism. General recursion is explicit through `fix`.

The canonical dynamic strategy is weak call-by-name. Internal evaluator representation is not a portable observable.

## Teaching-layer responsibilities

Stage 6, if activated after the 5.20 gate, introduces a research layer above the Core. It owns experimental artifacts for:

```text
curriculum dependency graph
lesson serialization
pedagogical examples
transmitted self-tests
held-out interpretation tests
held-out program-construction tests
receiver experiment protocol
assumption-leak classification
teaching-message bit accounting
```

The teaching layer MUST NOT silently import:

- English or another natural language;
- Unicode/UTF-8/Markdown/JSON as receiver knowledge;
- Go/Python/runtime semantics;
- an unlisted mathematical or computational notation;
- a universal machine or rule calculus not present in the selected receiver profile.

## Core reference-implementation modules

### `term`

Owns canonical in-memory terms and de Bruijn scope rules. It does not own a human source language.

### `wire`

Owns canonical term bit encoding/decoding and the self-delimiting natural-number code.

```text
encode : Term -> Bits
decode : Bits -> Result<Term, DecodeError>
```

### `types`

Owns type terms, schemes, substitutions, free-variable operations, and unification.

### `infer`

Owns Algorithm-W-style inference over NEX terms and the primitive type environment.

```text
infer : Term -> Result<TypeScheme, TypeError>
```

### `eval`

Owns reference evaluation. It implements the specified observable semantics rather than an unrelated optimization model.

### `primitives`

Owns the stable Core primitive-ID table, type schemes, and primitive reduction rules. Type inference and evaluation must derive from one authoritative primitive contract.

### `conformance`

Owns language-neutral vectors connecting the specification to portable encode/decode/static/evaluation observations.

Under Stage 6, selected transmitted conformance examples may additionally act as receiver self-tests, but the transmitted subset and its bits must be explicitly accounted for.

### `bench`

Owns reproducible measurements. Benchmarks are not conformance evidence.

### `stage6`

Owns Stage 6 planning/teaching experiment artifacts. It is not a new language implementation and must not become an alternate source of Core semantics.

## Dependency direction

Core reference implementation:

```text
term <- wire
term <- infer <- types
term <- eval
infer <- primitives -> eval
conformance -> Core public contracts
bench -> Core public contracts
```

Teaching research:

```text
receiver assumptions -> curriculum
NEX specification/conformance -> curriculum/self-tests
curriculum -> exact teaching serialization (future)
serialization -> teaching-bit accounting (future)
held-out tasks -> receiver experiment
```

A curriculum may reference the normative Core contract, but the normative Core MUST NOT depend on the curriculum.

## Architectural guardrails

Without a separate ADR and new Core version, Stage 6 does not add:

- new NEX-1 term constructors or primitive IDs;
- incompatible wire changes;
- mutable Core memory;
- OS/system bindings;
- native code generation;
- production frontend features;
- self-hosting claims.

The teaching layer is allowed to fail, grow, reorder lessons, or use temporary pedagogical encodings without destabilizing NEX-1 v0.1. That separation is deliberate: first test how to teach the existing exact system; change the system only if the evidence later requires it.
