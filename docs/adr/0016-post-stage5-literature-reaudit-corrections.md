# ADR-0016: Correct research claims after the post-Stage-5 literature re-audit

**Status:** Accepted  
**Date:** 2026-09-19

## Context

After Stages 0–5 were closed, the project re-audited its design rationale, empirical conclusions, receiver-assumption model, and supporting literature. The re-audit found no defect that invalidates NEX-1 v0.1 wire, static, or dynamic semantics, but it found several places where rationale, evidence wording, or receiver assumptions were too strong.

The corrections in this ADR are methodological and documentary. They do not change the NEX-1 v0.1 term grammar, primitive table, wire encoding, HM inference rules, or weak call-by-name semantics.

The project objective is **not to establish historical novelty**. Related work is examined because it contains relevant solutions, assumptions, failure modes, and teaching strategies for the actual objective: transmitting a computational system that an unknown receiver can learn well enough to decode, type-check, execute, and eventually program.

## Decisions

### 1. Treat `minimal` as an unproven aspiration, not an established property

The project has not proved global minimality under program size, specification size, bootstrap size, or total transmitted information. Public research claims therefore use **compact** or **small experimental core** rather than presenting NEX as a proven minimal language.

Historical occurrences of `minimal` in the v0.1 specification are interpreted as a design aspiration meaning deliberately small, not as an optimality theorem.

### 2. Correct the SK/SKI typing rationale

ADR-0002's rejection of pure SKI remains a v0.1 engineering/design decision, but static typing is not a valid reason to imply that combinatory logic is intrinsically unsuitable. Hindley's 1969 principal-type-scheme result for combinatory logic [SRC-0018] shows that typed combinatory systems are a legitimate competitor.

The retained rationale is instead:

- eliminating binders can enlarge transmitted programs under a chosen translation;
- NEX wants direct `Let`, natural literals, and typed data operations;
- total transmitted burden must be measured rather than inferred from basis size alone.

### 3. Make total-cost claims lengths of concrete transmitted objects

`C = S + B + P` remains useful conceptual shorthand, but it is not an unconditional machine-free information scalar.

Exact claims are conditioned on an explicit receiver profile and serialization. The preferred form is:

```text
C | A = |M_A|
```

where `M_A` is the exact transmitted object under declared prior `A`.

If the object is defensibly partitioned:

```text
C | A = (S | A) + (B | A,S) + (P | A,S,B)
```

If specification and executable bootstrap are inseparable:

```text
C | A = (SB | A) + (P | A,SB)
```

This refines, rather than rejects, the Stage 4–5 ledger and is consistent with algorithmic-description and MDL literature [SRC-0016, SRC-0017, SRC-0019].

### 4. Refine receiver assumptions: `A1` no longer hides a recursive rule language

`assumptions-v0.1.json` remains frozen as historical Stage 5 evidence. Its `M_RULES` atom was later judged too strong for a generic mathematical prior because interpreting recursively defined executable rules already presupposes syntax and operational conventions.

`assumptions-v0.2.json` is therefore the current model:

```text
A0       exact digital frame prior
A1       A0 + elementary naturals and finite-sequence mathematics
A1(R)    A1 + one exact formal rule calculus R and binary serialization
A2(U)    A1 + one exact universal machine U and input framing
A_host(H) engineering control only
```

`A1(R)` and `A2(U)` are separate stronger branches; neither is silently treated as a free consequence of elementary mathematics.

The mathematical atoms in `A1` are themselves an experimental assumption, not a claim that mathematics must be represented identically by every extraterrestrial intelligence [SRC-0029].

### 5. Narrow the interpretation of Stage 5 differential evidence

The `942/942` result remains valid, but the cases are not 942 independently designed semantic programs. The deterministic harness contains:

```text
17   frozen corpus programs
325  generated valid cases = 25 numeric parameterizations x 13 AST templates
100  generated static-error cases = 25 parameterizations x 4 error families
500  generated wire cases with randomized term shapes, tested at wire level
```

The accepted statement is:

> Stage 5 provides strong **differential-conformance evidence of reconstructability on the tested surface**.

It does not prove semantic correctness, specification completeness, or independence of failures. Knight–Leveson [SRC-0024] and differential-testing literature [SRC-0027] motivate this caution.

The portable WHNF observation `Function` is intentionally coarse: it hides whether the implementation uses a lambda closure or an unsaturated primitive value. Future exhaustive tests should therefore exercise returned functions through application contexts rather than relying only on the top-level `Function` label.

### 6. Do not inherit a type-safety theorem from HM literature automatically

Milner and Damas–Milner justify the selected inference discipline, but NEX-specific primitives, forcing rules, and `fix` require a NEX-specific metatheory before preservation/progress may be claimed as a theorem.

Current implementations and two-implementation conformance are strong empirical evidence, not a formal proof of type safety.

If mutable references/effects are introduced later, v0.1 `Let` generalization MUST be revisited. Tofte's result [SRC-0025] shows that unrestricted HM polymorphism is not sound in the presence of create/update references.

### 7. Keep the call-by-need result but name the metric exactly

The Stage 4 value `226151 -> 2484` is a reduction in the project-defined Go evaluator **transition counter**, not a claim of 98.90% reduction in wall-clock time, CPU instructions, allocations, memory, or bootstrap complexity.

Literature establishes a strong relationship between call-by-need and call-by-name for standard lambda calculi [SRC-0012, SRC-0013, SRC-0023], but NEX's extended primitives still require a NEX-specific equivalence argument for a formal theorem.

### 8. Use interstellar-language prior work as design evidence, not as a novelty gate

The maintained comparison must include at least:

- Freudenthal's Lincos [SRC-0020];
- CosmicOS and its progressive use of programs/simulations [SRC-0021];
- Lingua Cosmica work using constructive type theory [SRC-0022];
- DeVito–Oehrle's science-based language and explicit prior-knowledge reasoning [SRC-0028];
- exosemiotic criticism of assuming mathematics/science to be universally represented [SRC-0029].

The project does not need to be historically first to succeed. The comparison is used to answer engineering questions:

- how can meaning be taught through examples?;
- which prior assumptions are defensible and how strongly do they reduce the message?;
- can types reduce ambiguity and serve as validation information?;
- how can programs become part of the teaching process?;
- how can the receiver check that it reconstructed the intended computation?

The detailed comparison is maintained in `docs/RELATED-WORK.md` and its Russian mirror.

### 9. Keep Stage 4 measurements local to their frozen corpora and baselines

The 17-program corpus remains useful but small and hand-designed. Constructor shares, `Let` break-even observations, and aggregate evaluator counts are corpus-specific.

`Prim = 460 bits` does not by itself show that shortening the `Prim` constructor prefix is the right optimization. The current constructor prefixes have Kraft sum 1, so a shorter top-level constructor code requires compensating changes elsewhere. Future primitive experiments should split constructor-prefix cost from primitive-ID payload cost.

### 10. Separate the stable Core from the future teaching/bootstrap protocol

The related-work comparison suggests that NEX currently has a strong **target computational system** but not yet a dedicated **teaching sequence** that establishes its meaning for an unknown receiver.

Future work should therefore treat the architecture as:

```text
receiver prior A
    -> NEX teaching/bootstrap message T
    -> reconstructed NEX-1 competence
    -> conformance/self-test
    -> canonical NEX programs P
```

The teaching layer may use redundant or pedagogical representations while the final NEX-1 Core remains canonical and compact. The Core MUST NOT be redesigned merely because its canonical de Bruijn/wire representation is not the easiest first lesson.

### 11. Strengthen supporting evidence before incompatible Core redesign

The teaching/bootstrap stage should be accompanied by supporting evidence work:

1. NEX-specific preservation/progress/canonical-form metatheory;
2. a formal or mechanized argument that an allowed call-by-need implementation preserves NEX Core observations;
3. bounded exhaustive enumeration of small well-scoped/well-typed terms across independent implementations, including function application contexts;
4. hold-out and externally specified workload families in addition to the design corpus;
5. a finite machine-readable teaching/bootstrap artifact whose transmitted bits can be measured exactly.

These are higher-value research tasks than immediately changing the NEX-1 v0.1 wire format.

## Consequences

- Stages 0–5 remain complete; their exact recorded measurements remain valid within documented conditions.
- NEX-1 v0.1 normative semantics are unchanged.
- Some earlier motivations and prose claims are narrowed.
- The receiver-assumption taxonomy advances from historical v0.1 to current v0.2 without rewriting Stage 5 history.
- Related work is used to improve teachability and bootstrap design, not to create an artificial novelty requirement.
- The next stage should treat teachability as a first-class research object while keeping the Core stable.

## Evidence

This ADR is based on:

- `docs/RESEARCH-AUDIT-2026-09-19.md`;
- `docs/RESEARCH-AUDIT-2026-09-19.ru.md`;
- `docs/RELATED-WORK.md`;
- `docs/RELATED-WORK.ru.md`;
- the source registry `docs/SOURCES.md`.
