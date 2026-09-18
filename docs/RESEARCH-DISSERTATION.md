# NEX-1: A Minimal Architecture-Neutral Typed Core for Information-Efficient Transmission of Computation

## Design, formalization, executable semantics, empirical validation, and independent reconstruction

**Document type:** living dissertation-style research manuscript  
**Canonical language:** English  
**Russian mirror:** `RESEARCH-DISSERTATION.ru.md`  
**Evidence horizon:** Stages 0–5 complete as of 2026-09-18  
**Project:** NEX / `aliens_nex`

> This manuscript is a research synthesis maintained inside the repository. It does not replace the normative specification `docs/NEX-1-v0.1.md`, ADRs, tests, or reproducible experiment artifacts.

---

## Abstract

This research asks whether executable computational knowledge can be transmitted to a receiver for whom no shared programming language, processor architecture, ABI, operating system, text encoding, or implementation environment may be assumed. The objective is not program size alone but the joint information model

```text
C = S + B + P,
```

where `S` is information needed to specify the computational system, `B` is information needed by the receiver to realize an initial computational basis, and `P` is transmitted program payload.

NEX-1 v0.1 is a small statically typed functional core with six term constructors (`Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`), de Bruijn indices, rank-1 Hindley–Milner inference, arbitrary-precision naturals, a fixed primitive basis, explicit recursion through `fix`, self-delimiting binary representation, and weak call-by-name semantics. The design draws on de Bruijn [1], Binary Lambda Calculus [2], Hindley–Milner inference [3,4], PCF/LCF-style recursion [5], Elias coding [6], and established work on call-by-name and lazy evaluation [9–11].

Stages 1–3 established executable wire, static, and dynamic semantics. Stage 4 froze benchmark corpora and measurement rules. On the accepted 17-program corpus, canonical NEX occupies 1,371 bits over 345 AST nodes. Primitive references are the largest measured contributor at 460 bits (33.6%). Direct `Nat(255)` occupies 21 bits versus 2,300 bits for the tested repeated-`succ` construction. A principal-root-type envelope adds 134 bits, or 9.77% to program payload. On an identical three-program pure-lambda subset, Binary Lambda Calculus is smaller than NEX (30 versus 37 bits), so no universal NEX compactness claim is supported. An experimental call-by-need implementation preserved all 17 observable results while reducing measured Go-evaluator transitions from 226,151 to 2,484.

Stage 5 tested whether NEX behavior can be reconstructed independently of the Go implementation. A Python implementation was created from a frozen specification/conformance packet before access to `reference/go`. After the Python implementation was frozen, 942 portable observations were compared: all 942 matched, with zero semantic mismatch and zero resource asymmetry. This is strong empirical evidence of independent reconstructability over the tested surface, not a formal completeness proof.

Stage 5 also made receiver assumptions explicit. Specification and bootstrap costs are now conditioned on a declared profile `A`, yielding `S | A`, `B | A`, and `C | A`. Profiles `A0`, `A1`, and `A2(U)` make progressively stronger assumptions; `A_host(H)` is a non-neutral terrestrial engineering control. If one transmitted artifact serves both specification and executable-bootstrap roles, it is counted once as `SB | A`.

The Stage 5.8 feasibility audit deliberately produced a negative complete-bootstrap result. A recursive-rule description under `A1` lacks an exact receiver-neutral binary rule language; a Binary Lambda Calculus route lacks a complete verified NEX interpreter; the Python implementation is finite but belongs only to `A_host(Python3.12)`. Therefore zero complete receiver-neutral bootstrap candidates are accepted and total `C | A` remains numerically unknown.

The central result of Stage 5 is therefore twofold: NEX-1 v0.1 is independently reconstructable on the tested semantic surface, while a defensible complete bootstrap cost has **not** yet been established. Future work should construct an actual dependency-closed bootstrap artifact rather than replace the unknown with host-source size or hidden assumptions.

**Keywords:** minimal programming language, architecture-neutral computation, de Bruijn indices, Hindley–Milner, Binary Lambda Calculus, binary program representation, bootstrap, independent implementation, differential conformance, reproducible research.

---

# 1. Research problem

Conventional software depends on extensive shared context: source syntax, text encodings, processors, operating systems, compilers, virtual machines, and data-representation conventions. In ordinary engineering this shared context is useful. For an unknown receiver it becomes hidden prior information.

A short program is therefore not necessarily an information-efficient program. A one-bit payload is unhelpful if it requires an enormous untransmitted interpreter. Conversely, a tiny universal interpreter may make every later program expensive. NEX studies the joint cost `C = S + B + P` and refuses to set unknown terms to zero.

The research object is architecture-neutral representation and execution of general-purpose computation under severe information constraints. The research subject is the trade-off among specification cost, receiver bootstrap cost, program representation, static type reconstruction, evaluation strategy, and explicit assumptions about the receiver.

The goal is to construct and empirically evaluate a compact executable core that can be independently reconstructed from communicated rules, while developing a reproducible method for evaluating total information cost.

---

# 2. Research questions

**RQ1.** Can NEX be given a deterministic, architecture-neutral, self-delimiting binary representation with executable conformance evidence?

**RQ2.** Can closed NEX programs recover principal rank-1 types without ordinary term-level annotations?

**RQ3.** Can simple normative call-by-name semantics coexist with a more efficient implementation that preserves portable observations?

**RQ4.** Which constructs dominate `P`, and are `Let` and direct `Nat` literals empirically justified?

**RQ5.** How does NEX program payload compare with selected alternative encodings on controlled common subsets?

**RQ6.** Can total cost `C` already be evaluated numerically?

**RQ7.** Can an implementation developed without access to `reference/go` reconstruct the same portable wire, static, and dynamic behavior from a frozen packet?

**RQ8.** Under which explicit receiver assumptions `A` can bootstrap be represented and measured as `B | A` or, when inseparable from specification, `SB | A`?

---

# 3. Theoretical basis

De Bruijn indices remove transmitted bound-variable names [1]. Binary Lambda Calculus provides a compact binary lambda baseline [2]. Milner and Damas–Milner provide the basis for rank-1 polymorphic inference and principal schemes [3,4], while Wells supplies a useful boundary against unrestricted implicit System F [7]. Plotkin's work motivates small typed recursive calculi and the distinction between call-by-name and call-by-value [5,9]. Elias supplies the universal integer-code basis used by `U(n)` [6]. Launchbury and Sestoft provide foundations for lazy sharing [10,11]. Iota/Jot and combinatory logic provide compact-basis comparison points [8,12]. Shannon, Kolmogorov, and Chaitin motivate explicit communication boundaries and interpreter-relative description length [15–17].

These sources motivate the research design; they do not prove that NEX or any chosen receiver profile is optimal.

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

The repository is treated as durable project memory. Claims are separated into external results, project design decisions, reproducible measurements, evidence-based inferences, and open unknowns.

Comparative corpora are frozen before optimization conclusions. Negative results are preserved. Resource refusal is distinguished from malformed input, type error, and proof of divergence.

For independent reconstruction, a versioned packet was frozen before the second implementation was written. The Go reference remained unavailable until the second implementation was content-hash frozen. Post-freeze differential testing compares portable observations only.

For bootstrap accounting, Stage 5 introduced explicit receiver profiles. Each transmitted bit must be counted once. Unknown interpreters cannot disappear into the prior after the fact.

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

## 5.5 Dynamic semantics

The normative strategy is weak call-by-name. Arguments and `Let` values are delayed, reduction does not occur beneath `Lam` before application, primitive forcing is selective, and general recursion is explicit through `fix`.

---

# 6. Results of Stages 1–4

Stages 1–3 produced executable wire, type, and evaluation conformance. Stage 4 then fixed an empirical corpus and measured design trade-offs.

For corpus v0.3:

| Metric | Value |
|---|---:|
| Programs | 17 |
| AST nodes | 345 |
| Wire bits | 1,371 |

Constructor attribution:

| Constructor | Bits | Share |
|---|---:|---:|
| `Prim` | 460 | 33.6% |
| `Var` | 286 | 20.9% |
| `App` | 264 | 19.3% |
| `Nat` | 244 | 17.8% |
| `Lam` | 84 | 6.1% |
| `Let` | 33 | 2.4% |

The early hypothesis that `App` would dominate was not supported; `Prim` is largest on this corpus.

`Let` has a real break-even: for a tested 5-bit payload it loses at two and three uses, ties at four, and saves 8 bits at eight uses. For a tested 14-bit payload it already saves bits at two uses.

For naturals:

```text
Nat(255)          21 bits
succ-chain(255) 2300 bits
```

This strongly rejects removal of direct `Nat` in favor of the tested repeated-`succ` construction.

A principal root-type envelope adds 134 bits:

```text
erased terms      1371 bits
root types         134 bits
hybrid total      1505 bits
                 +9.77%
```

This measures only `Delta P`; any bootstrap reduction remains unmeasured.

On the identical pure-lambda subset:

```text
NEX  37 bits
BLC  30 bits
```

Thus no universal NEX compactness claim is supported.

The experimental call-by-need evaluator preserved all 17 accepted observables while reducing measured transitions from 226,151 to 2,484. This is an implementation result, not a transmission-cost term.

---

# 7. Stage 5 — independent reconstruction

A frozen conformance packet was given to a separate implementation context without `reference/go`. The resulting Python implementation passed all packet vectors and 23 independent tests before comparison.

Frozen archive:

```text
sha256:783e4186f9a8c024f00a732deae33b547c81ed4d7639c610a1e8bc5997eb3fbe
```

After freezing, direct differential comparison used 942 deterministic cases:

```text
portable matches       942
semantic mismatches      0
resource asymmetries     0
```

One non-semantic ambiguity was recorded: global precedence among multiple independent static errors is unspecified. Both implementations currently choose scope-first, but this coincidence was not promoted into language semantics.

**Conclusion for RQ7:** independent reconstructability is strongly supported on the tested surface.

---

# 8. Stage 5 — receiver assumptions and bootstrap

ADR-0014 defines the first receiver-assumption ladder:

```text
A0      exact finite ordered binary frame
A1      A0 + discrete mathematical metalanguage
A2(U)   A1 + exact universal binary machine U and framing
A_host(H)  terrestrial engineering control only
```

Exact accounting is conditional:

```text
S | A
B | A
C | A
```

For inseparable specification/bootstrap material:

```text
SB | A
```

The physical layer below `A0` is outside the current experiment, not assigned zero cost.

Stage 5.8 applied a strict bootstrap acceptance contract.

### `A1` recursive-rule candidate

Rejected as incomplete. The project has no exact receiver-neutral binary syntax and operational semantics for the recursive-rule transmission language. English, UTF-8, Markdown, JSON, Go, and Python cannot be silently treated as `A1`.

### `A2(U=BLC)` candidate

Rejected as incomplete. BLC is a valid compact computational candidate, but the repository has no frozen, conformance-verified BLC program implementing the complete NEX decoder, type system, and evaluator. A BLC universal evaluator alone is not a NEX bootstrap.

### Python host control

The independent Python implementation is finite:

```text
NEX package source only             28,832 bytes
all frozen author-written files     52,859 bytes
```

These values belong to `A_host(Python3.12)` and are explicitly **not** `B`.

Accepted Stage 5.8 result:

```text
accepted complete bootstrap candidates  0
full B | A known                        false
full SB | A known                       false
total C | A computable                  false
```

**Conclusion for RQ8:** the accounting conditions are explicit, but no complete receiver-neutral bootstrap cost has yet been established.

---

# 9. Answers to research questions

**RQ1.** Supported for v0.1 by executable conformance and two agreeing implementations.

**RQ2.** Functionally supported; total-cost optimality of erased typing remains unresolved.

**RQ3.** Supported on tested programs: CBN observables are preserved by the experimental call-by-need implementation.

**RQ4.** Corpus-specific answer established: `Prim` dominates v0.3; `Let` has a break-even; direct `Nat` is strongly justified against the tested alternative.

**RQ5.** Mixed: BLC is smaller on the common pure-lambda subset; no global external winner is established.

**RQ6.** No. `P` is exact for stated corpora, but complete `S | A` and `B | A` are not yet known.

**RQ7.** Strongly supported empirically by the frozen independent implementation and 942/942 post-freeze agreement.

**RQ8.** Methodologically answered but numerically open: receiver profiles and admissible accounting are defined, while a complete bootstrap artifact is still missing.

---

# 10. Threats to validity

- The accepted benchmark corpus contains only 17 programs.
- External translations such as Jot are fixed project translations, not globally shortest programs.
- 942 differential cases do not exhaust the infinite term space.
- Cognitive independence is procedural, not mathematically provable.
- Runtime transition counters are implementation-specific.
- The explicit-typing alternative has not been implemented as a complete checker/bootstrap system.
- Receiver profiles are research conditions, not claims about an actual extraterrestrial civilization.
- The physical communication layer is excluded below `A0`.
- No machine-checked proof establishes full semantic equivalence or optimality.

---

# 11. Contributions to date

1. A compact architecture-neutral typed Core with canonical binary representation.
2. Executable separation of wire validity, scope validity, type validity, and finite resource refusal.
3. Language-neutral wire/static/dynamic conformance artifacts.
4. Frozen empirical methodology that preserves inconvenient results.
5. Exact constructor-level wire attribution and controlled `Let`/`Nat` experiments.
6. Controlled BLC/Jot/structural comparisons with explicit limitations.
7. A CBN/call-by-need observational experiment.
8. A frozen independent implementation and 942-case post-freeze differential result.
9. A versioned receiver-assumption model with conditional `S | A`, `B | A`, `C | A` accounting.
10. A documented negative bootstrap result that refuses host-source substitution or hidden interpreter assumptions.
11. A living bilingual research manuscript preserving positive, negative, and unresolved findings.

---

# 12. Conclusion and next research stage

Stage 5 closes with an intentionally asymmetric result.

The first question succeeded: NEX-1 v0.1 can be reconstructed independently on the tested semantic surface. The second question did not produce a complete bootstrap number: the current repository lacks a dependency-closed receiver-neutral artifact under the declared profiles.

This negative result is informative. It identifies the exact work required before total information cost can be computed. A later stage should choose one of two clean construction paths:

1. under `A1`, define an exact receiver-neutral recursive-rule transmission language and encode the complete NEX semantics in it; or
2. under `A2(U)`, freeze one exact universal machine `U` and implement a complete conformance-verified NEX decoder/typechecker/evaluator for that machine.

Until such an artifact exists, the project will not publish a scalar `B`, total `C`, or a claim of global NEX superiority.

---

# Glossary

**Architecture-neutral** — specified without dependence on a particular processor, ABI, OS, or host runtime.

**Bootstrap (`B`)** — receiver-side information required to realize enough machinery to process NEX; meaningful only relative to declared assumptions.

**Call-by-name (CBN)** — non-strict evaluation in which arguments are delayed and may be recomputed.

**Call-by-need** — lazy evaluation with sharing/memoization.

**Conformance packet** — frozen allowlisted specification, decisions, vectors, and observation rules supplied to an independent implementer.

**Differential conformance** — comparison of implementations on the same inputs using portable observations only.

**Principal type scheme** — the most general HM type scheme for a term.

**Receiver profile (`A`)** — explicit versioned prior knowledge/capability assumed before measured transmission.

**Receiver-neutral** — not dependent on undeclared terrestrial implementation conventions; not equivalent to prior-free.

**`SB | A`** — inseparable transmitted specification/bootstrap segment counted once.

**Weak-head normal form (WHNF)** — evaluation far enough to reveal the outer value/function/constructor.

---

# Bibliography

1. de Bruijn, N. G. (1972). *Lambda calculus notation with nameless dummies...* Indagationes Mathematicae, 75(5), 381–392. `[SRC-0001]`
2. Tromp, J. *Binary Lambda Calculus.* `[SRC-0002]`
3. Milner, R. (1978). *A Theory of Type Polymorphism in Programming.* JCSS 17(3), 348–375. `[SRC-0003]`
4. Damas, L.; Milner, R. (1982). *Principal Type-Schemes for Functional Programs.* POPL. `[SRC-0004]`
5. Plotkin, G. D. (1977). *LCF Considered as a Programming Language.* TCS 5(3), 223–255. `[SRC-0005]`
6. Elias, P. (1975). *Universal codeword sets and representations of the integers.* IEEE TIT 21(2), 194–203. `[SRC-0006]`
7. Wells, J. B. (1999). *Typability and type checking in System F are equivalent and undecidable.* APAL 98, 111–156. `[SRC-0007]`
8. Schönfinkel, M. (1924). *Über die Bausteine der mathematischen Logik.* `[SRC-0009]`
9. Plotkin, G. D. (1975). *Call-by-name, call-by-value and the lambda-calculus.* TCS 1(2), 125–159. `[SRC-0011]`
10. Launchbury, J. (1993). *A Natural Semantics for Lazy Evaluation.* POPL. `[SRC-0012]`
11. Sestoft, P. (1997). *Deriving a lazy abstract machine.* JFP 7(3), 231–264. `[SRC-0013]`
12. Barker, C. (2001). *Iota and Jot: the simplest languages?* `[SRC-0014]`
13. W3C WebAssembly Working Group. *WebAssembly Core Specification.* `[SRC-0008]`
14. The Go Project. *The Go Programming Language Specification.* `[SRC-0010]`
15. Shannon, C. E. (1948). *A Mathematical Theory of Communication.* `[SRC-0015]`
16. Kolmogorov, A. N. (1965). *Three approaches to the definition of the concept “quantity of information”.* `[SRC-0016]`
17. Chaitin, G. J. (1975). *A Theory of Program Size Formally Identical to Information Theory.* JACM 22(3), 329–340. `[SRC-0017]`

---

# Maintenance rule

Per ADR-0012, future reproducible measurements, independent conformance results, formal counterexamples, stage-level conclusions, or changes to `S/B/P/C` accounting must update this canonical manuscript and its Russian mirror unless a pull request explicitly documents why no research-text change is required.
