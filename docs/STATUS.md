# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Current state:** `Stage 4 — Complete; Stage 5 — Planned, not started`  
**Living research dissertation:** `docs/RESEARCH-DISSERTATION.md` / `docs/RESEARCH-DISSERTATION.ru.md` (ADR-0012)

## Completed milestones

- Stage 0 — specification/process/ADR baseline — Complete.
- Research source registry — Complete.
- Stage 1 — canonical wire foundation — Complete by PR #3, merge `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`.
- Stage 2 — static validation and principal HM type inference — Complete by PR #4, merge `cefe889d90a275897de31aa23c4b9742a388ec8f`.
- Stage 3 — dynamic semantics and reference evaluator — Complete by PR #5, merge `166cdc03282ea500263fdca7185f006f9b17a702`.
- Stage 4 — empirical validation and benchmarking — Complete by PR #6, squash merge `ebffde6c8669f65dfcba98d31d261d59b48d4dd0`.

## Stage 4 — Complete

Stage 4 is recorded in `docs/STAGE-4.md`; the research conclusions are synthesized in the living dissertation and ADR-0011.

The final PR head was:

```text
871d0bc44dbf18854d5e58b15191799b11b834af
```

It passed clean-checkout GitHub Actions run:

```text
35377200520  success
```

There were no open review threads or PR comments at the merge gate. The PR was mergeable and was squash-merged only after the full current head, including the dissertation/governance additions, had passed CI.

### Final Stage 4 evidence snapshot

Frozen accepted corpus v0.3:

```text
programs   17
wire_bits  1371
ast_nodes  345
```

Exact wire attribution:

```text
Prim  460 bits  33.6%
Var   286 bits  20.9%
App   264 bits  19.3%
Nat   244 bits  17.8%
Lam    84 bits   6.1%
Let    33 bits   2.4%
```

Important measured results:

- `Let` has a real payload/reuse-dependent break-even rather than being universally beneficial or wasteful.
- direct `Nat` strongly outperforms the tested repeated-`succ` construction; `Nat(255)` is 21 bits versus 2300 bits for the tested chain.
- the experimental principal-root-type envelope adds 134 bits to 1371 term bits, `+9.77% Delta P`; it does not establish a bootstrap saving.
- on the identical pure-lambda subset, BLC is 30 bits versus NEX 37 bits; no global NEX-over-BLC claim is supported.
- the selected tiny postfix structural baseline is 1529 bits versus NEX 1371 bits on full v0.3, but it reuses NEX numeric/primitive assumptions.
- experimental call-by-need preserves the same observable WHNF on all 17 accepted programs and reduces Go-reference transitions from 226151 to 2484 in aggregate (`98.90%`), but this is runtime/reference evidence, not transmission-cost evidence.
- exact program cost `P` is measurable; receiver-neutral `S` and especially bootstrap `B` remain unresolved, therefore total `C = S + B + P` is not yet numerically defensible.

### Stage 4 decision gate

ADR-0011 records the evidence-supported decisions:

- keep NEX-1 v0.1 stable;
- keep direct `Nat` and `Let`;
- keep erased HM for v0.1 while the total-cost typing comparison remains deferred;
- keep weak call-by-name normative and allow observationally equivalent call-by-need optimization;
- prioritize primitive-reference/profile encoding only as future compactness research, not as an immediate v0.1 change;
- make no global minimality/superiority claim;
- do not substitute host-source size for bootstrap `B`.

ADR-0012 additionally established the living English/Russian dissertation and the mandatory research-synthesis checkpoint for future material evidence.

## Remaining project-wide unknowns after Stage 4

The highest-value unresolved evidence is now:

1. **independent reconstructability** — there is still only one complete reference implementation, so specification/Go co-development may hide ambiguities;
2. **receiver-neutral bootstrap** — no accepted transmitted artifact yet defines/measures `B`;
3. **receiver-neutral specification cost** — Markdown byte size is not `S`;
4. broader-corpus generalization of Stage 4 constructor distributions;
5. formal proof of selected codec/type/evaluator properties;
6. independent total-cost comparisons under common receiver assumptions.

## Stage 5 — Planned; not started

The accepted planning document is `docs/STAGE-5.md`.

Working title:

> **Independent reconstruction and receiver-neutral bootstrap**

Stage 5 is intentionally an evidence stage, not a NEX-1 v0.2 redesign stage.

The plan is split into:

```text
5.0 independence protocol
5.1 conformance packet completeness audit
5.2 independent wire implementation
5.3 independent static semantics
5.4 independent dynamic semantics
5.5 differential conformance after the independence checkpoint
5.6 specification ambiguity audit / conformance hardening
5.7 receiver-assumption model for bootstrap
5.8 first measurable bootstrap candidate
5.9 research decision gate
```

The second implementation must be built from a frozen conformance/specification packet rather than by translating `reference/go`. Direct comparison against Go is postponed until the independent implementation reaches a declared freeze checkpoint.

For bootstrap accounting, Stage 5 introduces the principle that any measured bootstrap value must be conditional on explicit receiver assumptions:

```text
B | A
```

Unknown or undeclared assumptions must not disappear into an apparently exact bit count.

## Stage 5 starting gate

Do **not** start Stage 5 implementation merely because this plan exists.

Before coding the second implementation:

1. review `docs/STAGE-5.md`;
2. accept the independence protocol requirements;
3. choose the independent implementation language/toolchain and record the choice if research-significant;
4. generate/freeze the conformance packet;
5. only then begin Stage 5.2.

No NEX-1 v0.2 wire redesign, new Core primitive, system profile, production frontend, native backend, or self-hosting claim should begin before the Stage 5 evidence gate permits it.
