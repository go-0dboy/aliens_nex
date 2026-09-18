# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Active branch:** `stage5/receiver-assumptions`  
**Current state:** `Stage 4 — Complete; Stage 5 — In progress (5.0–5.6 merged/verified; 5.7 receiver-assumption model implemented on branch)`  
**Living research dissertation:** `docs/RESEARCH-DISSERTATION.md` / `docs/RESEARCH-DISSERTATION.ru.md` (ADR-0012)

## Completed milestones

- Stage 0 — specification/process/ADR baseline — Complete.
- Research source registry — Complete and maintained as research evolves.
- Stage 1 — canonical wire foundation — Complete by PR #3, merge `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`.
- Stage 2 — static validation and principal HM type inference — Complete by PR #4, merge `cefe889d90a275897de31aa23c4b9742a388ec8f`.
- Stage 3 — dynamic semantics and reference evaluator — Complete by PR #5, merge `166cdc03282ea500263fdca7185f006f9b17a702`.
- Stage 4 — empirical validation and benchmarking — Complete by PR #6, squash merge `ebffde6c8669f65dfcba98d31d261d59b48d4dd0`.
- Stage 5.0/5.1 — independence protocol + frozen conformance packet — Complete by PR #7, squash merge `04f4f84cce50a15638802babbe934b70e495911c`.
- Stage 5.2–5.6 — frozen independent Python reconstruction + post-freeze differential conformance — Complete by PR #8, squash merge `f500a5c5485b4cd5f6b5d9bd6bc76980f2f06cdb`.

Stage 4 final PR head `871d0bc44dbf18854d5e58b15191799b11b834af` passed clean-checkout CI `35377200520`; post-merge run `35377892126` passed.

PR #7 final head `534f5e10468d62fe728f80bcabd4636678bd4c40` passed `stage5-independence` run `35380403587`. Post-merge `main` commit `04f4f84cce50a15638802babbe934b70e495911c` passed push run `35383798779`.

PR #8 final head `5707dd3dafb5f49498ac3c8b163ddf8a04994845` passed:

```text
reference-go        35385704921  success
stage5-independence 35385705027  success
stage5-differential 35385705162  success
```

Post-merge `main` commit `f500a5c5485b4cd5f6b5d9bd6bc76980f2f06cdb` passed:

```text
reference-go        35386452647  success
stage5-independence 35386452451  success
stage5-differential 35386452447  success
```

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

### 5.2–5.4 — independent Python reconstruction — Complete for first independent implementation

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

### 5.5 — post-freeze differential conformance — Complete

Only after the archive SHA-256 was frozen did comparison with `reference/go` begin.

The comparison layer outside the frozen independent subtree compares only portable observations:

```text
canonical wire bits
normalized principal scheme / portable static error class
observable WHNF / portable evaluation error class
```

It deliberately does not compare object layout, fresh variable IDs, thunk/closure representation, transition counts, allocations, or other host-specific details.

Accepted deterministic differential set:

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

### 5.6 — ambiguity audit / hardening — Complete for current evidence

The independent reconstruction and 942-case differential run exposed no Core semantic contradiction requiring a NEX-1 v0.1 change.

Current findings:

- F1/F2 remain packet presentation conventions, already documented in Stage 5.1;
- the multiple-error-precedence question remains deliberately unspecified and did not produce a portable mismatch;
- no Go bug, independent-Python semantic bug, or conformance-vector contradiction has been identified by the accepted differential evidence.

Therefore no normative v0.1 semantic/wire hardening is currently justified by Stage 5.6. Future discrepancies must still be classified rather than resolved by blindly matching Go.

### 5.7 — receiver-assumption model — Implemented on active branch; verification pending

ADR-0014 introduces explicit conditional bootstrap accounting.

The core methodological rule is:

```text
B | A
```

rather than an unconditional scalar `B`.

The first versioned assumption registry is:

```text
stage5/receiver-assumptions/assumptions-v0.1.json
```

It defines an explicit assumption ladder:

```text
A0
  digital transport prior only
  exact finite ordered binary frame

A1
  A0 + explicit discrete mathematical metalanguage

A2(U)
  A1 + one exact fixed universal binary abstract machine U
  + exact self-delimiting program/data convention
```

and a separate engineering control:

```text
A_host(H)
  A1 + concrete terrestrial host H
  not eligible for receiver-neutral bootstrap claims
```

Important consequences:

- the physical signalling layer below `A0` is out of scope, not zero-cost;
- `A0 ⊂ A1 ⊂ A2(U)` is an inclusion relation of stated assumptions, not a numeric price or probability model;
- `U` remains a parameter in Stage 5.7; Stage 5.8 must freeze a concrete candidate before any `B | A2(U)` number is accepted;
- Go/Python/WebAssembly/x86/POSIX source/runtime measurements remain host controls, not receiver-neutral `B`;
- results under different assumption profiles cannot be ranked numerically without a later model that prices or normalizes the differing priors.

ADR-0014 also closes a potential accounting error. The conceptual objective remains:

```text
C = S + B + P
```

but exact transmitted-bit accounting must count every bit once. For disjoint specification/bootstrap segments:

```text
C | A = (S | A) + (B | A,S) + P
```

If one artifact inseparably serves both specification and executable-bootstrap roles:

```text
C | A = (SB | A) + P
```

and the same bits must not be counted once as `S` and again as `B`.

The model is machine-readable and validated by:

```text
python stage5/validate_receiver_assumptions.py
```

A dedicated `stage5-receiver-assumptions` workflow gates the model once a PR is opened.

New primary-source entries used materially by this decision are registered as SRC-0015 (Shannon), SRC-0016 (Kolmogorov), and SRC-0017 (Chaitin).

### Next gate — 5.8 first measurable bootstrap artifact

Do not select a compact language or machine merely because its own syntax is small.

Stage 5.8 must first choose what exact assumption profile is being instantiated, then freeze at least one concrete bootstrap candidate and measure the actual transmitted ledger.

For an `A2(U)` experiment, `U` must itself have exact versioned binary semantics before the bootstrap measurement is accepted.

At minimum the next experiment should attempt to separate or jointly account for:

```text
B_decode
B_static
B_eval
S or SB segments
P
```

without circularly omitting the interpreter needed to interpret the bootstrap.

## Remaining project-wide unknowns

- which concrete bootstrap representation and, for `A2(U)`, which exact machine `U` should be tested first;
- whether a sufficiently receiver-neutral bootstrap can be constructed under `A0` or `A1`, or only under a stronger `A2(U)` prior;
- the actual measured bootstrap cost `B | A` or joint `SB | A`;
- receiver-neutral specification cost `S | A` where it can be separated defensibly;
- whether total `C | A` becomes computable under any explicit assumption profile;
- how to compare different assumption profiles without pretending stronger priors are free;
- broader-corpus generalization of Stage 4 constructor distributions;
- formal proof of selected codec/type/evaluator properties;
- additional independent implementations in other paradigms/toolchains;
- independent total-cost comparisons against alternative computational systems under the same receiver-assumption profile.
