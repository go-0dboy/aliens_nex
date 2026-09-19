# Stage 5.11 — NEX-in-NEX meta-representation candidate

## Status

Implementation checkpoint for the post-Stage-5 self-sufficiency workstream introduced by ADR-0018.

Machine-readable contract:

```text
stage5/selfhost/meta-representation-v0.1.json
```

Validator:

```text
python stage5/selfhost/validate_meta_representation.py
```

This checkpoint does **not** claim self-hosting. It establishes the first prerequisite: finite internal representations for the data that a NEX implementation of NEX will need.

## Problem

NEX-1 v0.1 has no recursive algebraic type former, host string, byte array, object graph, mutable heap, or built-in list type. A self-interpreter therefore cannot assume the host AST/list/type objects used by the Go or Python implementations.

The relevant question is not whether those conveniences would make the implementation easier. The question for 5.11 is whether the existing Core can represent the required finite data at all without modification.

## Candidate decision

The first candidate deliberately uses only the existing mathematical natural-number value `N` as the physical carrier for every meta-object.

Finite products use the bijection:

```text
pair(a,b) = 2^a * (2*b + 1) - 1
```

For `z = pair(a,b)`, let:

```text
n = z + 1
a = v2(n)
b = ((n / 2^a) - 1) / 2
```

where `v2` counts factors of two. This gives a bijection `N x N <-> N`.

Finite sequences are encoded recursively:

```text
[]              = 0
head :: tail    = 1 + pair(head, encode(tail))
```

This permits arbitrary finite trees to be represented through tags plus numeric payloads while every runtime carrier remains `N`.

## Why the derived arithmetic does not add Core features

The representation requires derived functions such as:

```text
add
mul
pow2
halve
is_even
v2
```

They are not proposed as primitives. They are ordinary total recursive functions over natural numbers and are intended to be written using the existing NEX basis:

```text
fix
succ
pred
ifz
```

Whether this representation is efficient is a later measurement question. Stage 5.11 only establishes a candidate closure construction.

## Meta-objects covered

The v0.1 contract defines N-carried encodings for:

```text
Bits
Term
Type
Scheme
Substitution
TypeEnvironment
PortableObservation
StaticResult
ToolRequest
ToolResult
```

A separate runtime-state object is not frozen yet because the self evaluator may use substitution-based semantics instead of an encoded closure environment. If 5.15 needs additional finite state, it must be added through a new version of this contract rather than assumed silently.

## Term representation

Terms use numeric tags matching the six Core constructors:

```text
0 Var
1 Lam
2 App
3 Let
4 Nat
5 Prim
```

Unary payloads are encoded directly. Binary payloads are encoded with `pair(left,right)`.

Unknown tags are malformed meta-representation, not unknown NEX wire constructors.

## Type representation

Types use:

```text
0 TypeVar
1 Unit
2 Nat
3 Arrow
4 Product
5 Sum
```

Type variables carry numeric IDs. `Unit` and `Nat` require payload zero. Binary type formers carry a paired payload.

Schemes pair a canonical finite sequence of quantified IDs with a type code. Portable comparison may alpha-normalize bound IDs to `0..k-1`.

## Canonicality and failure classes

The candidate keeps these distinctions explicit:

- malformed meta-representation;
- malformed canonical NEX wire;
- invalid de Bruijn scope;
- unknown Core primitive;
- type error;
- external evaluator resource refusal.

Resource refusal is deliberately not serialized as semantic invalidity.

## Verification performed by the validator

The validator checks:

1. exact NEX-1 v0.1 constructor/type/primitive dependency inventory;
2. zero additional Core features;
3. every frozen meta-object has physical carrier `N`;
4. tag sets are unique and dense;
5. declared pair examples and bounded pair round trips;
6. bounded pair injectivity;
7. declared sequence examples and round trips;
8. all bit sequences of length `0..5` round-trip;
9. the forbidden-dependency guard remains present.

This is bounded executable evidence for the representation contract, not a formal proof that the eventual NEX implementation is correct or efficient.

## Current inference

The first self-hosting obstacle does **not** currently require recursive types or a new collection primitive: finite meta-objects have a concrete N-only encoding candidate.

That statement is deliberately narrow. We have not yet implemented the pair/sequence operations in NEX, measured their cost, or demonstrated the self wire codec.

## Next step

Stage 5.12 must implement the arithmetic/sequence foundation and then the canonical NEX `U(n)` and term wire codec as NEX programs against this frozen representation, comparing them with the Go/Python controls.
