# NEX-1: A Minimal Architecture-Neutral Typed Core for Information-Efficient Transmission of Computation

## Design, formalization, executable semantics, empirical validation, and independent reconstruction

**Document type:** living dissertation-style research manuscript  
**Canonical language:** English  
**Russian mirror:** `RESEARCH-DISSERTATION.ru.md`  
**Evidence horizon:** Stages 0–4 complete; verified Stage 5 checkpoints through 5.7 as of 2026-09-18  
**Project:** NEX / `aliens_nex`

> This manuscript is a research synthesis maintained inside the repository. It does not replace the normative specification `docs/NEX-1-v0.1.md`, ADRs, tests, or reproducible experiment artifacts.

---

## Abstract

This work investigates whether executable computational knowledge can be transmitted to a receiver for whom no shared programming language, processor architecture, ABI, operating system, text encoding, or implementation environment may be assumed. The objective is therefore not program size alone but the total information model

```text
C = S + B + P,
```

where `S` is information needed to specify the computational system, `B` is receiver-side information needed to realize an initial computational basis, and `P` is transmitted program payload.

The experimental system NEX-1 v0.1 is a small statically typed functional core with six term constructors (`Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`), de Bruijn indices, rank-1 Hindley–Milner polymorphism, arbitrary-precision naturals, a fixed primitive basis, explicit recursion through `fix`, a self-delimiting binary representation, and weak call-by-name (CBN) semantics. Its theoretical basis includes de Bruijn's nameless representation [1; SRC-0001], Binary Lambda Calculus [2; SRC-0002], Hindley–Milner inference and principal type schemes [3,4; SRC-0003, SRC-0004], PCF/LCF-style typed recursion [5; SRC-0005], and Elias universal coding [6; SRC-0006].

Stages 1–3 establish executable wire, static, and dynamic semantics. Stage 4 freezes benchmark corpora and measurement rules before optimization experiments. On the accepted 17-program corpus, canonical NEX occupies 1,371 bits over 345 AST nodes. On an identical three-program pure-lambda subset, Binary Lambda Calculus is smaller than NEX (30 versus 37 bits), so this work does not claim universal program-size superiority. An experimental call-by-need implementation preserves all 17 accepted observable results while reducing transition count in the measured Go evaluator from 226,151 to 2,484; this is implementation evidence rather than transmission-cost evidence.

Stage 5 tests independent reconstructability. A Python implementation was produced from a frozen specification/conformance packet without access to the Go reference source. After the Python implementation was frozen, the two implementations were compared on 942 portable observations; all 942 matched, with no semantic mismatch and no finite-resource asymmetry. This provides strong empirical evidence of independent reconstructability over the tested surface, but not a formal completeness proof.

Stage 5.7 makes receiver assumptions explicit. Specification and bootstrap costs are now conditioned on a declared assumption profile `A`, yielding `S | A`, `B | A`, and `C | A`. The first versioned model defines `A0`, `A1`, parameterized `A2(U)`, and terrestrial engineering control `A_host(H)`. If one transmitted object inseparably serves both specification and executable-bootstrap roles, its bits are counted once as `SB | A` rather than twice.

The main unresolved problem is therefore concrete: construct and exactly measure at least one finite bootstrap artifact under an explicit receiver profile without hiding an interpreter or double-counting transmitted bits. Until then, total `C | A` remains numerically unresolved.

**Keywords:** minimal programming language, architecture-neutral computation, binary program representation, de Bruijn indices, Hindley–Milner, Binary Lambda Calculus, bootstrap, independent implementation, differential conformance, reproducible research.

---

# 1. Introduction

## 1.1 Motivation

Conventional software relies on extensive shared context: character encodings, source syntax, processor models, word sizes, executable formats, operating systems, compilers, or virtual machines. These are useful assumptions in ordinary engineering. In a communication problem with an unknown receiver, the same assumptions become hidden parts of the cost.

A short program is therefore not necessarily an information-efficient program. A one-bit payload is unhelpful if its meaning depends on a large untransmitted interpreter. Conversely, an extremely small universal interpreter may make all later programs substantially larger. NEX studies the joint cost

```text
C = S + B + P.
```

Unknown quantities are not assigned zero merely because they have not yet been represented. Go or Python source code is not silently treated as receiver-neutral bootstrap information.

## 1.2 Research problem

The research problem is to determine whether a compact typed computational core can provide a useful trade-off among:

- transmitted program size;
- specification burden;
- receiver bootstrap burden;
- deterministic decoding, typing, and evaluation;
- independent reconstructability.

A further problem is that any numerical bootstrap claim depends on what the receiver is assumed to know beforehand. Total information cost must therefore be conditioned on an explicit receiver-assumption model.

## 1.3 Object and subject of research

**Object:** architecture-neutral representation and execution of general-purpose computation under severe information constraints.

**Subject:** trade-offs among specification cost, receiver bootstrap cost, program representation, static type reconstruction, evaluation strategy, independent conformance, and receiver assumptions.

## 1.4 Goal

Construct and empirically evaluate a small executable core that can be independently reconstructed from communicated rules, while developing a reproducible methodology for measuring its total information cost and comparing it with alternatives.

## 1.5 Research objectives

1. Define a small architecture-neutral computational core.
2. Define a canonical self-delimiting binary representation.
3. Build executable encode/decode conformance.
4. Formalize closed scope and principal type reconstruction.
5. Formalize weak non-strict dynamic semantics.
6. Separate semantic validity from finite implementation resource limits.
7. Freeze benchmark corpora before optimization experiments.
8. Measure constructor-level program cost and controlled alternatives.
9. Compare selected external representations under explicit common conditions.
10. Test independent implementation without reference-source access.
11. Make receiver assumptions an explicit part of bootstrap accounting.
12. Prevent double counting between specification and executable bootstrap.
13. Preserve positive, negative, and unresolved results in a living research manuscript.

## 1.6 Research questions

**RQ1.** Can NEX be given a deterministic, architecture-neutral, self-delimiting binary representation with executable conformance evidence?

**RQ2.** Can closed NEX programs recover principal rank-1 types without ordinary term-level type annotations?

**RQ3.** Can simple normative CBN semantics coexist with a more efficient implementation that preserves portable observations?

**RQ4.** Which constructs dominate `P`, and are `Let` and direct `Nat` literals empirically justified?

**RQ5.** How does NEX program payload compare with selected alternative encodings on controlled common subsets?

**RQ6.** Can total cost `C` already be evaluated numerically?

**RQ7.** Can an implementation developed without access to `reference/go` reconstruct the same portable wire, static, and dynamic behavior from a frozen specification/conformance packet?

**RQ8.** Under which explicit receiver assumptions `A` can an executable bootstrap be represented and measured as `B | A`, or as joint `SB | A` when specification and bootstrap are inseparable?

## 1.7 Working hypotheses

**H1.** Nameless binding plus compact prefix encoding can yield a small unambiguous canonical representation.

**H2.** Rank-1 HM inference can remove ordinary type annotations from `P`, but its total benefit depends on receiver bootstrap cost.

**H3.** `Let` and direct natural literals may reduce payload even though they enlarge the language definition.

**H4.** Weak CBN may remain normative while call-by-need sharing serves as an observationally equivalent optimization on the tested pure Core.

**H5.** NEX should not be presumed smaller than highly compressed untyped lambda encodings on pure lambda terms.

**H6.** Program payload alone cannot establish total superiority.

**H7.** A sufficiently explicit specification plus portable vectors can support independent reconstruction without reference-source guidance.

**H8.** Meaningful numerical bootstrap cost requires explicit receiver assumptions rather than a hidden host language or VM.

**H9.** A transmitted bit serving both specification and executable-bootstrap roles must be counted once, not independently in both `S` and `B`.

---

# 2. Theoretical and Related-Work Basis

## 2.1 Nameless binding

De Bruijn showed that bound variables can be represented by numerical position rather than names [1; SRC-0001]. NEX adopts the nameless principle and fixes zero-based indices, eliminating alpha-renaming from the canonical transmitted term.

## 2.2 Binary Lambda Calculus

Tromp's Binary Lambda Calculus (BLC) demonstrates direct compact binary encoding of lambda terms [2; SRC-0002]. NEX uses BLC both as conceptual precedent and as a falsifying comparison point for excessive compactness claims.

## 2.3 Hindley–Milner inference

Milner and Damas–Milner provide the basis for rank-1 polymorphic inference and principal type schemes [3,4; SRC-0003, SRC-0004]. Wells' undecidability result for System F gives a useful boundary against assuming that unrestricted implicit polymorphism preserves HM's inference properties [7; SRC-0007].

## 2.4 Recursion and naturals

Plotkin's LCF/PCF work provides precedent for a small typed functional language with naturals and fixed-point recursion [5; SRC-0005]. NEX uses a separate project-specific primitive basis and binary format.

## 2.5 Universal integer coding

Elias introduced universal code families for positive integers [6; SRC-0006]. NEX defines `U(n)` as Elias gamma coding of `n+1`, enabling non-negative indices, naturals, and primitive identifiers.

## 2.6 Evaluation strategy

Plotkin formalized call-by-name and call-by-value distinctions [9; SRC-0011]. Launchbury and Sestoft provide semantic and implementation foundations for lazy evaluation with sharing [10,11; SRC-0012, SRC-0013]. NEX keeps weak CBN normative and treats call-by-need as a potential implementation optimization when portable observations remain unchanged.

## 2.7 Compact combinatory alternatives

Combinatory logic and Barker's Iota/Jot material provide comparison points for very small computational bases [8,12; SRC-0009, SRC-0014]. NEX's Jot measurement characterizes one documented deterministic translation, not a shortest-program search.

## 2.8 Communication boundary and interpreter-relative description length

Shannon's communication model separates engineering transmission structure from semantic interpretation [15; SRC-0015]. NEX uses this only to state a boundary: signal discovery, modulation, synchronization, framing recovery, and error correction lie below current profile `A0`; they are not assumed to have zero cost.

Kolmogorov and Chaitin make algorithmic description length relative to a chosen effective description mechanism [16,17; SRC-0016, SRC-0017]. This motivates an explicit reference interpretation for any numerical executable-bootstrap claim. These works do not select a privileged universal machine for NEX and do not establish optimality of any future bootstrap artifact.

---

# 3. Methodology

## 3.1 Evidence-gated development

The project uses the cycle:

```text
Problem
 -> Contract
 -> Invariant
 -> Executable example or failing test
 -> Implementation
 -> Verification
 -> Diff review
 -> Status checkpoint
 -> Research synthesis update
```

The repository, rather than conversational history, is treated as durable project memory.

## 3.2 Evidence classes

The manuscript distinguishes:

1. established external results grounded in primary or official sources;
2. NEX design decisions;
3. reproducible NEX measurements;
4. inferences from current evidence;
5. open hypotheses and unknown quantities.

Repeated assertion does not convert a hypothesis into fact.

## 3.3 Reproducibility

Evidence is preserved through:

- language-neutral JSON conformance vectors;
- unit, property, and fuzz tests;
- frozen benchmark corpora;
- deterministic experiment tools;
- Git identities and content hashes;
- clean-checkout CI;
- versioned reports and machine-readable receiver-assumption profiles.

## 3.4 Frozen-corpus rule

Once a corpus has been used for a comparative conclusion, it is not rewritten. Unfavorable results are preserved. Corpus v0.2, where `factorial-5` exceeds the default non-memoizing CBN transition budget, remains part of the experimental history.

## 3.5 Independence protocol

A second implementation is not considered independent merely because it uses another language. Before implementation, a separate allowlisted packet is frozen with `reference/go` excluded. The resulting implementation is content-hash frozen before direct comparison with Go begins.

## 3.6 Differential conformance

Post-freeze comparison uses portable observations only:

```text
canonical wire bits
normalized principal type or portable static error class
observable WHNF or portable evaluation error class
```

Object layout, fresh type-variable numbering, closure representation, transition counters, and other host-specific details are excluded.

## 3.7 Conditional total-information accounting

Stage 5.7 makes receiver assumptions explicit. A profile `A` describes knowledge and computational capabilities treated as shared before the measured transmission.

The first hierarchy is:

```text
A0        exact finite ordered binary frame
A1        A0 + explicit discrete mathematical metalanguage
A2(U)     A1 + exact universal binary machine U
               + exact self-delimiting program/data convention
A_host(H) A1 + concrete terrestrial host H; engineering control only
```

Measured quantities are therefore conditional:

```text
S | A
B | A
C | A
```

For distinct transmitted specification and bootstrap segments:

```text
C | A = (S | A) + (B | A,S) + P.
```

For an inseparable object serving both roles:

```text
C | A = (SB | A) + P.
```

Each transmitted bit is counted once. Stage 5.7 does not yet assign a numerical price to the assumptions themselves, so transmitted lengths from different profiles are not directly rankable as total-cost winners.

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

Bound variables use zero-based de Bruijn indices.

## 4.2 Types

```text
T ::= a | 1 | N | T -> T | T * T | T + T
S ::= forall a1 ... an. T
```

Static semantics use rank-1 HM inference with unification, occurs check, fresh instantiation, and `Let` generalization.

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

IDs 11–31 are reserved for Core; profiles begin at 32.

## 4.4 Wire representation

`U(n)` is Elias gamma coding of `n+1`.

```text
00   U(k)   Var(k)
01   T      Lam(T)
10   T T    App(T,T)
110  T T    Let(T,T)
1110 U(n)   Nat(n)
1111 U(p)   Prim(p)
```

## 4.5 Dynamic semantics

The normative strategy is weak call-by-name. Arguments and `Let` values are delayed, no reduction occurs beneath `Lam` before application, primitive forcing is selective, and general recursion is explicit through `fix`.

---

# 5. Stages 0–3: Formal and Executable Foundation

## 5.1 Stage 0 — project governance

Stage 0 established the canonical specification, architecture boundaries, ADR process, source registry, testing rules, and repository-as-memory discipline.

## 5.2 Stage 1 — binary representation

Stage 1 implemented arbitrary-precision `U(n)`, term encode/decode, exact versus prefix decoding, malformed-input classes, and separate decoder resource limits.

The conformance set contains 17 integer, 12 term, and 15 invalid exact-input vectors.

Representative encodings:

```text
Var(0)                    001
Nat(0)                    11101
Prim(0)                   11111
Lam(Var(0))               01001
Lam(App(Prim(1),Var(0)))  01101111010001
```

**Conclusion:** RQ1 is supported for the v0.1 wire grammar by executable evidence.

## 5.3 Stage 2 — static semantics

Stage 2 implemented closed-scope validation, type/scheme representations, free type variables, substitutions, unification with occurs check, primitive schemes, instantiation, `Let` generalization, and Algorithm-W-style inference.

**Conclusion:** RQ2 is functionally supported, but erased typing is not yet proven optimal in total information cost.

## 5.4 Stage 3 — dynamic semantics

Stage 3 produced a weak CBN reference evaluator and portable WHNF conformance. Unused arguments, branches, and fields remain unforced. Finite implementation resource refusal is separated from syntax and type invalidity.

**Conclusion:** a stable executable semantic target exists for independent reconstruction.

---

# 6. Stage 4: Empirical Validation

## 6.1 Frozen corpus

Accepted corpus v0.3 contains 17 programs spanning pure lambdas, arithmetic and branching, products and sums, polymorphic `Let`, recursion, multiplication, factorial, Fibonacci, and repeated expensive bindings.

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

The early expectation that `App` would dominate is not supported on this corpus; primitive references are the largest measured category.

## 6.2 `Let` break-even

For one tested 5-bit payload, `Let` loses to duplication at two and three uses, ties at four, and saves 8 bits at eight uses. For one tested 14-bit payload, two uses already produce a saving.

**Conclusion:** `Let` has a real payload/reuse-dependent break-even and remains in v0.1.

## 6.3 Direct naturals

At `n=255`:

```text
Nat(255)           21 bits
tested succ chain 2300 bits
```

This does not prove global optimality of the current integer code, but it strongly rejects replacing direct naturals with the tested repeated-`succ` construction.

## 6.4 Root-type transmission

An experimental envelope transmitting only the inferred principal root type yields:

```text
erased terms       1371 bits
root types           134 bits
total               1505 bits
overhead            +9.77%
```

This measures only a change in `P`; no corresponding receiver-side reduction in type-checker/bootstrap cost has yet been constructed and measured.

## 6.5 External and structural comparisons

On the identical pure-lambda subset (`identity`, `constant`, `composition`):

```text
NEX  37 bits
BLC  30 bits
```

Thus this work does not support universal NEX program-size superiority over BLC.

A fixed lambda-to-SK-to-Jot translation yields 288 bits for that subset; it is not a shortest-Jot search. A project-defined postfix structural representation yields 1,529 bits on the full corpus versus NEX's 1,371, but it reuses NEX integer and primitive conventions and is not an independent total-cost competitor.

## 6.6 CBN versus call-by-need

All 17 accepted programs produce the same observable result under the reference CBN evaluator and the experimental call-by-need evaluator. For the measured Go implementations:

```text
CBN transitions          226151
call-by-need transitions   2484
reduction                 98.90%
```

Most savings occur in recursive and repeatedly forced workloads. This is not a claim of universal 98.90% speedup and is not itself a term in `C`.

## 6.7 Stage 4 conclusion

For corpus v0.3, `P = 1371` bits is exact. Markdown specification size and Go source size are useful engineering characteristics but are not receiver-neutral measurements of `S` or `B`.

**Conclusion:** total `C` is not yet numerically defensible.

---

# 7. Stage 5: Independent Reconstruction and Receiver Assumptions

## 7.1 Independent-implementation experiment

A specification and its first implementation can share the same unstated assumption. Stage 5 therefore freezes an implementation packet and excludes `reference/go` from the blind reconstruction phase.

The packet is tied to source snapshot:

```text
4f9c50aed13cdbdf72c9ce6510521477d49c05a5
```

Python 3.12+ with standard library only was selected as the first independent target. Before direct comparison, the received implementation was frozen as:

```text
nex1-independent-python-v0.1.zip
SHA-256 = 783e4186f9a8c024f00a732deae33b547c81ed4d7639c610a1e8bc5997eb3fbe
```

Archive checkpoint marker:

```text
a594b73b711998df04b45eec296086d5577fba2f
```

## 7.2 Independent verification result

Before opening the Go reference source, the implementation passed:

| Evidence | Result |
|---|---:|
| Integer wire vectors | 17 / 17 |
| Term wire vectors | 12 / 12 |
| Invalid exact-wire vectors | 15 / 15 |
| Scope vectors | 15 / 15 |
| Type vectors | 19 / 19 |
| Evaluation vectors | 21 / 21 |
| Independent unit tests | 23 / 23 |

Additional pre-comparison audit exercised 20,000 generated wire round trips, large arbitrary-precision integer cases, laziness cases, and resource-refusal separation.

The internal architecture is not a mechanical copy of Go. For example, recursive `fix` forcing uses a dedicated Python `FixThunk`. This is not proof of independence by itself, but it is consistent with the declared protocol.

## 7.3 Post-freeze differential comparison

Only after the Python archive was frozen was direct Go comparison allowed. The deterministic set contains:

| Group | Cases |
|---|---:|
| Frozen corpus v0.3 | 17 |
| Generated valid programs | 325 |
| Generated single-defect static programs | 100 |
| Generated wire terms | 500 |
| **Total** | **942** |

Result:

```text
portable matches       942
semantic mismatches      0
resource asymmetries     0
```

PR #8 passed its clean-checkout gates and was squash-merged as:

```text
f500a5c5485b4cd5f6b5d9bd6bc76980f2f06cdb
```

Post-merge verification on `main` also succeeded.

**Conclusion:** RQ7 is strongly supported over the tested surface. Finite conformance evidence cannot prove that every possible term is fully determined by the natural-language specification, but it materially reduces the risk that the first implementation depends on undocumented assumptions.

## 7.4 Ambiguity finding

The independent implementation separately noted diagnostic precedence for a term containing multiple independent static defects. Python checks scope first; post-freeze inspection found that Go currently does the same.

This coincidence is not promoted into normative semantics. Diagnostic ordering for multiple simultaneous errors does not affect valid-program semantics and has not demonstrated a portable requirement.

## 7.5 Receiver-assumption profiles

After independent reconstruction, the largest remaining uncertainty is bootstrap accounting. ADR-0014 defines the first versioned receiver-assumption model:

```text
A0
  - two distinguished binary symbols;
  - finite first-to-last ordering;
  - exact frame boundary and length;
  - no residual bit error inside the model.

A1 = A0 +
  - non-negative integers and basic arithmetic/order relations;
  - finite sequences, length, concatenation, positional indexing;
  - deterministic finite and recursive rule descriptions.

A2(U) = A1 +
  - exact binary operational semantics of one fixed universal machine U;
  - exact self-delimiting program/data convention for U.

A_host(H) = A1 +
  - concrete terrestrial host H;
  - engineering control only; not receiver-neutral.
```

The physical layer lies below `A0`. Signal discovery, modulation, synchronization, frame discovery, and error correction are not measured here; exclusion from scope is not a zero-cost claim.

Universal machine `U` in `A2(U)` remains a parameter. No numerical `B | A2(U)` is admissible until an exact versioned `U` is frozen.

## 7.6 Stage 5.7 result

The profile model is stored in a machine-readable registry and checked by a dedicated validator. It enforces the intended profile hierarchy, excludes terrestrial hosts from `A2(U)`, and checks exactly-once accounting rules.

First verified PR #9 checkpoint:

```text
stage5-receiver-assumptions  35387833962  success
stage5-independence          35387833785  success
stage5-differential          35387833852  success
```

The registry contains 4 effective assumption atoms for `A0`, 7 for `A1`, 9 for `A2(U)`, and 8 for control profile `A_host(H)`. These counts describe registry structure, not information content of the priors.

**Conclusion:** RQ8 now has a methodological answer, but no measured executable bootstrap yet exists.

---

# 8. Answers to Research Questions

**RQ1.** Supported for v0.1: the wire representation is deterministic, has language-neutral vectors, and is implemented independently twice.

**RQ2.** Functionally supported: tested closed programs recover principal schemes without ordinary term annotations. Total-cost optimality remains unresolved.

**RQ3.** Supported on the tested pure Core: normative CBN and experimental call-by-need produce the same accepted observations while differing substantially in internal work.

**RQ4.** On corpus v0.3, `Prim` is the largest measured category; `Let` has a measurable break-even; direct `Nat` is far smaller than the tested repeated-`succ` construction.

**RQ5.** Mixed: BLC is smaller on the identical pure-lambda subset, while the selected postfix structural representation is larger on corpus v0.3. No global winner is established.

**RQ6.** Not yet. Exact `P` is known for stated corpora, but `S | A` and `B | A` are not yet represented by complete measured receiver-neutral artifacts.

**RQ7.** Strongly supported empirically: the frozen independent implementation passed its packet and matched Go on all 942 accepted differential cases.

**RQ8.** Partially answered methodologically: explicit receiver profiles and conditional accounting rules now exist. A numerical answer requires Stage 5.8.

---

# 9. Threats to Validity and Limitations

## 9.1 Benchmark representativeness

Corpus v0.3 contains 17 programs and does not represent the full space of general-purpose software. Constructor shares and break-even points remain corpus-dependent.

## 9.2 Translation bias in external baselines

Some comparison programs are produced by project-defined deterministic translations. In particular, the Jot result does not characterize a shortest possible Jot program.

## 9.3 Finite independent evidence

A second implementation materially strengthens reconstructability evidence, but 942 differential cases do not cover the infinite space of valid and invalid terms. Untested specification ambiguity may remain.

## 9.4 Procedural cognitive independence

The protocol records which materials were available and freezes the implementation before reference comparison. It cannot mathematically prove that a model or implementer had never encountered similar ideas elsewhere. Independence is therefore an experimental condition rather than a theorem.

## 9.5 Implementation-specific runtime counters

Transition and depth counts from Stage 4 describe particular Go evaluators, not architecture-neutral computation units.

## 9.6 Incomplete explicit-typing alternative

Only principal root-type transmission has been measured. A complete alternative checker/bootstrap design has not yet been built.

## 9.7 Receiver profiles are experimental conditions

`A0`, `A1`, and `A2(U)` are not claims about what an extraterrestrial civilization or future machine actually knows. The model exposes assumptions but does not yet assign them real-world probabilities or bit-equivalent costs.

## 9.8 Physical-layer costs remain outside scope

`A0` begins with an already recovered finite ordered binary frame. Signal acquisition, modulation discovery, synchronization, framing recovery, physical units, and error correction are not measured.

## 9.9 Universal-machine sensitivity is unknown

`B | A2(U)` depends on the selected machine and its input convention. That sensitivity remains unmeasured until Stage 5.8 freezes concrete candidates.

## 9.10 No machine-checked semantic proof

Conformance, fuzzing, frozen checkpoints, and differential comparison are empirical methods. They do not replace formal proofs of codec correctness, principal typing, evaluator semantics, or optimality of the accounting model.

---

# 10. Research Contributions to Date

Current contributions are:

1. a concrete architecture-neutral typed Core with canonical binary representation;
2. executable separation of syntax validity, scope validity, type validity, and finite resource refusal;
3. language-neutral conformance sets for wire, static, and dynamic semantics;
4. frozen-corpus methodology that preserves inconvenient results;
5. exact constructor-level wire measurements and empirical results for `Let` and direct `Nat`;
6. controlled BLC, Jot, and structural comparisons without a global-winner claim;
7. evidence that call-by-need can greatly reduce implementation work while preserving accepted CBN observations;
8. a frozen independent-implementation protocol and a 942/942 post-freeze differential result;
9. conditional accounting `S | A`, `B | A`, `C | A`, together with joint `SB | A` to prevent hidden priors and double counting;
10. a living research record that preserves positive, negative, and unresolved findings.

---

# 11. Next Research Stage

## 11.1 Measurable bootstrap artifact

Stage 5.8 must freeze at least one finite transmitted object whose exact bit length can be reported under a declared receiver profile.

Two distinct tracks are currently useful:

```text
Track A: attempt a more receiver-neutral artifact under A1.

Track B: select one exact small universal machine U,
         freeze A2(U), and measure a NEX bootstrap for it.
```

These tracks answer different questions. A smaller bit count under `A2(U)` is not automatically superior to a larger count under `A1`, because `A2(U)` assumes more receiver-side computational structure.

## 11.2 Measurement requirements

A Stage 5.8 report must identify:

1. exact profile/version `A`;
2. every transmitted setup segment;
3. exact bit length of each segment;
4. role of each segment;
5. whether `S` and `B` can be defensibly separated;
6. every interpreter or machine required by the artifact;
7. the program payload `P` over which setup cost is amortized.

Where separation is meaningful, a useful decomposition is:

```text
B_decode
B_static
B_eval
S
```

Otherwise the report should use:

```text
SB | A.
```

A negative result is admissible. If no defensible executable artifact can be built under `A1` without hiding an interpreter, that is itself meaningful evidence.

---

# 12. Conclusion

This research began from a simple observation: conventional programming languages are designed for humans and known machines, while an extremely distant or otherwise unknown receiver may share neither. The project has turned that observation into a falsifiable system with a normative binary representation, static and dynamic semantics, reproducible measurement, and an independently developed second implementation.

The evidence has already corrected several plausible intuitions. `App` is not the largest measured wire contributor on the accepted corpus; direct naturals can be orders of magnitude smaller than a constructive `succ` chain; `Let` has conditional rather than universal value; BLC can beat NEX on a controlled pure-lambda subset; and a more efficient evaluator can greatly reduce internal work without changing normative semantics.

The independent implementation and 942/942 portable-observation agreement strengthen the central qualitative result: over the tested surface, NEX-1 v0.1 is determined by transmitted specification/conformance material rather than only by the original Go implementation. The original total-information question, however, remains open. It now requires an explicit receiver profile and a concrete bootstrap artifact whose bits can be counted without hidden interpreters or double counting.

Until that artifact exists, this work makes no claim of global NEX minimality and assigns no numerical value to total `C | A`.

---

# Glossary

**ABI (Application Binary Interface)** — binary interaction conventions between software and a platform.

**Architecture-neutral** — specified without dependence on a particular ISA, word size, ABI, operating system, or host runtime.

**AST (Abstract Syntax Tree)** — structural representation of a program term.

**Assumption atom** — one explicitly recorded item of receiver-side prior knowledge or capability in the Stage 5.7 registry.

**Binary Lambda Calculus (BLC)** — Tromp's compact binary representation of untyped lambda terms [2].

**Bootstrap (`B`)** — transmitted information required for the receiver to realize sufficient machinery to process NEX; in Stage 5.7+ measured only conditionally as `B | A`.

**Call-by-name (CBN)** — non-strict strategy in which arguments are delayed and may be recomputed on repeated use [9].

**Call-by-need** — lazy evaluation with sharing or memoization [10,11].

**Canonical representation** — project-defined unique representation used for transmission and conformance.

**Conformance vector** — language-neutral input and expected-result artifact.

**de Bruijn index** — numeric reference to a bound variable determined by binder nesting [1].

**Differential conformance** — comparing two implementations on the same inputs using only predefined portable observations.

**Independent checkpoint** — content-hash-identified state of a second implementation frozen before reference-source comparison.

**Joint specification/bootstrap segment (`SB | A`)** — transmitted bits inseparably serving both roles and therefore counted once.

**Occurs check** — unification condition preventing an infinite self-containing type.

**Portable observation** — result independent of host representation, such as canonical bits, normalized principal scheme, WHNF, or a portable error class.

**Principal type scheme** — most general HM type scheme for a term [4].

**Receiver-assumption profile (`A`)** — versioned set of receiver-side prior knowledge and computational capability conditioning measured costs.

**`A0`** — digital transport profile: one exact finite ordered binary frame is already available; physical acquisition is outside the model.

**`A1`** — `A0` plus an explicit discrete mathematical metalanguage, but no fixed NEX-aware universal computer.

**`A2(U)`** — `A1` plus one exact versioned universal binary machine `U` and its program/data convention.

**`A_host(H)`** — engineering-control profile using a concrete terrestrial host `H`; not eligible for receiver-neutral claims.

**Resource refusal** — implementation failure caused by a finite configured resource limit, distinct from malformed input or static invalidity.

**Self-delimiting encoding** — encoding whose object boundary can be recovered under the stated protocol without an externally supplied object length.

**Specification cost (`S`)** — transmitted information required to define the computational rules; in Stage 5.7+ stated relative to profile `A`.

**Total information cost (`C`)** — joint research objective over specification, bootstrap, and programs; in Stage 5.7+ treated as conditional `C | A`.

**Transmitted-program cost (`P`)** — exact canonical program bits for a stated program set.

**WHNF (weak-head normal form)** — evaluation only far enough to expose the outer value or function form.

---

# Bibliography

Stable `SRC-xxxx` identifiers correspond to `docs/SOURCES.md`.

1. **de Bruijn, N. G.** (1972). *Lambda calculus notation with nameless dummies, a tool for automatic formula manipulation, with application to the Church-Rosser theorem.* Indagationes Mathematicae (Proceedings), 75(5), 381–392. DOI: https://doi.org/10.1016/1385-7258(72)90034-0. `[SRC-0001]`
2. **Tromp, J.** *Binary Lambda Calculus.* https://tromp.github.io/cl/Binary_lambda_calculus.html. `[SRC-0002]`
3. **Milner, R.** (1978). *A Theory of Type Polymorphism in Programming.* Journal of Computer and System Sciences, 17(3), 348–375. DOI: https://doi.org/10.1016/0022-0000(78)90014-4. `[SRC-0003]`
4. **Damas, L.; Milner, R.** (1982). *Principal Type-Schemes for Functional Programs.* POPL. DOI: https://doi.org/10.1145/582153.582176. `[SRC-0004]`
5. **Plotkin, G. D.** (1977). *LCF Considered as a Programming Language.* Theoretical Computer Science, 5(3), 223–255. DOI: https://doi.org/10.1016/0304-3975(77)90044-5. `[SRC-0005]`
6. **Elias, P.** (1975). *Universal codeword sets and representations of the integers.* IEEE Transactions on Information Theory, 21(2), 194–203. DOI: https://doi.org/10.1109/TIT.1975.1055349. `[SRC-0006]`
7. **Wells, J. B.** (1999). *Typability and type checking in System F are equivalent and undecidable.* Annals of Pure and Applied Logic, 98(1–3), 111–156. DOI: https://doi.org/10.1016/S0168-0072(98)00047-5. `[SRC-0007]`
8. **Schönfinkel, M.** (1924). *Über die Bausteine der mathematischen Logik.* Mathematische Annalen, 92, 305–316. `[SRC-0009]`
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

## A.1 Normative and research documents

- `docs/NEX-1-v0.1.md` — canonical Core specification.
- `docs/NEX-1-v0.1.ru.md` — Russian informative mirror.
- `docs/ARCHITECTURE.md` — architecture boundaries.
- `docs/adr/` — architecture and research-method decisions.
- `docs/SOURCES.md` — external source registry.

## A.2 Conformance

- `conformance/wire-v0.1.json`.
- `conformance/static-v0.1.json`.
- `conformance/eval-v0.1.json`.

## A.3 Benchmark corpora

- `benchmarks/corpus-v0.1.json`.
- `benchmarks/corpus-v0.2.json` — preserved resource checkpoint.
- `benchmarks/corpus-v0.3.json` — accepted Stage 4 corpus.

## A.4 Independent reconstruction

- `stage5/conformance-packet-v0.1/` — packet definition.
- `stage5/build_packet.py` — reproducible packet builder.
- `independent/python/` — frozen first independent implementation.
- `stage5/independent-checkpoints/python-v0.1.json` — independent-source hash checkpoint.
- `stage5/differential/run.py` — post-freeze differential comparison.

## A.5 Receiver-assumption model

- `stage5/receiver-assumptions/assumptions-v0.1.json` — machine-readable `A0/A1/A2(U)/A_host(H)` registry.
- `stage5/validate_receiver_assumptions.py` — structural invariant validator.
- ADR-0014 — conditional accounting rules for `S | A`, `B | A`, `SB | A`, and `C | A`.

## A.6 Major Git and CI checkpoints

- Stage 1: `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`.
- Stage 2: `cefe889d90a275897de31aa23c4b9742a388ec8f`.
- Stage 3: `166cdc03282ea500263fdca7185f006f9b17a702`.
- Stage 4: `ebffde6c8669f65dfcba98d31d261d59b48d4dd0`.
- Independence protocol: `04f4f84cce50a15638802babbe934b70e495911c`.
- Independent implementation and differential checkpoint: `f500a5c5485b4cd5f6b5d9bd6bc76980f2f06cdb`.
- Verified Stage 5.7 PR #9 checkpoint: `0629089f3cd13574148da05252acf136018fdf1d`.
- Final checks for that checkpoint: `35388377913`, `35388377505`, `35388377502` — success.

---

# Appendix B. Evidence-Gated Decision Summary

| Question | Current decision | Evidence |
|---|---|---|
| Keep direct `Nat`? | Yes | Strong result against the tested repeated-`succ` construction; global integer-code optimality not established |
| Keep `Let`? | Yes | Measured payload/reuse break-even |
| Keep erased HM typing? | Yes for v0.1 | Functionally reproduced by two implementations; total checker/bootstrap comparison remains open |
| Keep CBN normative? | Yes | Specification plus two-implementation conformance |
| Permit call-by-need? | Yes as an optimization | 17/17 accepted observable results agree |
| Is NEX always smaller than BLC? | No such claim | BLC wins 30 versus 37 bits on the controlled pure-lambda subset |
| Is NEX independently reconstructable? | Strongly supported over tested surface | Frozen second implementation plus 942/942 differential agreement |
| Is total `C | A` known? | No | No measured bootstrap `B | A` or joint `SB | A` exists yet |

---

# Maintenance Rule

Per ADR-0012, new reproducible measurements, research-significant architectural decisions, external baselines, independent conformance results, proofs, counterexamples, stage-level conclusions, or revisions to the `S/B/P/C` model must update this canonical manuscript and its Russian mirror.

Per ADR-0003, the Russian mirror preserves semantic parity but is not required to reproduce English wording or sentence structure literally. Russian explanatory prose should be idiomatic; English forms are retained for identifiers, formal notation, system names, and terms where they materially aid precision or literature search.
