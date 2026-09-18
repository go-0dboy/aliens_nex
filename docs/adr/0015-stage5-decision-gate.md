# ADR-0015: Close Stage 5 with a negative complete-bootstrap result

- **Status:** Accepted
- **Date:** 2026-09-18

## Context

Stage 5 had two goals: independent reconstruction of NEX-1 v0.1 and explicit receiver-conditioned bootstrap accounting.

The independent-reconstruction goal succeeded on the accepted evidence set. The bootstrap-feasibility audit did not produce a complete receiver-neutral artifact satisfying the acceptance contract.

The Stage 5 definition of done explicitly permits this outcome if inability to construct a defensible candidate is documented as a negative result rather than replaced by host-source size or hidden assumptions.

## Decision

Stage 5 is considered complete after the final closeout checks with the following conclusions:

1. NEX-1 v0.1 is independently reconstructable on the tested evidence surface.
2. Receiver assumptions are explicit and versioned through `A0`, `A1`, `A2(U)`, and non-neutral `A_host(H)`.
3. Exact bootstrap/specification accounting is conditional on a declared profile and must obey the no-double-counting rule.
4. Stage 5.8 produced **zero accepted complete receiver-neutral bootstrap candidates**.
5. No scalar `B | A`, `SB | A`, or total `C | A` is accepted yet.
6. Python/Go source size remains an engineering proxy only and must not be substituted for bootstrap cost.
7. Future work should construct a real dependency-closed bootstrap artifact rather than redesign NEX-1 v0.1 merely to obtain a smaller local payload number.

## Evidence

Independent reconstruction:

```text
942 portable matches
0 semantic mismatches
0 resource asymmetries
```

Bootstrap feasibility:

```text
accepted complete bootstrap candidates  0
full B | A known                        false
total C | A computable                  false
```

Host engineering control:

```text
frozen Python NEX package source     28,832 bytes
all frozen author-written files      52,859 bytes
```

These host byte counts are explicitly not bootstrap values.

## Consequences

### Positive

- Stage 5 has a falsifiable, bounded conclusion instead of remaining indefinitely open.
- Unknown bootstrap cost remains visible rather than being silently treated as zero.
- The next stage has a precise construction target: close the dependency ledger of one actual bootstrap artifact.

### Limitations

- Total NEX information cost is still not numerically known.
- Independent reconstruction evidence is empirical, not a formal equivalence proof.
- Receiver profiles are experimental models, not claims about a real extraterrestrial receiver.

## Rejected alternatives

### Keep Stage 5 open until a complete bootstrap is built

Rejected. Stage 5 has already answered its feasibility question: under the current artifacts no admissible full bootstrap number exists. Continuing indefinitely would mix a new construction research program into the evidence stage.

### Use the Python implementation as `B`

Rejected. Python and its runtime are part of `A_host(Python3.12)` and are not receiver-neutral.

### Select BLC and count only its universal evaluator

Rejected. Without a complete verified NEX interpreter encoded for that basis, this does not close the NEX bootstrap dependency graph.
