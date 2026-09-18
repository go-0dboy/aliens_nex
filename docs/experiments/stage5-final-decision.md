# Stage 5 final decision gate

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

ADR-0014 and `stage5/receiver-assumptions/assumptions-v0.1.json` make receiver assumptions explicit:

```text
A0 < A1 < A2(U)
```

with `A_host(H)` retained only as a non-neutral engineering control.

Bootstrap/specification accounting is conditional:

```text
S | A
B | A
C | A
```

and an inseparable specification/bootstrap artifact is counted once as `SB | A`.

### Bootstrap feasibility

Stage 5.8 applied a strict acceptance contract to three candidate paths:

- recursive-rule description under `A1`;
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
- whether an exact recursive-rule transmission language under `A1` is smaller than a machine-program bootstrap under `A2(U)`;
- total-cost comparison of erased HM against explicit/hybrid typing once complete checker bootstrap artifacts exist.

## Stage decision

Stage 5 is complete as an evidence stage.

Its bootstrap result is deliberately negative: the work established the conditions under which a bootstrap number would be admissible and showed that the current repository does not yet contain such a complete artifact.

The correct next research stage is therefore not another NEX-1 v0.1 semantic redesign. It is construction of an **actual receiver-conditioned bootstrap artifact**, starting from one frozen computational basis or one exact rule-transmission language and closing its dependency ledger end to end.
