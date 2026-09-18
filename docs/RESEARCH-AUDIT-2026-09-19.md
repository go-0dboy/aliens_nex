# Post-Stage-5 Research Audit — 2026-09-19

**Scope:** Stages 0–5, NEX-1 v0.1, empirical conclusions, independent-reconstruction evidence, receiver assumptions, and relevant literature.  
**Normative effect:** none on NEX-1 v0.1 semantics.  
**Decision record:** ADR-0016.

## 1. Executive conclusion

The re-audit found **no error that invalidates NEX-1 v0.1, the recorded Stage 1–5 measurements, or the negative Stage 5 bootstrap result**.

It did find and correct:

1. one conceptual error in design rationale: combinatory logic was treated too dismissively with respect to static typing;
2. an accounting ambiguity: `C=S+B+P` was sometimes phrased too much like an unconditional information scalar;
3. an over-strong receiver prior: historical `A1` implicitly assumed an executable recursive-rule language;
4. evidence wording stronger than the experiments warranted around `942/942` and the 98.90% call-by-need counter reduction;
5. a related-work gap: Lincos, CosmicOS, Lingua Cosmica, DeVito–Oehrle, and exosemiotic criticism of universal-prior assumptions were missing from the central narrative;
6. open evidence gaps: NEX-specific type soundness, NEX-specific call-by-need equivalence, broader workloads, bounded-exhaustive testing, and a real finite teaching/bootstrap artifact.

These corrections do not require a v0.1 Core redesign.

A further clarification is important: **historical novelty is not a project success criterion**. Related work is examined to improve the design of a system that an unknown receiver can actually learn.

---

## 2. What the literature comparison is for

The project objective is operational:

> construct a formal computational system that an unknown receiver can be taught well enough to decode, type-check, execute, and eventually author programs in it.

Accordingly, previous interstellar-language projects are compared for engineering lessons rather than priority.

The relevant additions to the source registry include:

- Hindley on principal type schemes in combinatory logic — SRC-0018;
- Rissanen on shortest-description/model cost — SRC-0019;
- Freudenthal's Lincos — SRC-0020;
- Fitzpatrick's CosmicOS — SRC-0021;
- Ollongren & Vakoch on Lingua Cosmica/type theory — SRC-0022;
- Maraist, Odersky & Wadler on call-by-need — SRC-0023;
- Knight & Leveson on correlated multiversion failures — SRC-0024;
- Tofte on polymorphic references — SRC-0025;
- Wright & Felleisen on type-soundness proof methodology — SRC-0026;
- McKeeman on differential testing — SRC-0027;
- DeVito & Oehrle on a science-based alien language and prior knowledge — SRC-0028;
- Vakoch on exosemiotic limits of assuming universal mathematics/science — SRC-0029.

The detailed comparison is maintained in `docs/RELATED-WORK.md`.

---

# 3. Stage-by-stage audit

## Stage 0 — framing and architecture

### What remains sound

The central engineering insight is valid: program payload cannot be judged in isolation when its interpretation requires a specification, interpreter, abstract machine, or other prior agreement. The refusal to equate host source size with receiver-neutral bootstrap remains a strong methodological decision.

### Correction: total cost is conditional

The historical shorthand

```text
C = S + B + P
```

remains useful as a ledger, but exact numerical claims are now defined for one concrete transmitted object under an explicit receiver profile:

```text
C | A = |M_A|
```

When roles are separable:

```text
C | A = (S | A) + (B | A,S) + (P | A,S,B)
```

and when specification/bootstrap are inseparable:

```text
C | A = (SB | A) + (P | A,SB)
```

This makes the accounting compatible with description-length literature without pretending there is a privileged machine-free scalar.

### Related-work design lesson

Lincos demonstrates progressive semantic teaching. DeVito–Oehrle demonstrates the importance of explicit prior assumptions. Lingua Cosmica shows how types/formal logic can constrain interpretation. CosmicOS is especially close to the original NEX objective because it progressively introduces mathematics, programs, and simulations.

The main architectural implication is not a claim about novelty. It is that NEX should be viewed as two layers:

```text
teaching/bootstrap message
        -> learned NEX-1 Core
        -> canonical NEX programs
```

The Core is the exact final computational target; the missing layer is the finite teaching sequence that establishes its meaning.

### Terminology correction

`Minimal` is not established. Public research text uses **compact** or **small experimental core** unless a particular minimality claim is explicitly proved.

**Stage 0 result:** framing remains valid after accounting and teaching-layer clarification.

---

## Stage 1 — canonical binary wire format

The recursive wire grammar remains deterministic and self-delimiting when combined with `U(n)`. Constructor-prefix lengths are:

```text
2, 2, 2, 3, 4, 4
```

with Kraft sum:

```text
3 * 2^-2 + 2^-3 + 2 * 2^-4 = 1
```

so the top-level prefix space is fully allocated.

`U(n)` remains correctly defined as Elias gamma coding of `n+1`.

A useful optimization consequence follows: shortening the `Prim` constructor prefix cannot be free. Another code or the grammar factorization must change. Future primitive-cost work should separate:

```text
Prim constructor-prefix bits
primitive-ID U(p) bits
```

**Stage 1 result:** no wire defect found; optimization interpretation refined.

---

## Stage 2 — scope and Hindley–Milner inference

Rank-1 HM inference with `Let` generalization, fresh instantiation, unification, and occurs check remains well motivated for the current pure Core.

Typed `fix : forall a. (a -> a) -> a` permits divergence but does not by itself invalidate type safety.

### Corrected SK/SKI rationale

Combinatory logic is not intrinsically hostile to static typing. Hindley established principal type-scheme results for combinatory logic. Therefore pure SK/SKI remains a legitimate competitor.

The v0.1 decision not to use it is instead justified by representation and language-design trade-offs: bracket abstraction can enlarge terms, NEX wants direct `Let`/naturals/data operations, and basis size alone says nothing about total transmitted cost.

### Open proof gap

Milner's theorem does not automatically prove the exact NEX primitive/evaluation system sound. The project still lacks a NEX-specific proof of:

```text
canonical forms
preservation / subject reduction
an appropriate progress/safety theorem for partial computation
```

This is a proof gap, not evidence of unsoundness.

If future profiles add mutable references/state, the pure-Core `Let` generalization rule must be revisited rather than reused automatically.

**Stage 2 result:** no implementation/design defect found for the pure Core; one rationale corrected; metatheory remains open.

---

## Stage 3 — weak call-by-name semantics

The normative strategy remains coherent: no reduction under `Lam`, delayed arguments and `Let` values, selective primitive forcing, lazy product/sum payloads, and explicit recursion through `fix`.

Call-by-need literature strongly motivates sharing as an implementation technique, but a theorem for a standard lambda calculus is not automatically a theorem for NEX's exact primitives.

The accepted current statement is:

> the experimental call-by-need implementation preserved all tested NEX observations.

A NEX-specific equivalence proof remains future work.

**Stage 3 result:** no dynamic-semantics defect found.

---

## Stage 4 — empirical validation

The recorded frozen-corpus measurements remain valid:

```text
17 programs
345 AST nodes
1371 canonical NEX bits

Prim 460
Var  286
App  264
Nat  244
Lam   84
Let   33
```

They are corpus properties, not frequencies for software in general.

### Direct naturals

`Nat(255)=21 bits` versus the tested repeated-`succ` representation at `2300` bits strongly supports direct literals against that baseline. It does not establish global optimality of gamma coding.

### `Let`

The measured break-even remains valid and supports retaining `Let`; it does not imply that every local use of `Let` is smaller than duplication.

### External baselines

On the shared pure-lambda subset:

```text
NEX 37 bits
BLC 30 bits
```

No global winner follows. The Jot number remains the result of one deterministic translation, not a shortest-program search.

### Call-by-need metric

```text
226151 -> 2484
```

means a 98.90% reduction in the project-defined evaluator transition counter. It is not a measured 98.90% reduction in wall-clock time, CPU work, allocation, memory, or bootstrap size.

**Stage 4 result:** measurements stand; generalization and metric wording tightened.

---

## Stage 5 — independent reconstruction and bootstrap accounting

The independence protocol remains strong: the packet was frozen, the second implementer was isolated from `reference/go`, the Python artifact was content-hash frozen before comparison, and only portable observations were compared.

The result remains exactly:

```text
942 portable matches
0 semantic mismatches
0 resource asymmetries
```

### Correct interpretation of 942 cases

```text
17   frozen corpus programs
325  valid cases = 25 parameter sets x 13 AST templates
100  static-error cases = 25 parameter sets x 4 error families
500  randomized term shapes tested at wire level
```

The accepted wording is:

> strong differential-conformance evidence of reconstructability on the tested surface.

It is not a proof that both implementations are semantically correct or that the specification is complete.

The portable top-level observation `Function` is deliberately coarse: it does not expose whether a function value is represented as a lambda closure or an unsaturated primitive. Future exhaustive testing should therefore include application contexts that exercise returned function behavior.

### Receiver-assumption correction

Historical `assumptions-v0.1.json` put recursive-rule interpretation inside `A1`. The current corrected model is:

```text
A0       exact binary-frame prior
A1       elementary naturals + finite sequences only
A1(R)    A1 + exact formal rule calculus R
A2(U)    A1 + exact universal machine U and framing
A_host(H) non-neutral terrestrial host
```

`A1(R)` and `A2(U)` are separate branches. Even the mathematics in `A1` is an explicit experimental prior rather than an assertion that all extraterrestrial cognition shares one mathematical notation or conceptualization.

### Negative bootstrap result

Stage 5.8 still correctly accepts zero complete receiver-neutral bootstrap candidates. The re-audit strengthens this conclusion: the original `A1` rule candidate was missing the formal calculus it needed.

**Stage 5 result:** the experiment remains useful; evidence wording and prior taxonomy are more precise; the negative bootstrap conclusion stands.

---

# 4. Cross-stage conclusions

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
Stage 5 942/942 result
Stage 5 negative bootstrap result
```

The following statements require qualification and are no longer accepted as unqualified claims:

```text
NEX is globally minimal
SKI is unsuitable because static typing is unnatural
C is an unconditional information scalar
A1 includes a free executable recursive-rule language
942/942 proves correctness or specification completeness
98.90% transition reduction means 98.90% runtime speedup
```

Still open:

```text
formal NEX type safety
formal NEX CBN <-> call-by-need equivalence
representativeness of the 17-program corpus
bounded-exhaustive semantic coverage
complete finite receiver-neutral teaching/bootstrap message
numerical total C | A
```

---

# 5. Recommended next stage

The literature comparison changes the priority of the next stage.

The project already has a precisely defined **target language**. The largest missing component for the original objective is a **teaching/bootstrap message** that takes a receiver from an explicit prior profile to demonstrable NEX competence.

The next stage should therefore investigate:

```text
prior A
  -> finite teaching/bootstrap message T
  -> reconstructed NEX competence
  -> conformance/self-test
  -> canonical NEX programs P
```

Primary workstreams:

1. define a separate teaching layer above the stable NEX-1 Core;
2. design a progressive lesson sequence informed by Lincos and CosmicOS;
3. use typing and conformance examples as semantic constraints and receiver self-tests;
4. define an operational success criterion for “can program in NEX”;
5. produce a finite machine-readable teaching artifact and measure its exact bit length.

Supporting evidence work should continue in parallel:

- NEX-specific metatheory;
- NEX-specific call-by-need equivalence;
- bounded exhaustive cross-implementation testing, including function application contexts;
- hold-out and independently specified workload families.

An incompatible Core redesign should remain deferred unless new evidence directly requires it.

---

# 6. Final judgment

The Stage 0–5 program survives the full literature re-audit. No fundamental language error was found. The strongest features remain the executable wire/static/dynamic contracts, preservation of negative results, explicit receiver-conditioned accounting, blind independent reconstruction, and refusal to invent a bootstrap number.

The largest remaining gap is now clearer: **NEX has an exact computational Core but not yet an exact curriculum that teaches that Core to an unknown receiver.**

That gap, rather than historical novelty, is the appropriate focus of the next stage.
