# ADR-0007: Keep ordinary type annotations out of the NEX-1 v0.1 canonical wire format

- **Status:** Accepted
- **Date:** 2026-09-18

## Context

NEX-1 v0.1 currently transmits unannotated Core terms and reconstructs types using Hindley-Milner style rank-1 inference. This reduces repeated type information in transmitted programs, but it increases the receiver/bootstrap implementation because the receiver must implement type variables, substitutions, unification, occurs check, instantiation, generalization, and Algorithm W style inference.

The project's actual optimization target is not program bits alone:

```text
cost = specification + bootstrap implementation + transmitted programs
```

Therefore it is not sufficient to assume that omitted type annotations are always globally cheaper.

## Decision drivers

- preserve the already-defined NEX-1 v0.1 canonical term grammar;
- keep Stage 2 focused on validating the current specification rather than redesigning wire syntax mid-implementation;
- avoid transmitting redundant ordinary type annotations when principal types can be inferred in the supported fragment;
- retain the ability to test whether an explicit typed/certificate format would reduce total information cost;
- prevent frontend conveniences from silently becoming canonical wire requirements.

## Decision

For NEX-1 v0.1:

1. ordinary canonical Core terms contain no term-level type annotations;
2. type schemes such as `forall a. a -> a` exist in the static type system, not as ordinary term constructors;
3. a human-oriented frontend MAY accept type annotations for readability, checking, diagnostics, or documentation;
4. those annotations MUST be erased when the frontend emits a canonical v0.1 Core term;
5. Stage 2 will implement inference for this erased-type representation;
6. no claim is made that this representation minimizes total project cost.

## Accepted consequences

### Positive

- the v0.1 wire grammar remains unchanged while static validation is implemented;
- common inferred type information is not repeated in every transmitted term;
- independent receivers can reconstruct principal types from the same canonical term when they implement the specified inference discipline;
- frontend syntax remains separable from the canonical Core representation.

### Cost

- the receiver/bootstrap must contain a non-trivial inference engine;
- type inference becomes part of conformance and must be specified/tested precisely;
- implementations must canonicalize semantically equivalent principal types independently of internal fresh-variable IDs.

## Alternative considered: transmit explicit types with terms

**Deferred for quantitative comparison, not rejected permanently.**

A compact explicit representation could increase each transmitted program while allowing a substantially smaller checker/bootstrap. The total cost may therefore be lower for some transmission corpus or bootstrap assumptions.

The project must eventually compare at least:

```text
NEX-HM
  erased type information
  + inference bootstrap

NEX-explicit
  compact type information or type certificate
  + simpler validation bootstrap
```

The comparison must count specification size, bootstrap size, and transmitted corpus size under a stated encoding and measurement procedure.

## Alternative considered: require annotations only at selected boundaries

**Deferred.**

Hybrid designs may offer better trade-offs, for example transmitting compact types only for modules, shared definitions, recursion boundaries, or proof/checking certificates. Introducing such a design requires concrete encoding and measurements rather than intuition.

## Evidence classification

Established theory registered in `docs/SOURCES.md` supports the HM/principal-type mechanisms used by v0.1 (`SRC-0003`, `SRC-0004`).

The proposition that erased types minimize NEX total information cost is **not** an established external fact and is **not** an accepted project result. It remains an experimental hypothesis to benchmark.

## Follow-up validation

A future benchmark must define:

- the explicit/certificate type encoding;
- the receiver/checker implementation being measured;
- the program corpus;
- whether shared libraries/bootstrap are counted once or repeatedly;
- exact size metrics.

If explicit or hybrid type transmission is materially better, a new ADR must supersede this decision for a later NEX specification version. NEX-1 v0.1 must not be silently reinterpreted.
