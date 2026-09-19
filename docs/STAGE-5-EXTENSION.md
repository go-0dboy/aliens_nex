# Post-Stage-5 extension — NEX Core self-sufficiency before teaching

**Status:** Active  
**Date:** 2026-09-19  
**Historical Stage 5:** Complete and unchanged through 5.9  
**Decision:** ADR-0018  
**Stage 6:** Planned; not active until the 5.20 gate

## Purpose

This workstream tests whether the stable NEX-1 v0.1 Core is practically capable of expressing an implementation of its own portable semantics before the project begins the Stage 6 receiver-teaching experiment.

It is a post-Stage-5 extension, not a rewrite of the completed Stage 5 experiment. Stage 5.0–5.9 evidence remains frozen under ADR-0015.

The central question is:

> Can an exact, closed, well-typed NEX-1 program implement NEX-1 canonical decoding/encoding, validation, type inference, and evaluation, and then process its own canonical representation without hidden host-language semantics?

The target is **self-implementation/self-interpretation**, not a native CPU compiler.

## Global invariants

Throughout 5.10–5.20:

1. NEX-1 v0.1 term grammar, primitive IDs, type rules, wire format, and normative weak call-by-name semantics remain unchanged.
2. Go and Python may execute or check the NEX implementation, but no required NEX operation may secretly be delegated to a new host callback.
3. All self-hosted data required by the implementation must be representable using existing NEX values.
4. Resource limits are implementation controls, not semantic invalidity.
5. Every discovered bug or ambiguity gets a regression case or versioned research record.
6. Difficulty does not authorize a Core change; a change requires a later evidence-backed successor-Core ADR.
7. Stage 6 artifacts remain planning artifacts and are not treated as active experiment evidence during this workstream.

## 5.10 — freeze the self-sufficiency contract

**Status:** Complete when ADR-0018 and this document are merged.

Freeze:

- the required NEX-in-NEX components;
- the self-processing criterion;
- forbidden hidden host dependencies;
- portable observations;
- test layering;
- decision-gate outcomes.

The contract deliberately does not require `NEX -> x86/ARM/WASM`. Architecture-specific compilation belongs to a later explicit profile/backend question.

## 5.11 — NEX-in-NEX meta-representation

**Status:** Active.

Define finite encodings, expressible entirely with NEX-1 v0.1 values, for at least:

```text
Bits
Term
Type
Scheme
Substitution
Type environment
Runtime/evaluation state as needed
Error/result classes
Portable observations
Toolchain requests/results
```

The first candidate should prefer a deliberately austere representation rather than changing Core. In particular, arbitrary finite recursive host structures may be represented by natural-number encodings.

Acceptance:

- representation is finite and injective/canonical for the admitted object class;
- decode operations are computable using existing NEX primitives plus derived functions;
- no recursive type or host container is assumed;
- malformed/non-canonical encodings have an explicit rejection policy;
- machine-readable contract and validator exist;
- bounded round-trip examples pass.

## 5.12 — self wire codec

Implement in NEX:

```text
encodeU / decodeU
encodeTerm / decodeTerm
```

where transmitted/canonical bit strings are represented through the 5.11 internal `Bits` encoding.

Required checks:

```text
decode(encode(term)) == term
encode(decode(bits)) == canonical(bits)
```

Compare against existing Go/Python wire behavior and conformance vectors.

## 5.13 — self structural validation

Implement in NEX:

- de Bruijn scope validation;
- Core primitive-ID validation;
- closed-program validation;
- structural rejection classes needed before type inference.

Do not collapse malformed representation, invalid scope, unknown primitive, or resource refusal into one result.

## 5.14 — self Hindley–Milner inference

Implement the exact v0.1 static contract in NEX, including:

```text
fresh variables
free type variables
substitution
composition/application of substitutions
instantiation
generalization
unification
occurs check
Let polymorphism
primitive schemes
principal-scheme normalization for portable comparison
```

Differential comparison target:

```text
Go infer
Python infer
NEX infer executed by Go
NEX infer executed by Python
```

All compared paths must agree on normalized portable schemes or portable static-error classes for the frozen test surface.

## 5.15 — self evaluator

Implement the normative weak call-by-name semantics in NEX for:

```text
Var Lam App Let Nat Prim
fix succ pred ifz
pair fst snd
inl inr case
unit
```

The implementation may use substitution or an encoded environment internally, but portable behavior must follow the specification, including selective forcing.

Resource refusal remains separate from validity and from any proof of divergence.

## 5.16 — integrated NEX-in-NEX toolchain

Integrate 5.12–5.15 into one exact canonical implementation `I`, or a versioned closed family with an exact top-level interface.

Required capabilities:

```text
Decode
Encode
Validate
Infer
Evaluate
```

`I` itself must be:

- canonical NEX wire;
- closed;
- accepted by v0.1 scope/primitive validation;
- well-typed;
- reproducibly generated from versioned source construction artifacts if a helper frontend/generator is used.

A helper generator is engineering tooling only; the resulting canonical NEX term is the research object.

## 5.17 — self-processing

Run the implementation against its own canonical representation.

Minimum checks:

```text
I.decode(code(I)) -> representation(I)
I.encode(I.decode(code(I))) == code(I)
I.validate(code(I)) -> valid
I.infer(code(I)) -> expected normalized principal scheme
```

Then exercise at least one nested path conceptually equivalent to:

```text
host evaluator
  -> I
     -> code(I)
        -> held-out program P
```

Exact request/framing conventions must be versioned and included in the artifact contract.

## 5.18 — bounded and differential validation

Freeze bounds and workloads before observing final aggregate results.

Include:

- existing conformance vectors;
- a hold-out family not used to author `I`;
- bounded exhaustive or precisely complete small-term classes;
- malformed/internal-representation cases;
- static-error cases;
- terminating evaluation cases under a declared search/resource bound;
- function-valued cases tested through application contexts.

Compare portable observations across:

```text
Direct Go
Direct Python
NEX-in-NEX on Go
NEX-in-NEX on Python
```

Agreement is empirical evidence, not a proof oracle.

## 5.19 — supporting metatheory

Strengthen the formal argument for the exact target Core:

```text
canonical forms
preservation / subject reduction
progress-or-partial-computation safety appropriate to fix/divergence
```

Separately strengthen the claim that any allowed call-by-need implementation preserves NEX weak-CBN portable observations.

The 5.20 report must distinguish `formally proved`, `verified`, `inferred`, `hypothesis`, and `unknown` rather than blocking all engineering progress on unfinished mechanization.

## 5.20 — pre-Stage-6 decision gate

Classify the complete workstream as exactly one of:

```text
supported
supported_but_impractical
core_limitation_discovered
inconclusive
```

### `supported`

A complete NEX-in-NEX implementation exists, required self-processing passes, and frozen differential evidence supports the portable contracts.

Stage 6 may become Active without changing NEX-1 v0.1.

### `supported_but_impractical`

The construction exists but measured size/resource cost is problematic. Record the cost; do not silently redefine failure as a Core defect.

A separate decision determines whether Stage 6 uses v0.1 or whether a successor design experiment is justified.

### `core_limitation_discovered`

A required construction is blocked by a reproducible limitation attributable to the exact Core rather than to the chosen implementation technique alone.

Do not start Stage 6 on a changed language until a successor-Core ADR/specification/evidence cycle exists.

### `inconclusive`

The experiment did not establish self-sufficiency and did not establish a Core defect. Any move into Stage 6 requires an explicit weaker-scope decision.

## Evidence discipline

Every substage follows:

```text
Problem
 -> Contract
 -> Invariant
 -> Failing test / executable example
 -> Implementation
 -> Verification
 -> Diff review
 -> Status checkpoint
 -> Research synthesis checkpoint
```

Historical Stage 5 measurements must never be edited to make this later work appear to have been part of the original blind-reconstruction experiment.

## Definition of done

This extension is complete only when:

- [x] 5.10 contract and ADR exist;
- [ ] 5.11 machine-readable meta-representation exists and is validated;
- [ ] NEX self codec exists;
- [ ] NEX self structural validator exists;
- [ ] NEX self HM inference exists;
- [ ] NEX self evaluator exists;
- [ ] integrated canonical implementation `I` exists;
- [ ] self-processing evidence exists;
- [ ] frozen bounded/differential evidence exists;
- [ ] metatheory status is recorded precisely;
- [ ] 5.20 classification is recorded;
- [ ] `docs/STATUS.md` is current;
- [ ] both dissertation versions incorporate the research-significant result/decision before closeout;
- [ ] Stage 6 remains Planned until the gate permits activation.
