# NEX-1: A Minimal Architecture-Neutral Typed Core for Information-Efficient Transmission of Computation

## Design, formalization, executable semantics, empirical evaluation, independent reconstruction, and receiver-assumption accounting

**Document type:** living dissertation-style research manuscript  
**Canonical language:** English  
**Russian mirror:** `RESEARCH-DISSERTATION.ru.md`  
**Evidence horizon:** Stages 0–4 complete; Stage 5 independent reconstruction through differential conformance (5.0–5.6) complete; Stage 5.7 receiver-assumption model implemented, 2026-09-18  
**Project:** NEX / `aliens_nex`

> This manuscript is a scholarly research synthesis maintained inside the project repository. It is not yet formatted for the submission requirements of a particular university, national dissertation authority, or citation style. The normative language definition remains `docs/NEX-1-v0.1.md`; architecture and research-method decisions remain governed by Accepted ADRs.

---

## Abstract

This work investigates whether a very small, architecture-neutral, statically typed computational core can reduce the information required to transmit executable computational knowledge between parties that cannot assume a shared programming language, processor architecture, ABI, operating system, textual notation, or implementation environment. The research target is not program payload alone but a total information model

```text
C = S + B + P
```

where `S` is the information required to specify the computational system, `B` is receiver-side bootstrap information required to realize it under explicitly stated prior assumptions, and `P` is transmitted program payload.

The experimental system NEX-1 v0.1 uses six canonical term constructors (`Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`), zero-based de Bruijn indices, rank-1 Hindley–Milner let-polymorphism, arbitrary-precision natural literals, a small fixed primitive basis, explicit general recursion through `fix`, a self-delimiting binary representation, and weak call-by-name semantics. The design draws on de Bruijn's nameless representation [1; SRC-0001], Binary Lambda Calculus as a compact binary-lambda comparison point [2; SRC-0002], Hindley–Milner inference and principal type schemes [3,4; SRC-0003, SRC-0004], PCF/LCF-style typed recursion [5; SRC-0005], Elias universal coding [6; SRC-0006], and established distinctions between call-by-name and lazy sharing [9–11; SRC-0011–SRC-0013].

Stages 1–3 establish executable wire, static, and dynamic semantics. Stage 4 freezes benchmark corpora and measurement rules before optimization. On the accepted 17-program corpus v0.3, canonical NEX programs occupy 1,371 bits over 345 AST nodes. Primitive references are the largest measured wire contributor at 460 bits (33.6%). Direct `Nat(255)` occupies 21 bits versus 2,300 bits for the tested repeated-`succ` construction. `Let` exhibits a measurable break-even instead of being uniformly beneficial. Transmitting an experimental principal root-type envelope adds 134 bits, or 9.77% program-payload overhead, without proving a bootstrap reduction. Binary Lambda Calculus is smaller than NEX on the identical three-program pure-lambda subset (30 versus 37 bits), preventing a claim of universal NEX program-size superiority. An experimental call-by-need evaluator preserves all 17 accepted observable results while reducing Go-reference transition counts from 226,151 to 2,484 in aggregate; this is implementation evidence rather than transmission-cost evidence.

Stage 5 asks whether the specification and language-neutral conformance artifacts determine NEX behavior independently of the original Go implementation. A versioned conformance packet was frozen before a second implementation was written. A separate model/context, given that packet rather than `reference/go`, reconstructed the wire codec, closed-scope checker, rank-1 HM inference, and weak call-by-name evaluator in Python 3.12+ using only the standard library. Before comparison with Go, the implementation passed 17/17 integer wire vectors, 12/12 term wire vectors, 15/15 invalid wire vectors, 15/15 scope vectors, 19/19 type vectors, 21/21 evaluation vectors, and 23/23 independent tests. The received implementation was frozen by archive SHA-256 before the Go implementation was opened. A subsequent deterministic post-freeze differential experiment compared 942 architecture-neutral observations and produced 942 matches, zero semantic mismatches, and zero finite-resource asymmetries. This is strong empirical evidence of independent reconstructability over the tested semantic surface, not a formal proof of specification completeness.

Stage 5.7 then addresses a deeper accounting problem: an executable bootstrap bit length is not meaningful without saying what the receiver already knows. ADR-0014 therefore conditions specification/bootstrap claims on an explicit receiver prior `A`. The first versioned model defines `A0` (an exact finite ordered binary frame), `A1` (`A0` plus a stated discrete mathematical metalanguage), `A2(U)` (`A1` plus one exact fixed universal binary abstract machine `U` and its self-delimiting program/data convention), and `A_host(H)` as a terrestrial engineering control that is ineligible for receiver-neutral claims. The project consequently uses `B | A`, `S | A`, and `C | A` rather than treating `B` as an unconditional scalar. It also introduces a no-double-counting rule: if one transmitted artifact inseparably serves both specification and executable-bootstrap roles, its bits are reported once as `SB | A` rather than once as `S` and again as `B`.

This model does not yet provide a numerical bootstrap cost. In particular, Stage 5.7 does not choose the universal machine parameter `U`, does not assign a bit price to receiver priors, and does not rank stronger-prior profiles against weaker-prior profiles by transmitted bits alone. The principal unresolved task is therefore Stage 5.8: freeze at least one concrete bootstrap candidate under one declared profile and measure the actual transmitted ledger without circularly omitting its interpreter. Until then, total `C | A` remains numerically unresolved and this work makes no claim that NEX is globally minimal or globally superior to alternative calculi.

**Keywords:** minimal programming language, architecture-neutral computation, binary lambda calculus, de Bruijn indices, Hindley–Milner, program encoding, bootstrap, conditional information cost, receiver assumptions, call-by-name, call-by-need, independent implementation, differential conformance, reproducible research.

---

# 1. Introduction

## 1.1 Motivation

Most executable software relies on extensive shared context: character encodings, source syntax, processor models, machine words, object formats, operating-system services, compilers, virtual machines, and conventions for representing data and control. In ordinary software engineering this shared context is beneficial. It becomes a liability in a thought experiment where sender and receiver may share only a communication channel and some mathematical regularities.

The motivating question is therefore not merely how to compress a program. It is how to transmit reusable computational knowledge when the receiver cannot be assumed to know a terrestrial programming language, CPU, ABI, operating system, text encoding, or runtime.

A trivial one-bit program is not useful if its meaning depends on an enormous untransmitted interpreter. Conversely, an extremely small universal interpreter may make every later program disproportionately large. NEX therefore treats the problem as joint information accounting:

```text
C = S + B + P
```

The model is deliberately strict about unknowns. A quantity is not set to zero merely because it has not yet been represented. Host source code is not silently treated as an alien bootstrap. Stage 5.7 further makes the receiver prior itself explicit: a measured bootstrap is always conditional on a declared assumption profile.

## 1.2 Research problem

The research problem is to determine whether a compact typed functional core can provide a favorable total-information trade-off for transmitting general-purpose computation without assuming a shared implementation platform, whether that core can be reconstructed independently from a finite transmitted specification/conformance package, and under which explicitly declared receiver priors a concrete bootstrap can later be measured.

The problem combines:

1. representational compactness;
2. deterministic parsing and validation;
3. static reconstructability of types;
4. general-purpose computational expressiveness;
5. non-strict operational semantics;
6. receiver bootstrap burden;
7. independent reconstructability;
8. prior-assumption dependence of executable descriptions;
9. empirical falsifiability against alternatives.

## 1.3 Object and subject of research

**Object:** architecture-neutral representation, validation, and execution of general-purpose computation under severe communication constraints.

**Subject:** trade-offs among specification size, receiver bootstrap complexity, transmitted-program size, static type reconstruction, evaluation strategy, independent conformance, and explicitly conditioned receiver priors in a minimal typed lambda-based core.

## 1.4 Goal

The goal is to construct and empirically evaluate a minimal executable core whose binary form and semantics are explicit enough for independent reconstruction, while developing a reproducible method for deciding whether its total communication cost can eventually outperform alternative computational representations under the same stated receiver assumptions.

## 1.5 Research objectives

1. Define a small architecture-neutral Core and stable invariants.
2. Define a canonical self-delimiting wire representation.
3. Build executable encode/decode conformance.
4. Define closed-scope and principal-type semantics.
5. Define weak non-strict dynamic semantics.
6. Separate language validity from finite implementation resource refusal.
7. Freeze benchmark corpora before optimization-driven experiments.
8. Measure exact constructor-level wire cost and controlled alternatives.
9. Compare selected external baselines without hiding unequal assumptions.
10. Separate exact program cost from specification/bootstrap proxies.
11. Test whether a second implementation can reconstruct behavior without reading the first implementation.
12. Expose receiver assumptions explicitly before assigning a numerical bootstrap cost.
13. Prevent double counting where specification and executable bootstrap share transmitted bits.
14. Preserve positive, negative, contradictory, and unresolved findings in a living research record.

## 1.6 Research questions

**RQ1.** Can NEX terms be given a deterministic, architecture-neutral, self-delimiting binary representation with executable conformance evidence?

**RQ2.** Can closed NEX programs reconstruct principal rank-1 types without ordinary term-level type annotations?

**RQ3.** Can a simple weak call-by-name semantics coexist with substantially more efficient implementations that preserve portable observable results?

**RQ4.** Which Core constructs dominate transmitted program cost, and are seemingly non-minimal constructs such as `Let` and direct `Nat` literals justified empirically?

**RQ5.** How does NEX program payload compare with selected alternative encodings under controlled, explicitly limited comparisons?

**RQ6.** Can the total objective `C = S + B + P` already be evaluated numerically?

**RQ7.** Can an implementation developed without access to `reference/go` reconstruct the same portable NEX wire, static, and dynamic behavior from a frozen specification/conformance packet?

**RQ8.** Under what explicitly stated receiver assumptions `A` can a bootstrap artifact be represented and measured as `B | A` or, where specification and bootstrap are inseparable, `SB | A`?

## 1.7 Working hypotheses

**H1.** Nameless binding plus compact prefix encoding can yield a small unambiguous canonical wire form.

**H2.** Rank-1 HM inference can avoid ordinary term-level type payload, but its global benefit depends on bootstrap cost.

**H3.** `Let` and direct natural literals may reduce program payload even though they enlarge the language definition.

**H4.** Weak call-by-name can remain normative while sharing/memoization is an observationally equivalent implementation optimization for tested pure Core programs.

**H5.** NEX should not be presumed smaller than highly compressed untyped lambda encodings on pure lambda terms.

**H6.** Program payload alone cannot establish total superiority.

**H7.** If the normative specification and portable vectors are sufficiently explicit, a cognitively isolated implementation can reconstruct NEX behavior without reference-source guidance.

**H8.** A meaningful numerical bootstrap cost requires the receiver's prior assumptions to be made explicit rather than hidden in a host language or virtual machine.

**H9.** Exact total-information accounting requires a transmitted-bit ledger in which a bit serving both specification and executable-bootstrap roles is counted once, not independently in both `S` and `B`.

---

# 2. Theoretical and Related-Work Basis

## 2.1 Nameless binding

De Bruijn demonstrated that bound variables can be represented by numerical position rather than names [1]. NEX adopts the nameless principle and fixes zero-based indices. Alpha-renaming therefore disappears from the canonical transmitted term.

## 2.2 Binary Lambda Calculus

Tromp's Binary Lambda Calculus shows that lambda terms can be encoded directly and compactly as binary strings [2]. NEX uses BLC as both conceptual precedent and falsifying baseline. NEX does not copy the BLC grammar and differs materially through types, `Let`, direct naturals, and fixed primitives; comparisons must therefore state the common subset explicitly.

## 2.3 Hindley–Milner inference

Milner's polymorphic type discipline and the Damas–Milner principal-type result provide the theoretical basis for NEX rank-1 let-polymorphism [3,4]. NEX uses principal inference to omit ordinary type annotations from v0.1 terms. Wells' undecidability result for System F provides a useful boundary against assuming that unrestricted implicit polymorphism retains the same decidability properties [7].

## 2.4 Recursion and numeric computation

Plotkin's LCF/PCF work supplies precedent for small typed functional languages with natural-number operations and fixed-point recursion [5]. NEX's exact primitive basis and wire format are project-specific.

## 2.5 Universal integer codes

Elias introduced universal codeword families for positive integers [6]. NEX defines `U(n)` as Elias gamma coding of `n+1`, allowing non-negative indices, natural literals, and primitive identifiers.

## 2.6 Evaluation strategy

Plotkin formalized important distinctions between call-by-name and call-by-value [9]. Launchbury and Sestoft provide semantic and implementation foundations for lazy sharing [10,11]. NEX keeps weak call-by-name normative and treats call-by-need as a possible implementation optimization when portable observations remain unchanged.

## 2.7 Combinatory alternatives

Classical combinatory logic and Barker's Iota/Jot material motivate compact alternative representations [8,12]. NEX's Jot experiment uses a documented deterministic translation and does not claim shortest Jot programs.

## 2.8 Portable core and embedding separation

The WebAssembly Core specification provides a modern example of separating portable computation from embedding assumptions [13]. NEX adopts only the architectural separation principle, not WebAssembly's instruction set or runtime model.

## 2.9 Communication boundaries and machine-relative program descriptions

Shannon's communication model explicitly distinguishes the source/transmitter/channel/receiver/destination engineering structure from message semantics [15; SRC-0015]. NEX does not infer from this that a binary frame is universally natural or free; it uses the distinction to state where the present digital-semantic experiment begins. Physical acquisition, synchronization, modulation discovery, and error correction remain below the `A0` boundary rather than being silently priced at zero.

Kolmogorov's algorithmic approach makes description length dependent on an effective description method rather than yielding one implementation-free scalar [16; SRC-0016]. Chaitin's program-size formulation similarly operates with a specified self-delimiting program interpretation [17; SRC-0017]. NEX uses these results methodologically: a numerical executable bootstrap requires a fixed interpretation. They do not identify a privileged universal machine for an unknown civilization and do not establish that any NEX bootstrap is algorithmically optimal.

---

# 3. Methodology

## 3.1 Evidence-gated development

The repository uses the research/engineering cycle:

```text
Problem
 -> Contract
 -> Invariant
 -> Executable example / failing test
 -> Implementation
 -> Verification
 -> Diff review
 -> Status checkpoint
 -> Research synthesis checkpoint
```

The repository, not conversational history, is durable research memory.

## 3.2 Evidence classes

Claims are separated into:

1. external established results supported by primary/official sources;
2. NEX design decisions;
3. reproducible NEX measurements;
4. interpretations/inferences from current evidence;
5. unresolved hypotheses or unknowns.

A hypothesis does not become a fact merely because it is repeated in later documents.

## 3.3 Reproducibility

Evidence is preserved through:

- language-neutral wire/static/evaluation conformance JSON;
- unit/property/fuzz tests;
- frozen benchmark corpora;
- deterministic experiment CLIs;
- Git commit identities and file hashes;
- clean-checkout GitHub Actions;
- versioned experimental reports;
- machine-readable receiver-assumption profiles and validators.

## 3.4 Frozen-corpus rule

Once a benchmark corpus has been used for comparative conclusions, it is immutable. An inconvenient result is retained rather than rewritten. Corpus v0.2, where `factorial-5` exceeds the default non-memoizing CBN transition budget, is preserved for precisely this reason.

## 3.5 Independence protocol

A second implementation is not automatically independent merely because it is written in another language. If the implementer has read the reference source, shared implicit assumptions may be copied unintentionally.

Stage 5 therefore freezes a packet before the blind reconstruction and excludes `reference/go`. The independent implementation is frozen by a content hash before direct comparison becomes permissible. Only after that boundary is the reference implementation opened for differential testing.

This protocol makes cognitive independence an explicit experimental condition rather than an informal claim.

## 3.6 Differential conformance

Post-freeze differential comparison uses portable observations only:

```text
wire bits
normalized principal type / portable static error
observable weak-head result / portable evaluation error
```

Implementation internals such as object layout, closure representation, fresh-variable IDs, allocation counts, and transition counts are deliberately excluded.

## 3.7 Conditional total-information accounting

The historical research model is:

```text
C = S + B + P
```

Stage 5.7 makes the receiver prior explicit. A receiver-assumption profile `A` denotes knowledge/capability that is shared before the measured transmission. Such a prior is not transmitted in the measured message, but it is not therefore claimed to have zero information content.

The first profiles are:

```text
A0      exact finite ordered binary frame
A1      A0 + stated discrete mathematical metalanguage
A2(U)   A1 + exact universal binary abstract machine U
              + exact self-delimiting program/data convention
A_host(H) A1 + concrete terrestrial host H, engineering control only
```

Accordingly:

```text
B | A
S | A
C | A
```

replaces an unconditional bootstrap scalar in exact Stage 5 claims.

A second accounting issue is overlap between specification and executable bootstrap. If their transmitted segments are disjoint, the ledger may report:

```text
C | A = (S | A) + (B | A,S) + P
```

If one artifact inseparably serves both roles, the correct form is:

```text
C | A = (SB | A) + P
```

Every transmitted bit is counted exactly once. Stage 5.7 does not assign a numerical price to the assumption atoms themselves, so a smaller transmitted bootstrap under a stronger prior cannot be declared a cross-profile total-cost winner.

Current interpretation:

- `P`: exact canonical program bits for a stated corpus once the NEX wire contract is established;
- `S | A`: transmitted specification segment under a declared receiver prior, not yet measured by an accepted receiver-neutral artifact;
- `B | A,S`: executable realization segment where a separate specification has already been supplied;
- `SB | A`: joint segment when specification and execution roles cannot be defensibly partitioned;
- `R`: host/reference implementation size, an engineering proxy that must not be substituted for any receiver-neutral bootstrap quantity.

---

# 4. NEX-1 v0.1

## 4.1 Terms

```text
Term ::= Var(index)
       | Lam(body)
       | App(function, argument)
       | Let(value, body)
       | Nat(value)
       | Prim(id)
```

Zero-based de Bruijn indices eliminate transmitted variable names.

## 4.2 Types

```text
T ::= a | 1 | N | T -> T | T * T | T + T
S ::= forall a1 ... an. T
```

The static system uses rank-1 HM-style inference with unification, occurs check, fresh instantiation, and let-generalization.

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

IDs 11–31 are reserved Core space; profiles begin at 32.

## 4.4 Wire format

`U(n)` is Elias gamma coding of `n+1`. Term prefixes are:

```text
00   U(k)   Var(k)
01   T      Lam(T)
10   T T    App(T,T)
110  T T    Let(T,T)
1110 U(n)   Nat(n)
1111 U(p)   Prim(p)
```

## 4.5 Dynamic semantics

The normative reference semantics are weak call-by-name. Arguments and `Let` values are delayed, no reduction occurs beneath a lambda before application, and primitive forcing is selective. General recursion is explicit through `fix`.

---

# 5. Stages 0–3: Formal and Executable Foundation

## 5.1 Stage 0 — governance and research baseline

Stage 0 established the canonical English specification, Russian mirrors for primary documents, ADR governance, source registry, testing/workflow rules, and repository-as-memory discipline. Its contribution is methodological: later results can be traced to explicit decisions rather than retrospective narrative.

## 5.2 Stage 1 — wire foundation

Stage 1 implemented canonical arbitrary-precision `U(n)` and term encode/decode, exact versus prefix decoding, malformed-input classes, and separate resource-limit refusal.

The conformance set contains 17 integer vectors, 12 term vectors, and 15 invalid exact-input vectors. Representative encodings include:

```text
Var(0)                    001
Nat(0)                    11101
Prim(0)                   11111
Lam(Var(0))               01001
Lam(App(Prim(1),Var(0)))  01101111010001
```

**Conclusion:** RQ1 is supported empirically for the v0.1 wire grammar.

## 5.3 Stage 2 — static semantics

Stage 2 implemented closed de Bruijn scope validation, type/scheme representations, free-variable analysis, substitutions, unification, occurs checking, primitive schemes, fresh instantiation, let-generalization, and Algorithm-W-style inference.

A successful closed term is normalized to a principal type scheme independent of internal fresh-variable numbering.

**Conclusion:** RQ2 is functionally supported, but total-cost optimality of erased types is not established.

## 5.4 Stage 3 — dynamic semantics

Stage 3 defined a weak call-by-name evaluator and language-neutral observable WHNF conformance. Non-strict examples verify that unused arguments/branches/fields remain unforced. Evaluation resource limits are separated from malformed syntax, type invalidity, and proofs of divergence.

**Conclusion:** a simple executable non-strict semantics exists and becomes a stable target for independent implementations.

---

# 6. Stage 4: Empirical Validation

## 6.1 Frozen corpus

The accepted v0.3 corpus contains 17 programs spanning pure lambdas, arithmetic/control primitives, products, sums, polymorphic `Let`, recursion, multiplication, factorial, Fibonacci, a recognizer, and repeated expensive binding.

Aggregate:

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

The early intuition that `App` should dominate is not supported on this corpus; primitive references are the largest measured category.

## 6.2 `Let` break-even

For one tested 5-bit payload, `Let` costs more at two and three repetitions, ties at four, and saves eight bits at eight repetitions. For a tested 14-bit payload, two uses already save five bits.

**Conclusion:** `Let` is neither universally beneficial nor universally wasteful; it has a payload/reuse-dependent break-even. v0.1 retains it.

## 6.3 Direct naturals

At `n=255`:

```text
Nat(255)           21 bits
tested succ chain 2300 bits
```

This does not prove global optimality of the current numeric representation, but strongly rejects removing direct naturals in favor of the tested construction.

## 6.4 Type-transmission experiment

An experimental envelope carrying only the inferred principal root type yields:

```text
erased terms       1371 bits
root type payload   134 bits
hybrid total       1505 bits
overhead           +9.77%
```

This measures only `Delta P`; no receiver-neutral reduction in type-checker/bootstrap cost has yet been measured. Erased HM is therefore retained without claiming global optimality.

## 6.5 External/structural baselines

On the identical pure-lambda subset (`identity`, `constant`, `composition`):

```text
NEX  37 bits
BLC  30 bits
```

Thus no universal NEX program-size superiority over BLC is supported.

A deterministic lambda-to-SK-to-Jot translation yields 288 bits for that subset; it is not a shortest-Jot search. A project-defined tiny postfix structural baseline yields 1,529 bits over the full v0.3 corpus versus NEX 1,371, but it reuses NEX integer/primitive assumptions and is not a total-bootstrap competitor.

## 6.6 Call-by-name versus call-by-need

All 17 accepted programs have the same observable WHNF in the reference CBN and experimental call-by-need evaluators.

```text
CBN transitions          226151
call-by-need transitions   2484
reduction                 98.90%
```

Savings are concentrated in repeated/recursive workloads; this is not a claim of uniform 98.90% speedup and is not a term in transmission cost `C`.

## 6.7 Accounting result

For corpus v0.3, `P=1371` bits exactly. The English Markdown specification occupies 23,440 UTF-8 bytes, but English/UTF-8/Markdown are receiver assumptions and the value is only a proxy. Selected Go reference source occupies 43,013 UTF-8 bytes, but Go and its runtime are host assumptions; therefore `R != B`.

**Conclusion:** RQ6 remains negative. Total `C` cannot yet be assigned a defensible scalar.

---

# 7. Stage 5: Independent Reconstruction and Receiver Priors

## 7.1 Why a second implementation matters

A specification and its first implementation can share the same unstated assumption. Internal tests may remain green because both artifacts were developed together. Therefore a stronger test is whether a second implementer can reconstruct the system without seeing the first implementation.

The experimental condition is stricter than simply choosing a second programming language. Prior exposure to the Go reference would contaminate the reconstruction. ADR-0013 therefore requires a frozen packet and a blind implementation phase.

## 7.2 Frozen conformance packet

The packet is frozen against source commit:

```text
4f9c50aed13cdbdf72c9ce6510521477d49c05a5
```

The first target is Python 3.12+ with standard library only. The packet contains the canonical specification, wire/static/evaluation vectors, selected normative ADRs, exact source hashes, and packet-local observation rules. It excludes Go evaluator architecture and Stage 4 implementation/experiment material.

The packet audit identified two presentation omissions:

- normalized principal-scheme text (`T0`, `T1`, ...);
- explicit JSON AST fixture mapping.

These were documented as comparison conventions, not added as new NEX semantics.

## 7.3 Independent implementation checkpoint

A separate model/context received only the frozen packet and experiment instructions. It returned an independent Python implementation whose received archive is frozen as:

```text
nex1-independent-python-v0.1.zip
SHA-256 = 783e4186f9a8c024f00a732deae33b547c81ed4d7639c610a1e8bc5997eb3fbe
```

The archive carries an external checkpoint marker in its ZIP comment:

```text
a594b73b711998df04b45eec296086d5577fba2f
```

Before any Go comparison, independent verification produced:

| Evidence | Result |
|---|---:|
| Integer wire vectors | 17 / 17 |
| Term wire vectors | 12 / 12 |
| Invalid exact-wire vectors | 15 / 15 |
| Scope vectors | 15 / 15 |
| Type vectors | 19 / 19 |
| Evaluation vectors | 21 / 21 |
| Independent unit tests | 23 / 23 |

A separate pre-comparison audit additionally exercised 20,000 generated wire round trips, large arbitrary-precision integer cases, typing/laziness examples, and resource-refusal separation without observing a defect.

The implementation's internal choices are not identical to Go. For example, recursive `fix` forcing uses a dedicated Python `FixThunk` rather than reproducing the Go evaluator's exact recursive representation. Such differences are not proof of independence, but they reduce the plausibility of a mechanical translation.

## 7.4 Frozen-source protection

The imported Python implementation is protected by a manifest recording exact byte lengths and SHA-256 for every author-written file. CI verifies those hashes before running the independent verifier. The original conformance packet is re-materialized from its frozen source hashes rather than maintained as a second editable copy.

This boundary prevents post-comparison repairs from being retroactively presented as independent reconstruction.

## 7.5 Post-freeze differential experiment

Only after the archive identity was frozen was the Go reference opened for direct comparison.

The accepted deterministic set uses seed `20260918` and contains:

| Group | Cases |
|---|---:|
| Frozen corpus v0.3 | 17 |
| Generated valid terms | 325 |
| Generated single-defect static terms | 100 |
| Generated wire terms | 500 |
| **Total** | **942** |

Portable observations compared:

```text
canonical wire bits
normalized principal type / static error class
observable WHNF / evaluation error class
```

Results:

```text
portable matches       942
semantic mismatches      0
resource asymmetries     0
success                true
```

PR #8 final clean-checkout evidence:

```text
reference-go        35385704921  success
stage5-independence 35385705027  success
stage5-differential 35385705162  success
```

PR #8 was squash-merged as `f500a5c5485b4cd5f6b5d9bd6bc76980f2f06cdb`. Post-merge `main` verification also succeeded in runs `35386452647`, `35386452451`, and `35386452447`.

## 7.6 Interpretation

The result supports H7 and provides the strongest current answer to RQ7:

> For the frozen conformance suite, accepted benchmark corpus, and deterministic generated differential cases tested, an implementation produced without translating `reference/go` reconstructed the same portable wire, static, and observable dynamic behavior.

The scope of that conclusion is deliberately bounded. A finite differential set cannot prove that the prose specification determines every possible valid and invalid term. Shared theory or the packet vectors may still leave an untested corner ambiguous. The result is strong empirical conformance evidence, not formal semantic equivalence.

## 7.7 Ambiguity findings

The independent implementation recorded one additional issue: for a term containing multiple independent static defects, the specification does not define a global diagnostic precedence. The Python implementation validates scope first. Post-freeze inspection shows that Go currently also checks scope first, but this agreement is not promoted into language semantics because no portable requirement has been demonstrated.

No accepted differential case exposed:

- a Go semantic bug;
- an independent Python semantic bug;
- a contradictory conformance vector;
- a new Core semantic omission requiring an incompatible v0.1 change.

The correct current decision is therefore to leave multi-error precedence implementation-specific rather than add unnecessary normative surface.

## 7.8 Independent-reconstruction conclusion

RQ7 is strongly supported for the current evidence horizon. NEX-1 v0.1 is no longer supported only by a specification co-developed with one reference implementation; it has a frozen second reconstruction and a zero-mismatch post-freeze differential checkpoint.

This conclusion changes the priority of the research. The largest unresolved question is now no longer whether the current semantics can be independently reconstructed, but what receiver assumptions and bootstrap information are necessary before such reconstruction is possible from a truly receiver-neutral channel.

## 7.9 Receiver-assumption model

ADR-0014 turns that open question into a versioned experimental contract rather than an informal phrase such as “the alien knows mathematics.”

The canonical machine-readable registry is `stage5/receiver-assumptions/assumptions-v0.1.json`.

The first assumption ladder is:

```text
A0  digital transport prior
    - two distinguished binary symbols
    - finite first-to-last ordering
    - exact frame start/end/length
    - no residual bit error inside the model

A1  A0 + discrete mathematical metalanguage
    - non-negative integers and basic arithmetic/order concepts
    - finite sequences, length, concatenation, positional indexing
    - deterministic finite/recursive rule descriptions

A2(U)  A1 + fixed universal-machine prior
       - exact binary operational semantics of one named U
       - exact self-delimiting program/data convention for that U

A_host(H)  A1 + concrete terrestrial host H
           - engineering control only
           - not receiver-neutral
```

The hierarchy does not say that these assumptions are universal, free, or equally plausible for an unknown civilization. It says exactly which prior is being conditioned on for a particular experiment.

The physical layer below `A0` is deliberately excluded from the current NEX experiment. This means signal discovery, modulation, synchronization, error correction, and discovery of a frame boundary have not been priced. Their omission is a scope boundary, not a zero-cost claim.

The universal machine in `A2(U)` remains a parameter. Stage 5.7 intentionally does not select one. Any future numerical claim must identify an exact versioned `U`; otherwise the executable description length is under-specified.

A key methodological result is that cross-profile bit totals are not directly rankable. For example, a 100-bit bootstrap conditioned on `A2(U)` cannot automatically be declared superior to a 500-bit bootstrap conditioned only on `A1`, because the former assumes strictly more receiver-side computational structure. Stage 5.7 does not yet assign a bit-equivalent cost or probability to those priors.

A second methodological result is the no-double-counting ledger. If a compact artifact both defines NEX and executes it, the same bits cannot be charged separately to `S` and `B`; the inseparable segment is reported as `SB | A`.

Thus RQ8 now has a partial answer: explicit receiver profiles and admissible accounting notation have been defined, but no executable bootstrap has yet been measured under them.

---

# 8. Answers to Research Questions

## RQ1 — deterministic wire

**Supported empirically.** Canonical encoding/decoding has language-neutral vectors, fuzz/property evidence, and now two independently developed implementations agreeing on packet and generated observations.

## RQ2 — erased rank-1 typing

**Functionally supported; total-cost optimality unresolved.** Both implementations reconstruct normalized principal schemes without ordinary term annotations. Stage 4's root-type experiment adds 9.77% `P`, but bootstrap savings of an explicit checker are unknown.

## RQ3 — simple semantics with efficient implementations

**Supported on tested programs.** Weak CBN is independently reconstructed; experimental call-by-need preserves accepted observables while greatly reducing repeated work on selected recursive workloads.

## RQ4 — constructor costs and `Let`/`Nat`

**Corpus-specific answer established.** `Prim` is the largest measured category on v0.3. Direct `Nat` is strongly justified against repeated `succ`; `Let` has a real break-even and is retained.

## RQ5 — alternatives

**Mixed.** BLC is smaller on the identical pure-lambda subset; NEX is smaller than the selected structural postfix baseline on v0.3. No total-cost external winner can yet be declared.

## RQ6 — total information cost

**Not yet computable.** `P` is exact for stated corpora. Stage 5.7 now defines how `S`, `B`, or joint `SB` must be conditioned on a receiver profile, but it does not yet provide a measured receiver-neutral bootstrap artifact.

## RQ7 — independent reconstruction

**Strongly supported for the tested evidence set.** The frozen Python reconstruction passed the packet independently and matched Go on all 942 accepted post-freeze differential cases with zero resource asymmetry.

## RQ8 — receiver-neutral bootstrap under assumptions

**Partially answered methodologically; numerical answer still open.** Stage 5.7 defines `A0`, `A1`, parameterized `A2(U)`, and non-neutral `A_host(H)`, together with `B | A`, `S | A`, and `SB | A` accounting. Stage 5.8 must instantiate at least one concrete artifact and, for an `A2` experiment, one exact `U` before a bit count can be accepted.

---

# 9. Threats to Validity and Limitations

## 9.1 Benchmark representativeness

Corpus v0.3 contains only 17 programs. Constructor distributions and break-even results remain corpus-specific.

## 9.2 Translation bias

Some baseline programs are project-designed translations rather than independently optimized shortest programs. The Jot result in particular characterizes one deterministic path only.

## 9.3 Independent implementation is finite evidence

The second implementation substantially strengthens reconstructability evidence but does not prove full specification completeness. The independent implementer used the same frozen packet, including conformance examples; untested ambiguity may remain.

## 9.4 Cognitive independence is procedural, not mathematically provable

The experiment records a blind packet boundary and an independence declaration, but no technical mechanism can prove that a model/implementer had never encountered related material elsewhere. The claim is therefore methodological and evidence-based, not absolute.

## 9.5 Differential generator coverage

The 942-case set covers all accepted v0.3 corpus programs, multiple valid construction templates, major static-error classes, and arbitrary well-shaped wire terms. It is not exhaustive over the infinite term space.

## 9.6 Runtime counters are implementation-specific

Transition/depth measurements from Stage 4 describe particular Go evaluators. They are not architecture-neutral computational-cost units.

## 9.7 Type-transmission alternative remains incomplete

Only a principal root-type envelope was measured. No complete alternative explicit typing/bootstrap system has yet been built.

## 9.8 Receiver-assumption profiles are research models, not facts about aliens

`A0`, `A1`, and `A2(U)` are explicit experimental conditions. They are not claims about what an extraterrestrial civilization, a future machine, or any concrete receiver actually knows. The model improves honesty by exposing priors, but it does not solve the epistemic problem of assigning a real-world probability or bit-equivalent cost to those priors.

## 9.9 Physical-layer cost remains outside the present boundary

`A0` begins with an already recovered finite ordered binary frame. The research has not measured signal acquisition, modulation discovery, timing, synchronization, framing discovery, noise correction, or physical units. These omitted costs are not claimed to be zero.

## 9.10 Reference-machine sensitivity remains unmeasured

`A2(U)` is parameterized because executable bit length depends on the selected machine and input convention. Until Stage 5.8 freezes and compares concrete candidates, the sensitivity of `B | A2(U)` to `U` remains unknown.

## 9.11 Receiver-neutral `S`, `B`, and joint `SB` remain numerically unresolved

Stage 5.7 supplies a disciplined conditional model but no measured bootstrap artifact. This remains the largest gap relative to the motivating total-information objective.

## 9.12 No machine-checked proof

Conformance, fuzzing, frozen checkpoints, differential testing, and the receiver-prior validator are empirical/structural methods. They do not replace a formal proof of codec correctness, principal typing, evaluator semantics, cross-implementation equivalence, or optimality of the assumption model.

---

# 10. Research Contributions to Date

1. A concrete architecture-neutral typed Core with canonical binary representation.
2. Executable separation of wire validity, scope validity, type validity, and finite resource refusal.
3. Language-neutral conformance corpora for wire, static, and dynamic semantics.
4. Frozen benchmark methodology that prevents post hoc workload rewriting.
5. Exact constructor-level wire attribution for a fixed corpus.
6. Empirical break-even evidence for `Let` and strong direct-`Nat` evidence against repeated `succ`.
7. A quantified first experiment on erased versus transmitted root type information.
8. Controlled BLC/Jot/structural-stack comparisons with explicit limitations.
9. An observational CBN/call-by-need experiment demonstrating substantial implementation-level savings on selected workloads.
10. A total-information accounting discipline that refuses to equate host source size with bootstrap cost.
11. A versioned independence protocol and frozen conformance packet.
12. A second implementation reconstructed without translating the reference implementation.
13. A hash-frozen pre-comparison checkpoint separating independent reconstruction from later differential analysis.
14. A 942-case post-freeze differential result with 942 portable matches, zero semantic mismatch, and zero resource asymmetry.
15. A machine-readable versioned receiver-assumption ladder `A0 ⊂ A1 ⊂ A2(U)` with a non-neutral host control `A_host(H)`.
16. Conditional bootstrap/specification notation `B | A`, `S | A`, `C | A` that prevents undeclared receiver priors from disappearing from claims.
17. A no-double-counting transmitted-bit ledger with an explicit joint `SB | A` category when specification and executable bootstrap are inseparable.
18. A living dissertation process that preserves positive, negative, and unresolved findings as research evidence changes.

---

# 11. Next Research: Measurable Bootstrap

## 11.1 Freeze one assumption profile before measuring

Stage 5.7 has removed the ambiguity in the phrase “receiver-neutral bootstrap”: future measurements must name a profile.

Two distinct tracks are now useful:

```text
Track A: attempt a more receiver-neutral artifact under A1
Track B: instantiate A2(U) with one exact tiny universal machine U
         and measure an executable bootstrap under that stronger prior
```

These tracks answer different questions. A numerically smaller Track B bootstrap cannot be called globally superior merely because it assumes more computational machinery for free in the conditional prior.

## 11.2 Concrete bootstrap candidates

Possible research directions remain:

- a tiny mathematical abstract machine;
- a minimal calculus/combinator bootstrap;
- a layered decoder → validator → evaluator artifact;
- a compact executable notation with an explicitly accounted decoding basis.

No candidate is preselected as the answer.

## 11.3 Exact ledger requirements

Every Stage 5.8 report must identify:

1. the exact receiver profile and version;
2. every transmitted setup segment;
3. exact bit length per segment;
4. which role each segment serves;
5. whether `S` and `B` are separable or require a joint `SB` segment;
6. all interpreters/machines required to interpret the candidate;
7. the program payload `P` to which the setup is being amortized.

Where defensible, report:

```text
B_decode
B_static
B_eval
S
```

Otherwise report the irreducible joint segment:

```text
SB | A
```

A result may be negative. If no defensible executable artifact can be constructed under `A1`, that finding is scientifically preferable to moving a hidden interpreter into the prior after the fact.

## 11.4 Future verification

Later work may include:

- sensitivity analysis across multiple exact choices of `U`;
- a third independent implementation in another paradigm;
- theorem-prover verification of prefix decoding, substitution/unification invariants, and evaluator properties;
- broader source-normalized corpora;
- full erased-versus-explicit checker/bootstrap comparison;
- total-cost comparisons against alternative computational systems under the same assumption profile.

---

# 12. Conclusion

The research began with a simple intuition: software languages are normally designed for humans and known machines, but an extremely constrained receiver may share neither. The work has progressively transformed that intuition into a falsifiable experimental system.

NEX-1 v0.1 now has a canonical wire representation, principal rank-1 type reconstruction, weak call-by-name semantics, executable conformance, reproducible benchmark measurements, negative external comparisons, and explicit accounting boundaries. Stage 4 demonstrated that several aesthetic intuitions are unreliable: `App` is not the largest measured wire contributor on the accepted corpus; direct naturals can save orders of magnitude against a naive constructive alternative; `Let` has a conditional break-even; BLC can be smaller on pure lambda terms; and call-by-need can dramatically reduce receiver work without changing tested observables.

Stage 5 added independent reconstruction evidence. A frozen packet was given to a separate implementation context before the Go source was available. That reconstruction independently passed all packet vectors and was frozen by content hash. Only then was the Go reference opened. The subsequent deterministic 942-case differential comparison produced 942 portable matches, no semantic mismatch, and no resource asymmetry. This result does not prove NEX globally correct, minimal, or optimal, but it materially strengthens the claim that the current NEX-1 v0.1 specification/conformance package is independently reconstructable over the tested semantic surface.

Stage 5.7 then makes explicit something the original `C = S + B + P` shorthand left implicit: bootstrap size is conditional on what the receiver already knows. The project now distinguishes a minimal digital transport boundary `A0`, an explicit mathematical metalanguage prior `A1`, a parameterized universal-machine prior `A2(U)`, and terrestrial host controls. The physical layer below `A0` is outside the current model rather than free; stronger priors cannot be treated as costless winners; and overlapping specification/bootstrap bits must be charged once through a joint `SB | A` segment.

The dominant remaining unknown is therefore concrete rather than rhetorical: can an actual finite bootstrap artifact be frozen and counted under one of these profiles without circular accounting? Until Stage 5.8 supplies such an artifact, the project will not claim a numerical total `C | A` or global superiority. Preserving that uncertainty is part of the research method by which stronger future claims can become reproducible and falsifiable.

---

# Glossary

**ABI (Application Binary Interface)** — binary interaction conventions for compiled software and a platform.

**Alpha-equivalence** — equivalence of lambda terms differing only in bound-variable names.

**Architecture-neutral** — specified without dependence on a particular processor ISA, word size, ABI, operating system, or host runtime.

**AST (Abstract Syntax Tree)** — structural in-memory representation of a term.

**`A0`** — Stage 5.7 digital-transport prior: one exact finite ordered binary frame with no residual bit error inside the model; physical acquisition remains below the model boundary.

**`A1`** — `A0` plus an explicitly enumerated discrete mathematical metalanguage, but no fixed universal computer and no NEX-specific semantics.

**`A2(U)`** — `A1` plus one exact versioned universal binary abstract machine `U` and its exact self-delimiting program/data convention.

**`A_host(H)`** — engineering-control profile that assumes a concrete terrestrial host `H`; explicitly ineligible for receiver-neutral bootstrap claims.

**Assumption atom** — one explicitly stated element of receiver-side prior knowledge/capability in the Stage 5.7 machine-readable registry.

**Binder** — construct introducing a bound variable; `Lam` and the body side of `Let` bind in NEX v0.1.

**Binary Lambda Calculus (BLC)** — Tromp's compact binary representation of untyped lambda terms [2].

**Bootstrap (`B`)** — receiver-side information required to realize enough machinery to process NEX; exact Stage 5 claims write this conditionally as `B | A`.

**Call-by-name (CBN)** — non-strict strategy in which arguments are delayed and may be recomputed on repeated use [9].

**Call-by-need** — lazy evaluation with sharing/memoization [10,11]. Experimental as an NEX implementation strategy, not normative semantics.

**Canonical representation** — project-defined unique representation used for wire/conformance observations.

**Conformance packet** — frozen allowlisted specification, decisions, vectors, and observation rules supplied to an independent implementer.

**Conformance vector** — language-neutral input/expected-output test artifact.

**Conditional bootstrap cost (`B | A`)** — transmitted bootstrap length measured under an explicit receiver-assumption profile `A`; it is not an unconditional machine-free scalar.

**de Bruijn index** — numeric bound-variable reference determined by binder structure [1].

**Differential conformance** — running two implementations on the same inputs and comparing only agreed portable observations.

**Erased typing** — ordinary term wire syntax omits type annotations and reconstructs types through inference.

**Hindley–Milner (HM)** — rank-1 polymorphic inference discipline underlying NEX static semantics [3,4].

**Independent checkpoint** — immutable hash-identified implementation state frozen before reference implementation comparison.

**Joint specification/bootstrap segment (`SB | A`)** — transmitted bits that inseparably serve both specification and executable-bootstrap roles and are therefore counted once rather than independently in `S` and `B`.

**Occurs check** — unification test preventing an infinite self-containing type.

**Portable observation** — result defined independently of host representation, such as canonical bits, normalized principal scheme, or observable WHNF.

**Principal type scheme** — most general HM type scheme for a term [4].

**Primitive (`Prim`)** — fixed Core operation identified by a numeric ID.

**Receiver-assumption profile (`A`)** — versioned set of prior receiver knowledge/capability conditioned on by a bootstrap/specification measurement.

**Receiver-neutral** — not depending on undeclared terrestrial implementation conventions. It does not mean prior-free.

**Resource asymmetry** — one implementation reaches a finite resource guard while another produces a result; not automatically a semantic disagreement.

**Resource refusal** — implementation failure due to finite configured resources, distinct from malformed input, static invalidity, or proof of divergence.

**Specification cost (`S`)** — information required to communicate computational rules; exact Stage 5 accounting writes `S | A` when a separate specification segment exists.

**Thunk** — delayed computation conceptually containing a term/action and environment/context.

**Total information cost (`C`)** — historical research objective `C = S + B + P`; exact Stage 5 measurements condition it on an explicit receiver profile.

**Transmitted-program cost (`P`)** — exact canonical program bits for a specified program set after the wire contract is established.

**Unification** — solving type equalities by substitutions.

**Weak-head normal form (WHNF)** — evaluation only far enough to reveal the outer value/function/constructor.

**Wire format** — canonical transmitted bit representation of NEX terms.

---

# Bibliography

Stable source identifiers correspond to `docs/SOURCES.md`. Primary/official sources are preferred; NEX-specific conclusions are not attributed to external literature.

1. **de Bruijn, N. G.** (1972). *Lambda calculus notation with nameless dummies, a tool for automatic formula manipulation, with application to the Church-Rosser theorem.* Indagationes Mathematicae (Proceedings), 75(5), 381–392. DOI: https://doi.org/10.1016/1385-7258(72)90034-0. `[SRC-0001]`
2. **Tromp, J.** *Binary Lambda Calculus.* Author-maintained technical reference. https://tromp.github.io/cl/Binary_lambda_calculus.html. `[SRC-0002]`
3. **Milner, R.** (1978). *A Theory of Type Polymorphism in Programming.* Journal of Computer and System Sciences, 17(3), 348–375. DOI: https://doi.org/10.1016/0022-0000(78)90014-4. `[SRC-0003]`
4. **Damas, L.; Milner, R.** (1982). *Principal Type-Schemes for Functional Programs.* POPL. DOI: https://doi.org/10.1145/582153.582176. `[SRC-0004]`
5. **Plotkin, G. D.** (1977). *LCF Considered as a Programming Language.* Theoretical Computer Science, 5(3), 223–255. DOI: https://doi.org/10.1016/0304-3975(77)90044-5. `[SRC-0005]`
6. **Elias, P.** (1975). *Universal codeword sets and representations of the integers.* IEEE Transactions on Information Theory, 21(2), 194–203. DOI: https://doi.org/10.1109/TIT.1975.1055349. `[SRC-0006]`
7. **Wells, J. B.** (1999). *Typability and type checking in System F are equivalent and undecidable.* Annals of Pure and Applied Logic, 98(1–3), 111–156. DOI: https://doi.org/10.1016/S0168-0072(98)00047-5. `[SRC-0007]`
8. **Schönfinkel, M.** (1924). *Über die Bausteine der mathematischen Logik.* Mathematische Annalen, 92, 305–316. Comparative combinatory background. `[SRC-0009]`
9. **Plotkin, G. D.** (1975). *Call-by-name, call-by-value and the lambda-calculus.* Theoretical Computer Science, 1(2), 125–159. DOI: https://doi.org/10.1016/0304-3975(75)90017-1. `[SRC-0011]`
10. **Launchbury, J.** (1993). *A Natural Semantics for Lazy Evaluation.* POPL. DOI: https://doi.org/10.1145/158511.158618. `[SRC-0012]`
11. **Sestoft, P.** (1997). *Deriving a lazy abstract machine.* Journal of Functional Programming, 7(3), 231–264. DOI: https://doi.org/10.1017/S0956796897002712. `[SRC-0013]`
12. **Barker, C.** (2001). *Iota and Jot: the simplest languages?* Archived author-maintained technical reference. `[SRC-0014]`
13. **W3C WebAssembly Working Group.** *WebAssembly Core Specification.* https://www.w3.org/TR/wasm-core/. `[SRC-0008]`
14. **The Go Project.** *The Go Programming Language Specification; math/big; testing/fuzzing documentation.* https://go.dev/ref/spec. `[SRC-0010]`
15. **Shannon, C. E.** (1948). *A Mathematical Theory of Communication.* Bell System Technical Journal, 27, 379–423 and 623–656. `[SRC-0015]`
16. **Kolmogorov, A. N.** (1965). *Three approaches to the definition of the concept “quantity of information”.* Problemy Peredachi Informatsii, 1(1), 3–11. `[SRC-0016]`
17. **Chaitin, G. J.** (1975). *A Theory of Program Size Formally Identical to Information Theory.* Journal of the ACM, 22(3), 329–340. DOI: https://doi.org/10.1145/321892.321894. `[SRC-0017]`

---

# Appendix A. Reproducibility Artifacts

## A.1 Normative/research artifacts

- `docs/NEX-1-v0.1.md` — canonical Core specification.
- `docs/NEX-1-v0.1.ru.md` — Russian mirror.
- `docs/ARCHITECTURE.md` — architecture boundaries.
- `docs/adr/` — decisions, including ADR-0014 receiver-assumption accounting.
- `docs/SOURCES.md` — source registry.

## A.2 Conformance

- `conformance/wire-v0.1.json`.
- `conformance/static-v0.1.json`.
- `conformance/eval-v0.1.json`.

## A.3 Benchmarks

- `benchmarks/corpus-v0.1.json`.
- `benchmarks/corpus-v0.2.json` — preserved resource checkpoint.
- `benchmarks/corpus-v0.3.json` — accepted Stage 4 corpus.

## A.4 Independent reconstruction

- `stage5/conformance-packet-v0.1/` — packet definition/audit.
- `stage5/build_packet.py` — reproducible packet builder.
- `independent/python/` — frozen first independent reconstruction.
- `stage5/independent-checkpoints/python-v0.1.json` — file/hash checkpoint.
- `stage5/verify_independent_checkpoint.py` — frozen-file verifier.
- `stage5/differential/run.py` — post-freeze differential runner.
- `reference/go/cmd/nexdiffprobe` — Go portable-observation adapter.

## A.5 Receiver-assumption model

- `docs/adr/0014-condition-bootstrap-cost-on-receiver-assumptions.md` — accounting decision.
- `stage5/receiver-assumptions/assumptions-v0.1.json` — canonical profile/atom registry.
- `stage5/receiver-assumptions/README.md` — interpretation and limits.
- `stage5/validate_receiver_assumptions.py` — structural/invariant validator.
- `.github/workflows/stage5-receiver-assumptions.yml` — dedicated clean-checkout gate.

## A.6 Merge and CI evidence

- Stage 1 merge: `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`.
- Stage 2 merge: `cefe889d90a275897de31aa23c4b9742a388ec8f`.
- Stage 3 merge: `166cdc03282ea500263fdca7185f006f9b17a702`.
- Stage 4 merge: `ebffde6c8669f65dfcba98d31d261d59b48d4dd0`.
- Stage 5 protocol/packet merge: `04f4f84cce50a15638802babbe934b70e495911c`.
- Stage 5 independent/differential merge: `f500a5c5485b4cd5f6b5d9bd6bc76980f2f06cdb`.
- Stage 5 independent/differential final PR CI: `35385704921`, `35385705027`, `35385705162` — success.
- Stage 5 independent/differential post-merge CI: `35386452647`, `35386452451`, `35386452447` — success.
- Differential report: 942/942 portable matches, zero mismatches, zero resource asymmetries.
- Stage 5.7 receiver-assumption CI: pending PR verification at this evidence horizon.

---

# Appendix B. Evidence-Gated Decision Summary

| Question | Current decision | Evidence status |
|---|---|---|
| Keep direct `Nat`? | Keep in v0.1 | Strong corpus experiment against repeated `succ`; not global numeric-code optimality |
| Keep `Let`? | Keep in v0.1 | Measured break-even; depends on payload/reuse |
| Keep erased HM? | Keep in v0.1; defer global redesign | Two implementations infer same tested principal schemes; bootstrap comparison still missing |
| Is CBN normative? | Yes | Specification + two-implementation conformance |
| Use call-by-need? | Allowed optimization when observably equivalent | Stage 4 17/17 agreement; runtime savings on selected workloads |
| Optimize `App` first? | No current evidence for priority | `Prim` is larger on v0.3 |
| Is NEX smaller than BLC? | No global claim | BLC wins 30 vs 37 bits on identical pure-lambda subset |
| Is NEX independently reconstructable? | Strongly supported for tested surface | Frozen independent implementation + 942/942 post-freeze differential agreement |
| Is unconditional `B` meaningful? | No current claim | Stage 5.7 requires explicit `B | A` |
| Can stronger-prior and weaker-prior bootstrap bit counts be ranked directly? | No | Prior strength is unpriced in v0.1 assumption model |
| May shared specification/bootstrap bits be counted twice? | No | ADR-0014 exact ledger; use joint `SB | A` if inseparable |
| Is NEX globally smallest? | No claim | Evidence insufficient |
| Is total `C` known? | No | Receiver-conditioned `S/B/SB` artifact not yet measured |

---

# Maintenance Rule

Per ADR-0012, this manuscript is part of the research process. A future change that creates a defensible new measurement, research-significant architectural decision, external baseline, independent conformance result, formal proof/counterexample, stage-level conclusion, revised `S/B/P/C` model, or falsification/qualification of a prior hypothesis must update this English manuscript and its Russian mirror in the same PR unless the PR explicitly documents why no research-text change is required.
