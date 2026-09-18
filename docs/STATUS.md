# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Active work:** Stage 5 closeout  
**Current state:** `Stages 0–5 complete`  
**Living dissertation:** `docs/RESEARCH-DISSERTATION.md` / `docs/RESEARCH-DISSERTATION.ru.md`

## Completed stages

- Stage 0 — project/specification/ADR baseline — Complete.
- Stage 1 — canonical wire format — Complete, PR #3.
- Stage 2 — static validation and rank-1 HM inference — Complete, PR #4.
- Stage 3 — weak call-by-name dynamic semantics — Complete, PR #5.
- Stage 4 — empirical validation and benchmarking — Complete, PR #6.
- Stage 5 — independent reconstruction and receiver-conditioned bootstrap evidence — Complete.

## Stage 5 summary

### Independent reconstruction

PR #7 established the blind protocol and frozen conformance packet. PR #8 imported the independently produced Python implementation and performed post-freeze differential comparison.

Accepted result:

```text
cases total           942
portable matches      942
semantic mismatches     0
resource asymmetries    0
```

This strongly supports independent reconstructability over the tested semantic surface. It is not a formal completeness proof.

### Receiver assumptions

PR #9 / ADR-0014 introduced versioned receiver profiles:

```text
A0 < A1 < A2(U)
```

plus non-neutral engineering control `A_host(H)`.

Exact accounting is conditional:

```text
S | A
B | A
C | A
```

and inseparable specification/bootstrap bits are counted once as `SB | A`.

### Bootstrap feasibility

Stage 5.8 tested three candidate paths:

- recursive rule description under `A1` — incomplete;
- BLC as candidate basis under `A2(U=BLC)` — incomplete because no complete verified NEX-on-BLC interpreter exists;
- Python 3.12 — verified host control only, not receiver-neutral bootstrap.

Accepted Stage 5.8 result:

```text
accepted complete bootstrap candidates  0
full B | A known                        false
full SB | A known                       false
total C | A computable                  false
```

Host control only:

```text
Python NEX package source            28,832 bytes
all frozen author-written files      52,859 bytes
```

These sizes are explicitly **not** bootstrap cost.

### Final Stage 5 decision

ADR-0015 closes Stage 5 as an evidence stage with a negative complete-bootstrap result.

Established:

- NEX-1 v0.1 is independently reconstructable on the tested evidence surface;
- receiver assumptions and accounting boundaries are explicit;
- host source size is not `B`;
- unknown bootstrap cost is not treated as zero.

Still unknown:

- a complete accepted `B | A` or `SB | A`;
- numerical total `C | A`;
- sensitivity to the universal machine `U`;
- full erased-HM versus explicit/hybrid total-cost comparison.

## Current normative state

NEX-1 v0.1 remains unchanged by Stages 4–5. No v0.2 wire redesign, new Core primitives, mutable memory profile, production frontend, native backend, or self-hosting claim was introduced.

## Next recommended research stage

Construct an actual dependency-closed bootstrap artifact instead of continuing the Stage 5 feasibility audit.

Two clean directions remain:

1. under `A1`, define an exact receiver-neutral rule-transmission language and encode/verify the complete NEX semantics in it;
2. under `A2(U)`, freeze one exact universal machine and implement a complete conformance-verified NEX decoder/typechecker/evaluator for that machine.

Only after such an artifact exists should the project return to numerical `B | A`, `C | A`, typing-bootstrap trade-offs, or compactness redesign.
