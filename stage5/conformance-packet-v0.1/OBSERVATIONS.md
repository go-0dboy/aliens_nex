# Portable conformance observations for packet v0.1

This file defines comparison formatting needed by the Stage 5 independent-conformance experiment. It does **not** add NEX language semantics.

## 0. Conformance JSON term fixtures

JSON is only the fixture representation used by the conformance packet. It is not NEX source syntax and is not the canonical wire format.

Map packet JSON objects to the abstract six-constructor `Term` grammar exactly as follows:

```text
{"kind":"Var",  "value":"K"} -> Var(K)
{"kind":"Lam",  "a":TERM}      -> Lam(TERM)
{"kind":"App",  "a":F, "b":X} -> App(F,X)
{"kind":"Let",  "a":V, "b":B} -> Let(V,B)
{"kind":"Nat",  "value":"N"} -> Nat(N)
{"kind":"Prim", "value":"P"} -> Prim(P)
```

`value` fields are decimal strings denoting non-negative mathematical integers and must not be restricted to the host machine integer width.

Unknown `kind` values or missing constructor fields are malformed **fixture data**. They are not NEX wire-error cases unless an explicit wire vector describes the corresponding bit stream.

## 1. Principal type scheme text

`conformance/static-v0.1.json` stores expected principal types as text. NEX-1 v0.1 defines principal types up to renaming of type variables, but the normative specification does not otherwise require a host implementation to use the same internal type-variable IDs.

For packet comparison only, normalize a successful closed principal type scheme as follows.

### 1.1 Type variable names

Rename quantified variables to:

```text
T0, T1, T2, ...
```

in order of first occurrence while traversing the scheme body from left to right.

Internal fresh-variable numbers are never observable.

### 1.2 Quantifier rendering

If the normalized scheme has quantified variables, render:

```text
forall T0 T1 ... . BODY
```

with a single space between variable names and after the period.

If there are no quantified variables, render only `BODY`.

### 1.3 Monotype rendering

Use exactly:

```text
1
N
T0
(A -> B)
(A * B)
(A + B)
```

Function, product, and sum nodes are fully parenthesized. No precedence convention is needed.

### 1.4 Alpha-equivalence

The canonical text is only a conformance observation. Two inferred schemes that differ solely in internal variable IDs are semantically the same before normalization.

## 2. Error observations

Where a packet vector specifies an error label, compare the portable class only:

```text
out_of_scope
unknown_primitive
type_mismatch
occurs_check
```

Host exception classes, stack traces, diagnostic wording, and internal error structures are not portable observations.

Wire conformance uses the error categories already encoded by `wire-v0.1.json`; implementation-specific details are not compared.

## 3. Evaluation observations

`conformance/eval-v0.1.json` observes weak-head form only.

Portable result forms are the forms present in that file, including:

```text
Function
Nat(value)
Unit
Pair
Inl
Inr
```

The observation must not recursively force delayed pair fields or sum payloads merely to serialize a result.

A host closure, environment, thunk, memo cell, or primitive-application object is never a portable result.

## 4. Resource refusal

Exact transition/fuel counts are implementation-specific and must not be compared between the independent implementation and Go.

A configured resource refusal must remain distinguishable from:

```text
malformed input
scope invalidity
type invalidity
unknown primitive
normal WHNF result
```

The packet does not require both implementations to refuse after the same number of internal operations.

## 5. What this file deliberately does not specify

This file does not prescribe:

- environment versus substitution evaluation;
- closure representation;
- thunk representation;
- memoization;
- object layout;
- fresh-variable allocation strategy;
- substitution data structures;
- recursion implementation;
- Python API shape.

Those choices remain independent implementation decisions as long as portable observations conform to the packet.
