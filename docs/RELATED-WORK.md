# Related work: teaching computation to an unknown receiver

This document compares NEX with systems that pursue closely related goals: constructing a formal message for an unknown extraterrestrial or otherwise unknown receiver, progressively teaching concepts, or transmitting executable/program-like structures.

The purpose is **not** to establish novelty. Prior work is used as design evidence: what has already been tried, which assumptions were made, how recipients were expected to infer meaning, and which parts of the NEX communication problem remain unsolved.

## 1. Comparison criterion

The comparison is organized around the actual NEX objective:

> Can a receiver with no assumed terrestrial programming environment be taught enough formal structure to decode, type-check, execute, and eventually author programs in the transmitted computational system?

The relevant dimensions are therefore:

- how prior knowledge is treated;
- whether meaning is taught progressively through examples;
- whether executable computation is central;
- whether the system has a precise operational semantics;
- whether static typing contributes to validation;
- whether the transmitted representation is canonical and bit-exact;
- whether the receiver can test that it reconstructed the system correctly;
- whether specification/bootstrap/program costs are kept explicit.

## 2. Lincos

Freudenthal's *Lincos* [SRC-0020] is foundational prior work on constructing a language for cosmic communication. It develops meaning progressively from formal/mathematical material toward richer discourse.

Design lesson for NEX:

- do not expect a receiver to understand a dictionary or prose specification;
- introduce semantics through controlled examples whose interpretation becomes progressively constrained;
- reuse previously established concepts to teach later concepts.

Lincos is broader than a programming language and is not an exact binary typed execution protocol. Its importance for NEX is pedagogical: it demonstrates that the communication problem is a **teaching sequence**, not merely a compact grammar.

## 3. DeVito–Oehrle

DeVito and Oehrle's science-based language [SRC-0028] explicitly reasons about what prior scientific knowledge a technologically capable receiver might share.

Design lesson for NEX:

- the size of the message depends strongly on the prior assumptions;
- stronger assumptions can shorten the teaching/bootstrap message;
- such assumptions must be declared, not silently treated as universal.

This maps naturally to NEX receiver profiles. The current `A0`, `A1`, `A1(R)`, `A2(U)`, and `A_host(H)` are experimental conditions, not claims about what an extraterrestrial intelligence must know.

## 4. Lingua Cosmica

Lingua Cosmica work uses formal logic and constructive type theory to reduce ambiguity in interstellar messages [SRC-0022].

Design lesson for NEX:

- type information can do more than reject ordinary programming mistakes;
- a type discipline can constrain possible interpretations of a transmitted expression;
- the teaching protocol should exploit typing as a semantic checksum, not only as a compiler feature.

NEX differs in using a concrete rank-1 HM-style executable Core with a canonical binary wire representation, but the broader role of types as communication constraints is shared.

## 5. CosmicOS

CosmicOS [SRC-0021] is the closest current comparison to NEX's original objective. It explicitly bootstraps mathematics and logic, then introduces the ability to run programs and simulations. Its message proceeds through examples and progressively richer computational concepts.

The key difference is architectural emphasis:

| Question | CosmicOS emphasis | NEX emphasis |
|---|---|---|
| How does the receiver learn? | progressive examples and executable curriculum | not yet implemented as a dedicated layer |
| Final computation model | Lisp-like/program-and-simulation oriented | six-constructor typed Core |
| Binding/readability | human-like symbolic forms are useful during teaching | canonical de Bruijn representation removes transmitted names |
| Static validation | not centered on HM inference | central to NEX v0.1 |
| Exact canonical bit representation | not the main research objective | central |
| Independent reconstruction evidence | not the current NEX-style experiment | frozen blind Python reconstruction + differential check |
| Explicit transmitted-bit ledger | not the main objective | central research methodology |

The main lesson is that CosmicOS already addresses the layer NEX currently lacks: **how to teach a receiver to operate the computational system**.

NEX currently addresses the complementary problem more rigorously: **what exact computational system should both parties eventually agree on, and how can its representation and reconstruction be checked?**

## 6. NEX as a two-layer system

The comparison suggests that the project should distinguish two artifacts:

```text
NEX Teaching / Bootstrap Message
        |
        | progressively establishes meaning
        v
NEX-1 Core
        |
        | exact canonical programs
        v
subsequent transmitted computation
```

### NEX-1 Core

The Core remains the stable target learned by the receiver:

```text
Var Lam App Let Nat Prim
HM rank-1 typing
weak call-by-name semantics
fixed Core primitive table
canonical binary wire
```

The Core should not be redesigned merely to make the first teaching lesson more human-readable. A teaching representation may be redundant or pedagogical while the final canonical representation remains compact.

### Teaching / bootstrap layer

The teaching layer should progressively establish enough meaning for the receiver to reconstruct the Core. Candidate lessons include:

1. binary symbols, ordering, and framing assumptions;
2. natural numbers and finite sequences;
3. self-delimiting integer representation;
4. structural composition / trees;
5. direct natural values and simple primitive equations;
6. application and functions;
7. binding and the relation between pedagogical examples and de Bruijn indices;
8. products and sums;
9. recursion;
10. type constructors and type judgments;
11. principal type inference examples;
12. canonical NEX wire encoding;
13. conformance exercises that test decoder, typechecker, and evaluator reconstruction.

The exact order is a hypothesis for Stage 6, not an accepted protocol yet.

## 7. Conformance vectors as teaching exercises

A major NEX asset is that the existing conformance material can be reinterpreted as a receiver self-test.

A receiver that believes it understands the message should be able to predict or reconstruct, for selected examples:

```text
term -> canonical bits
term -> principal type / static rejection
term -> observable weak-head result
```

This does not prove understanding in a philosophical sense, but it provides an operational criterion:

> two independently reconstructed systems that pass the same transmitted exercises agree on the tested computational behavior.

Stage 5 demonstrated a terrestrial version of this idea: an isolated implementation context received a finite specification/conformance packet, built a separate implementation, and later matched the Go implementation on the tested surface.

## 8. What NEX should borrow — and what it should not

Useful ideas to borrow:

- from Lincos: progressive semantic teaching through constrained examples;
- from DeVito–Oehrle: explicit analysis of prior knowledge;
- from CosmicOS: an executable curriculum that moves from elementary concepts to programs and simulations;
- from Lingua Cosmica: formal/type constraints as tools for reducing semantic ambiguity.

What should remain specifically NEX:

- the stable exact NEX-1 Core;
- canonical binary program representation;
- strict separation of validity, typing, evaluation, and resource refusal;
- explicit receiver-conditioned accounting;
- reproducible conformance and independent reconstruction experiments;
- preservation of negative results and unknown costs.

## 9. Consequence for the next stage

The next project stage should not begin by optimizing another Core prefix or by selecting a universal machine only because it is small.

It should first answer:

> What finite transmitted teaching/bootstrap sequence is sufficient to take a receiver from an explicitly declared prior profile to demonstrable ability to decode, type-check, execute, and construct NEX programs?

This turns the original project objective into an experimentally testable program:

```text
prior A
  -> teaching/bootstrap message T
  -> reconstructed NEX competence
  -> conformance/self-test
  -> canonical program transmission P
```

A later exact cost model can then count the actual transmitted `T`/bootstrap material rather than guessing it from host source code.
