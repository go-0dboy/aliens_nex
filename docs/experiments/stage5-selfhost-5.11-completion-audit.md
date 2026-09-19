# Stage 5.11 completion audit — representation contract before Stage 5.12 closeout

**Date:** 2026-09-19  
**Status:** Gate 0 result — Stage 5.11 is not yet Complete  
**Core:** NEX-1 v0.1 unchanged

## Question

Before continuing Stage 5.12, verify whether Stage 5.11 satisfies its original representation contract strongly enough to serve as the representation basis required by Stage 5.12 and later self-hosting work.

Strict sequencing is now:

```text
5.11 Complete
  -> 5.12 Complete
     -> 5.13 may begin
```

## What meta-representation-v0.2 already provides

`stage5/selfhost/meta-representation-v0.2.json` is substantially complete as a **mathematical N-only representation contract**. It defines finite representations for:

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

It also freezes:

- the exact pow2-adic pair;
- sequence encoding;
- exact tagged-value encoding;
- Term and Type tags;
- Scheme/substitution/environment canonicality rules;
- portable observations;
- static/tool result classes;
- forbidden host/Core dependencies;
- bounded examples.

Therefore the problem is **not** that v0.2 omitted Scheme/Substitution/TypeEnvironment. Those contracts exist and must remain historical evidence.

## Why Stage 5.11 is nevertheless not Complete

The accepted Stage 5.12 experiments discovered that the operational representation strategy diverged from v0.2:

### v0.2 contract

```text
Bits : N
Term : N
recursive structure via pow2-adic pair / N sequences
```

### accepted 5.12e/5.12f operational path

```text
BitStream = N -> N
0/1       = bit data
2         = EOF
Cursor    = N
```

The numeric `Term : N` path also exposed a practical recursive-size problem, and the compact bit-interleaving replacement exposed a separate bounded execution-cost problem. These negative results do not make v0.2 mathematically invalid, but they do mean the successful 5.12 implementation is **not operating on the exact 5.11 Bits/Term representation that Stage 5.12 was supposed to consume**.

That mismatch must be resolved explicitly; it cannot be hidden by saying that 5.11 was complete while 5.12 silently used another carrier.

## Audit decision

**Stage 5.11 remains Active / incomplete.**

The next research object must be a versioned **operational meta-representation v0.3** that reconciles the successful functional-stream/cursor path with the complete set of representation roles required by 5.11.

Historical v0.1/v0.2 remain unchanged and retain their value as mathematical/engineering evidence.

## Requirements for meta-representation v0.3

Before Stage 5.11 can be marked Complete, v0.3 must state exact physical NEX carriers and canonicality/equality rules for all roles needed by the self-hosting workstream.

At minimum:

```text
Bits
Term
Type
Scheme
Substitution
TypeEnvironment
Error/result classes
PortableObservation
ToolRequest
ToolResult
Runtime/evaluation state as needed by the already frozen 5.10–5.20 target
```

The design must satisfy all of the following.

### 1. Reconcile Bits with accepted evidence

The operational `Bits` representation must account for the accepted functional-stream evidence:

```text
BitStream = N -> N
0/1 = data
2   = EOF
```

If v0.3 chooses a different carrier, it must explain why the accepted 5.12e/5.12f path is no longer the operational representation rather than silently mixing contracts.

### 2. Freeze an operational Term carrier

The carrier must support complete `encodeTerm/decodeTerm`, later validation, inference, evaluation, and self-processing without recursive Core types or hidden host structures.

A stream-backed reference such as conceptually:

```text
TermRef = BitStream * Cursor
```

may be evaluated, but it is not automatically accepted. The contract must define:

- validity invariant for the referenced offset;
- exact term equality;
- canonicality;
- child addressing;
- ownership/lifetime of the underlying immutable stream;
- how an independent NEX encoder reconstructs canonical term wire;
- why the representation is not merely an identity shortcut that avoids decoding semantics.

### 3. Do not repeat the recursive-N size pathology

Recursive `Type`, `Scheme`, substitutions, environments, observations, or runtime state must not be assigned to the rejected practical numeric strategy without an explicit new feasibility argument.

The representation may use a common stream/cursor family for multiple meta-object classes, but each class needs its own exact canonical grammar and validation rule.

### 4. Preserve separation of layers

The v0.3 representation contract must distinguish:

- malformed internal meta-representation;
- malformed/truncated canonical NEX wire;
- scope error;
- unknown primitive;
- HM/type error;
- evaluation result;
- resource refusal.

Resource refusal remains an execution-control outcome, not a semantic error code.

### 5. Existing Core only

Forbidden:

- recursive types;
- new term constructors;
- new primitives;
- mutable memory;
- host strings/byte arrays/ASTs used as semantic state;
- hidden host callbacks implementing NEX operations;
- incompatible canonical NEX wire changes.

### 6. Machine-readable contract + validator

v0.3 must have:

- a machine-readable artifact;
- a validator;
- bounded examples for every representation family;
- explicit lineage from v0.2;
- a table saying which v0.2 contracts are retained, replaced, or superseded operationally.

## Stage 5.11 completion gate

Stage 5.11 may be marked Complete only when:

- [x] historical v0.1 is preserved;
- [x] exact v0.2 numeric/tagged contract is preserved and validated;
- [x] practical failure modes of recursive numeric representation are recorded;
- [x] functional BitStream feasibility is established on frozen development + hold-out evidence;
- [ ] operational v0.3 reconciles Bits/Term with the successful stream/cursor path;
- [ ] v0.3 covers every representation role required by the 5.10–5.20 self-hosting contract;
- [ ] v0.3 has exact canonicality/equality/error rules;
- [ ] v0.3 has machine-readable validation and bounded examples;
- [ ] no hidden Core/host dependency exists;
- [ ] status/manuscript/PR consistently mark 5.11 Complete only after those checks pass.

## Consequence for Stage 5.12

No new `encodeTerm/decodeTerm` implementation should be started yet.

The immediate next task is to design and freeze `meta-representation-v0.3` and its validator. Once 5.11 is Complete, Stage 5.12 resumes at Gate 1 of `docs/STAGE-5.12-CLOSEOUT.md` using that exact representation contract.