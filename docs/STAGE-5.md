# Stage 5 — Independent reconstruction and receiver-conditioned bootstrap

**Status:** Complete  
**Completed:** 2026-09-18  
**Prerequisite:** Stage 4 complete

## Purpose

Stage 5 tested two questions:

1. can NEX-1 v0.1 be reconstructed independently from its specification/conformance material rather than by translating the Go reference implementation?;
2. can bootstrap cost be made explicit and measurable without hiding a terrestrial runtime, interpreter, or undeclared receiver prior?

Stage 5 did not redesign NEX-1 v0.1.

## 5.0–5.1 — independence protocol and frozen packet

PR #7 established ADR-0013, the allowlisted conformance packet and a blind implementation boundary. `reference/go` was excluded until the independent checkpoint was frozen.

The packet audit exposed two presentation-level omissions—canonical type-variable rendering and JSON fixture mapping—without changing NEX semantics.

## 5.2–5.6 — independent implementation and differential conformance

A separate Python 3.12 standard-library-only implementation was produced from the frozen packet.

Frozen archive:

```text
nex1-independent-python-v0.1.zip
sha256:783e4186f9a8c024f00a732deae33b547c81ed4d7639c610a1e8bc5997eb3fbe
```

Before Go comparison it passed all packet vectors and 23 independent tests. Post-freeze differential comparison then produced:

```text
cases total           942
portable matches      942
semantic mismatches     0
resource asymmetries    0
```

Conclusion: independent reconstructability is strongly supported on the tested evidence surface. This is empirical evidence, not a formal proof over all possible inputs.

## 5.7 — receiver-assumption model

ADR-0014 and `stage5/receiver-assumptions/assumptions-v0.1.json` define:

```text
A0      exact finite ordered binary frame
A1      A0 + discrete mathematical metalanguage
A2(U)   A1 + exact universal binary machine U and framing
A_host(H)  non-neutral terrestrial host control
```

Exact accounting is conditional:

```text
S | A
B | A
C | A
```

If specification and executable bootstrap are inseparable, their bits are counted once as `SB | A`.

No cross-profile numerical winner may be claimed without accounting for stronger/weaker priors.

## 5.8 — bootstrap feasibility audit

Machine-readable audit:

```text
stage5/bootstrap/attempt-v0.1.json
```

Validation:

```text
python stage5/bootstrap/validate_attempt.py
```

Three candidate paths were examined:

- recursive rule description under `A1` — incomplete because no exact receiver-neutral binary rule language is frozen;
- Binary Lambda Calculus under `A2(U=BLC)` — incomplete because no frozen, conformance-verified complete NEX interpreter exists in BLC;
- Python 3.12 implementation under `A_host(Python3.12)` — finite verified engineering control only, not receiver-neutral bootstrap.

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

## 5.9 — decision gate

ADR-0015 closes Stage 5 with a negative complete-bootstrap result.

### Established

- NEX-1 v0.1 is independently reconstructable on the tested evidence surface.
- Receiver assumptions are explicit and versioned.
- Host implementation size is not bootstrap cost.
- Every transmitted bit must be assigned once to `S`, `B`, `SB`, or `P` under an explicit profile.

### Conditional

- `P` is exact for stated corpora.
- `S`, `B`, and `C` are meaningful only relative to an explicit receiver profile.

### Rejected

- `B = 0` because it is unknown;
- `B = size(Go/Python source)`;
- counting a universal evaluator without a complete NEX interpreter as NEX bootstrap;
- silently moving missing interpreters into receiver assumptions.

### Still unknown

- a complete accepted `B | A` or `SB | A`;
- numerical total `C | A`;
- sensitivity to the selected universal machine `U`;
- total-cost erased-HM versus explicit/hybrid typing once complete bootstrap artifacts exist.

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

## Next research direction

A later stage should construct an actual dependency-closed bootstrap artifact. Two legitimate tracks remain:

```text
A1: define an exact receiver-neutral recursive-rule transmission language and encode full NEX in it;
A2(U): freeze one exact universal machine U and implement the complete NEX decoder/typechecker/evaluator as a verified program for U.
```

That is a new construction problem and is intentionally separated from Stage 5.
