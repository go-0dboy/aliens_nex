# NEX-1: A Minimal Architecture-Neutral Typed Core for Information-Efficient Transmission of Computation

## Design, formalization, executable semantics, empirical evaluation, and independent reconstruction protocol

**Document type:** living dissertation-style research manuscript  
**Canonical language:** English  
**Russian mirror:** `RESEARCH-DISSERTATION.ru.md`  
**Evidence horizon:** Stages 0–4 complete; Stage 5.0–5.1 protocol checkpoint, 2026-09-18  
**Project:** NEX / `aliens_nex`

> This manuscript is a scholarly research synthesis maintained inside the project repository. It is not yet formatted for the submission requirements of a particular university, national dissertation authority, or citation style. The normative language definition remains `docs/NEX-1-v0.1.md`; architecture and research-method decisions remain governed by Accepted ADRs.

---

## Abstract

This work investigates whether a very small, architecture-neutral, statically typed computational core can reduce the information required to transmit executable computational knowledge between parties that cannot assume a shared programming language, processor architecture, ABI, operating system, textual notation, or implementation environment. The object of research is architecture-neutral representation and reconstruction of general-purpose computation under severe communication constraints. The optimization target is not program payload alone but the total information model

```text
C = S + B + P
```

where `S` is the information required to specify the computational system, `B` is the receiver-neutral bootstrap information required to realize it, and `P` is transmitted program payload.

The experimental system NEX-1 v0.1 uses six canonical term constructors (`Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`), zero-based de Bruijn indices, rank-1 Hindley–Milner let-polymorphism, direct arbitrary-precision natural literals, products and sums through fixed primitives, explicit general recursion through `fix`, a self-delimiting prefix binary representation, and weak call-by-name semantics. Its theoretical basis includes de Bruijn's nameless lambda notation [1], Binary Lambda Calculus as a compact binary-lambda comparison point [2], Hindley–Milner inference and principal type schemes [3,4], PCF/LCF-style typed recursion [5], Elias integer coding [6], and established distinctions between call-by-name and lazy sharing [9–11].

Stages 1–3 established executable wire, static, and dynamic semantics. Stage 4 froze measurement rules and benchmark corpora before optimization and produced reproducible empirical comparisons. On the accepted 17-program corpus v0.3, canonical NEX terms occupy 1,371 bits over 345 AST nodes. Primitive references are the largest measured wire contributor at 460 bits (33.6%), followed by variables at 286 bits (20.9%), applications at 264 bits (19.3%), naturals at 244 bits (17.8%), lambdas at 84 bits (6.1%), and `Let` at 33 bits (2.4%). Direct `Nat(255)` uses 21 bits versus 2,300 bits for the tested repeated-`succ` construction. `Let` has a measurable payload/reuse break-even rather than being universally beneficial. A non-normative principal-root-type envelope adds 134 bits, or 9.77% program-payload overhead, without establishing any bootstrap saving.

On an identical three-program pure-lambda subset, Binary Lambda Calculus is smaller than NEX (30 versus 37 bits), so universal NEX program-size superiority is not supported. A project-defined tiny postfix structural encoding uses 1,529 bits over the full corpus versus 1,371 bits for NEX, but it reuses NEX integer and primitive conventions and is not an independent total-bootstrap comparison. An experimental call-by-need implementation preserves the same observable weak-head results on all 17 accepted programs while reducing Go-reference evaluator transitions from 226,151 to 2,484 in aggregate (98.90%), with most savings concentrated in recursive or repeatedly forced workloads. This is implementation evidence, not transmission-cost evidence.

The central negative result remains that total information cost `C` is not numerically known. `P` is exact for a selected corpus, but Markdown size is only a textual proxy for `S`, Go source size is only a host/reference proxy `R`, and the actual receiver-neutral bootstrap `B` remains unknown.

Stage 5 begins by testing whether NEX can be reconstructed independently of the Go reference. ADR-0013 freezes an implementation-input boundary and selects Python 3.12 standard-library-only for the first independent reconstruction. Crucially, a second implementation is not treated as independent merely because it is written in another language: the current co-development context already knows the Go design and is therefore cognitively contaminated. Strong independent evidence requires a fresh isolated context or another implementer receiving only a frozen conformance packet and allowlisted primary theory. The Stage 5.1 packet audit has already exposed two presentation-layer omissions: canonical alpha-normalized text for principal type schemes and an explicit JSON test-fixture mapping for the six-term AST. Both were documented as packet observation conventions without changing NEX-1 v0.1 semantics.

The principal contribution to date is therefore not a claim of global minimality. It is an executable, falsifiable, independently testable research framework in which stronger claims about compactness, reconstructability, and total information cost can eventually be evaluated rather than assumed.

**Keywords:** minimal programming language, architecture-neutral computation, binary lambda calculus, de Bruijn indices, Hindley–Milner, program encoding, bootstrap, information cost, call-by-name, call-by-need, independent conformance, reproducible benchmarking.

---

# 1. Introduction

## 1.1 Motivation

Most programming-language and executable-format design assumes shared conventions: character encodings, textual syntax, processor models, word sizes, object formats, operating-system services, compiler conventions, or virtual-machine specifications. Such assumptions are normal in terrestrial software engineering but become problematic when sender and receiver may share only an ordered binary channel and basic mathematical regularities.

The motivating thought experiment is deliberately extreme: how can one transmit not merely data but reusable computational knowledge when no terrestrial language, CPU, ABI, operating system, or source notation may be assumed?

Minimizing program text alone is insufficient. A one-bit program is useless if understanding it requires an enormous uncommunicated interpreter. Conversely, an extremely small interpreter may make every later program larger. NEX therefore studies the joint objective

```text
C = S + B + P
```

rather than syntax size in isolation.

## 1.2 Research problem

The research problem is to determine whether a compact typed functional core can provide a favorable total-information trade-off for transmitting general-purpose computation without assuming a shared implementation platform.

The coupled dimensions are:

1. **representational compactness** — small, unambiguous, self-delimiting binary programs;
2. **semantic reconstructability** — scope, types, and execution meaning recoverable from communicated rules;
3. **computational expressiveness** — general recursion and compositional data construction;
4. **verification burden** — deterministic rejection of malformed and ill-typed programs;
5. **bootstrap burden** — program savings must not hide a large receiver implementation requirement;
6. **empirical falsifiability** — compactness claims must be measured against frozen workloads and explicit alternatives.

## 1.3 Object and subject

**Object:** architecture-neutral representation and execution of general-purpose computation under severe communication constraints.

**Subject:** trade-offs among specification size, receiver bootstrap complexity, transmitted-program size, static verifiability, evaluation strategy, and reconstructability in a minimal typed lambda-based core.

## 1.4 Goal

The goal is to construct and empirically evaluate a minimal executable core whose binary form and semantics are explicit enough to support independent reconstruction, while developing a reproducible method for determining whether its total communication cost can eventually outperform alternative computational representations.

## 1.5 Research objectives

1. Define a minimal architecture-neutral Core and its invariants.
2. Define a canonical self-delimiting wire representation.
3. Implement executable encode/decode conformance.
4. Define and implement static scope/type semantics.
5. Define and implement dynamic semantics without hidden machine behavior.
6. Produce language-neutral conformance artifacts.
7. Freeze benchmark corpora before optimization-driven comparisons.
8. Measure constructor-level wire cost and internal design trade-offs.
9. Compare selected external/structural baselines under explicit assumptions.
10. Distinguish exact program cost from specification, implementation, and bootstrap proxies.
11. Test whether an independent implementation can reconstruct the same language from the published packet.
12. Make receiver assumptions explicit before assigning any numerical bootstrap cost.
13. Preserve positive, negative, conditional, and unresolved findings in a living research record.

## 1.6 Research questions

**RQ1.** Can a small typed lambda core be given a deterministic, architecture-neutral, self-delimiting binary representation with executable conformance tests?

**RQ2.** Can static validity and principal types be reconstructed without transmitting ordinary term-level type annotations?

**RQ3.** Can the dynamic semantics remain simple and non-strict while allowing materially more efficient receiver implementations that preserve observable results?

**RQ4.** Which Core constructs dominate transmitted program cost, and do apparently non-minimal constructs such as `Let` and direct `Nat` justify their presence empirically?

**RQ5.** How does NEX program payload compare with selected alternatives under controlled, explicitly limited comparisons?

**RQ6.** Can `C = S + B + P` already be evaluated numerically, and if not, what evidence is missing?

**RQ7.** Does the published NEX specification and conformance packet determine behavior independently of the Go reference implementation?

**RQ8.** Under which explicit receiver assumptions can a measurable bootstrap cost `B | A` be defined without substituting host-language source size?

## 1.7 Working hypotheses

**H1.** A nameless lambda representation with compact prefix encoding can provide a small, unambiguous program wire format while retaining direct structural decoding.

**H2.** HM-style erased typing can reduce repeated program payload, but its total benefit depends on the unknown bootstrap cost of inference [3,4].

**H3.** A small number of semantic conveniences such as direct naturals and `Let` can reduce total program payload despite enlarging the language definition.

**H4.** Weak call-by-name can serve as a simple normative semantics while call-by-need sharing can be an observationally equivalent implementation optimization on the tested pure fragment [9–11].

**H5.** NEX should not be assumed to dominate highly compressed untyped lambda encodings such as BLC on pure lambda terms; comparative performance must be measured [2].

**H6.** Program payload alone is insufficient to establish overall superiority; receiver-neutral models of `S` and `B` are required.

**H7.** A sufficiently explicit NEX specification and language-neutral conformance suite should allow an implementation produced without access to the Go source to reconstruct the same portable behavior.

## 1.8 Scientific novelty and significance at the present evidence horizon

The novelty claimed here is not invention of lambda calculus, de Bruijn indices, HM inference, or lazy evaluation. Those are established foundations. The research novelty lies in combining them into an explicitly information-accounted transmission experiment and treating specification, bootstrap, program payload, conformance, and implementation independence as one falsifiable engineering-research system.

Current practical significance includes executable conformance artifacts, reproducible measurement tooling, frozen benchmark discipline, and a protocol by which hidden assumptions in a co-developed specification/reference implementation can be exposed by independent reconstruction.

---

# 2. Theoretical and Related-Work Basis

## 2.1 de Bruijn indices

De Bruijn showed that bound variables can be represented without names by numeric references determined by binder structure [1; SRC-0001]. NEX adopts the principle and chooses zero-based indices. Alpha-renaming therefore carries no wire information.

## 2.2 Binary Lambda Calculus

Tromp's Binary Lambda Calculus provides a compact binary representation of untyped lambda terms using de-Bruijn-style structure [2; SRC-0002]. It is both a conceptual precedent and a falsifying compactness baseline. NEX does not copy BLC: NEX adds static typing, `Let`, direct naturals, and fixed primitives. Hence Stage 4 compares BLC only on the identical pure-lambda subset.

## 2.3 Hindley–Milner inference

Milner's polymorphic type discipline supplies decidable inference for a useful rank-1 let-polymorphic language [3; SRC-0003], and Damas–Milner establish principal type schemes [4; SRC-0004]. NEX uses these ideas to reconstruct types rather than transmit ordinary term annotations. Wells' System F undecidability result [7; SRC-0007] is a boundary reminder that stronger implicit polymorphism does not automatically retain those properties.

## 2.4 Typed recursion

Plotkin's LCF/PCF work provides precedent for a small typed functional language with naturals and fixed-point recursion [5; SRC-0005]. NEX's exact primitive set, sums/products, wire representation, and HM `Let` remain project-specific.

## 2.5 Self-delimiting integers

Elias introduced universal integer codes including gamma coding [6; SRC-0006]. NEX defines `U(n)` as Elias gamma coding of `n + 1` so non-negative naturals, de Bruijn indices, and primitive IDs can be self-delimiting.

## 2.6 Evaluation strategy

Plotkin formalized the distinction between call-by-name and call-by-value [9; SRC-0011]. Launchbury formalized lazy evaluation with sharing [10; SRC-0012], and Sestoft developed an abstract-machine treatment [11; SRC-0013]. NEX uses weak CBN normatively and studies call-by-need only as an observationally equivalent optimization candidate.

## 2.7 Combinatory alternatives

Combinatory logic provides alternative small computational bases [8; SRC-0009]. Barker's Iota/Jot material supplies the exact Jot mapping used by the Stage 4 experiment [12; SRC-0014]. The project makes no shortest-Jot-program claim.

## 2.8 Portable core versus embedding

WebAssembly Core is not a semantic basis for NEX, but it is a modern example of separating a portable computational core from host embedding [13; SRC-0008]. NEX adopts that separation principle while not adopting WebAssembly's concrete instruction, memory, or module architecture.

---

# 3. Research Methodology

## 3.1 Artifact-centered method

The project uses the cycle

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

The repository, not chat history, is durable research memory.

## 3.2 Evidence classes

The project distinguishes:

1. established external result;
2. NEX design decision;
3. reproducible NEX measurement;
4. inference from current evidence;
5. open hypothesis or unknown.

This prevents repeated hypotheses from silently becoming facts.

## 3.3 Reproducibility

Evidence is backed where possible by wire/static/evaluation conformance vectors, malformed-input cases, unit/property/fuzz tests, frozen corpora, deterministic experiment CLIs, and clean-checkout GitHub Actions.

## 3.4 Frozen-corpus rule

ADR-0010 makes a benchmark corpus immutable after comparative results are published from it. The preserved v0.2 corpus, where `factorial-5` exceeds the default CBN transition budget, demonstrates that inconvenient outcomes are retained rather than rewritten.

## 3.5 Total-information accounting

```text
C = S + B + P
```

Current meanings:

- `P`: exact canonical program bits for a specified corpus;
- `S`: receiver-neutral specification transmission cost, not yet represented by one accepted artifact;
- `B`: receiver-neutral bootstrap transmission cost, unknown;
- `R`: host/reference implementation proxy, never substituted for `B`.

## 3.6 Independence as an experimental variable

Stage 5 adds a further methodological requirement: implementation independence itself must be controlled.

Writing a second implementation in a new host language is insufficient if its author already knows the internal structure of the first implementation. ADR-0013 therefore separates:

```text
packet/protocol construction
        from
independent implementation evidence
```

The first independent implementation may use only a frozen packet, selected primary theory, and Python 3.12 standard-library documentation. `reference/go/**` and implementation-revealing project material remain excluded until a pre-comparison checkpoint is frozen.

This is a methodological limitation of the current session as well: because it co-developed the Go reference, it may define the packet and neutral infrastructure but cannot honestly label a new implementation authored from remembered Go design as independent evidence.

---

# 4. NEX-1 v0.1 Design

## 4.1 Terms

```text
Term ::= Var(index)
       | Lam(body)
       | App(function, argument)
       | Let(value, body)
       | Nat(value)
       | Prim(id)
```

## 4.2 Types

```text
T ::= a | 1 | N | T -> T | T * T | T + T
S ::= forall a1 ... an. T
```

Static semantics use rank-1 HM-style inference with fresh instantiation, let-generalization, unification, and occurs checking [3,4].

## 4.3 Core primitives

```text
0  fix
1  succ
2  pred
3  ifz
4  pair
5  fst
6  snd
7  inl
8  inr
9  case
10 unit
```

IDs 11–31 are reserved Core space; external profiles begin at 32.

## 4.4 Wire representation

```text
00   U(k)   Var(k)
01   T      Lam(T)
10   T T    App(T,T)
110  T T    Let(T,T)
1110 U(n)   Nat(n)
1111 U(p)   Prim(p)
```

`U(n)` is Elias gamma of `n + 1`.

## 4.5 Dynamic semantics

The normative reference semantics are weak call-by-name. Arguments and `Let` values are delayed; evaluation does not reduce under `Lam` before application. Primitive forcing is selective, and `fix` provides general recursion.

---

# 5. Stage 0 — Research and Architectural Baseline

Stage 0 established canonical documentation, required Russian mirrors, architecture/domain/workflow/testing documents, ADR governance, repository-as-memory rules, and a primary-source registry.

**Conclusion.** A minimal-language experiment first required a mechanism preventing silent semantic drift and retrospective rewriting of rationale.

---

# 6. Stage 1 — Canonical Wire Foundation

Stage 1 implemented arbitrary-precision `U(n)`, the six-constructor term model, canonical encode/decode, exact-versus-prefix APIs, malformed-input errors, and resource limits distinct from wire invalidity.

The completed wire corpus contained 17 integer vectors, 12 term vectors, and 15 invalid exact-input vectors. Representative encodings include:

```text
Var(0)                    001
Nat(0)                    11101
Prim(0)                   11111
Lam(Var(0))               01001
Lam(App(Prim(1),Var(0)))  01101111010001
```

**Conclusion.** RQ1 is supported for the implemented wire grammar by executable conformance evidence, though not yet by formal proof or an independent decoder.

---

# 7. Stage 2 — Static Validation and Principal Types

Stage 2 added closed de Bruijn scope validation, type representation, free-variable calculation, substitutions, unification with occurs check, primitive schemes, instantiation, generalization, and Algorithm-W-style principal inference.

The v0.1 wire continues to erase ordinary term-level type annotations. ADR-0007 treats this as a design choice rather than a proven global optimum.

**Conclusion.** RQ2 is functionally supported by the reference implementation, while the total `S+B+P` comparison against explicit/certified alternatives remains open.

---

# 8. Stage 3 — Dynamic Semantics and Reference Evaluation

Stage 3 implemented weak CBN semantics and tested laziness itself. Terms equivalent to

```text
(lambda x. 7) divergingTerm
ifz 0 42 divergingTerm
fst (pair 1 divergingTerm)
```

return `7`, `42`, and `1` without evaluating irrelevant computation. Curried primitives, `fix`, WHNF observation, and resource refusal are covered by language-neutral evaluation vectors.

**Conclusion.** RQ3 is supported at the normative-semantics level; optimized sharing was left to empirical evaluation.

---

# 9. Stage 4 — Empirical Validation and Benchmarking

Stage 4 is complete by PR #6, squash merge `ebffde6c8669f65dfcba98d31d261d59b48d4dd0`. The final full PR head passed CI run `35377200520`; post-merge `main` passed run `35377892126`.

## 9.1 Frozen corpus

Accepted corpus v0.3 contains 17 programs spanning pure lambda structure, arithmetic/control primitives, pairs, sums, polymorphic `Let`, recursion, multiplication, factorial, Fibonacci, a small recognizer, and repeated expensive bindings.

```text
programs   17
wire bits  1371
AST nodes  345
```

## 9.2 Wire attribution

| Constructor | Bits | Share |
|---|---:|---:|
| `Prim` | 460 | 33.6% |
| `Var` | 286 | 20.9% |
| `App` | 264 | 19.3% |
| `Nat` | 244 | 17.8% |
| `Lam` | 84 | 6.1% |
| `Let` | 33 | 2.4% |

The early expectation that `App` would dominate is not supported on v0.3. `Prim` is the largest measured contributor; the conclusion remains corpus-specific.

## 9.3 `Let` break-even

For a tested 5-bit payload, `Let` costs +4 bits at two uses, +2 at three, ties at four, and saves 8 bits at eight uses. For the tested 14-bit payload, two uses already save 5 bits.

**Decision:** retain `Let`.

## 9.4 Direct naturals

At the measured endpoint:

```text
Nat(255)          21 bits
succ-chain(255) 2300 bits
```

**Decision:** retain direct `Nat`; this does not prove global numeric-code optimality.

## 9.5 Root-type transmission experiment

```text
erased term bits  1371
root type bits      134
hybrid total       1505
overhead           +9.77%
```

This measures `Delta P` only and does not prove that an explicit checker would reduce `B` enough to compensate.

**Decision:** retain erased HM in v0.1 pending real bootstrap/checker evidence.

## 9.6 Baselines

On the identical pure-lambda subset:

```text
NEX  37 bits
BLC  30 bits
Jot via fixed SK translation  288 bits
```

Thus NEX cannot claim universal program-size superiority over BLC.

On full v0.3:

```text
NEX canonical wire  1371 bits
tiny postfix stack  1529 bits
```

The tiny-stack comparison reuses NEX numeric/primitive conventions and is therefore structural, not an independent total-bootstrap comparison.

## 9.7 CBN versus call-by-need

All 17 accepted programs produced the same observable WHNF under normative CBN and experimental call-by-need.

```text
CBN transitions             226151
call-by-need transitions      2484
reduction                    98.90%
memo hits                       237
programs improved              6/17
```

Representative heavy workloads include `factorial-4` at 209,315 -> 895 transitions and `fibonacci-5` at 7,424 -> 512. The counters are Go-reference measurements, not architecture-neutral costs or terms in `C`.

**Decision:** keep CBN normative; permit observationally equivalent call-by-need optimization.

## 9.8 Total-information accounting

```text
P exact                         1371 bits
spec Markdown proxy           23440 UTF-8 bytes
selected Go reference Core    43013 UTF-8 bytes
B                              unknown
C                              not numerically computable
```

Markdown is not accepted as receiver-neutral `S`; Go source is `R`, not `B`.

**Stage 4 conclusion.** The evidence supports several local v0.1 design choices but does not support global minimality or a numerical total-cost claim.

---

# 10. Stage 5 — Independent Reconstruction and Receiver-Neutral Bootstrap

Stage 5 is in progress. The current evidence horizon covers Stage 5.0 and Stage 5.1 only; the independent implementation itself has deliberately not started in the co-development context.

## 10.1 Stage 5.0 — independence protocol

ADR-0013 freezes the first implementation-input packet against repository commit:

```text
4f9c50aed13cdbdf72c9ce6510521477d49c05a5
```

The first independent implementation target is:

```text
Python 3.12+
standard library only
```

Python was selected because its host model differs materially from Go and its integers are arbitrary precision without a third-party dependency. This choice is methodological; Python source size is not bootstrap `B`.

The frozen packet allowlists the canonical NEX-1 specification, wire/static/evaluation conformance files, and only the accepted ADRs required for Core validity/resource semantics. `reference/go/**`, Stage 4 experiment material, benchmark corpora, status/dissertation/history documents, and ADR-0008's Go evaluator architecture are excluded as implementation guidance before the independence checkpoint.

The current co-development context has prior knowledge of the Go reference. Consequently, any second implementation authored from that remembered design would be a useful port but weak independent evidence. Strong evidence requires a fresh isolated context or another implementer receiving only the materialized packet and allowlisted primary theory.

## 10.2 Reproducible packet

`stage5/conformance-packet-v0.1/manifest.json` records exact Git blob hashes of every frozen source file. `stage5/build_packet.py` verifies those hashes, validates conformance schema IDs, materializes only allowlisted files, and writes a generated SHA-256 file manifest.

Dedicated GitHub Actions run `35379868436` completed successfully. It published standalone artifact:

```text
name: nex1-independent-conformance-packet-v0.1
artifact id: 10560808823
archive size: 28199 bytes
artifact digest: sha256:fca1fddff742674c4e0b832ea53022d712f292d1361dfbe9b1b62c022ead15c3
```

The archive size is an engineering artifact size, not `S` or `B`.

## 10.3 Stage 5.1 completeness audit

The packet audit found no currently known missing Core semantic rule blocking a first independent implementation, but it found two presentation-layer omissions.

### F1 — principal type observation format

The specification defines principal schemes semantically up to alpha-renaming, while static conformance stores text such as `forall T0 T1. ...`. The packet therefore now defines canonical comparison rendering by renaming quantified variables `T0`, `T1`, ... in first-occurrence order and fully parenthesizing compound monotypes.

**Classification:** conformance observation-format omission, not a Core typing ambiguity.

### F2 — JSON fixture mapping

The conformance files used JSON objects with `kind`, `value`, `a`, and `b`, but JSON itself is not NEX wire syntax and the mapping had not been explicitly documented as a fixture contract.

**Classification:** test-fixture representation omission, not a Core wire ambiguity.

Both F1 and F2 are now defined in `stage5/conformance-packet-v0.1/OBSERVATIONS.md` without changing NEX-1 v0.1 semantics.

### F3 — intentionally unspecified implementation details

Fresh type-variable allocation, substitution-map layout, evaluator object representation, and environment-versus-substitution machinery remain deliberately implementation-specific. The packet compares normalized principal schemes and observable WHNF, not host internals.

### F4 — error precedence

The packet does not invent a global precedence rule for hypothetical inputs containing multiple independent static defects. Existing conformance cases specify their required portable error class. If independent/generated testing demonstrates a need for a portable precedence rule, Stage 5.6 will add the smallest explicit rule and vector.

## 10.4 Interpretation

The Stage 5.1 findings are modest but scientifically useful: independent reconstruction forces the project to distinguish **language semantics** from **test presentation conventions** and **reference implementation architecture**. This is precisely the class of hidden dependency that cannot be discovered merely by adding more tests against the same implementation.

## 10.5 Next checkpoint

Stage 5.2–5.4 must be implemented in a fresh isolated context from the frozen packet. A pre-comparison implementation commit must then be frozen before `reference/go` is opened for differential testing. Any discrepancy will be classified as specification ambiguity/omission, Go bug, independent implementation bug, conformance gap, or deliberately unspecified behavior.

The bootstrap half of Stage 5 will subsequently define explicit receiver assumption sets and seek conditional measurements written as `B | A`, rather than pretending that one unconditional alien prior is known.

---

# 11. Discussion and Answers to Research Questions

## 11.1 RQ1

**Supported for the reference implementation; independent confirmation pending.** Wire grammar and executable vectors are mature, but Stage 5 will test whether the same behavior can be reconstructed without Go implementation knowledge.

## 11.2 RQ2

**Functionally supported, globally unresolved.** HM principal inference works without ordinary term annotations. Stage 4 measured +9.77% `P` for one root-type envelope, but bootstrap savings remain unknown.

## 11.3 RQ3

**Strongly supported on the tested corpus.** Weak CBN provides simple normative behavior, while a separate call-by-need implementation preserved observables and greatly reduced repeated work on selected recursive workloads.

## 11.4 RQ4

**Corpus-specific answer:** `Prim` is the largest measured v0.3 wire contributor; `Let` and direct `Nat` are empirically justified against the tested alternatives.

## 11.5 RQ5

**Mixed result.** BLC is smaller on the identical pure-lambda subset; NEX is smaller than the selected tiny postfix baseline on full v0.3. No total-cost external winner can be declared.

## 11.6 RQ6

**No.** `P` is exact for frozen corpora, but receiver-neutral `S` and `B` are not yet available.

## 11.7 RQ7

**Not yet answered.** Stage 5.0–5.1 establish a credible test protocol and already reveal presentation-layer omissions, but no isolated second implementation has yet been frozen.

## 11.8 RQ8

**Not yet answered.** The project has adopted the principle that bootstrap measurements must be conditioned on explicit assumptions (`B | A`), but Stage 5.7–5.8 have not begun.

---

# 12. Threats to Validity and Limitations

1. **Small corpus.** Seventeen programs cannot represent all software distributions.
2. **Hand-construction bias.** Some benchmark terms and translations were manually designed.
3. **Single complete implementation.** Go remains the only full implementation; Stage 5 is intended to address this.
4. **Cognitive contamination.** The current development context knows the Go implementation; it cannot be used as the sole source of "independent" implementation evidence.
5. **Runtime counters are host-specific.** Transition/depth statistics are not portable units of computation.
6. **Explicit-type experiment is incomplete.** Root-type transmission does not implement an alternative checker/bootstrap.
7. **External baselines are limited.** BLC comparison is narrow; tiny stack reuses NEX conventions; Jot depends on one translation.
8. **Receiver-neutral `S` and `B` remain unknown.** This is the largest gap relative to the motivating objective.
9. **No machine-checked proof.** Fuzzing, vectors, and CI are empirical evidence, not formal proof.
10. **Packet completeness is provisional.** The strongest audit is the independent implementation itself; any request to "check Go" before the checkpoint is evidence of a specification/packet gap.

---

# 13. Research Contributions to Date

1. A concrete architecture-neutral typed Core with canonical binary representation.
2. Executable separation of wire validity, scope validity, type validity, and resource refusal.
3. Language-neutral conformance corpora for wire, static, and dynamic semantics.
4. Evidence-gated development with frozen benchmarks before optimization.
5. Exact constructor-level wire attribution on a frozen corpus.
6. Measured break-even evidence for `Let` and strong evidence for direct `Nat` against repeated `succ`.
7. A quantified first experiment on erased versus transmitted root type information.
8. Controlled comparisons with BLC, a Jot translation, and a structural stack baseline.
9. An observational CBN/call-by-need experiment demonstrating large implementation-level savings on selected workloads.
10. A total-information accounting model that refuses to equate host source size with receiver-neutral bootstrap cost.
11. A living dissertation process preserving positive, negative, conditional, and unresolved findings.
12. A frozen independent-conformance protocol that explicitly controls implementation knowledge leakage.
13. A reproducible standalone packet artifact with content hashes and a dedicated CI gate.
14. Early specification-audit findings separating semantic rules from conformance presentation conventions.

---

# 14. Future Research

## 14.1 Isolated independent implementation

Implement wire, static, and normative dynamic semantics in Python 3.12 using only the frozen packet and allowed theory. Freeze the implementation before any Go comparison.

## 14.2 Differential conformance

After the independent freeze, compare portable outputs against Go and classify every discrepancy rather than forcing one side to match the other.

## 14.3 Receiver-assumption model

Define explicit assumption sets covering channel/framing, binary ordering, mathematical concepts, integer coding, term structure, and execution semantics. Bootstrap costs must be written conditionally as `B | A`.

## 14.4 First measurable bootstrap artifact

Investigate a concrete transmitted artifact such as a tiny abstract machine, layered decoder-validator-evaluator description, or another explicitly decodable representation. Circular interpreter assumptions must be accounted for rather than hidden.

## 14.5 Primitive-reference encoding

`Prim` remains the largest measured wire category, but compactness redesign is intentionally deferred until independent reconstruction is complete.

## 14.6 Full typing alternatives

A meaningful erased-versus-explicit comparison requires an actual alternative verifier/checker and bootstrap accounting, not only root-type transmission.

## 14.7 Broader corpora and formal verification

Future work should expand common-source corpora and consider proof-assistant formalization of decoder, substitution/unification, and evaluation properties after executable semantics stabilize further.

---

# 15. Conclusion

The research began from a deceptively simple question: if programming languages are designed for humans and known machines, what computational representation should be used when the sender cannot assume either?

The work shows that the answer cannot be reduced to shortest syntax. NEX-1 v0.1 has a compact canonical binary form, reconstructible principal typing in the reference implementation, and explicitly non-strict semantics. Stage 4 then demonstrated why measurement matters: direct naturals are strongly justified against the tested successor construction, `Let` has a real break-even, BLC is smaller on the measured pure-lambda subset, call-by-need can remove enormous repeated runtime work without changing program bits, and `Prim` rather than `App` is the largest measured wire contributor on v0.3. At the same time, total `C` remains unknown because receiver-neutral `S` and `B` are not yet defined.

Stage 5 changes the question from "does our implementation pass our tests?" to "can an implementation that did not see our implementation recover the same system?" The first protocol checkpoint already demonstrates the value of that shift by exposing presentation assumptions that were harmless inside one codebase but insufficiently explicit for an external implementer.

The next decisive evidence must therefore come from two sources: an isolated second implementation and a measurable bootstrap under explicit receiver assumptions. Only after those results should NEX-1 v0.2 compactness redesign be considered.

---

# Glossary

**ABI (Application Binary Interface)** — conventions governing binary interaction between compiled components and a platform.

**Alpha-equivalence** — equivalence of lambda terms differing only in bound-variable names.

**Architecture-neutral** — defined without dependence on a particular processor ISA, word size, ABI, OS, or host runtime.

**AST (Abstract Syntax Tree)** — structural in-memory program representation.

**Binary Lambda Calculus (BLC)** — John Tromp's compact binary representation of untyped lambda terms [2].

**Bootstrap (`B`)** — receiver-neutral information required to realize enough machinery to process NEX; currently unknown.

**Call-by-name (CBN)** — non-strict strategy in which an argument is not evaluated before use and may be recomputed [9].

**Call-by-need** — lazy evaluation with sharing/memoization [10,11].

**Cognitive independence** — for this project, an implementation condition in which the implementer/context has not used the excluded reference implementation as implementation guidance before the freeze checkpoint.

**Conformance packet** — frozen, versioned set of specification, normative decisions, vectors, and observation conventions supplied to the independent implementation.

**Conformance vector** — language-neutral input/expected-output artifact used to test specification agreement.

**de Bruijn index** — numeric reference to binding depth instead of a variable name [1].

**Erased typing** — ordinary term wire omits type annotations and reconstructs them by inference.

**Hindley–Milner (HM)** — rank-1 polymorphic type-inference discipline used by NEX [3,4].

**Occurs check** — unification check preventing a variable from being unified with a type containing itself.

**Principal type scheme** — most general HM type scheme from which other valid types can be instantiated [4].

**Primitive (`Prim`)** — fixed Core operation identified by a numeric ID.

**Receiver-neutral** — not relying on uncommunicated terrestrial implementation conventions.

**Resource refusal** — implementation failure due to finite limits, distinct from malformed syntax, static invalidity, or a normal result.

**Specification cost (`S`)** — information required to communicate the computational rules themselves.

**Thunk** — delayed computation, conceptually a term plus its environment or equivalent delayed representation.

**Total information cost (`C`)** — research objective `C = S + B + P`.

**Transmitted-program cost (`P`)** — exact canonical program bits for a specified workload.

**Weak-head normal form (WHNF)** — evaluation only far enough to reveal the outer computational form.

**Wire format** — canonical transmitted bit representation of NEX terms.

---

# Bibliography

Stable source identifiers correspond to `docs/SOURCES.md`.

1. **de Bruijn, N. G.** (1972). *Lambda calculus notation with nameless dummies, a tool for automatic formula manipulation, with application to the Church-Rosser theorem.* DOI: https://doi.org/10.1016/1385-7258(72)90034-0. `[SRC-0001]`
2. **Tromp, J.** *Binary Lambda Calculus.* https://tromp.github.io/cl/Binary_lambda_calculus.html. `[SRC-0002]`
3. **Milner, R.** (1978). *A Theory of Type Polymorphism in Programming.* DOI: https://doi.org/10.1016/0022-0000(78)90014-4. `[SRC-0003]`
4. **Damas, L.; Milner, R.** (1982). *Principal Type-Schemes for Functional Programs.* DOI: https://doi.org/10.1145/582153.582176. `[SRC-0004]`
5. **Plotkin, G. D.** (1977). *LCF Considered as a Programming Language.* DOI: https://doi.org/10.1016/0304-3975(77)90044-5. `[SRC-0005]`
6. **Elias, P.** (1975). *Universal codeword sets and representations of the integers.* DOI: https://doi.org/10.1109/TIT.1975.1055349. `[SRC-0006]`
7. **Wells, J. B.** (1999). *Typability and type checking in System F are equivalent and undecidable.* DOI: https://doi.org/10.1016/S0168-0072(98)00047-5. `[SRC-0007]`
8. **Schönfinkel, M.** (1924). *Über die Bausteine der mathematischen Logik.* Mathematische Annalen 92, 305–316. `[SRC-0009]`
9. **Plotkin, G. D.** (1975). *Call-by-name, call-by-value and the lambda-calculus.* DOI: https://doi.org/10.1016/0304-3975(75)90017-1. `[SRC-0011]`
10. **Launchbury, J.** (1993). *A Natural Semantics for Lazy Evaluation.* DOI: https://doi.org/10.1145/158511.158618. `[SRC-0012]`
11. **Sestoft, P.** (1997). *Deriving a lazy abstract machine.* DOI: https://doi.org/10.1017/S0956796897002712. `[SRC-0013]`
12. **Barker, C.** (2001). *Iota and Jot: the simplest languages?* Archived author-maintained reference: https://web.archive.org/web/20201112014512/http://www.nyu.edu/projects/barker/Iota/. `[SRC-0014]`
13. **W3C WebAssembly Working Group.** *WebAssembly Core Specification.* https://www.w3.org/TR/wasm-core/. `[SRC-0008]`
14. **The Go Project.** *The Go Programming Language Specification; math/big; testing/fuzzing documentation.* https://go.dev/ref/spec. `[SRC-0010]`

---

# Appendix A. Reproducibility and Project Artifacts

## A.1 Normative / architectural

- `docs/NEX-1-v0.1.md` — canonical Core specification.
- `docs/NEX-1-v0.1.ru.md` — Russian mirror.
- `docs/ARCHITECTURE.md` — architecture boundaries.
- `docs/adr/` — architecture/research decisions.
- `docs/SOURCES.md` — external source registry.

## A.2 Conformance

- `conformance/wire-v0.1.json`
- `conformance/static-v0.1.json`
- `conformance/eval-v0.1.json`

## A.3 Benchmarks and Stage 4 tools

- `benchmarks/corpus-v0.1.json`
- `benchmarks/corpus-v0.2.json`
- `benchmarks/corpus-v0.3.json`
- `reference/go/cmd/nexbench`
- `reference/go/cmd/nexexperiment`
- `reference/go/cmd/nextypeexperiment`
- `reference/go/cmd/nexbaseline`
- `reference/go/cmd/nexstrategy`
- `reference/go/cmd/nexaccount`
- `reference/go/cmd/nexreport`

## A.4 Stage 5 packet

- `docs/adr/0013-stage5-independence-protocol.md`
- `stage5/conformance-packet-v0.1/manifest.json`
- `stage5/conformance-packet-v0.1/OBSERVATIONS.md`
- `stage5/conformance-packet-v0.1/AUDIT.md`
- `stage5/build_packet.py`
- `.github/workflows/stage5-independence.yml`

Dedicated packet verification:

```text
GitHub Actions run 35379868436 — success
artifact 10560808823
sha256:fca1fddff742674c4e0b832ea53022d712f292d1361dfbe9b1b62c022ead15c3
```

## A.5 Stage completion evidence

- Stage 1 merge: `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`.
- Stage 2 merge: `cefe889d90a275897de31aa23c4b9742a388ec8f`.
- Stage 3 merge: `166cdc03282ea500263fdca7185f006f9b17a702`.
- Stage 4 merge: `ebffde6c8669f65dfcba98d31d261d59b48d4dd0`.
- Stage 4 post-merge CI: `35377892126` — success.

---

# Appendix B. Evidence-Gated Decision Summary

| Question | Current decision | Evidence status |
|---|---|---|
| Keep direct `Nat`? | Keep in v0.1 | Strong corpus experiment against repeated `succ`; not global optimality |
| Keep `Let`? | Keep in v0.1 | Measured break-even |
| Keep erased HM? | Keep in v0.1; defer global redesign | Working inference + root-type `Delta P`; bootstrap comparison missing |
| Is CBN normative? | Yes | Specification/conformance |
| Use call-by-need? | Allowed optimization when observably equivalent | 17/17 corpus agreement; reference-runtime savings |
| Optimize `Prim` first? | Future priority only | Largest measured v0.3 wire category |
| Is NEX smaller than BLC? | No global claim | BLC wins 30 vs 37 bits on the shared lambda subset |
| Is total `C` known? | No | Receiver-neutral `S` and `B` unresolved |
| Is NEX independently reconstructable? | Not yet established | Stage 5 packet/protocol ready; isolated implementation pending |
| Can current context implement "independently"? | No | Prior Go design exposure is recorded as cognitive contamination |

---

# Maintenance Rule

Per ADR-0012, any future change producing a material measurement, research-significant decision, external baseline/source, independent conformance result, formal proof/counterexample, stage-level conclusion, revised `S/B/P/C` evidence, or falsification/qualification of a prior hypothesis must update this English manuscript and its Russian mirror in the same PR unless the PR explicitly documents why no research-text change is required.
