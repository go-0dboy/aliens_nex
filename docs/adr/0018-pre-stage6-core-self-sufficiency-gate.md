# ADR-0018: Require a pre-Stage-6 NEX Core self-sufficiency gate

- **Status:** Accepted
- **Date:** 2026-09-19

## Context

Stages 0–5 established and empirically validated the NEX-1 v0.1 Core on the recorded evidence surface. ADR-0015 closed Stage 5 with a negative complete-bootstrap result rather than leaving the historical experiment open indefinitely. ADR-0017 then defined Stage 6 as a separate teaching/bootstrap protocol over the stable Core.

A remaining architectural question became explicit before Stage 6 execution: the project has not yet demonstrated that NEX-1 v0.1 can express a complete implementation of its own portable wire, static, and dynamic semantics. The project vocabulary already defines **self-hosting** as a state in which a NEX implementation can process its own implementation expressed in NEX or in a NEX-hosted toolchain.

Computational universality alone is not sufficient evidence for this project. A theoretical encoding may exist while the exact v0.1 type discipline, data representation, or primitive basis makes a complete self-implementation impractical or exposes a genuine missing Core capability. Conversely, implementation inconvenience alone is not evidence that the Core must change.

Starting receiver teaching before testing this question would risk teaching a target whose practical self-sufficiency has not been exercised.

## Decision drivers

- Preserve the completed historical results of Stage 5.
- Keep Stage 6 planned and its teaching/Core separation intact.
- Test the existing NEX-1 v0.1 Core before changing it.
- Prefer executable evidence over an appeal to universality.
- Detect genuine Core limitations before teaching work depends on them.
- Avoid importing a CPU, ABI, native backend, host runtime, strings, byte arrays, or another hidden language merely to claim self-hosting.
- Keep every stronger claim tied to a concrete artifact and reproducible test.

## Decision

Introduce a **post-Stage-5 Core self-sufficiency extension**, numbered 5.10–5.20, before Stage 6 is activated.

This extension does **not** reopen or rewrite Stage 5.0–5.9. Their artifacts, measurements, negative bootstrap result, and ADR-0015 remain historical evidence.

Stage 6 remains **Planned**. ADR-0017 remains Accepted. Its teaching/bootstrap architecture is not superseded.

The pre-Stage-6 extension will attempt to construct a canonical NEX-1 program (or explicitly versioned family of canonical NEX-1 programs) that implements the following portable contracts using only NEX-1 v0.1 Core semantics:

```text
canonical-bit representation <-> encoded NEX term
encoded NEX term -> scope/primitive validation
encoded NEX term -> principal type or portable static error
encoded NEX term -> portable weak-head observation or resource refusal
```

The implementation must ultimately be integrated into a NEX-in-NEX toolchain `I` and tested on its own canonical representation.

### Required evidence before a positive self-sufficiency claim

At minimum:

1. finite internal representations for bits, terms, types, schemes, substitutions/environments, errors, and portable observations are specified without adding Core features;
2. NEX-written canonical encode/decode exists and agrees with the normative wire contract;
3. NEX-written scope and primitive validation exists;
4. NEX-written rank-1 HM inference exists, including occurs check and `Let` generalization;
5. NEX-written weak call-by-name evaluation exists for primitive IDs `0..10`;
6. the integrated implementation itself is a canonical, closed, well-typed NEX program;
7. self-processing checks include at least decode/encode, static validation, and type inference over `code(I)`;
8. direct Go, direct Python, NEX-in-NEX-on-Go, and NEX-in-NEX-on-Python agree on a frozen portable test surface;
9. function-valued observations are strengthened through application contexts where applicable;
10. resource refusal is reported separately from invalidity and from any claim of divergence.

A native compiler such as `NEX -> x86` is **not** required by this gate. That would introduce target-specific ISA/ABI/memory assumptions outside the architecture-neutral Core. The relevant first claim is a self-implementation/self-interpreter of the exact NEX-1 semantics.

### Core change rule

During 5.10–5.20, difficulty is evidence to record, not permission to edit the language.

The extension MUST NOT add merely for implementation convenience:

- new NEX-1 term constructors;
- new Core primitive IDs;
- recursive types;
- mutable memory;
- bit/byte/string host objects;
- incompatible wire changes;
- host callbacks hidden behind a NEX primitive;
- native backend assumptions.

If reproducible evidence shows that the exact v0.1 Core prevents a required construction, the result is classified as a **Core limitation discovered**. Any language change then requires a separate successor-Core ADR/version and invalidates no historical v0.1 evidence.

## Work sequence

The extension is defined in `docs/STAGE-5-EXTENSION.md`:

```text
5.10 contract and gate
5.11 NEX-in-NEX meta-representation
5.12 self wire codec
5.13 self structural validation
5.14 self HM type inference
5.15 self evaluator
5.16 integrated NEX-in-NEX toolchain
5.17 self-processing
5.18 bounded/differential validation
5.19 supporting metatheory
5.20 pre-Stage-6 decision gate
```

## Decision gate outcomes

Stage 5.20 must classify the result as one of:

- `supported` — complete self-implementation and required checks succeeded on the declared evidence surface;
- `supported_but_impractical` — construction exists but measured size/resource burden is problematic;
- `core_limitation_discovered` — a required construction is blocked by a demonstrated Core limitation;
- `inconclusive` — the experiment does not justify either a positive self-sufficiency claim or a Core redesign.

Only a positive outcome allows Stage 6 to move from Planned to Active without another architectural decision. A limitation outcome requires a successor-Core decision first. An inconclusive outcome requires an explicit decision about whether and under what weaker claim Stage 6 may proceed.

## Accepted consequences

- Stage 6 is intentionally delayed, not discarded.
- ADR-0017's separation between teaching representation and canonical Core remains valid.
- NEX-1 v0.1 remains unchanged while the extension tests it.
- A self-hosting claim cannot be inferred from universality alone.
- A failed or expensive attempt remains a useful research result.
- Host Go/Python implementations remain controls and execution substrates for the NEX program, not hidden components of the NEX-in-NEX implementation.

## Alternatives considered

### Start Stage 6 immediately

Deferred. Teaching work remains valuable, but the project should first exercise whether the stable target can implement its own portable semantics.

### Reopen historical Stage 5

Rejected. ADR-0015 explicitly closed Stage 5 with a bounded negative bootstrap result. The new construction program is a later extension and must remain historically distinguishable.

### Accept theoretical universality as sufficient

Rejected. It would not expose representation/type-system friction and would provide no concrete self-processing artifact.

### Require a native-code self-compiler

Rejected for this gate. Native compilation requires a target machine/profile and answers a different question from architecture-neutral Core self-sufficiency.

### Redesign NEX first to make self-hosting convenient

Rejected. The existing Core must be tested before evidence can justify a successor design.

## Evidence and references

This decision is grounded in the existing project artifacts rather than a new external theorem:

- `docs/DOMAIN.md` definitions of Bootstrap and Self-hosting;
- `docs/STAGE-5.md` and ADR-0015 negative bootstrap result;
- ADR-0016 research-claim discipline;
- ADR-0017 teaching/Core separation;
- `docs/TESTING.md` bounded-exhaustive and formal-metatheory requirements;
- `docs/WORKFLOW.md` evidence-gated development process.

## Follow-up validation

- freeze a versioned 5.11 meta-representation contract;
- validate that it depends only on existing v0.1 Core capabilities;
- implement each subsequent layer failure-first;
- preserve host controls and portable comparisons;
- update `docs/STATUS.md` after each evidence checkpoint;
- update both dissertation versions in this workstream when ADR-0012's research-synthesis trigger is reached, and before the 5.20 gate is closed.
