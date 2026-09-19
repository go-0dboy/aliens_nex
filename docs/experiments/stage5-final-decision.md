# Stage 5 final decision gate

> **Subsequent status (2026-09-19):** this is the historical Stage 5 closeout record. The receiver-assumption taxonomy was later corrected by ADR-0016 / `assumptions-v0.2.json`, which separates plain `A1` from `A1(R)`. ADR-0017 then separated teaching from the stable Core, and ADR-0018 inserted the mandatory 5.10–5.20 Core self-sufficiency extension before Stage 6 activation. The negative Stage 5 bootstrap result remains unchanged. Current continuation is `5.11 Complete -> 5.12 Complete -> 5.13 Planned`; Stage 6 remains Planned until the 5.20 gate.

## Scope

Stage 5 tested two independent questions:

1. can NEX-1 v0.1 be reconstructed without translating the Go reference implementation?;
2. can the receiver-side bootstrap term be made explicit and measurable without hiding host machinery or undeclared prior knowledge?

## Established

### Independent reconstruction

A frozen Python implementation was produced from an allowlisted conformance packet before direct access to `reference/go`.

Pre-comparison evidence passed all packet vectors and 23 independent tests. The frozen implementation was then compared against Go on 942 deterministic portable observations:

```text
portable matches       942
semantic mismatches      0
resource asymmetries     0
```

This strongly supports independent reconstructability over the tested surface. It is not a formal proof for all possible terms or errors.

### Receiver assumptions

ADR-0014 and `stage5/receiver-assumptions/assumptions-v0.1.json` make the historical Stage 5 receiver assumptions explicit:

```text
A0 < A1 < A2(U)
```

with `A_host(H)` retained only as a non-neutral engineering control.

This is the frozen v0.1 taxonomy used by the Stage 5 experiment. The current corrected taxonomy is in `assumptions-v0.2.json` and adds the distinct `A1(R)` branch without rewriting this historical experiment.

Bootstrap/specification accounting is conditional:

```text
S | A
B | A
C | A
```

and an inseparable specification/bootstrap artifact is counted once as `SB | A`.

### Bootstrap feasibility

Stage 5.8 applied a strict acceptance contract to three candidate paths:

- recursive-rule description under the historical v0.1 `A1` assumption;
- Binary Lambda Calculus as a candidate universal basis under `A2(U=BLC)`;
- the verified Python implementation under `A_host(Python3.12)`.

No candidate satisfies all requirements for a complete receiver-neutral bootstrap.

```text
accepted complete bootstrap candidates  0
full B | A known                        false
full SB | A known                       false
total C | A computable                  false
```

The Python implementation is finite and measured as an engineering control:

```text
NEX package source only             28,832 bytes
all frozen author-written files     52,859 bytes
```

These values are not `B`.

## Conditional conclusions

- NEX-1 v0.1 behavior is independently reconstructable on the tested evidence surface.
- Program cost `P` is exact for the stated corpora.
- Specification/bootstrap costs are meaningful only relative to a declared receiver profile.
- A complete numerical `C | A` remains unavailable because no accepted full bootstrap artifact exists.
- A smaller transmitted artifact under a stronger profile cannot be ranked globally against a larger artifact under a weaker profile without pricing or otherwise normalizing the priors.

## Contradicted or rejected claims

Stage 5 rejects the following shortcuts:

- `B = 0` because bootstrap has not yet been represented;
- `B = size(reference implementation)`;
- `B = size(Python source)`;
- counting a universal evaluator without a complete NEX interpreter as the NEX bootstrap;
- counting English/UTF-8/Markdown/JSON as receiver-neutral under `A1` without declaring those conventions;
- silently strengthening `A` after observing a desirable bit count.

## Unknown after Stage 5

- an accepted complete `B | A` or `SB | A`;
- total numerical `C | A`;
- sensitivity of complete NEX bootstrap size to the choice of universal machine `U`;
- whether an exact recursive-rule transmission language, now modeled explicitly as `A1(R)` in the corrected taxonomy, is smaller than a machine-program bootstrap under `A2(U)`;
- total-cost comparison of erased HM against explicit/hybrid typing once complete checker bootstrap artifacts exist.

## Stage decision

Stage 5 is complete as an evidence stage.

Its bootstrap result is deliberately negative: the work established the conditions under which a bootstrap number would be admissible and showed that the Stage 5 repository did not contain such a complete artifact.

At the time of this decision, the next construction target was an actual receiver-conditioned bootstrap artifact rather than another NEX-1 v0.1 semantic redesign. Later ADR-0017/0018 refined the ordering: the stable Core first passes the post-Stage-5 5.10–5.20 self-sufficiency gate, and only then may Stage 6 teaching/bootstrap become Active.
