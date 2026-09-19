# Stage 6 — Teaching NEX to an unknown receiver

**Status:** Planned; blocked by the ADR-0018 Stage 5.20 gate  
**Date:** 2026-09-19  
**Prerequisite:** Stage 5.20 outcome explicitly permits Stage 6 activation; Stages 5.11 and 5.12 are Complete, Stage 5.13 is the next Planned self-sufficiency substage  
**Decisions:** ADR-0017 teaching/Core separation; ADR-0018 pre-Stage-6 self-sufficiency gate

## Purpose

Stage 6 addresses the original project goal more directly:

> construct a finite transmitted teaching/bootstrap sequence that can take a receiver from an explicit prior profile to demonstrable ability to decode, type-check, execute, and construct NEX programs.

Stage 6 keeps NEX-1 v0.1 stable. It investigates a separate teaching layer above the Core rather than changing the Core merely for pedagogical convenience. ADR-0018 delays execution of this plan until the 5.10–5.20 self-sufficiency extension reaches its decision gate; completion of 5.11 and 5.12 does not by itself activate Stage 6.

## 6.0 — freeze the experiment contract

Before authoring a teaching sequence, freeze:

- the receiver-assumption profile used by the experiment;
- what information the experimental receiver may access;
- what material is forbidden;
- the competence criteria;
- the held-out task policy;
- the accounting boundary;
- the distinction between teaching representation and canonical NEX representation.

The first experiment SHOULD prefer a clearly stated receiver profile from `assumptions-v0.2.json`. If an additional formal calculus or machine is required, it must be named as `A1(R)` or `A2(U)` rather than silently added to `A1`.

## 6.1 — machine-readable curriculum model

Create a versioned curriculum artifact. Each lesson must declare at least:

```text
id
prerequisites
concepts_introduced
assumptions_used
teaching_examples
self_tests
portable_success_observations
status
```

A lesson cannot depend on a concept that has not already been established by its prerequisites or declared receiver prior.

The first planning artifact is `stage6/curriculum-plan-v0.1.json`. It is a **plan**, not transmitted teaching content and therefore has no accepted `T_bits` value.

## 6.2 — foundational lessons

Develop and test lessons for the lowest-level shared structure required by the selected profile, potentially including:

```text
binary symbols and ordering
frame boundaries
natural numbers
finite sequences
self-delimiting integers
structural/tree composition
```

If the selected experiment starts at a stronger prior where some of these are already assumed, the skipped concepts must be traceable to explicit assumption atoms.

## 6.3 — computation lessons

Progressively introduce operational concepts without depending on unintroduced terrestrial notation:

```text
values
primitive equations
application
functions
binding
products/sums
selective forcing
recursion
```

Pedagogical notation may be used, but its syntax/meaning must itself be established and counted if transmitted.

## 6.4 — static typing lessons

Teach enough structure to reconstruct the static contract:

```text
N and 1
function/product/sum types
type judgments
polymorphic primitive schemes
unification constraints
Let polymorphism
principal schemes / normalization used for self-test
```

The stage should test whether types help the receiver disambiguate intended program structure, not merely whether an already implemented HM checker passes vectors.

## 6.5 — transition to canonical NEX wire

The receiver must ultimately learn the actual NEX-1 canonical representation:

```text
Var Lam App Let Nat Prim
zero-based de Bruijn indices
U(n) = gamma(n+1)
constructor prefixes
exact bit length / packing boundary
```

A friendly teaching notation does not replace this target.

## 6.6 — transmitted self-tests

Construct a finite self-test suite that a receiver can use to check its own reconstruction.

Self-tests SHOULD cover at least:

- integer encoding/decoding;
- term encoding/decoding;
- scope rejection;
- primitive validation;
- principal type inference;
- occurs check/type mismatch;
- selective forcing/laziness;
- products/sums;
- terminating recursion;
- resource refusal distinguished from invalidity.

The exact transmitted self-test set is part of teaching cost and must be counted when serialized.

## 6.7 — held-out competence tests

The experiment must distinguish memorization from competence.

Held-out tasks are not included in the teaching message. They should test:

### Interpretation

Given new canonical NEX programs, recover expected static/evaluation observations.

### Construction

Given a task relation expressible using already taught concepts, construct a valid NEX term satisfying it.

Example task forms may include finite equations or input/output relations such as:

```text
f(0) = 1
f(1) = 2
f(2) = 3
```

but the actual task language must be exactly defined and must not smuggle English semantics into the receiver experiment.

Construction tasks are mandatory because “can run NEX” is weaker than “can program in NEX”.

## 6.8 — receiver experiments

Run the teaching artifact against one or more isolated receiver proxies.

Possible engineering proxies include:

- a fresh implementation context;
- an LLM with no repository/chat access;
- a human implementer given only the declared prior plus teaching artifact;
- later, a deliberately minimal automated learner/interpreter.

For every receiver class record exactly what background capability is supplied. Results are evidence about that receiver class, not evidence about extraterrestrial cognition in general.

## 6.9 — assumption-leak audit

Every time the receiver needs clarification not derivable from the declared prior plus transmitted material, classify it as one of:

```text
missing lesson
ambiguous lesson
hidden receiver assumption
host/tool leakage
success-criterion defect
```

Do not patch the experimental receiver privately. Update the versioned curriculum/message and rerun from a clean receiver context.

## 6.10 — exact teaching artifact and accounting

Only after the teaching protocol has an exact finite binary serialization and dependency closure may the project publish:

```text
T_bits | A
```

The ledger must state whether `T` contains specification/bootstrap/self-test material already represented by historical `S`, `B`, or `SB` terminology. No bit may be counted twice.

The first exact teaching artifact does not need to be optimal. It needs to be finite, dependency-closed, reproducible, and honestly measured.

## 6.11 — decision gate

At the end of Stage 6 classify each major hypothesis:

```text
supported
not supported
inconclusive
blocked by undeclared prior
```

Questions include:

- can a receiver reconstruct canonical NEX from the teaching artifact?;
- do transmitted self-tests detect incorrect reconstructions?;
- can the receiver solve held-out interpretation tasks?;
- can it construct valid held-out NEX programs?;
- which lessons dominate transmitted bits?;
- which assumptions dominate feasibility?;
- does teaching evidence reveal a genuine Core defect, or only a pedagogical-layer defect?

Only the last case can motivate a NEX-1 successor design discussion.

## Initial curriculum hypothesis

The initial order to test is:

```text
binary/framing
 -> naturals/sequences
 -> self-delimiting integers
 -> structure/trees
 -> primitive equations
 -> application/functions
 -> binding/de Bruijn
 -> products/sums
 -> recursion
 -> types/judgments
 -> principal-type examples
 -> canonical NEX wire
 -> self-tests
 -> held-out construction tasks
```

This order comes from project reasoning plus lessons from Lincos/CosmicOS. It is not normative and may be falsified by experiments.

## Measurements

Stage 6 should report, where available:

```text
teaching artifact exact bits
lesson count
bits per lesson/concept
transmitted self-test bits
receiver success/failure by competence category
held-out interpretation pass rate
held-out construction pass rate
number/classification of assumption leaks
number of curriculum revisions before success
```

Do not collapse receiver accuracy or human/LLM behavior into an architecture-neutral semantic property of NEX.

## Supporting evidence workstreams

These remain important but secondary to the Stage 6 teaching objective:

1. NEX-specific canonical forms / preservation / progress-or-safety metatheory;
2. NEX-specific call-by-need observational-preservation proof or mechanization;
3. bounded exhaustive small-term Go/Python comparison, including function application contexts;
4. hold-out and externally specified benchmark families.

## Scope guard

Stage 6 MUST NOT add merely to make teaching easier:

- incompatible NEX-1 wire changes;
- new NEX-1 Core constructors or primitives;
- mutable memory/system APIs;
- production frontend features;
- native backend;
- self-hosting claims.

A pedagogical syntax/encoding may be experimental and separate from canonical NEX-1.

## Definition of done

Stage 6 is complete only when:

- [ ] a receiver profile is selected and frozen for the experiment;
- [ ] the curriculum/message is finite and machine-readable;
- [ ] every lesson's prerequisites and assumptions are dependency-closed;
- [ ] exact transmitted serialization exists;
- [ ] transmitted self-tests exist;
- [ ] held-out interpretation tasks exist;
- [ ] held-out program-construction tasks exist;
- [ ] at least one clean receiver experiment is reproduced;
- [ ] assumption leaks are recorded and resolved/versioned rather than hidden;
- [ ] exact teaching-message bit cost is reported under the chosen profile;
- [ ] NEX-1 v0.1 remains unchanged unless a separate evidence-backed successor ADR is opened;
- [ ] English and Russian research synthesis is updated.
