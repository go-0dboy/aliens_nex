# ADR-0017: Separate the NEX teaching/bootstrap protocol from the stable NEX-1 Core

**Status:** Accepted  
**Date:** 2026-09-19

**Follow-up sequencing decision:** ADR-0018 was accepted later on the same date and inserts the mandatory 5.10–5.20 Core self-sufficiency gate before Stage 6 may become Active. ADR-0017 remains Accepted: its teaching/Core separation is unchanged; only activation timing is controlled by ADR-0018. Current continuation: 5.11 and 5.12 Complete, 5.13 Planned.

## Context

Stages 0–5 established a stable NEX-1 v0.1 Core, exact wire/static/dynamic contracts, empirical measurements, and strong differential-conformance evidence that a second implementation can reconstruct the tested behavior from a frozen packet.

Stage 5 also showed that no complete receiver-neutral bootstrap artifact has yet been constructed.

The post-Stage-5 literature comparison with Lincos, DeVito–Oehrle, Lingua Cosmica, and CosmicOS clarified an architectural gap. NEX currently specifies **what computational system the receiver should ultimately know**, but it does not yet specify **how an unknown receiver is progressively taught that system**.

The canonical Core representation is optimized for precision and compactness, not necessarily for first-contact pedagogy. For example, de Bruijn indices remove transmitted names but need not be the easiest first representation from which a receiver infers binding.

## Decision drivers

- Preserve the already validated NEX-1 v0.1 Core while testing teachability.
- Avoid redesigning canonical wire syntax merely to make early lessons more intuitive.
- Make every receiver assumption explicit.
- Turn “learned NEX” into an operationally testable claim.
- Require program construction, not only passive interpretation, because the project goal is to teach programming.
- Produce a finite machine-readable transmitted teaching artifact whose bit length can eventually be measured exactly.
- Reuse existing conformance vectors as receiver self-tests where appropriate.
- Keep terrestrial student models/LLMs clearly labelled as engineering proxies rather than models of alien cognition.

## Decision

Stage 6 treats NEX as a two-layer system:

```text
receiver prior A
    -> NEX Teaching / Bootstrap Message T
    -> reconstructed NEX-1 competence
    -> conformance / self-test
    -> canonical NEX program transmission P
```

### Stable target: NEX-1 Core

NEX-1 v0.1 remains the target computational system:

```text
Var Lam App Let Nat Prim
rank-1 HM typing
weak call-by-name semantics
Core primitive IDs 0..10
canonical binary wire
```

Stage 6 MUST NOT make an incompatible Core change merely to simplify teaching.

### Separate teaching representation

The teaching/bootstrap message MAY use a representation that is redundant, staged, example-heavy, or otherwise non-canonical if every symbol and rule required to interpret that representation is itself accounted for under the selected receiver profile.

Pedagogical notation is not automatically part of NEX Core and cannot be assumed free.

### Operational competence

Stage 6 MUST define “receiver has learned NEX” operationally. At minimum a successful experimental receiver must demonstrate all of the following without access to the Go/Python reference implementations:

1. **Decode competence** — decode selected canonical NEX bit strings into the intended abstract terms.
2. **Encode competence** — produce canonical NEX bits for selected terms.
3. **Static competence** — distinguish supplied valid/invalid cases and recover the expected normalized principal schemes where required.
4. **Evaluation competence** — obtain expected portable weak-head observations for supplied and held-out terms.
5. **Construction competence** — construct valid NEX programs for held-out tasks whose specification does not reveal the solution term.
6. **Self-test competence** — use transmitted exercises to detect at least selected intentionally wrong reconstructions or answers.

Passing examples copied from the teaching sequence is insufficient for construction competence.

### Held-out tasks

Program-construction tests MUST be withheld from the teaching examples. Their task meaning must be expressible using concepts already established by the teaching protocol, for example through finite input/output examples, equations, or another exactly defined relation.

### Cost boundary

The teaching artifact is not assigned a scalar cost until an exact binary serialization and dependency closure exist.

When a concrete artifact exists, its exact transmitted length is recorded separately, for example:

```text
T_bits | A
```

and incorporated into an exact transmitted object ledger without silently double-counting specification/bootstrap material.

### Experimental receiver models

A human, LLM, or isolated implementation context MAY be used as an engineering receiver proxy. Such a result tests the protocol against that receiver class only. It MUST NOT be described as proof that an extraterrestrial intelligence would understand the message.

## Initial curriculum hypothesis

The initial Stage 6 ordering is a hypothesis to test, not normative NEX semantics:

1. binary symbols, sequence order, and framing;
2. naturals and finite sequences;
3. self-delimiting integer representation;
4. structural composition / trees;
5. natural values and simple primitive equations;
6. application and functions;
7. binding, including the transition from pedagogical examples to de Bruijn indices;
8. products and sums;
9. recursion;
10. type constructors and type judgments;
11. principal type inference examples;
12. canonical NEX term wire encoding;
13. conformance/self-test exercises;
14. held-out construction tasks.

The order may change only through measured teaching evidence, with the previous version preserved.

## Accepted consequences

- Stage 6 becomes primarily a teachability/bootstrap experiment, not a Core-optimization stage.
- The canonical Core and the teaching language may intentionally differ.
- A longer teaching representation may still be preferable if it substantially reduces ambiguity or failure to reconstruct the Core.
- Existing conformance vectors gain a second role as potential self-test material, but a future teaching packet must decide which vectors are transmitted and count their bits.
- “Can execute NEX” and “can program in NEX” are separate milestones.
- Exact total communication cost remains unresolved until a finite serialized teaching/bootstrap artifact exists.

## Alternatives considered

### Immediately redesign NEX-1 Core for teachability

**Rejected for Stage 6.** The project already has evidence for the current Core. Pedagogical difficulty should first be addressed by a separate teaching representation so that Core changes remain evidence-driven.

### Treat the prose specification as the teaching message

**Rejected.** English, Markdown, UTF-8, mathematical notation, and human documentation conventions are undeclared terrestrial dependencies under receiver-neutral profiles.

### Treat a small universal machine as sufficient teaching

**Rejected as a complete solution.** An exact machine may provide execution substrate under `A2(U)`, but the receiver still needs the NEX decoder/typechecker/evaluator program and enough framing/meaning to identify and validate it.

### Require only interpreter reconstruction

**Rejected.** The project goal includes teaching the receiver to program. Held-out program construction is therefore required in addition to reconstructing an evaluator.

## Evidence / references

Design lessons are summarized in `docs/RELATED-WORK.md` and grounded in SRC-0020 (Lincos), SRC-0021 (CosmicOS), SRC-0022 (Lingua Cosmica), SRC-0028 (DeVito–Oehrle), and SRC-0029 (exosemiotic limits of universal-prior assumptions).

Stage 5 independent reconstruction provides a terrestrial precedent for the structure “finite communicated rules/examples -> independent implementation -> conformance check”, while remaining explicitly weaker than an alien-understanding experiment.

## Follow-up validation

Stage 6 must produce, before any claim of success:

- a versioned machine-readable curriculum contract;
- one explicitly selected receiver-assumption profile;
- an exact serialization for transmitted teaching material;
- transmitted self-tests;
- held-out interpretation and construction tasks;
- a reproducible receiver experiment protocol;
- an assumption-leak audit;
- exact artifact bit counts only after dependency closure;
- research synthesis in both dissertation versions.
