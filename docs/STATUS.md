# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Active branch:** `stage5/independence-protocol`  
**Current state:** `Stage 4 — Complete; Stage 5 — In progress (5.0/5.1 protocol checkpoint)`  
**Living research dissertation:** `docs/RESEARCH-DISSERTATION.md` / `docs/RESEARCH-DISSERTATION.ru.md` (ADR-0012)

## Completed milestones

- Stage 0 — specification/process/ADR baseline — Complete.
- Research source registry — Complete.
- Stage 1 — canonical wire foundation — Complete by PR #3, merge `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`.
- Stage 2 — static validation and principal HM type inference — Complete by PR #4, merge `cefe889d90a275897de31aa23c4b9742a388ec8f`.
- Stage 3 — dynamic semantics and reference evaluator — Complete by PR #5, merge `166cdc03282ea500263fdca7185f006f9b17a702`.
- Stage 4 — empirical validation and benchmarking — Complete by PR #6, squash merge `ebffde6c8669f65dfcba98d31d261d59b48d4dd0`.

Stage 4 final PR head `871d0bc44dbf18854d5e58b15191799b11b834af` passed clean-checkout CI `35377200520`. Post-merge `main` commit `ebffde6c8669f65dfcba98d31d261d59b48d4dd0` passed push CI `35377892126`.

The final Stage 4 evidence and conclusions remain in `docs/STAGE-4.md`, ADR-0011, and the living dissertation. Key unresolved variables remain receiver-neutral specification cost `S` and bootstrap `B`; total `C = S + B + P` is not yet numerically defensible.

## Stage 5 — In progress

Working title:

> **Independent reconstruction and receiver-neutral bootstrap**

Plan: `docs/STAGE-5.md`.

Stage 5 remains an evidence stage. No NEX-1 v0.2 redesign, new Core primitive, system profile, production frontend, native backend, or self-hosting work is authorized by this stage.

### 5.0 — independence protocol — Implemented on branch; pending PR verification

ADR-0013 records the first independent-reconstruction protocol.

Frozen NEX source snapshot:

```text
4f9c50aed13cdbdf72c9ce6510521477d49c05a5
```

First independent implementation target:

```text
Python 3.12+
standard library only
```

Python is selected to reduce implementation similarity to Go and because arbitrary-precision integers require no third-party package. Python source size is explicitly **not** bootstrap cost `B`.

The packet allowlist includes only:

- canonical `docs/NEX-1-v0.1.md`;
- wire/static/evaluation conformance JSON;
- ADR-0002, ADR-0006, ADR-0007, ADR-0009;
- packet-local observation/audit documents;
- explicitly allowlisted primary theory.

`reference/go/**`, Stage 4 experiment material, benchmark corpus, dissertation/status/stage-history documents, and ADR-0008's Go evaluator architecture are excluded as implementation guidance before the independent checkpoint.

### Cognitive-independence limitation — Recorded

The current co-development context already participated in the Go reference implementation. Therefore code authored here from remembered Go design **must not** be labelled independent implementation evidence.

Strong Stage 5 independent evidence requires:

```text
fresh isolated implementation context
or
another implementer
```

receiving only the frozen packet and allowed theory.

The current context is allowed to build protocol, packet, audit, CI, and neutral comparison infrastructure.

### Frozen conformance packet — Implemented

Packet metadata:

```text
stage5/conformance-packet-v0.1/manifest.json
packet_id = nex1-independent-conformance-packet-v0.1
```

The manifest records exact Git blob hashes for every frozen source file.

`stage5/build_packet.py`:

- verifies the expected frozen source commit identity in the manifest;
- verifies Git-blob hashes of all allowlisted source files;
- validates conformance JSON schema IDs;
- materializes only allowlisted source and packet-local files;
- generates a SHA-256 content manifest for the standalone packet.

`.github/workflows/stage5-independence.yml` verifies and materializes the packet with Python 3.12 and uploads the standalone packet as a workflow artifact.

### 5.1 — conformance packet completeness audit — Implemented on branch

Audit: `stage5/conformance-packet-v0.1/AUDIT.md`.

The audit found no known missing Core semantic rule that blocks a first independent implementation, but it found two presentation-layer omissions:

**F1 — principal type observation format.** Principal schemes are semantic up to alpha-renaming, while static conformance stores strings using `T0`, `T1`, ... . The canonical conformance text rule was not explicitly specified.

**F2 — fixture JSON AST shape.** The conformance files demonstrated `kind/value/a/b` JSON objects but did not explicitly define that JSON mapping as a test-fixture contract.

Both are resolved in:

```text
stage5/conformance-packet-v0.1/OBSERVATIONS.md
```

as packet-only comparison/fixture conventions. They do not alter NEX-1 v0.1 wire or semantics.

Additional audit conclusions:

- Algorithm W internal substitution/fresh-ID strategy remains deliberately implementation-specific; only normalized principal schemes are portable.
- evaluator representation remains deliberately implementation-specific; ADR-0008 is excluded from the packet.
- a global precedence rule for hypothetical terms containing multiple independent static defects is not invented. If differential testing makes such a rule necessary, Stage 5.6 will add the smallest portable conformance case.

### Next gate

Before Stage 5.2 can claim independent evidence:

1. PR A (protocol + packet) must pass its dedicated clean-checkout CI;
2. the materialized packet artifact must be frozen;
3. a fresh isolated implementation context must receive only that packet and allowed external theory;
4. independent wire/static/dynamic implementation must reach a declared pre-comparison commit;
5. only then may `reference/go` be opened for differential conformance.

## Remaining project-wide unknowns

- whether a truly isolated second implementation reconstructs the same NEX behavior;
- what specification ambiguities the independent attempt will expose;
- actual receiver-neutral bootstrap artifact and conditional cost `B | A`;
- receiver-neutral specification cost `S`;
- broader-corpus generalization of Stage 4 constructor distributions;
- formal proof of selected codec/type/evaluator properties;
- independent total-cost comparisons under common receiver assumptions.
