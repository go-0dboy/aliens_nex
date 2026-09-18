# NEX-1: A Compact Architecture-Neutral Typed Core for Teaching and Transmitting Computation

## Design, executable semantics, empirical validation, independent reconstruction, and receiver-conditioned teaching/bootstrap

**Document type:** living dissertation-style research manuscript  
**Canonical language:** English  
**Russian mirror:** `RESEARCH-DISSERTATION.ru.md`  
**Evidence horizon:** Stages 0–5 complete; post-Stage-5 literature re-audit incorporated as of 2026-09-19  
**Project:** NEX / `aliens_nex`

> This manuscript is a research synthesis. It does not replace the normative NEX-1 v0.1 specification, ADRs, conformance vectors, source code, or reproducible experiment artifacts.

---

## Abstract

This research asks whether an unknown receiver can be taught a formal computational system well enough to decode, type-check, execute, and eventually author programs in it, without assuming a shared terrestrial programming language, processor architecture, ABI, operating system, text encoding, or runtime.

NEX-1 v0.1 is the current target computational Core. It has six term constructors (`Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`), zero-based de Bruijn indices, rank-1 Hindley–Milner inference, arbitrary-precision naturals, explicit general recursion through `fix`, a fixed typed primitive basis, a self-delimiting binary representation, and weak call-by-name semantics.

The historical accounting shorthand

```text
C = S + B + P
```

is retained as a conceptual ledger for specification, bootstrap, and program payload. Exact numerical claims are stricter: under a declared receiver-assumption profile `A`, total transmitted cost is the length of one concrete transmitted object `M_A`,

```text
C | A = |M_A|.
```

A decomposition into `S`, `B`, and `P` is valid only when the corresponding transmitted roles are explicitly serialized and counted without overlap.

Stages 1–3 established executable wire, static, and dynamic semantics. Stage 4 froze benchmark corpora before optimization conclusions. On the accepted 17-program corpus, canonical NEX occupies 1,371 bits over 345 AST nodes; `Prim` contributes 460 bits (33.6%). Direct `Nat(255)` occupies 21 bits versus 2,300 bits for the tested repeated-`succ` construction. A root-principal-type envelope adds 134 bits, or 9.77% to program payload. On an identical three-program pure-lambda subset, Binary Lambda Calculus is smaller than NEX (30 versus 37 bits). An experimental call-by-need evaluator preserved all 17 accepted results while reducing the project-defined Go evaluator transition counter from 226,151 to 2,484; this is not a wall-clock speedup claim.

Stage 5 tested reconstruction from a frozen specification/conformance packet. A Python implementation was produced without access to `reference/go` and frozen before comparison. Post-freeze differential testing produced 942 matching portable observations, zero semantic mismatches, and zero resource asymmetries. This is strong differential-conformance evidence of reconstructability on the tested surface, not a proof of semantic correctness or specification completeness.

Stage 5 also made receiver assumptions explicit. The corrected current taxonomy distinguishes `A0` (exact binary frame), `A1` (elementary discrete mathematics), `A1(R)` (an exact formal rule calculus), `A2(U)` (an exact universal machine and framing), and `A_host(H)` (a terrestrial engineering control). No complete receiver-neutral bootstrap artifact has yet been accepted, so full `B | A` and total `C | A` remain unknown.

The post-Stage-5 literature re-audit did not reveal a fundamental defect in NEX-1 v0.1. It did clarify the next research problem. Lincos, DeVito–Oehrle, Lingua Cosmica, and especially CosmicOS show that an interstellar formal system is not only a grammar or interpreter: it is also a **teaching sequence**. NEX therefore needs a separate teaching/bootstrap layer that progressively establishes the meaning of the stable NEX-1 Core and provides receiver self-tests.

The next stage should construct and measure that finite teaching artifact rather than immediately redesign the Core.

**Keywords:** architecture-neutral computation, teaching protocol, binary program representation, de Bruijn indices, Hindley–Milner, bootstrap, receiver assumptions, Binary Lambda Calculus, differential conformance, interstellar communication.

---

# 1. Research problem

Conventional software assumes extensive shared context: source syntax, text encodings, processors, executable formats, operating systems, compilers, virtual machines, and data conventions. For an unknown receiver these are not free facts; they are part of the interpretation problem.

A short program is not useful if its meaning depends on a large untransmitted interpreter. Conversely, a tiny interpreter may force all later programs to become unnecessarily large. More fundamentally, even a perfect interpreter artifact is useless if the receiver cannot determine what it is supposed to mean or how to validate its reconstruction.

The project therefore studies two coupled objects:

1. **NEX-1 Core** — the exact target computational system;
2. **a teaching/bootstrap message** — the finite transmitted sequence that establishes enough semantics for the receiver to reconstruct and use that Core.

The central practical goal is:

> given an explicit receiver prior, construct a finite message after which the receiver can demonstrably decode, type-check, execute, and construct NEX programs.

Historical novelty is not a success criterion. Prior work is valuable insofar as it improves this construction.

---

# 2. Research questions

**RQ1.** Can NEX be given a deterministic, architecture-neutral, self-delimiting binary representation with executable conformance evidence?

**RQ2.** Can closed NEX programs recover principal rank-1 types without ordinary transmitted type annotations?

**RQ3.** Can weak call-by-name remain a simple normative semantics while a sharing implementation preserves portable observations?

**RQ4.** Which constructs dominate program payload on the frozen corpus, and are `Let` and direct `Nat` empirically justified against the tested alternatives?

**RQ5.** How does NEX payload compare with selected external encodings on explicitly shared subsets?

**RQ6.** Can complete transmitted cost already be evaluated numerically?

**RQ7.** Can a second implementation, produced without access to `reference/go`, reconstruct the same portable wire, static, and dynamic observations from a frozen packet?

**RQ8.** Under which explicit receiver assumptions can a complete bootstrap be represented and measured without hiding an interpreter or double-counting transmitted bits?

**RQ9.** What finite teaching/bootstrap sequence is sufficient to move a receiver from an explicit prior profile to operational NEX competence?

RQ9 is the main question for the next stage.

---

# 3. Related work and design lessons

## 3.1 Computational representation and type theory

De Bruijn indices provide nameless bound-variable references [SRC-0001]. Binary Lambda Calculus provides a compact binary lambda representation and external baseline [SRC-0002]. Milner and Damas–Milner provide the basis for rank-1 let-polymorphism and principal type schemes [SRC-0003, SRC-0004]. Plotkin's work provides classical typed-recursive-calculus and evaluation-strategy foundations [SRC-0005, SRC-0011]. Elias provides the integer-code family from which NEX uses gamma coding of `n+1` [SRC-0006].

The re-audit corrected an earlier rationale: combinatory logic is not intrinsically incompatible with static typing. Hindley established principal type-scheme results for combinatory logic [SRC-0018]. SK/SKI therefore remains a legitimate competitor; NEX's v0.1 choice is a representation/design trade-off, not a claim that typed combinators are impossible.

## 3.2 Call-by-need

Launchbury and Sestoft formalize lazy evaluation and sharing [SRC-0012, SRC-0013]. Maraist, Odersky, and Wadler establish a strong observational relationship between call-by-need and call-by-name in their studied calculus [SRC-0023]. These sources motivate the NEX optimization experiment but do not replace a NEX-specific equivalence proof for its exact `fix`, naturals, sums/products, and forcing rules.

## 3.3 Description length and receiver assumptions

Shannon separates engineering transmission from semantic meaning [SRC-0015]. Kolmogorov and Chaitin emphasize interpretation-relative algorithmic/program-size descriptions [SRC-0016, SRC-0017]. Rissanen similarly includes model/description burden in shortest-description reasoning [SRC-0019]. These results motivate the receiver-conditioned `C | A = |M_A|` formulation.

## 3.4 Interstellar teaching languages

Freudenthal's **Lincos** [SRC-0020] demonstrates progressive semantic teaching through constrained examples. DeVito and Oehrle [SRC-0028] emphasize the role of assumed prior scientific knowledge. Work on **Lingua Cosmica** uses constructive type theory to constrain logical interpretation [SRC-0022]. **CosmicOS** [SRC-0021] is especially close to the NEX objective because it progressively introduces mathematics, logic, executable programs, and simulations.

These projects are not treated as obstacles to NEX. They provide design lessons.

The most important comparison is:

| Question | CosmicOS emphasis | NEX emphasis |
|---|---|---|
| How does the receiver learn? | progressive executable curriculum | not yet a dedicated protocol |
| Final computational system | Lisp-like programs/simulations | small typed Core |
| Static checking | not centered on HM | central |
| Exact canonical binary representation | not primary objective | primary objective |
| Independent reconstruction test | not NEX-style | frozen blind Python implementation |
| Exact bit ledger | not primary objective | central methodology |

The architectural conclusion is therefore:

```text
NEX Teaching / Bootstrap Message
        -> NEX-1 Core competence
        -> canonical NEX programs
```

The teaching representation may be redundant or pedagogical even if the final Core representation remains compact.

## 3.5 Limits of assumed mathematics

The receiver profiles are experimental conditions, not claims about extraterrestrial cognition. Exosemiotic work explicitly questions whether mathematics and science should be assumed to be conceptualized identically by another intelligence [SRC-0029]. Therefore `A1` is an explicit prior chosen for an experiment, not a universal fact.

## 3.6 Independent implementations and differential testing

Stage 5 reduces implementation leakage, but agreement between two implementations is not a proof oracle. Knight–Leveson show that independently developed versions can exhibit correlated failures [SRC-0024], and differential testing cannot reveal a defect shared by every implementation [SRC-0027]. This directly constrains the meaning of `942/942`.

---

# 4. Methodology

The project uses an evidence-gated workflow:

```text
Problem
 -> Contract
 -> Invariant
 -> Executable example or failing test
 -> Implementation
 -> Verification
 -> Diff review
 -> Status checkpoint
 -> Research synthesis
```

The repository is durable project memory. Claims are classified as external facts, project decisions, reproducible measurements, evidence-based inferences, hypotheses, or unknowns.

Comparative corpora are frozen before optimization conclusions. Negative results are preserved. Resource refusal is kept separate from malformed input, static invalidity, and proof of divergence.

For independent reconstruction, an allowlisted packet was frozen before the second implementation. The second implementation was content-hash frozen before access to `reference/go`. Differential testing then compared only portable observations.

For total accounting:

```text
C | A = |M_A|
```

with disjoint-role decomposition only when defensible:

```text
C | A = (S | A) + (B | A,S) + (P | A,S,B)
```

or joint specification/bootstrap:

```text
C | A = (SB | A) + (P | A,SB)
```

Every transmitted bit is counted once.

---

# 5. NEX-1 v0.1

## 5.1 Terms

```text
Term ::= Var(index)
       | Lam(body)
       | App(function, argument)
       | Let(value, body)
       | Nat(value)
       | Prim(id)
```

Bound variables use zero-based de Bruijn indices.

## 5.2 Types

```text
T ::= a | 1 | N | T -> T | T * T | T + T
S ::= forall a1 ... an. T
```

Static semantics use rank-1 HM inference with unification, occurs check, fresh instantiation, and `Let` generalization.

The existing implementations are strong executable evidence, but NEX-specific canonical-forms/preservation/progress-or-safety proofs remain open [SRC-0026]. If future profiles add mutable references or comparable effects, the v0.1 generalization rule must be revisited [SRC-0025].

## 5.3 Core primitives

```text
0 fix   1 succ   2 pred   3 ifz
4 pair  5 fst    6 snd    7 inl
8 inr   9 case   10 unit
```

## 5.4 Wire representation

`U(n)` is Elias gamma coding of `n+1`.

```text
00   U(k)   Var(k)
01   T      Lam(T)
10   T T    App(T,T)
110  T T    Let(T,T)
1110 U(n)   Nat(n)
1111 U(p)   Prim(p)
```

Constructor prefix lengths are `2,2,2,3,4,4`, whose Kraft sum is 1. A future shorter `Prim` constructor prefix therefore requires compensating change elsewhere; `Prim`'s measured corpus cost should be decomposed into constructor-prefix and primitive-ID contributions before redesign.

## 5.5 Dynamic semantics

The normative strategy is weak call-by-name. Arguments and `Let` values are delayed, reduction does not occur beneath `Lam` before application, primitive forcing is selective, pair/sum payloads remain delayed, and recursion is explicit through `fix`.

Call-by-need remains an allowed implementation strategy only when portable Core observations are preserved.

---

# 6. Results of Stages 1–4

Stages 1–3 produced executable wire, type, and evaluation conformance. Stage 4 froze an empirical corpus before optimization conclusions.

For corpus v0.3:

| Metric | Value |
|---|---:|
| Programs | 17 |
| AST nodes | 345 |
| Canonical wire bits | 1,371 |

Constructor attribution:

| Constructor | Bits | Share |
|---|---:|---:|
| `Prim` | 460 | 33.6% |
| `Var` | 286 | 20.9% |
| `App` | 264 | 19.3% |
| `Nat` | 244 | 17.8% |
| `Lam` | 84 | 6.1% |
| `Let` | 33 | 2.4% |

These are properties of the frozen corpus, not frequency estimates for software in general.

### `Let`

For the tested 5-bit payload, `Let` loses to duplication at two and three uses, ties at four, and wins at eight. For the tested 14-bit payload it saves bits at two uses. This supports retaining `Let` while acknowledging a real break-even.

### Direct naturals

```text
Nat(255)          21 bits
succ-chain(255) 2300 bits
```

This strongly supports direct naturals against the tested repeated-`succ` alternative, but does not prove global optimality of gamma coding.

### Root type transmission

```text
erased terms      1371 bits
root type data      134 bits
hybrid total       1505 bits
                  +9.77%
```

Only `Delta P` is measured; any reduction in checker/bootstrap burden remains unconstructed.

### External baselines

On the identical three-program pure-lambda subset:

```text
NEX  37 bits
BLC  30 bits
```

No global winner follows. The Jot result is one deterministic translation, not a shortest-program search.

### CBN versus call-by-need

All 17 accepted observables agreed. The project-defined evaluator counters were:

```text
CBN           226151
call-by-need    2484
reduction      98.90%
```

This is a transition-counter reduction, not a wall-clock or CPU-speed claim.

---

# 7. Stage 5 — independent reconstruction

The second implementation received a frozen packet without access to `reference/go` and was frozen before direct comparison.

Frozen archive:

```text
sha256:783e4186f9a8c024f00a732deae33b547c81ed4d7639c610a1e8bc5997eb3fbe
```

Post-freeze comparison produced:

```text
942 portable matches
0 semantic mismatches
0 resource asymmetries
```

The 942 cases consist of:

```text
17   frozen corpus programs
325  valid cases = 25 parameter sets x 13 AST templates
100  static-error cases = 25 parameter sets x 4 error families
500  randomized term shapes tested at wire level
```

The accepted conclusion is strong differential-conformance evidence of reconstructability on the tested surface.

A further limitation is that the top-level portable observation `Function` is deliberately coarse. Future exhaustive testing should apply returned functions in generated contexts rather than relying only on the `Function` label.

---

# 8. Receiver assumptions and bootstrap

The current corrected model is:

```text
A0       exact binary-frame prior
A1       elementary naturals and finite-sequence mathematics
A1(R)    A1 + exact formal rule calculus R and serialization
A2(U)    A1 + exact universal machine U and framing
A_host(H) terrestrial engineering control
```

Historical Stage 5 `assumptions-v0.1.json` is preserved unchanged; current work uses `assumptions-v0.2.json`.

Stage 5.8 tested three paths:

- recursive rules under historical `A1`: incomplete because the rule language itself was unspecified;
- BLC under `A2(U=BLC)`: incomplete because no complete verified NEX interpreter in BLC exists;
- Python 3.12: finite engineering control but not receiver-neutral bootstrap.

Accepted result:

```text
accepted complete bootstrap candidates  0
full B | A known                        false
full SB | A known                       false
total C | A computable                  false
```

This negative result is retained.

---

# 9. Answers to current research questions

**RQ1.** Supported for v0.1 by executable conformance and two agreeing implementations.

**RQ2.** Functionally supported; total-cost optimality and formal NEX-specific type safety remain unresolved.

**RQ3.** Supported empirically on tested programs; a NEX-specific equivalence theorem remains open.

**RQ4.** Answered for the frozen corpus: `Prim` is largest there, `Let` has a break-even, and direct `Nat` strongly beats the tested repeated-`succ` construction.

**RQ5.** Mixed: BLC is smaller on the controlled pure-lambda subset; no global winner is established.

**RQ6.** No. Exact `P` exists for stated corpora, but complete `S | A`/`B | A`/`C | A` do not.

**RQ7.** Strongly supported as differential-conformance evidence on the tested surface.

**RQ8.** Methodologically clarified but numerically open; no complete receiver-neutral bootstrap exists.

**RQ9.** Not yet answered. This is the primary next-stage question.

---

# 10. Threats to validity

- The accepted design corpus contains only 17 programs and is hand-designed.
- External translations such as Jot are fixed project translations, not globally shortest programs.
- The 942 differential cases are structured families, not 942 independently designed semantic workloads.
- Two independent implementations can share correlated errors.
- `Function` is a deliberately coarse portable observation unless tested through application contexts.
- Runtime counters are implementation-specific.
- The explicit-typing alternative has not been implemented as a complete checker/bootstrap system.
- Receiver profiles are research conditions, not claims about actual extraterrestrial knowledge.
- The physical communication layer is outside `A0` and is not assigned zero cost.
- No machine-checked proof establishes complete NEX semantic correctness or optimality.

---

# 11. Contributions/results to date

The project has produced:

1. a compact architecture-neutral typed Core with canonical binary representation;
2. executable separation of wire validity, scope validity, type validity, evaluation, and finite resource refusal;
3. language-neutral wire/static/dynamic conformance artifacts;
4. frozen empirical methodology that preserves inconvenient and negative results;
5. exact constructor-level wire attribution and controlled `Let`/`Nat` experiments;
6. controlled BLC/Jot/structural comparisons with explicit limitations;
7. a CBN/call-by-need observational experiment;
8. a frozen independent implementation and 942-case post-freeze differential result;
9. a versioned receiver-assumption model and conditional transmitted-bit accounting;
10. a documented negative complete-bootstrap result;
11. a literature-informed distinction between the stable Core and the missing teaching/bootstrap layer.

These are project results, not claims that every underlying idea is historically new.

---

# 12. Next research stage: teaching NEX

The next stage should construct a **NEX Teaching / Bootstrap Message** as a separate layer over the stable Core.

The target pipeline is:

```text
receiver prior A
    -> finite teaching message T
    -> reconstructed NEX competence
    -> conformance/self-test
    -> canonical NEX programs P
```

A candidate curriculum may introduce, in a progressively constrained order:

1. binary symbols, sequence order, and framing assumptions;
2. naturals and finite sequences;
3. self-delimiting integer coding;
4. structural composition / trees;
5. natural values and simple primitive equations;
6. application and functions;
7. binding and the relationship between pedagogical notation and de Bruijn indices;
8. products and sums;
9. recursion;
10. type constructors and judgments;
11. principal type examples;
12. canonical NEX wire encoding;
13. transmitted conformance exercises for decoder, typechecker, and evaluator self-test.

This order is a hypothesis, not yet an accepted protocol.

The stage must define an operational success criterion for receiver competence. A useful criterion is not philosophical “understanding” but reproducible capability: given specified exercises, the reconstructed system produces the expected canonical bits, type judgments/rejections, and observable results, and can construct valid programs for a held-out task family.

Supporting work should include NEX-specific metatheory, bounded-exhaustive cross-implementation testing, function application contexts, and hold-out workloads.

No incompatible NEX-1 Core redesign should be introduced merely to make the curriculum easier; pedagogical notation may differ from the final canonical representation.

---

# 13. Conclusion

Stages 0–5 establish a stable experimental Core and substantial evidence that its explicit specification/conformance material is reconstructable. They do not yet solve the original communication problem completely.

The literature comparison makes the missing component precise. NEX has concentrated on the **final computational agreement**: exact terms, typing, evaluation, canonical bits, and conformance. Systems such as Lincos and CosmicOS show that a practical unknown-receiver message must also contain a **curriculum**.

The next research task is therefore to build a finite transmitted curriculum that teaches the stable NEX-1 Core and makes successful reconstruction operationally testable. Once such an artifact exists, its exact bit length can finally replace speculative bootstrap proxies.

---

# Bibliography and source registry

The durable bibliography with exact source usage and limitations is maintained in `docs/SOURCES.md`. Stable source IDs used in this manuscript include SRC-0001 through SRC-0029.

The interstellar-teaching comparison is maintained separately in `docs/RELATED-WORK.md`.

---

# Maintenance rule

Per ADR-0012, reproducible measurements, research-significant decisions, independent-conformance results, formal counterexamples/proofs, stage-level conclusions, or changes to the accounting model must update this canonical manuscript and its Russian mirror unless the corresponding PR explicitly explains why no manuscript change is required.
