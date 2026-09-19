# NEX-1: A Compact Architecture-Neutral Typed Core for Teaching and Transmitting Computation

## Design, executable semantics, empirical validation, independent reconstruction, Core self-sufficiency, and receiver-conditioned teaching/bootstrap

**Document type:** living dissertation-style research manuscript  
**Canonical language:** English  
**Russian mirror:** `RESEARCH-DISSERTATION.ru.md`  
**Evidence horizon:** Stages 0–5 complete; post-Stage-5 literature re-audit incorporated; pre-Stage-6 Core self-sufficiency work active through the Stage 5.12e functional-stream checkpoint as of 2026-09-19  
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

Stage 5 also made receiver assumptions explicit. The corrected taxonomy distinguishes `A0` (exact binary frame), `A1` (elementary discrete mathematics), `A1(R)` (an exact formal rule calculus), `A2(U)` (an exact universal machine and framing), and `A_host(H)` (a terrestrial engineering control). No complete receiver-neutral bootstrap artifact has yet been accepted, so full `B | A` and total `C | A` remain unknown.

The post-Stage-5 literature re-audit did not reveal a fundamental defect in NEX-1 v0.1. It clarified that a future receiver-facing system needs a separate teaching sequence, as illustrated by Lincos, DeVito–Oehrle, Lingua Cosmica, and especially CosmicOS. However, before activating that teaching stage, ADR-0018 introduced a stricter prerequisite: test whether the **unchanged Core can implement enough of itself** to justify teaching it as the stable target.

The pre-Stage-6 self-sufficiency work has already produced mixed but informative evidence. NEX-written arithmetic and the integer component of the canonical wire codec are executable. A first numeric recursive representation using `2^a(2b+1)-1` is mathematically valid but has pathological recursive code-size growth; a bit-interleaving alternative avoids that growth but exceeds frozen sharing-depth budgets on moderate cases. These negative results were preserved rather than repaired by raising limits. A different representation, finite bit streams as functions `N -> N` with `0/1` data and `2` as EOF, was therefore preregistered under an anti-tuning protocol. Its indexed v0.2 candidate passed 26/26 frozen development observations and a separately preregistered 11/11 hold-out with zero Python-need, Go-need, or Go-CBN resource refusals under the frozen budgets. This establishes a practical finite-bit-stream representation checkpoint on the tested surface; it does not yet establish complete `Term` decoding, type inference, evaluation, self-processing, or receiver-neutral bootstrap.

The immediate research question is therefore Core self-sufficiency, not yet the teaching curriculum. Stage 6 remains planned and becomes active only after the 5.10–5.20 decision gate has enough evidence to classify the unchanged Core.

**Keywords:** architecture-neutral computation, self-hosting, teaching protocol, binary program representation, de Bruijn indices, Hindley–Milner, bootstrap, receiver assumptions, Binary Lambda Calculus, differential conformance, interstellar communication.

---

# 1. Research problem

Conventional software assumes extensive shared context: source syntax, text encodings, processors, executable formats, operating systems, compilers, virtual machines, and data conventions. For an unknown receiver these are not free facts; they are part of the interpretation problem.

A short program is not useful if its meaning depends on a large untransmitted interpreter. Conversely, a tiny interpreter may force all later programs to become unnecessarily large. More fundamentally, even a perfect interpreter artifact is useless if the receiver cannot determine what it is supposed to mean or how to validate its reconstruction.

The project therefore studies three coupled questions:

1. **NEX-1 Core** — what exact computational system should be the stable target;
2. **Core self-sufficiency** — whether that unchanged target can implement its own wire/static/dynamic machinery far enough to process itself;
3. **teaching/bootstrap** — what finite transmitted sequence can establish enough meaning for an unknown receiver to reconstruct and use that Core.

The central practical goal is:

> given an explicit receiver prior, construct a finite message after which the receiver can demonstrably decode, type-check, execute, and construct NEX programs, without silently importing a terrestrial implementation platform.

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

**RQ10.** Can the unchanged NEX-1 v0.1 Core express and execute a complete implementation of its own canonical wire, static, and dynamic semantics, including self-processing of the implementation's canonical representation?

RQ10 is the immediate pre-Stage-6 question. RQ9 remains the receiver-facing teaching question after the self-sufficiency gate is resolved.

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

Freudenthal's **Lincos** [SRC-0020] demonstrates progressive semantic teaching through constrained examples. DeVito and Oehrle [SRC-0028] emphasize the role of assumed prior scientific knowledge. Work on **Lingua Cosmica** uses constructive type theory to constrain logical interpretation [SRC-0022]. **CosmicOS** [SRC-0021] is especially relevant because it progressively introduces mathematics, logic, executable programs, and simulations.

These projects are design inputs, not obstacles. Their main lesson for NEX is that a final compact computational agreement and a teaching sequence are different artifacts.

```text
receiver prior
    -> teaching/bootstrap message
    -> NEX-1 competence
    -> canonical NEX programs
```

The self-sufficiency gate adds a prerequisite to this chain: before teaching NEX-1 as the stable target, the project tests whether NEX-1 can implement its own essential machinery without incompatible Core extensions.

## 3.5 Limits of assumed mathematics

Receiver profiles are experimental conditions, not claims about extraterrestrial cognition. Exosemiotic work explicitly questions whether mathematics and science would necessarily be conceptualized identically by another intelligence [SRC-0029]. `A1` is therefore an explicit prior chosen for an experiment, not a universal fact.

## 3.6 Independent implementations and differential testing

Stage 5 reduces implementation leakage, but agreement between two implementations is not a proof oracle. Knight–Leveson show that independently developed versions can exhibit correlated failures [SRC-0024], and differential testing cannot reveal a defect shared by every implementation [SRC-0027]. This constrains the interpretation of both the historical `942/942` result and later Python/Go self-hosting controls.

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

For Stage 5.12 representation work, an explicit anti-tuning protocol was added before the first runtime execution of `functional-stream-v0.2`. It fixes resource budgets, forbids deleting failed cases or raising limits for the same candidate, requires a new version after an algorithmic change, and distinguishes previously observed development cases from a separately preregistered hold-out. A hold-out failure rejects the tested version rather than authorizing tuning on the same hidden cases.

Frozen representation budgets are:

```text
Python call-by-need  5,000,000 transitions / depth 8,000
Go call-by-need      5,000,000 transitions / depth 20,000
Go normative CBN     5,000,000 transitions / depth 20,000
```

For the current representation experiments, Go-CBN refusal is recorded as a resource result rather than automatically classified as semantic invalidity; Python/Go sharing refusal or a semantic mismatch is an acceptance failure under the frozen protocol.

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

The implementations are strong executable evidence, but NEX-specific canonical-forms/preservation/progress-or-safety proofs remain open [SRC-0026]. If future profiles add mutable references or comparable effects, the v0.1 generalization rule must be revisited [SRC-0025].

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

Constructor prefix lengths are `2,2,2,3,4,4`, whose Kraft sum is 1. Any future shorter constructor prefix requires compensating changes elsewhere.

## 5.5 Dynamic semantics

The normative strategy is weak call-by-name. Arguments and `Let` values are delayed, reduction does not occur beneath `Lam` before application, primitive forcing is selective, pair/sum payloads remain delayed, and recursion is explicit through `fix`.

Call-by-need is an implementation strategy whose portability requires preservation of observable Core behavior; current empirical agreement is not a complete theorem.

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

For the tested 5-bit payload, `Let` loses to duplication at two and three uses, ties at four, and wins at eight. For the tested 14-bit payload it saves bits at two uses. Direct `Nat(255)` occupies 21 bits versus 2,300 bits for the tested repeated-`succ` construction.

A root-principal-type envelope changes 1,371 erased-term bits to 1,505 bits, an increase of 134 bits or 9.77%. Only this payload delta is measured; a reduction in checker/bootstrap burden has not been constructed.

On the identical three-program pure-lambda subset:

```text
NEX  37 bits
BLC  30 bits
```

No global winner follows. The Jot result is one deterministic translation, not a shortest-program search.

The accepted 17-program CBN/call-by-need experiment produced:

```text
CBN           226151 transitions
call-by-need    2484 transitions
reduction      98.90%
```

This is a project-defined transition-counter reduction, not a wall-clock or CPU-speed claim.

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

The cases consist of 17 frozen corpus programs, 325 valid parameterized cases, 100 static-error cases, and 500 randomized wire-level term shapes.

The accepted conclusion is strong differential-conformance evidence of reconstructability on the tested surface. The top-level portable observation `Function` remains deliberately coarse; stronger future testing should apply returned functions in generated contexts.

---

# 8. Receiver assumptions and bootstrap

The current corrected model is:

```text
A0        exact binary-frame prior
A1        elementary naturals and finite-sequence mathematics
A1(R)     A1 + exact formal rule calculus R and serialization
A2(U)     A1 + exact universal machine U and framing
A_host(H) terrestrial engineering control
```

Historical Stage 5 `assumptions-v0.1.json` is preserved unchanged; current work uses `assumptions-v0.2.json`.

Stage 5.8 tested recursive-rule, BLC-machine, and Python-host paths. None supplied an accepted complete receiver-neutral bootstrap.

```text
accepted complete bootstrap candidates  0
full B | A known                        false
full SB | A known                       false
total C | A computable                  false
```

This negative result is retained. Later self-sufficiency evidence does not retroactively turn host implementations into receiver-neutral bootstrap.

---

# 9. Pre-Stage-6 Core self-sufficiency gate

ADR-0018 inserts post-Stage-5 work 5.10–5.20 before Stage 6 activation. Historical Stage 5.0–5.9 remains closed. The gate asks whether the unchanged v0.1 Core can carry an implementation `I` that can eventually perform:

```text
Decode
Encode
Validate
Infer
Evaluate
```

and process `code(I)` itself.

A native x86/ARM/WASM compiler is not required by this gate because such a backend imports a separately specified target machine, ABI, and memory model.

## 9.1 Stage 5.12a — arithmetic foundation

Six closed NEX-written helpers were frozen and checked by Python and Go:

```text
add, mul, odd, halve, pow2, shift_right
```

```text
canonical functions                         6
canonical bits, counted as separate terms  756
test applications per implementation        22
Python/Go wire/type/Nat observations        matched
```

The 756-bit number is an engineering artifact size, not a bootstrap-cost claim.

## 9.2 Stage 5.12b — numeric pair/sequence and sharing

Seven NEX-written pair/sequence helpers occupy 3,290 bits as separate terms. On the frozen 37-case workload:

```text
Python CBN resource refusals                8
Go CBN resource refusals                    5
Python call-by-need resource refusals       0
Go call-by-need resource refusals           0
Python/Go need mismatches                    0
```

The largest successful Go contrast was `unpair_right(27)`: 4,857,667 CBN transitions versus 1,793 call-by-need transitions, approximately 2709x on the project counter. The result makes sharing an explicit engineering feasibility condition for this representation, not a new language semantic rule.

## 9.3 Stage 5.12c — NEX-written integer wire codec

The integer component of canonical wire is implemented in NEX itself.

```text
canonical functions                         6
canonical bits, counted as separate terms  11,881
encodeU bits                                3,860
decodeU bits                                4,249
execution cases                                25
Python need resource refusals                  1
Go need resource refusals                      0
Go CBN resource refusals                      13
```

Returned Python/Go need observations agree wherever Python returns, and both direct host `U(n)` controls agree with the NEX-written results. This is a real self-codec prerequisite, not yet complete `Term` encode/decode.

## 9.4 Stage 5.12d — rejected recursive numeric representations

The original mathematical pair

```text
pair(a,b) = 2^a * (2*b+1) - 1
```

is total and invertible, but recursive use can make outer code length depend on the **numeric value** of an already encoded subtree. This is operationally unsuitable for materializing realistic self ASTs.

A bit-interleaving bijection avoids that size explosion. Its exact NEX implementation was tested rather than accepted from the host formula alone. Under the frozen workload it produced:

```text
canonical functions                     3
canonical bits                        1,531
execution cases                          27
Python need resource refusals             6
Go need resource refusals                 4
Go CBN resource refusals                 14
returned semantic mismatches               0
```

The candidate is therefore rejected as the primary recursive representation under the frozen budgets. Resource limits were not raised to manufacture a pass.

## 9.5 Stage 5.12e — fixed-type functional streams

The next representation used higher-order functions rather than one recursively packed natural:

```text
Stream = N -> N
0 = bit 0
1 = bit 1
2 = EOF
```

The first v0.1 producer materialized a recursive `cons` chain. It was typeable, but four development cases reached transition `5,000,001` under a 5,000,000 Python-need budget. The failure is preserved as a negative checkpoint.

Before the successor was executed, the project froze an anti-tuning protocol. It prohibits increasing budgets or deleting failures for the same version, classifies all already observed inputs as development evidence, and preregisters a separate hold-out. Algorithmic changes after execution require a new candidate version.

`functional-stream-v0.2` replaced only the producer algorithm with direct indexed recursion over `(count,index)`. At freeze time its runtime result was unknown. Its first development execution then produced:

```text
canonical functions                         10
canonical bits, counted as separate terms  1,634
execution cases                              26
Python need resource refusals                 0
Go need resource refusals                     0
Go CBN resource refusals                      0
Python/Go need values matched               26/26
largest Python need transitions             13,855
largest Go need transitions                  6,418
```

After a green historical checkpoint regression, the unchanged candidate was executed once against 11 preregistered hold-out cases:

```text
Python need resource refusals                0
Go need resource refusals                    0
Go CBN resource refusals                     0
Python/Go need values matched              11/11
largest Python need transitions            13,747
largest Go need transitions                  6,368
```

The candidate and hold-out Git blob identities were checked before execution. No candidate wire, expected observation, test input, or resource budget was changed after preregistration.

The accepted interpretation is deliberately narrow:

> unchanged NEX-1 v0.1 can represent and query dynamically sized finite bit streams through a fixed rank-1 HM function type on the tested development and preregistered hold-out surfaces, within the frozen resource budgets.

This does **not** yet establish a practical `Term` representation, HM environments, substitutions, evaluator state, full self-hosting, or receiver-neutral bootstrap.

The next Stage 5.12 experiment must therefore define a cursor/parser interface over functional streams and freeze its result representation, development workload, resource budgets, and hold-out **before** collecting acceptance evidence.

---

# 10. Answers to current research questions

**RQ1.** Supported for v0.1 by executable conformance and two agreeing implementations.

**RQ2.** Functionally supported; total-cost optimality and formal NEX-specific type safety remain unresolved.

**RQ3.** Supported empirically on tested programs; a NEX-specific equivalence theorem remains open.

**RQ4.** Answered for the frozen corpus: `Prim` is largest there, `Let` has a break-even, and direct `Nat` strongly beats the tested repeated-`succ` construction.

**RQ5.** Mixed: BLC is smaller on the controlled pure-lambda subset; no global winner is established.

**RQ6.** No. Exact `P` exists for stated corpora, but complete `S | A`/`B | A`/`C | A` do not.

**RQ7.** Strongly supported as differential-conformance evidence on the tested surface.

**RQ8.** Methodologically clarified but numerically open; no complete receiver-neutral bootstrap exists.

**RQ9.** Not yet answered. It remains the planned teaching question after the self-sufficiency gate.

**RQ10.** Partially supported. NEX-written arithmetic and integer-wire machinery are executable; one fixed-type finite-stream representation has passed frozen development and preregistered hold-out workloads. Complete `Term` codec, validation, HM inference, evaluator, integrated toolchain, and self-processing remain unconstructed.

---

# 11. Threats to validity

- The accepted Stage 4 design corpus contains only 17 programs and is hand-designed.
- External translations such as Jot are fixed project translations, not globally shortest programs.
- The 942 differential cases are structured families, not 942 independently designed semantic workloads.
- Two independent implementations can share correlated errors.
- `Function` is a deliberately coarse portable observation unless tested through application contexts.
- Runtime transition counters are implementation-specific and are not wall-clock timings.
- The self-sufficiency workloads remain bounded and project-designed.
- Passing a preregistered hold-out reduces tuning risk but does not establish general correctness.
- Call-by-need agreement is empirical; NEX-specific observational-preservation metatheory remains open.
- The explicit-typing alternative has not been implemented as a complete checker/bootstrap system.
- Receiver profiles are research conditions, not claims about actual extraterrestrial knowledge.
- The physical communication layer is outside `A0` and is not assigned zero cost.
- No machine-checked proof establishes complete NEX semantic correctness, self-hosting, or optimality.

---

# 12. Contributions/results to date and research ordering

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
11. a literature-informed separation between the stable Core and a future teaching/bootstrap layer;
12. ADR-0018 and a pre-Stage-6 executable self-sufficiency gate;
13. NEX-written arithmetic and integer-wire prerequisites;
14. preserved negative evidence for two recursive numeric representation strategies;
15. an anti-tuning protocol with candidate versioning, frozen resource budgets, and preregistered hold-out;
16. a functional finite-bit-stream representation that passed both frozen development and preregistered hold-out workloads on the tested surface.

These are project results, not claims that every underlying idea is historically new.

The research order is now:

```text
complete 5.10–5.20 Core self-sufficiency evidence
        -> classify NEX-1 v0.1 at the 5.20 gate
        -> if the target remains supportable, activate Stage 6 teaching/bootstrap work
```

The immediate next technical experiment is a NEX-written cursor/parser over the accepted finite-stream interface. It must be preregistered before acceptance execution. Later steps remain structural validation, HM inference, evaluation, integration, self-processing, bounded/differential validation, and supporting metatheory.

Stage 6 remains **Planned**, not Active. Its retained target pipeline is:

```text
receiver prior A
    -> finite teaching message T
    -> reconstructed NEX competence
    -> conformance/self-test
    -> canonical NEX programs P
```

The existing Stage 6 curriculum artifact remains a plan, not an accepted teaching message and not a source of `T_bits`.

---

# 13. Conclusion

Stages 0–5 establish a stable experimental Core and substantial evidence that its explicit specification/conformance material is reconstructable. They do not solve the original communication problem completely.

The literature comparison makes one missing component clear: an unknown receiver eventually needs a curriculum, not merely a grammar or interpreter. The post-Stage-5 self-sufficiency work makes another prerequisite clear: before teaching NEX-1 as the stable target, the project should know whether the unchanged Core can carry its own essential implementation machinery.

Current evidence is neither a blanket success nor a Core-failure result. NEX-written arithmetic and integer wire coding work. Two recursive numeric data strategies exposed genuine practical problems and were recorded as negative evidence. A function-valued finite-stream representation then passed both a frozen development workload and a separately preregistered hold-out without changing the candidate or resource budgets. This removes one immediate concern—that rank-1 HM necessarily prevents dynamically sized finite bit data—but it does not answer whether complete syntax, typing, evaluator state, and self-processing can be made practical.

The immediate research task is therefore to continue the 5.10–5.20 gate with a preregistered stream cursor/parser and then the remaining self-static/self-dynamic machinery. Only after the 5.20 decision should the project activate Stage 6 and construct the finite transmitted teaching artifact. Once a complete teaching/bootstrap artifact exists, its exact bit length can replace speculative bootstrap proxies.

---

# Bibliography and source registry

The durable bibliography with exact source usage and limitations is maintained in `docs/SOURCES.md`. Stable source IDs used in this manuscript include SRC-0001 through SRC-0029.

The interstellar-teaching comparison is maintained separately in `docs/RELATED-WORK.md`.

---

# Maintenance rule

Per ADR-0012, reproducible measurements, research-significant decisions, independent-conformance results, formal counterexamples/proofs, stage-level conclusions, or changes to the accounting model must update this canonical manuscript and its Russian mirror unless the corresponding PR explicitly explains why no manuscript change is required.
