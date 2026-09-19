# Stage 5.12 closeout plan — complete self wire codec before Stage 5.13

**Status:** Active planning / implementation blocked until prerequisites are checked  
**Date:** 2026-09-19  
**Core:** NEX-1 v0.1 unchanged  
**Parent decision:** ADR-0018  
**Stage 6:** Planned  

## Sequencing correction

This document corrects the project ordering after the accepted Stage 5.12f bounded stream-parser checkpoint.

The ordering is strict:

```text
5.11 Complete
  -> 5.12 Complete
     -> 5.13 may begin
```

Stage 5.12f is a checkpoint **inside Stage 5.12**. It is not the completion of Stage 5.12 and it does not authorize work on Stage 5.13.

Any earlier wording in status, manuscript, or PR discussion that described Stage 5.13 structural validation as the immediate next implementation step is superseded by this closeout plan.

No Stage 5.13 implementation branch or code is to be created until the Stage 5.12 completion gate below is satisfied.

## Why Stage 5.12 is still open

The frozen Stage 5 extension contract requires Stage 5.12 to implement in NEX:

```text
encodeU / decodeU
encodeTerm / decodeTerm
```

with required checks:

```text
decodeTerm(encodeTerm(term)) == term
encodeTerm(decodeTerm(bits)) == canonical(bits)
```

and differential comparison against the existing Go/Python wire behavior.

Current evidence establishes:

- NEX-written integer wire helpers and `encodeU/decodeU` checkpoints;
- a practical functional finite-bit-stream representation on tested surfaces;
- NEX-written `decodeUAt`, `readHead`, `skipTerm`, and `exactTerm`;
- bounded recursive traversal of canonical NEX term wire;
- preregistered development/hold-out evidence for the stream parser.

It does **not** yet establish complete `encodeTerm/decodeTerm` or their required round trips. Therefore Stage 5.12 remains Active.

## Gate 0 — predecessor audit: Stage 5.11 must be Complete

Before adding another Stage 5.12 implementation candidate, re-audit the original Stage 5.11 definition of done.

The original representation scope includes at least:

```text
Bits
Term
Type
Scheme
Substitution
Type environment
Runtime/evaluation state as needed
Error/result classes
Portable observations
Toolchain requests/results
```

The existing v0.1/v0.2 numeric representation checkpoints and the later functional-stream evidence must be compared with this original scope.

Gate 0 outcomes:

1. **5.11 already satisfies its exact contract** — record the evidence and mark 5.11 Complete; or
2. **5.11 has missing representation contracts** — finish and validate them before proceeding with new 5.12 code.

No redefinition of 5.11 is allowed merely to make the status green. If the representation strategy evolved from all-`N` carriers to stream/cursor carriers, that evolution must be explicitly versioned and reconciled with the original 5.11 acceptance criteria.

## Gate 1 — freeze the exact Stage 5.12 Term representation

The next unresolved question is not yet an algorithm. It is the exact internal representation on which `decodeTerm` and `encodeTerm` operate.

Before implementation, freeze a machine-readable representation contract that states:

- the physical NEX carrier for a decoded `Term`;
- whether it is materialized or stream-backed;
- exact equality for decoded terms;
- exact canonicalization rule;
- exact success/error result type;
- treatment of malformed/truncated/trailing wire;
- whether unknown primitive IDs remain a structural Term value for Stage 5.13 to reject, rather than being rejected by the wire codec;
- how child terms are addressed without recursive Core types;
- how `encodeTerm` obtains every constructor and payload needed to reproduce canonical wire;
- no hidden host AST/list/string/byte-array callback.

A stream-backed/offset representation may be considered, but it must not be accepted merely because it makes `decodeTerm` an identity operation. The contract must demonstrate that the representation is sufficient for an independent NEX-written encoder and for later static/dynamic consumers.

If this representation changes the accepted 5.11 meta-representation contract, create a new explicit representation version and satisfy Gate 0 before proceeding.

## Gate 2 — preregister Stage 5.12 completion workloads

Before first execution of the full Term-codec candidate, freeze:

### Development workload

Must cover all six constructors:

```text
Var Lam App Let Nat Prim
```

and include:

- leaf terms with small and larger U payloads;
- nested unary terms;
- both-child constructors with asymmetric subtree sizes;
- deep mixed nesting;
- offsets/cursors where applicable;
- truncated constructor prefixes;
- truncated U payloads;
- truncated child terms;
- trailing data;
- canonical exact input;
- functionally produced streams, not only host literals.

### Hold-out workload

A separate preregistered set not used to author the candidate.

Previously observed parser cases are **development/historical evidence** and may not be relabelled as hold-out.

### Resource budgets

Retain the frozen Stage 5.12 anti-tuning budgets unless an explicit pre-execution contract gives a research reason for a different measurement profile. Budgets must never be increased after observing a candidate result to manufacture a pass.

## Gate 3 — implement NEX-written `decodeTerm`

Implement a closed, well-typed canonical NEX term that consumes the Stage 5.12 `Bits` representation and returns the frozen Stage 5.12 `Term` representation or an explicit wire/decode error.

Acceptance requires:

- reproducible generator/artifact;
- canonical NEX wire;
- closed scope;
- principal type recorded;
- all development observations correct;
- Python and Go sharing implementations agree on returned portable observations;
- resource refusals recorded separately from wire/decode errors;
- normative CBN measured separately and not silently substituted by call-by-need.

## Gate 4 — implement NEX-written `encodeTerm`

Implement a closed, well-typed canonical NEX term that consumes the frozen decoded-Term representation and emits canonical functional bit stream output.

The encoder must reconstruct constructor prefixes and U payloads from the NEX representation itself. Host code may build test applications and observe results, but may not supply missing encoding decisions through callbacks.

Acceptance uses the same artifact/type/differential/resource discipline as Gate 3.

## Gate 5 — round-trip and canonicalization laws

Freeze and execute explicit laws over the admitted bounded surface:

```text
decodeTerm(encodeTerm(term)) == term
encodeTerm(decodeTerm(bits)) == canonical(bits)
```

The second law applies only where decoding succeeds under the frozen codec contract.

Required comparisons:

```text
Direct Go codec
Direct Python codec
NEX codec executed by Go
NEX codec executed by Python
```

For function-valued stream results, equality must be tested extensionally over the exact canonical bit interval plus EOF behavior; observing only `Function` is insufficient.

## Gate 6 — bounded exhaustive/differential strengthening for the codec

Before Stage 5.12 can be called Complete, add at least one precisely defined small complete class, for example by a frozen combination of:

- maximum AST node count;
- bounded Var/Nat/Prim payload range;
- all six constructors where the bound permits them.

For every admitted term in that class:

- direct Go and Python canonical encodings agree;
- NEX `encodeTerm` agrees extensionally with the canonical wire;
- NEX `decodeTerm` accepts the canonical wire;
- round-trip observations agree;
- malformed cases remain separately classified.

This is bounded evidence, not a global proof.

## Gate 7 — one-shot hold-out

Only after:

- representation contract frozen;
- candidate artifacts frozen;
- development pass frozen;
- full historical checkpoint green;

may the unchanged candidate be executed once against the preregistered Stage 5.12 completion hold-out.

A hold-out failure rejects that candidate version. The same version may not be tuned against the revealed hold-out.

## Gate 8 — Stage 5.12 completion review

Stage 5.12 may be marked **Complete** only when all of the following are true:

- [ ] Gate 0: Stage 5.11 is formally Complete under its original/evidence-backed versioned contract;
- [x] NEX integer wire codec prerequisites exist;
- [x] functional bit-stream representation checkpoint exists;
- [x] bounded NEX stream parser checkpoint exists;
- [ ] exact Term representation for full codec is frozen and validated;
- [ ] NEX `decodeTerm` exists and passes frozen development evidence;
- [ ] NEX `encodeTerm` exists and passes frozen development evidence;
- [ ] both required round-trip/canonicalization laws pass;
- [ ] Go/Python/NEX-on-Go/NEX-on-Python differential checks pass on the frozen surface;
- [ ] bounded exhaustive small-class codec evidence passes;
- [ ] unchanged candidate passes the preregistered one-shot hold-out;
- [ ] negative/resource outcomes are preserved rather than hidden;
- [ ] no Core v0.1 rule or primitive was changed for convenience;
- [ ] historical regression is green on final Stage 5.12 head;
- [ ] `docs/STATUS.md` marks 5.12 Complete and 5.13 Planned;
- [ ] both living dissertation versions describe the completed 5.12 result and limitations;
- [ ] PR/diff review confirms no hidden host semantic dependency.

Only after this checklist is complete may the project discuss or begin Stage 5.13.

## Immediate next action

The immediate next action is **Gate 0: audit Stage 5.11 completion against its original definition of done**.

No new codec implementation should be written until that audit is recorded, because the full `Term` codec depends on a representation contract and the project has explicitly adopted strict sequential completion.