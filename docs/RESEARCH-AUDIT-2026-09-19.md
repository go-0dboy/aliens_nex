# Post-Stage-5 Research Audit — 2026-09-19

**Scope:** Stages 0–5, current NEX-1 v0.1 specification, empirical conclusions, independent-reconstruction claims, receiver-assumption model, and related literature.  
**Normative effect:** none on NEX-1 v0.1 semantics.  
**Decision record:** ADR-0016.

## 1. Executive conclusion

The re-audit found **no error that invalidates NEX-1 v0.1, the recorded Stage 1–5 measurements, or the negative Stage 5 bootstrap result**.

It did find:

1. one factual/conceptual error in earlier design rationale: combinatory logic was treated too dismissively with respect to static typing;
2. two methodology problems requiring correction: total description cost was sometimes phrased too much like an unconditional information scalar, and Stage 5's original `A1` prior hid too much computational interpretation;
3. several places where evidence wording was stronger than the experiment warranted, especially around `942/942` independent reconstruction and the `98.90%` call-by-need transition reduction;
4. a substantial related-work gap: Lincos, CosmicOS, and Lingua Cosmica were missing from the core research narrative;
5. open proof/evidence gaps: NEX-specific type soundness, NEX-specific call-by-need equivalence, broader workloads, and an actual dependency-closed bootstrap artifact.

The corrections narrow claims; they do not require a v0.1 wire/Core redesign.

---

## 2. Literature added by this audit

The audit compared NEX against additional primary or author-maintained sources now registered in `docs/SOURCES.md`:

- Hindley (1969) on principal type schemes in combinatory logic — SRC-0018;
- Rissanen (1978) on shortest-description/model cost — SRC-0019;
- Freudenthal's Lincos (1960) — SRC-0020;
- Fitzpatrick's CosmicOS — SRC-0021;
- Ollongren & Vakoch on constructive type theory for Lingua Cosmica — SRC-0022;
- Maraist, Odersky & Wadler on call-by-need observational equivalence — SRC-0023;
- Knight & Leveson on correlated failures of independently developed versions — SRC-0024;
- Tofte on polymorphic references — SRC-0025;
- Wright & Felleisen on type-soundness proof methodology — SRC-0026;
- McKeeman on differential testing — SRC-0027.

These sources change the interpretation of some NEX claims, but not the current Core semantics.

---

# 3. Stage-by-stage audit

## Stage 0 — research framing and architecture

### What remains sound

The central engineering question is legitimate: a program payload cannot be judged in isolation when its interpretation requires a specification, interpreter, abstract machine, or other prior agreement. The project's refusal to equate host source size with receiver-neutral bootstrap remains a strong methodological decision.

The decomposition

```text
C = S + B + P
```

is useful as a ledger of transmitted responsibilities.

### Correction: not an unconditional information scalar

Kolmogorov/Chaitin-style description length and MDL-style reasoning are relative to a description method, model, or computational interpretation. Therefore exact NEX claims are now framed as lengths of a concrete transmitted object under explicit receiver assumptions:

```text
C | A = |M_A|
```

A decomposed form is valid only when the exact object can be partitioned without double counting:

```text
C | A = (S | A) + (B | A,S) + (P | A,S,B)
```

or, when specification and bootstrap are inseparable:

```text
C | A = (SB | A) + (P | A,SB)
```

The old formula is retained as conceptual shorthand, not as a machine-free absolute quantity.

### Correction: novelty claim

Lincos predates NEX as a formal language for extraterrestrial communication. CosmicOS explicitly introduces programs and simulations after bootstrapping mathematics and logic. Lingua Cosmica research has used constructive type theory in interstellar-message design.

Therefore NEX must **not** claim novelty for:

- inventing a formal language for aliens;
- using executable/program-like constructs in an interstellar message;
- introducing types into interstellar-message research.

The narrower candidate contribution is the combination of compact typed binary representation, exact program accounting, explicit receiver-conditioned bootstrap accounting, reproducible comparative experiments, negative-result preservation, and blind independent reconstruction.

### Terminology correction

`Minimal` is not established. The research manuscript and project overview now prefer **compact** or **small experimental core**. Any historical `minimal` wording in the v0.1 specification is a design aspiration, not an optimality theorem.

**Stage 0 audit result:** valid framing after terminology/accounting/related-work corrections.

---

## Stage 1 — canonical binary wire format

### What remains sound

The recursive wire grammar is deterministic and self-delimiting when combined with `U(n)`. The six top-level constructor prefixes have lengths:

```text
2, 2, 2, 3, 4, 4
```

Their Kraft sum is exactly:

```text
3 * 2^-2 + 2^-3 + 2 * 2^-4 = 1
```

so the top-level constructor prefix space is fully allocated. This is consistent with a complete prefix code.

`U(n)` remains correctly defined as Elias gamma coding of `n+1`; direct arbitrary-precision naturals are therefore self-delimiting.

### New implication for optimization

Because the constructor-prefix Kraft sum is already 1, a future attempt to shorten the `Prim` **constructor prefix** cannot be free: another constructor or the grammar factorization must change. Stage 4's `Prim = 460 bits` observation therefore does not by itself identify the top-level `Prim` prefix as the dominant inefficiency.

Future primitive experiments should report at least:

```text
Prim constructor-prefix bits
primitive-ID U(p) bits
```

separately.

**Stage 1 audit result:** no semantic/wire error found; optimization interpretation refined.

---

## Stage 2 — scope and Hindley–Milner inference

### What remains sound

Rank-1 HM inference with let-generalization, fresh instantiation, unification, and occurs check is well grounded in Milner/Damas–Milner. The current pure Core has no mutable references, so the ordinary HM generalization discipline is a reasonable v0.1 choice.

Typed `fix : forall a. (a -> a) -> a` permits divergence but does not by itself invalidate static typing. The design is consistent with the tradition of typed recursive calculi such as PCF/LCF.

### Corrected SK/SKI rationale

Earlier ADR-0002 wording could be read as if SKI/combinatory logic did not naturally support the project's static-typing objective. That is incorrect as a general claim. Hindley (1969) established principal type-scheme results directly for combinatory logic.

The v0.1 decision not to use pure SKI remains defensible for different reasons:

- bracket abstraction can enlarge transmitted terms;
- NEX wants direct `Let`, naturals, and typed data operations;
- basis size alone does not determine `S+B+P`.

### Open proof gap

Milner's soundness theorem is not automatically a theorem about NEX's exact language. NEX adds its own primitive table, product/sum forcing behavior, natural operations, and `fix` semantics.

The repository currently has strong executable evidence but no NEX-specific proof of:

```text
preservation / subject reduction
progress or an appropriate partial-computation safety theorem
canonical forms for the Core values
```

This is an evidence gap, not evidence of unsoundness.

### Future effects warning

If a future profile adds mutable references/state, current unrestricted pure-Core `Let` generalization must not simply be reused. Tofte's polymorphic-reference result shows why HM polymorphism and mutable reference creation/update need modified restrictions.

**Stage 2 audit result:** implementation/design remains credible for the pure Core; one rationale corrected; formal type-safety proof still missing.

---

## Stage 3 — weak call-by-name dynamic semantics

### What remains sound

The normative strategy is internally coherent: no reduction under `Lam`, delayed function arguments and `Let` values, selective primitive forcing, lazy pair/sum payloads, and explicit recursion through `fix`.

The Go evaluator implements this model with non-memoizing thunks. The independent Python evaluator reconstructs the same portable observations on the tested surface.

### Call-by-need interpretation

Established call-by-need calculi provide strong theoretical precedent that sharing can preserve call-by-name observations for standard lambda calculi. The NEX experiment is therefore theoretically motivated.

However, a published theorem for a standard lambda calculus does not automatically prove equivalence for NEX's exact `fix`, natural, product, sum, and primitive-forcing rules.

The correct current claim is:

> the experimental call-by-need implementation preserved all tested NEX Core observations.

A NEX-specific equivalence proof remains future work.

**Stage 3 audit result:** no dynamic-semantics defect found; formal equivalence remains open.

---

## Stage 4 — empirical validation and benchmarking

### Exact measurements remain valid

The recorded values are reproducible properties of the frozen artifacts:

```text
17 programs
345 AST nodes
1371 canonical NEX bits
```

and constructor attribution:

```text
Prim 460
Var  286
App  264
Nat  244
Lam   84
Let   33
```

The direct-`Nat`, `Let`, hybrid-root-type, BLC, Jot-translation, structural-stack, and evaluator-strategy numbers remain valid within their documented comparisons.

### Corpus limitation

The corpus is small and hand-designed. Freezing it before optimization protects against changing the benchmark after seeing a result, but does not remove selection bias from the initial workload choice.

Therefore constructor shares and aggregate runtime measurements are **corpus properties**, not language-wide frequency estimates.

Future empirical work should separate:

```text
design/training corpus
hold-out corpus
externally specified tasks
generated or bounded-exhaustive typed terms
```

### Direct `Nat`

`Nat(255)=21 bits` versus the tested repeated-`succ` representation at 2300 bits is correct and strongly supports keeping direct literals against that baseline. It does not establish Elias gamma or `Nat` as globally optimal against all integer coding schemes.

### `Let`

The measured break-even remains valid. It supports retaining `Let`, but does not imply every local `Let` occurrence is smaller than duplication.

### BLC and Jot

The BLC result remains especially important because it is inconvenient evidence preserved by the project:

```text
NEX 37 bits
BLC 30 bits
```

on the identical three-program pure-lambda subset. No global winner follows.

The Jot number remains only the result of one deterministic lambda -> SK -> Jot translation; it is not a shortest-Jot comparison.

### Call-by-need metric clarification

The recorded change

```text
226151 -> 2484
```

is a reduction in the project's instrumented Go evaluator transition counter. It is **not** a measurement of wall-clock speed, CPU instructions, allocations, memory use, or bootstrap size. The 98.90% figure must be described as transition-counter reduction.

**Stage 4 audit result:** measurements stand; generalization and metric wording tightened.

---

## Stage 5 — independent reconstruction and bootstrap accounting

### Independence protocol remains strong

Freezing the packet, isolating the second implementer from `reference/go`, freezing the Python artifact before comparison, and comparing only portable observations remain good research controls.

The final result remains exactly:

```text
942 portable matches
0 semantic mismatches
0 resource asymmetries
```

### Corrected interpretation of 942 cases

Inspection of `stage5/differential/run.py` shows the exact composition:

```text
17   frozen corpus programs
325  valid cases: 25 parameter sets x 13 fixed AST templates
100  static-error cases: 25 parameter sets x 4 fixed error families
500  randomized term shapes tested at wire level
```

Thus `942/942` is a valid count of portable observations, but not 942 independently designed semantic workloads.

The accepted wording is now:

> strong differential-conformance evidence of reconstructability on the tested surface.

It is not a proof that the specification is complete or that both implementations are semantically correct. Knight–Leveson's multiversion experiment is a useful warning that independently developed versions can still share correlated faults; differential testing likewise cannot reveal an error common to all compared implementations.

### Receiver-assumption correction

The historical `assumptions-v0.1.json` placed the ability to interpret deterministic recursive rules inside `A1`. On re-audit this was judged too strong: an executable recursive-rule language already requires exact syntax and operational conventions.

The current model is `assumptions-v0.2.json`:

```text
A0       exact binary-frame prior
A1       elementary naturals + finite sequences only
A1(R)    A1 + exact formal rule calculus R
A2(U)    A1 + exact universal machine U and framing
A_host(H) non-neutral terrestrial host
```

`A1(R)` and `A2(U)` are distinct branches, not a hidden strength ordering.

### Negative bootstrap result remains valid

Stage 5.8 accepted zero complete receiver-neutral bootstrap candidates. The audit strengthens rather than weakens that conclusion: the original `A1` rule candidate was indeed missing the very formal language whose interpretation it implicitly needed.

Python/Go source sizes remain engineering controls and not `B`.

**Stage 5 audit result:** experiment remains useful; evidence wording and prior taxonomy corrected; negative bootstrap conclusion preserved.

---

# 4. Cross-stage findings

## No invalidating error found

No reviewed evidence requires changing:

```text
Term ::= Var | Lam | App | Let | Nat | Prim
Core primitive IDs 0..10
zero-based de Bruijn binding
U(n) = gamma(n+1)
canonical v0.1 wire prefixes
rank-1 pure-Core HM inference
weak call-by-name normative semantics
Stage 4 frozen measurements
Stage 5 frozen Python checkpoint
Stage 5 942/942 differential result
Stage 5 negative bootstrap result
```

## Claims that were corrected

The following are no longer acceptable without qualification:

```text
NEX is minimal
SKI is unsuitable because static typing is unnatural
C is an unconditional information scalar
A1 may freely assume executable recursive-rule interpretation
942/942 proves correctness or specification completeness
98.90% transitions means 98.90% runtime speedup
```

## Claims that remain explicitly unproved

```text
global compactness/minimality
formal NEX type safety
formal NEX CBN <-> call-by-need equivalence
representativeness of the 17-program corpus
complete receiver-neutral B | A
numerical total C | A
NEX superiority over external alternatives
```

---

# 5. Recommended next evidence stage

Before a NEX-1 v0.2 redesign, the audit recommends a formal-and-exhaustive evidence stage with four workstreams:

1. **Metatheory:** preservation, canonical forms, and an appropriate progress/safety theorem for the current pure Core.
2. **Evaluation equivalence:** a NEX-specific proof or mechanized argument that the allowed call-by-need evaluator preserves portable Core observations.
3. **Broader conformance:** bounded exhaustive enumeration of small closed well-scoped/well-typed terms across the independent implementations, plus hold-out/external workload families.
4. **Bootstrap construction:** build one actual dependency-closed artifact under `A1(R)` or `A2(U)` and measure the exact transmitted object.

A primitive-reference or other wire redesign should come after these evidence gaps are addressed, unless a separate experiment is explicitly scoped as exploratory.

---

# 6. Final audit judgment

The Stage 0–5 research program survives the literature re-audit. The strongest parts are the executable wire/static/dynamic contracts, preservation of negative benchmark results, explicit separation of host proxies from bootstrap, blind independent implementation protocol, and refusal to invent a bootstrap number.

The main weaknesses are not hidden implementation failures but **claim calibration and evidence breadth**: prior interstellar-language work was under-cited, combinatory typing was mischaracterized in one rationale, `A1` hid too much computational structure, formal metatheory is absent, and the empirical corpora remain narrow.

These corrections are recorded without rewriting historical experiment artifacts. NEX-1 v0.1 remains the stable experimental object.
