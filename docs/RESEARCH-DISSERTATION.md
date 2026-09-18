# NEX-1: A Compact Experimental Architecture-Neutral Typed Core for Information-Efficient Transmission of Computation

## Design, executable semantics, empirical validation, independent reconstruction, and receiver-conditioned accounting

**Document type:** living dissertation-style research manuscript  
**Canonical language:** English  
**Russian mirror:** `RESEARCH-DISSERTATION.ru.md`  
**Evidence horizon:** Stages 0–5 complete; post-Stage-5 literature re-audit incorporated as of 2026-09-19  
**Project:** NEX / `aliens_nex`

> This manuscript is a research synthesis. It does not replace the normative NEX-1 v0.1 specification, ADRs, conformance vectors, source code, or reproducible experiment artifacts.

---

## Abstract

This work studies whether executable computational knowledge can be transmitted to a receiver for whom no shared programming language, processor architecture, ABI, operating system, text encoding, or terrestrial runtime may be assumed. The project therefore studies not program payload alone, but the combined burden of describing a computational system, establishing enough machinery to execute it, and transmitting programs.

Historically this objective was written as

```text
C = S + B + P,
```

where `S` denotes specification information, `B` receiver bootstrap information, and `P` program payload. The post-Stage-5 literature re-audit makes the exact interpretation stricter: numerical total cost is the bit length of one concrete transmitted object `M_A` under an explicit receiver-assumption profile `A`,

```text
C | A = |M_A|.
```

A decomposition into `S`, `B`, and `P` is valid only when the transmitted roles are explicitly serialized and counted without overlap.

NEX-1 v0.1 is a small statically typed functional Core with six term constructors (`Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`), zero-based de Bruijn indices, rank-1 Hindley–Milner inference, arbitrary-precision naturals, a fixed primitive basis, explicit general recursion through `fix`, a self-delimiting binary representation, and weak call-by-name semantics.

Stages 1–3 established executable wire, static, and dynamic semantics. Stage 4 froze benchmark corpora before drawing optimization conclusions. On the accepted 17-program corpus, NEX occupies 1,371 bits over 345 AST nodes. `Prim` contributes 460 bits (33.6%) on that corpus. Direct `Nat(255)` occupies 21 bits versus 2,300 bits for the tested repeated-`succ` construction. A root-principal-type envelope adds 134 bits, or 9.77% to program payload. On an identical three-program pure-lambda subset, Binary Lambda Calculus is smaller than NEX (30 versus 37 bits). The experimental call-by-need evaluator preserved all 17 accepted observable results while reducing the project-defined Go evaluator transition counter from 226,151 to 2,484; this is not a wall-clock speedup claim.

Stage 5 tested reconstruction from a frozen specification/conformance packet. A Python implementation was produced without access to `reference/go` and frozen before comparison. Post-freeze differential testing produced 942 matching portable observations, zero semantic mismatches, and zero resource asymmetries. The re-audit narrows the interpretation: this is strong **differential-conformance evidence of reconstructability on the tested surface**, not a proof of specification completeness or semantic correctness.

Stage 5 also made receiver assumptions explicit. The corrected current taxonomy distinguishes an exact binary-frame prior `A0`, an elementary mathematical prior `A1`, a parameterized formal-rule-calculus prior `A1(R)`, a parameterized universal-machine prior `A2(U)`, and a non-neutral host control `A_host(H)`. No complete receiver-neutral bootstrap artifact has yet been accepted, so full `B | A` and total `C | A` remain numerically unknown.

A targeted post-Stage-5 literature re-audit found no defect that invalidates NEX-1 v0.1 or the recorded Stage 1–5 measurements. It did correct several claims: typed combinatory logic is a legitimate static-typing competitor; NEX is not proven globally minimal; prior work such as Lincos, CosmicOS, and Lingua Cosmica materially narrows novelty claims; the 17-program corpus is not representative of all software; and NEX-specific type-safety and call-by-need equivalence theorems remain open.

**Keywords:** compact programming language, architecture-neutral computation, binary program representation, de Bruijn indices, Hindley–Milner, bootstrap, receiver assumptions, Binary Lambda Calculus, differential conformance, reproducible research.

---

# 1. Research problem and objective

Conventional software assumes a large body of shared context: textual syntax, encodings, processor behavior, executable formats, operating systems, compilers, virtual machines, and data conventions. In an unknown-receiver setting, these are not free background facts; they are part of the interpretation problem.

A one-bit program is not information-efficient if it requires an enormous untransmitted interpreter. Conversely, an extremely small universal interpreter may make every later program unnecessarily large. The research object is therefore architecture-neutral representation and execution of general-purpose computation under severe information constraints. The subject is the trade-off among program representation, specification burden, receiver bootstrap, static typing, evaluation strategy, and explicitly declared receiver assumptions.

The goal is to construct and evaluate a compact typed executable Core while developing a reproducible method for deciding which costs are measured, which are conditional, and which remain unknown.

The project does **not** claim that NEX is globally minimal or globally superior to external languages.

---

# 2. Research questions

**RQ1.** Can NEX be given a deterministic, architecture-neutral, self-delimiting binary representation with executable conformance evidence?

**RQ2.** Can closed NEX programs recover principal rank-1 types without ordinary transmitted term annotations?

**RQ3.** Can weak call-by-name remain a simple normative semantics while a sharing implementation preserves portable observations?

**RQ4.** Which constructs dominate program payload on the frozen corpus, and are `Let` and direct `Nat` literals empirically justified against the tested alternatives?

**RQ5.** How does NEX program payload compare with selected external encodings on explicitly shared subsets?

**RQ6.** Can full transmitted cost already be evaluated numerically?

**RQ7.** Can a second implementation, produced without access to `reference/go`, reconstruct the same portable wire, static, and dynamic observations from a frozen packet?

**RQ8.** Under which explicit receiver assumptions can a complete bootstrap be represented and measured without hiding an interpreter or double-counting transmitted bits?

**RQ9.** After comparison with broader prior work, which NEX claims remain contributions, which are rediscoveries or combinations of known ideas, and which still require formal or empirical validation?

---

# 3. Related work and novelty boundary

## 3.1 Computational representation and type theory

De Bruijn indices provide the basis for transmitting bound-variable structure without names [1]. Binary Lambda Calculus provides a compact binary lambda representation and an external pure-lambda baseline [2]. Milner and Damas–Milner provide the theoretical basis for rank-1 let-polymorphism and principal type schemes [3,4]. Plotkin's PCF/LCF work provides a classical precedent for small typed languages with natural numbers and fixed-point recursion [5]. Elias supplies the universal-code family from which NEX uses gamma coding of `n+1` [6].

The post-Stage-5 re-audit adds an important correction: combinatory logic is not intrinsically incompatible with static typing. Hindley's 1969 work establishes principal type-scheme results for combinatory logic [18]. Pure SK/SKI therefore remains a legitimate typed competitor; NEX rejects it for v0.1 because of total representation/design trade-offs, not because it cannot support useful static typing.

## 3.2 Evaluation strategy

Plotkin distinguishes call-by-name from call-by-value [9]. Launchbury and Sestoft formalize lazy evaluation and implementation with sharing [10,11]. Maraist, Odersky, and Wadler provide a call-by-need calculus with the same observational equivalence relation as call-by-name for their studied lambda calculus [23]. This supports the direction of NEX's sharing experiment, but it is not automatically a theorem for NEX's exact `fix`, naturals, sums/products, and primitive-forcing rules.

## 3.3 Description length and receiver assumptions

Shannon supplies the communication-system boundary but deliberately separates engineering transmission from semantic meaning [15]. Kolmogorov and Chaitin establish that algorithmic/program-size descriptions are relative to an effective interpretation [16,17]. Rissanen's shortest-description work likewise treats model/description burden as part of the comparison [19]. These results motivate conditioning NEX accounting on an explicit profile rather than claiming a machine-free scalar information cost.

## 3.4 Interstellar-language prior art

NEX is not the first formal-language project aimed at an unknown extraterrestrial receiver. Freudenthal's **Lincos** (1960) is direct prior art in constructing a language for cosmic communication [20]. **CosmicOS** bootstraps mathematical and logical concepts and explicitly uses programs and simulations [21]. Work on **Lingua Cosmica** has applied constructive type theory to interstellar-message content [22].

Consequently, NEX does not claim novelty for “a language for aliens,” for the use of programs in interstellar communication, or for introducing types into that domain.

The narrower candidate contribution is the combination of:

- a compact typed binary Core with an executable specification;
- exact canonical program-bit accounting;
- explicit separation of program payload, specification, bootstrap, and receiver prior;
- frozen comparative experiments that retain negative results;
- a blind second implementation followed by post-freeze differential conformance;
- refusal to replace unknown bootstrap cost with host-source proxies.

## 3.5 Independent implementations and differential testing

The Stage 5 protocol reduces implementation leakage, but two implementations agreeing is not a correctness proof. Knight and Leveson's multiversion experiment demonstrates that independently developed programs can exhibit correlated failures [24]. Differential testing is valuable when a simple oracle is unavailable, but it cannot reveal a fault shared by all compared implementations [27]. These results directly constrain the interpretation of NEX's `942/942` agreement.

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

The repository is treated as durable project memory. The project distinguishes external facts, project decisions, reproducible measurements, inferences, hypotheses, and unknowns.

Comparative corpora are frozen before optimization conclusions. Negative results are preserved. Resource exhaustion is kept separate from malformed input, static rejection, and proof of divergence.

For independent reconstruction, an allowlisted packet was frozen before the second implementation. The second implementation was content-hash frozen before `reference/go` became available. Differential testing then compared only portable observations.

For total accounting, the exact object is now written as:

```text
C | A = |M_A|
```

If roles are disjoint:

```text
C | A = (S | A) + (B | A,S) + (P | A,S,B)
```

If specification and executable bootstrap are inseparable:

```text
C | A = (SB | A) + (P | A,SB)
```

This prevents unknown interpreters from disappearing into an undeclared prior and prevents the same bit from being counted twice.

---

# 5. NEX-1 v0.1 experimental object

## 5.1 Terms and binding

```text
Term ::= Var(index)
       | Lam(body)
       | App(function, argument)
       | Let(value, body)
       | Nat(value)
       | Prim(id)
```

Bound variables use zero-based de Bruijn indices. Top-level programs are closed.

## 5.2 Types

```text
T ::= a | 1 | N | T -> T | T * T | T + T
S ::= forall a1 ... an. T
```

Static semantics use rank-1 HM inference with fresh instantiation, unification, occurs check, and generalization at `Let`.

The existing implementations are strong executable evidence. However, Milner's type-soundness results do not automatically prove NEX's exact primitive/evaluation system sound. A NEX-specific preservation/canonical-forms/progress-or-safety proof remains future work [26].

If future profiles add mutable references or comparable effects, the v0.1 pure-Core generalization rule must be revisited; unrestricted HM polymorphism is not sound for ordinary create/update polymorphic references [25].

## 5.3 Core primitives

```text
0 fix   1 succ   2 pred   3 ifz
4 pair  5 fst    6 snd    7 inl
8 inr   9 case   10 unit
```

`fix : forall a. (a -> a) -> a` permits general recursion and therefore divergence.

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

The constructor prefix lengths are `2,2,2,3,4,4`, with Kraft sum exactly 1. The top-level constructor code space is therefore fully allocated. A future attempt to shorten the `Prim` constructor prefix must compensate elsewhere or change the grammar factorization; `Prim`'s large corpus contribution does not alone prove that its top-level prefix is the main inefficiency.

## 5.5 Dynamic semantics

The normative strategy is weak call-by-name. Arguments and `Let` values are delayed, reduction does not occur beneath `Lam` before application, primitive forcing is selective, and general recursion is explicit through `fix`.

Call-by-need remains an allowed implementation strategy only when portable Core observations are preserved.

---

# 6. Results of Stages 1–4

Stages 1–3 produced executable wire, type, and evaluation conformance. Stage 4 froze the accepted empirical corpus before optimization conclusions.

## 6.1 Corpus measurements

For corpus v0.3:

| Metric | Value |
|---|---:|
| Programs | 17 |
| AST nodes | 345 |
| Canonical NEX wire bits | 1,371 |

Constructor attribution:

| Constructor | Bits | Share |
|---|---:|---:|
| `Prim` | 460 | 33.6% |
| `Var` | 286 | 20.9% |
| `App` | 264 | 19.3% |
| `Nat` | 244 | 17.8% |
| `Lam` | 84 | 6.1% |
| `Let` | 33 | 2.4% |

These are exact properties of the frozen corpus, not estimates of constructor frequencies in “software in general.” The corpus is small and hand-designed; freezing removes post-result benchmark editing but not initial selection bias.

## 6.2 `Let`

The tested representation has a measurable break-even. For one 5-bit payload, `Let` loses at two and three uses, ties at four, and wins at eight. For the tested 14-bit payload it already saves bits at two uses. This justifies retaining `Let` as a meaningful design option but does not imply every local `Let` is wire-optimal.

## 6.3 Direct natural literals

```text
Nat(255)          21 bits
succ-chain(255) 2300 bits
```

Direct `Nat` is therefore strongly supported against the tested repeated-`succ` construction. This does not establish Elias gamma or the literal representation as globally optimal among all integer codes.

## 6.4 Erased HM versus transmitted root type

```text
erased terms      1371 bits
root type data      134 bits
hybrid total       1505 bits
                  +9.77%
```

This establishes only `Delta P`. A compensating reduction in checker/specification/bootstrap burden has not been built or measured.

## 6.5 External baselines

On the identical three-program pure-lambda subset:

```text
NEX  37 bits
BLC  30 bits
```

Therefore no universal NEX compactness claim is supported.

The measured Jot result is 288 bits through one deterministic NEX-lambda -> SK -> Jot translation. It is not a shortest-Jot result.

The project-defined tiny postfix structural baseline measures 1,529 bits on the full 17-program corpus versus 1,371 for NEX, but it reuses NEX conventions and is not an independent total-cost comparison.

## 6.6 Call-by-name versus call-by-need

The experimental sharing evaluator preserved all 17 accepted observations. The reference instrumentation reported:

```text
CBN transition counter        226151
call-by-need counter            2484
reduction                     98.90%
```

This means 98.90% fewer counted evaluator transitions according to the project instrumentation. It is not a statement about wall-clock time, CPU instructions, allocation count, peak memory, or bootstrap size.

---

# 7. Stage 5 — independent reconstruction

The second implementation received a frozen packet without access to the Go reference source. Its frozen archive is:

```text
sha256:783e4186f9a8c024f00a732deae33b547c81ed4d7639c610a1e8bc5997eb3fbe
```

Before direct comparison it passed all supplied packet vectors and 23 implementation tests.

Post-freeze differential testing produced:

```text
portable matches       942
semantic mismatches      0
resource asymmetries     0
```

The 942 cases comprise:

```text
17   frozen corpus programs
325  valid cases = 25 numeric parameter sets x 13 fixed AST templates
100  static-error cases = 25 parameter sets x 4 error families
500  randomized term shapes tested at wire level
```

The accepted interpretation is therefore:

> strong differential-conformance evidence that the published packet is sufficient to reconstruct the tested portable behavior independently of the Go source.

The result is not a proof that the specification is complete, nor that both implementations are correct on all inputs. Shared interpretation errors remain possible.

One presentation-level ambiguity was recorded: precedence among multiple independent static errors is not normative. Both implementations currently perform scope checking before unknown-primitive diagnosis, but that coincidence was not promoted into language semantics.

---

# 8. Receiver assumptions and bootstrap accounting

## 8.1 Historical Stage 5 model

The Stage 5 experiment froze `assumptions-v0.1.json`, with profiles `A0`, `A1`, `A2(U)`, and `A_host(H)`. It successfully made hidden receiver assumptions visible and prohibited host-source substitution for `B`.

The later literature re-audit found one conceptual weakness: historical `A1` included the ability to interpret recursively defined rules without itself fixing a formal rule language.

## 8.2 Corrected current model

The current `assumptions-v0.2.json` separates that computational prior:

```text
A0        exact finite ordered binary frame
A1        A0 + elementary naturals and finite-sequence mathematics
A1(R)     A1 + exact formal rule calculus R and binary serialization
A2(U)     A1 + exact universal binary machine U and input framing
A_host(H) terrestrial engineering control only
```

`A1(R)` and `A2(U)` are distinct stronger branches. Neither is assumed to arise automatically from elementary mathematics.

## 8.3 Bootstrap feasibility result

Stage 5 examined three paths:

- a recursive-rule description: incomplete because no exact transmitted formal calculus had been frozen;
- BLC under `A2(U=BLC)`: incomplete because no complete frozen conformance-verified NEX interpreter exists in BLC;
- Python under `A_host(Python3.12)`: finite and testable, but non-neutral.

Host-control source measurements were:

```text
NEX Python package source           28,832 bytes
all frozen author-written files     52,859 bytes
```

They are explicitly **not** bootstrap cost.

Accepted result:

```text
accepted complete receiver-neutral bootstrap candidates  0
full B | A known                                           false
full SB | A known                                          false
total C | A computable                                     false
```

The corrected `A1/A1(R)` distinction strengthens this negative result: the missing formal rule calculus is a real unresolved dependency rather than a free mathematical convention.

---

# 9. Answers to the research questions

**RQ1.** Supported for v0.1 by executable wire conformance and two implementations agreeing on the tested portable observations.

**RQ2.** Functionally supported for the current pure Core; total-cost optimality of erased typing and a formal NEX type-safety theorem remain open.

**RQ3.** Empirically supported on the frozen programs; a NEX-specific formal call-by-name/call-by-need equivalence theorem remains open.

**RQ4.** Answered only for the frozen corpus and tested alternatives: `Prim` contributes the most bits, `Let` has a break-even, and direct `Nat` strongly beats the tested repeated-`succ` representation.

**RQ5.** Mixed: BLC is smaller on the shared pure-lambda subset; no global external winner has been established.

**RQ6.** No. Program payload is exact for declared corpora/contracts, but complete receiver-conditioned setup/bootstrap and total message cost remain unknown.

**RQ7.** Strongly supported as differential-conformance evidence on the tested surface, not as a correctness theorem.

**RQ8.** Methodologically clarified but numerically open: admissible prior profiles and accounting rules are explicit, while no complete neutral bootstrap exists.

**RQ9.** The broad ideas of interstellar formal language, executable messages, types, lambda/calculus encodings, and lazy evaluation all have substantial prior art. NEX's defensible contribution is the particular quantitative, typed, reproducible, receiver-conditioned methodology and its concrete experimental artifacts rather than invention of those underlying ideas.

---

# 10. Threats to validity

- The accepted design corpus contains only 17 hand-designed programs.
- Freezing prevents post-result edits but does not eliminate pre-freeze selection bias.
- Some external comparisons use fixed translations rather than globally shortest programs.
- The 325 generated-valid semantic cases use 13 structural templates; the 100 static-error cases use four error families.
- The 500 randomized cases are wire-level, not full semantic workloads.
- Differential agreement cannot reveal an error shared by both implementations.
- Cognitive independence is procedural, not mathematically provable.
- Runtime transition counters are implementation-specific and are not direct runtime or energy measurements.
- No NEX-specific machine-checked type-safety proof currently exists.
- No NEX-specific formal call-by-need equivalence proof currently exists.
- Receiver profiles are experimental conditions, not claims about actual extraterrestrial knowledge.
- The physical communication layer below `A0` is outside the current model.
- No complete receiver-neutral bootstrap artifact exists.
- Global optimality/minimality is not established.

---

# 11. Contributions to date

Subject to the limitations above, the project has produced:

1. a compact architecture-neutral typed Core with a canonical binary representation;
2. executable separation of wire validity, scope validity, type validity, evaluation, and finite resource refusal;
3. language-neutral wire/static/dynamic conformance artifacts;
4. a frozen measurement methodology that retains negative and inconvenient results;
5. exact constructor-level accounting and controlled `Let`, `Nat`, and type-information experiments;
6. controlled external/structural comparisons with explicit domain restrictions;
7. an instrumented CBN/call-by-need implementation experiment with precise metric boundaries;
8. a blind independent implementation and post-freeze differential-conformance result;
9. an explicit, versioned receiver-assumption taxonomy and no-double-counting ledger;
10. a documented negative complete-bootstrap result instead of a proxy substitution;
11. a living bilingual research record plus a separate post-Stage-5 literature audit that records corrections rather than rewriting historical evidence.

These are project contributions; they are not claims that every component idea is novel.

---

# 12. Conclusion and next evidence stage

The post-Stage-5 re-audit did not reveal a hidden defect requiring rollback of NEX-1 v0.1. Its main effect is to make the research more conservative and more precise.

The wire representation, pure-Core HM implementation, weak call-by-name evaluator, frozen Stage 4 measurements, independent Python checkpoint, `942/942` differential result, and negative bootstrap result all remain valid within their stated conditions. What changed is the interpretation around them: combinatory logic is recognized as a typed competitor; total description cost is explicitly conditional; the `A1` prior is weakened and parameterized when a rule calculus is needed; differential agreement is not confused with proof; and prior interstellar-language research is acknowledged directly.

Before an incompatible NEX-1 redesign, the highest-value next evidence stage is:

1. **NEX metatheory:** preservation, canonical forms, and an appropriate progress/safety theorem for the current pure Core;
2. **evaluation equivalence:** a formal or mechanized NEX-specific argument that the allowed call-by-need implementation preserves portable observations;
3. **broader conformance:** bounded exhaustive enumeration of small closed well-scoped/well-typed terms across independent implementations, plus hold-out and externally specified workloads;
4. **bootstrap construction:** one dependency-closed artifact under an exact `A1(R)` or `A2(U)` profile.

Only after these gaps are reduced should global compactness, total `C | A`, or incompatible Core/wire redesigns be argued from stronger evidence.

---

# Glossary

**Architecture-neutral** — specified without dependence on a particular processor, ABI, OS, or host runtime.

**Bootstrap (`B`)** — transmitted information required, under declared prior assumptions, to realize enough machinery to process the target system.

**Call-by-name (CBN)** — non-strict evaluation in which arguments are delayed and may be recomputed.

**Call-by-need** — non-strict evaluation with sharing/memoization.

**Canonical program payload (`P`)** — exact NEX wire length once the NEX contract is already fixed; a conditional description length, not a prior-free information quantity.

**Differential conformance** — comparing independent implementations on common inputs using portable observations; agreement is evidence, not a proof oracle.

**Receiver profile (`A`)** — explicit versioned prior knowledge/capability assumed outside the measured transmitted object.

**`A1(R)`** — elementary mathematical prior plus one exactly specified formal rule calculus `R` and its serialization.

**`A2(U)`** — elementary mathematical prior plus one exactly specified universal binary machine `U` and input framing.

**`C | A = |M_A|`** — exact total length of one concrete transmitted object under receiver assumptions `A`.

**Weak-head normal form (WHNF)** — evaluation far enough to reveal the outer computational form.

---

# Bibliography

1. de Bruijn, N. G. (1972). *Lambda calculus notation with nameless dummies, a tool for automatic formula manipulation, with application to the Church-Rosser theorem.* `[SRC-0001]`
2. Tromp, J. *Binary Lambda Calculus.* `[SRC-0002]`
3. Milner, R. (1978). *A Theory of Type Polymorphism in Programming.* `[SRC-0003]`
4. Damas, L.; Milner, R. (1982). *Principal Type-Schemes for Functional Programs.* `[SRC-0004]`
5. Plotkin, G. D. (1977). *LCF Considered as a Programming Language.* `[SRC-0005]`
6. Elias, P. (1975). *Universal codeword sets and representations of the integers.* `[SRC-0006]`
7. Wells, J. B. (1999). *Typability and type checking in System F are equivalent and undecidable.* `[SRC-0007]`
8. Schönfinkel, M. (1924). *Über die Bausteine der mathematischen Logik.* `[SRC-0009]`
9. Plotkin, G. D. (1975). *Call-by-name, call-by-value and the lambda-calculus.* `[SRC-0011]`
10. Launchbury, J. (1993). *A Natural Semantics for Lazy Evaluation.* `[SRC-0012]`
11. Sestoft, P. (1997). *Deriving a lazy abstract machine.* `[SRC-0013]`
12. Barker, C. (2001). *Iota and Jot: the simplest languages?* `[SRC-0014]`
13. W3C WebAssembly Working Group. *WebAssembly Core Specification.* `[SRC-0008]`
14. The Go Project. *The Go Programming Language Specification.* `[SRC-0010]`
15. Shannon, C. E. (1948). *A Mathematical Theory of Communication.* `[SRC-0015]`
16. Kolmogorov, A. N. (1965). *Three approaches to the definition of the concept “quantity of information”.* `[SRC-0016]`
17. Chaitin, G. J. (1975). *A Theory of Program Size Formally Identical to Information Theory.* `[SRC-0017]`
18. Hindley, J. R. (1969). *The Principal Type-Scheme of an Object in Combinatory Logic.* `[SRC-0018]`
19. Rissanen, J. (1978). *Modeling by shortest data description.* `[SRC-0019]`
20. Freudenthal, H. (1960). *Lincos: Design of a Language for Cosmic Intercourse, Part 1.* `[SRC-0020]`
21. Fitzpatrick, P. *CosmicOS: a next-generation Contact message.* `[SRC-0021]`
22. Ollongren, A.; Vakoch, D. A. (2011). *Typing logic contents using Lingua Cosmica.* `[SRC-0022]`
23. Maraist, J.; Odersky, M.; Wadler, P. (1998). *The call-by-need lambda calculus.* `[SRC-0023]`
24. Knight, J. C.; Leveson, N. G. (1986). *An Experimental Evaluation of the Assumption of Independence in Multiversion Programming.* `[SRC-0024]`
25. Tofte, M. (1990). *Type Inference for Polymorphic References.* `[SRC-0025]`
26. Wright, A. K.; Felleisen, M. (1994). *A Syntactic Approach to Type Soundness.* `[SRC-0026]`
27. McKeeman, W. M. (1998). *Differential Testing for Software.* `[SRC-0027]`

The detailed source-use and limitation notes are maintained in `docs/SOURCES.md`.

---

# Maintenance rule

Per ADR-0012 and ADR-0016, future reproducible measurements, formal results, counterexamples, independent-conformance evidence, stage-level conclusions, or material literature corrections must update this canonical manuscript and its Russian mirror unless the corresponding change explicitly documents why no research-text update is required.
