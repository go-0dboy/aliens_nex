# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Active branch:** `stage5/independent-differential`  
**Current state:** `Stage 4 — Complete; Stage 5 — In progress (independent reconstruction through 5.5 verified)`  
**Living research dissertation:** `docs/RESEARCH-DISSERTATION.md` / `docs/RESEARCH-DISSERTATION.ru.md` (ADR-0012)

## Completed milestones

- Stage 0 — specification/process/ADR baseline — Complete.
- Research source registry — Complete.
- Stage 1 — canonical wire foundation — Complete by PR #3, merge `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`.
- Stage 2 — static validation and principal HM type inference — Complete by PR #4, merge `cefe889d90a275897de31aa23c4b9742a388ec8f`.
- Stage 3 — dynamic semantics and reference evaluator — Complete by PR #5, merge `166cdc03282ea500263fdca7185f006f9b17a702`.
- Stage 4 — empirical validation and benchmarking — Complete by PR #6, squash merge `ebffde6c8669f65dfcba98d31d261d59b48d4dd0`.
- Stage 5.0/5.1 — independence protocol + frozen conformance packet — Complete by PR #7, squash merge `04f4f84cce50a15638802babbe934b70e495911c`.

Stage 4 final PR head `871d0bc44dbf18854d5e58b15191799b11b834af` passed clean-checkout CI `35377200520`; post-merge run `35377892126` passed.

PR #7 final head `534f5e10468d62fe728f80bcabd4636678bd4c40` passed `stage5-independence` run `35380403587`. Post-merge `main` commit `04f4f84cce50a15638802babbe934b70e495911c` passed push run `35383798779`.

## Stage 5 — In progress

Working title:

> **Independent reconstruction and receiver-neutral bootstrap**

Plan: `docs/STAGE-5.md`.

Stage 5 remains an evidence stage. No NEX-1 v0.2 redesign, new Core primitive, system profile, production frontend, native backend, or self-hosting work is authorized by this stage.

### 5.0 — independence protocol — Complete

ADR-0013 fixes the first independent-reconstruction protocol.

Frozen source snapshot:

```text
4f9c50aed13cdbdf72c9ce6510521477d49c05a5
```

Independent implementation target:

```text
Python 3.12+
standard library only
```

The blind phase excludes `reference/go/**`, Stage 4 experiment material, benchmark corpus, dissertation/status/history documents, and ADR-0008's Go evaluator architecture. A fresh isolated implementation context or different implementer is required before a result may be labelled independent evidence.

### 5.1 — frozen conformance packet and completeness audit — Complete

Packet ID:

```text
nex1-independent-conformance-packet-v0.1
```

`stage5/build_packet.py` verifies exact Git blob hashes, validates conformance schemas, materializes the allowlisted packet, and emits a SHA-256 content manifest. The packet CI publishes a standalone artifact.

The audit found two presentation-layer omissions and made them explicit as packet-only conventions:

1. alpha-normalized principal-scheme rendering (`T0`, `T1`, ...);
2. JSON `kind/value/a/b` fixture representation.

Neither changes NEX-1 v0.1 semantics or wire format.

No global precedence is defined for terms containing multiple independent static errors; such precedence remains deliberately implementation-specific unless future evidence requires a portable rule.

### 5.2–5.4 — independent Python reconstruction — Verified checkpoint

A separate model/implementation context received the frozen packet rather than the repository/reference implementation and returned `nex1-independent-python-v0.1.zip`.

Received archive checkpoint:

```text
SHA-256:
783e4186f9a8c024f00a732deae33b547c81ed4d7639c610a1e8bc5997eb3fbe

ZIP comment / external checkpoint marker:
a594b73b711998df04b45eec296086d5577fba2f
```

The archive contains its own independence declaration, implementation notes, ambiguity log, Python implementation, tests, and verifier. The frozen author-written files are imported under `independent/python/` and protected by `stage5/independent-checkpoints/python-v0.1.json`, which records exact byte lengths and SHA-256 values for every file. CI re-materializes the canonical packet rather than maintaining a second editable packet copy.

Before opening `reference/go`, the independent implementation was verified against the frozen packet:

```text
wire integer vectors     17 / 17
wire term vectors        12 / 12
invalid wire vectors     15 / 15
scope vectors            15 / 15
type vectors             19 / 19
evaluation vectors       21 / 21
independent unit tests   23 / 23
```

Additional pre-comparison local audit included 20,000 deterministic/random wire round trips, large arbitrary-precision `U(n)` values, additional typing/evaluation/laziness cases, and resource-refusal separation; no defect was found in those checks.

The independent implementation chose materially different host representations in several places (for example, a dedicated recursive `FixThunk` rather than reproducing the Go evaluator's exact recursion representation). This supports, but does not mathematically prove, cognitive/architectural independence.

One ambiguity was independently recorded: error precedence for a term containing multiple independent static defects is not globally specified. The Python implementation chooses scope validation first but explicitly classifies that choice as implementation ordering rather than portable semantics.

### 5.5 — post-freeze differential conformance — Verified

Only after the archive SHA-256 was frozen did comparison with `reference/go` begin.

PR #8 adds a comparison layer outside the frozen independent subtree. It compares only portable observations:

```text
canonical wire bits
normalized principal scheme / portable static error class
observable WHNF / portable evaluation error class
```

It deliberately does not compare object layout, fresh variable IDs, thunk/closure representation, transition counts, allocations, or other host-specific details.

Clean-checkout Stage 5 differential run:

```text
stage5-differential run 35384938381 — success
reference-go run        35384938291 — success
stage5-independence     35384938418 — success
```

Generated report artifact:

```text
nex-stage5-differential-report-v0.1
artifact id 10563821507
artifact digest sha256:bda41629934f1c7b8f2554726002c3af5186d8cb19df649d8fab72129f8ba62a
seed 20260918
```

Differential result:

```text
cases total                942
frozen corpus v0.3          17
generated valid            325
generated static-error     100
generated wire             500
portable matches           942
semantic mismatches          0
resource asymmetries         0
```

This is the strongest current evidence that NEX-1 v0.1 behavior is reconstructable from the frozen specification/conformance packet independently of the original Go implementation. It is empirical conformance evidence, not a formal proof that the specification is complete for every possible term or implementation.

### 5.6 — ambiguity audit / hardening — Current conclusion

The independent reconstruction and 942-case differential run exposed no new Core semantic contradiction requiring a NEX-1 v0.1 change.

Current findings:

- F1/F2 remain packet presentation conventions, already documented in Stage 5.1;
- the multiple-error-precedence question remains deliberately unspecified and did not produce a portable mismatch;
- no Go bug, independent-Python semantic bug, or conformance-vector contradiction has been identified by the accepted differential evidence so far.

Therefore no normative v0.1 semantic/wire hardening is currently justified by Stage 5.6. Future discrepancies must still be classified rather than resolved by blindly matching Go.

### Next gate — 5.7 receiver-assumption model

The independent-reconstruction half of Stage 5 is now supported strongly enough to move to the bootstrap half without redesigning NEX.

Next work must define explicit receiver assumption sets before measuring bootstrap:

```text
A0 / A1 / A2 ...
physical/channel assumptions
binary order/framing assumptions
mathematical assumptions
integer/code assumptions
term/binding/type/evaluation assumptions
```

Any future bootstrap number must be written conditionally:

```text
B | A
```

and never replaced by Go/Python source size or an undeclared interpreter dependency.

## Remaining project-wide unknowns

- receiver-neutral assumption sets and a defensible measurable bootstrap artifact `B | A`;
- receiver-neutral specification cost `S`;
- whether total `C = S + B + P` becomes computable under any explicit assumption set;
- broader-corpus generalization of Stage 4 constructor distributions;
- formal proof of selected codec/type/evaluator properties;
- additional independent implementations in other paradigms/toolchains;
- independent total-cost comparisons against alternative computational systems under common receiver assumptions.
