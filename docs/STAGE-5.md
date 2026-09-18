# Stage 5 — Independent reconstruction and receiver-conditioned bootstrap

**Status:** Complete  
**Completed:** 2026-09-18  
**Post-stage literature clarification:** 2026-09-19, ADR-0016  
**Prerequisite:** Stage 4 complete

## Purpose

Stage 5 tested two questions:

1. can NEX-1 v0.1 be reconstructed from specification/conformance material without translating the Go reference implementation?;
2. can bootstrap cost be made explicit and measurable without hiding a terrestrial runtime, interpreter, or undeclared receiver prior?

Stage 5 did not redesign NEX-1 v0.1.

## 5.0–5.1 — independence protocol and frozen packet

PR #7 established ADR-0013, the allowlisted conformance packet, and a blind implementation boundary. `reference/go` was excluded until the independent checkpoint was frozen.

The packet audit exposed two presentation-level omissions—canonical type-variable rendering and JSON fixture mapping—without changing NEX semantics.

## 5.2–5.6 — independent implementation and differential conformance

A separate Python 3.12 standard-library-only implementation was produced from the frozen packet.

Frozen archive:

```text
nex1-independent-python-v0.1.zip
sha256:783e4186f9a8c024f00a732deae33b547c81ed4d7639c610a1e8bc5997eb3fbe
```

Before Go comparison it passed all packet vectors and 23 independent tests. Post-freeze differential comparison produced:

```text
cases total           942
portable matches      942
semantic mismatches     0
resource asymmetries    0
```

The post-Stage-5 audit records the case composition explicitly:

```text
17   frozen corpus programs
325  valid cases = 25 parameter sets x 13 fixed AST templates
100  static-error cases = 25 parameter sets x 4 fixed error families
500  randomized term shapes tested at wire level
```

Accepted claim:

> strong differential-conformance evidence of reconstructability on the tested surface.

This is not a formal proof of specification completeness or semantic correctness. Independent implementations can share correlated failures, and differential testing cannot expose an error common to every compared implementation [SRC-0024, SRC-0027].

The portable `Function` observation is deliberately coarse. Future exhaustive work should test returned functions through application contexts as well as top-level WHNF labels.

## 5.7 — receiver-assumption model

The historical Stage 5.7 artifact remains frozen:

```text
stage5/receiver-assumptions/assumptions-v0.1.json
```

It introduced the central rule that specification/bootstrap/total cost are conditional on explicit receiver assumptions and that transmitted bits cannot be double-counted.

The post-Stage-5 audit found historical `A1` too strong because it included the ability to interpret recursively defined rules without fixing a rule language. The current corrected taxonomy is:

```text
stage5/receiver-assumptions/assumptions-v0.2.json
```

with:

```text
A0        exact finite ordered binary frame
A1        A0 + elementary naturals / finite-sequence mathematics
A1(R)     A1 + exact formal rule calculus R and binary serialization
A2(U)     A1 + exact universal binary machine U and framing
A_host(H) non-neutral terrestrial host control
```

`A1(R)` and `A2(U)` are separate stronger branches. Even the mathematics in `A1` is an explicitly declared experimental prior rather than a claim about actual extraterrestrial cognition.

Exact accounting is stated as:

```text
C | A = |M_A|
```

for one exact transmitted object `M_A`. When roles are separable:

```text
C | A = (S | A) + (B | A,S) + (P | A,S,B)
```

and when specification/bootstrap are inseparable:

```text
C | A = (SB | A) + (P | A,SB)
```

## 5.8 — bootstrap feasibility audit

Machine-readable historical audit:

```text
stage5/bootstrap/attempt-v0.1.json
```

Validation:

```text
python stage5/bootstrap/validate_attempt.py
```

Three candidate paths were examined:

- recursive rule description under historical `A1` — incomplete because no exact receiver-neutral binary rule language was frozen;
- Binary Lambda Calculus under `A2(U=BLC)` — incomplete because no frozen, conformance-verified complete NEX interpreter exists in BLC;
- Python 3.12 under `A_host(Python3.12)` — finite verified engineering control only, not receiver-neutral bootstrap.

Accepted result:

```text
accepted complete bootstrap candidates  0
full B | A known                        false
full SB | A known                       false
total C | A computable                  false
```

Host-control measurements:

```text
Python NEX package source            28,832 bytes
all frozen author-written files      52,859 bytes
```

These values are explicitly **not** `B`.

The corrected `A1/A1(R)` boundary reinforces the negative result: the missing formal rule calculus was a real unresolved dependency.

## 5.9 — decision gate

ADR-0015 closes Stage 5 with a negative complete-bootstrap result.

### Established

- NEX-1 v0.1 is reconstructable by a blind second implementation on the tested evidence surface.
- The frozen Go/Python comparison produced 942/942 portable agreement with the case structure stated above.
- Receiver assumptions and accounting boundaries are explicit and versioned.
- Host implementation size is not bootstrap cost.
- Unknown bootstrap cost is not treated as zero.
- Every transmitted bit belongs to one exact ledger segment under a declared profile.

### Conditional / local

- `P` is exact for stated corpora under the fixed NEX wire contract.
- `S`, `B`, `SB`, and total `C` are meaningful only relative to an explicit receiver profile and exact serialization.
- The 942-case result is empirical differential-conformance evidence, not a correctness theorem.

### Rejected

- `B = 0` because it is unknown;
- `B = size(Go/Python source)`;
- counting a universal evaluator without a complete NEX interpreter as NEX bootstrap;
- silently moving missing interpreters/calculi into receiver assumptions;
- interpreting 942/942 as proof of complete semantic correctness.

### Still unknown

- a complete accepted `B | A`, `SB | A`, or total `C | A`;
- sensitivity to selected rule calculus `R` or universal machine `U`;
- NEX-specific formal type safety;
- formal equivalence of allowed call-by-need to NEX weak CBN semantics;
- total-cost erased-HM versus explicit/hybrid typing once complete bootstrap artifacts exist;
- a finite teaching sequence that can establish NEX competence for an unknown receiver.

## Definition of done

- [x] independent protocol and frozen packet;
- [x] second implementation produced without translating `reference/go`;
- [x] independent wire/static/dynamic conformance;
- [x] post-freeze differential comparison;
- [x] ambiguity audit;
- [x] explicit versioned receiver assumptions;
- [x] bootstrap candidate attempt completed, with inability to construct a defensible full candidate recorded as a negative result;
- [x] host-source size never substituted for `B`;
- [x] final decision gate recorded;
- [x] living dissertation updated in English and Russian;
- [x] no NEX-1 v0.2/system/frontend redesign introduced.

## Post-Stage-5 audit status

The 2026-09-19 literature re-audit is recorded in ADR-0016 and `docs/RESEARCH-AUDIT-2026-09-19*.md`. It does not reopen Stage 5 or rewrite frozen historical artifacts; it narrows claim wording, advances the receiver-assumption taxonomy to v0.2, and uses Lincos/CosmicOS/related work as design evidence for the next stage.

## Handoff to Stage 6

The comparison with Lincos, DeVito–Oehrle, Lingua Cosmica, and especially CosmicOS reveals that Stage 5's bootstrap question was only part of the original communication problem. A receiver needs not only an executable basis but a **teaching sequence** from which the intended computational meaning can be reconstructed and checked.

The handoff is therefore:

```text
receiver prior A
    -> NEX teaching/bootstrap message T
    -> reconstructed NEX-1 competence
    -> conformance/self-test
    -> canonical NEX program transmission P
```

Stage 6 should make `T` the primary research object while keeping NEX-1 v0.1 stable. Formal metatheory, bounded-exhaustive differential testing, function application contexts, and hold-out workloads remain supporting workstreams.

The exact Stage 6 contract belongs in its own document/ADR and must not be backfilled into the completed Stage 5 experiment.
