# Stage 5.12 closeout plan — complete self wire codec before Stage 5.13

**Status:** Active  
**Date:** 2026-09-19  
**Core:** NEX-1 v0.1 unchanged  
**Parent decision:** ADR-0018  
**Stage 6:** Planned  

## Sequencing rule

The ordering is strict:

```text
5.11 Complete
  -> 5.12 Complete
     -> 5.13 may begin
```

Stage 5.11 is now Complete under `meta-representation-v0.3`.

Stage 5.12f remains a checkpoint **inside Stage 5.12**. It is not the completion of Stage 5.12 and it does not authorize Stage 5.13 work.

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

and differential comparison against existing Go/Python wire behavior.

Current evidence establishes:

- NEX-written integer wire helpers and `encodeU/decodeU` checkpoints;
- a practical functional finite-bit-stream representation on tested surfaces;
- NEX-written `decodeUAt`, `readHead`, `skipTerm`, and `exactTerm`;
- bounded recursive traversal of canonical NEX term wire;
- preregistered development/hold-out evidence for the stream parser;
- a completed Stage 5.11 operational representation contract v0.3.

It does **not** yet establish complete `encodeTerm/decodeTerm` or their required round trips. Therefore Stage 5.12 remains Active.

## Gate 0 — predecessor audit: Stage 5.11 Complete

**Status: Complete.**

Durable evidence:

```text
stage5/selfhost/meta-representation-v0.3.json
stage5/selfhost/validate_meta_representation_v0_3.py
docs/experiments/stage5-selfhost-5.11-completion-audit.md
docs/experiments/stage5-selfhost-meta-representation-v0.3.md
```

The accepted operational carriers are:

```text
FiniteBits      = (N -> N) * N
FiniteNatTokens = (N -> N) * N
```

The accepted `Term` representation is a canonical finite natural-token prefix tree:

```text
Var(k)   -> [0,k]
Lam(t)   -> [1] ++ t
App(a,b) -> [2] ++ a ++ b
Let(v,b) -> [3] ++ v ++ b
Nat(n)   -> [4,n]
Prim(p)  -> [5,p]
```

The full codec must use this exact v0.3 representation unless a later versioned representation decision explicitly supersedes it before candidate execution.

## Gate 1 — freeze the exact Stage 5.12 full-codec interface

The representation question is now resolved by Stage 5.11 v0.3. Gate 1 must freeze the exact NEX interfaces and result/error contracts for the full codec before implementation.

At minimum, freeze:

- physical types of `Bits`, `Term`, decode result, and encode result;
- exact `decodeTerm` success/error result shape;
- exact `encodeTerm` success/error result shape if encoding malformed internal tokens is representable;
- malformed/truncated/trailing wire classes;
- malformed Term-token classes;
- treatment of unknown primitive IDs: the wire codec preserves `Prim(id)` and Stage 5.13 performs primitive validity checks;
- extensional equality for function-valued Bits;
- exact canonicalization rule;
- no hidden host AST/list/string/byte-array callback.

The contract must preserve the v0.3 anti-identity rule: `decodeTerm` transforms wire Bits into Term tokens and `encodeTerm` reconstructs canonical wire from the token representation itself.

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
- malformed Term token streams;
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

Implement a closed, well-typed canonical NEX term that consumes accepted v0.3 `Bits` and returns accepted v0.3 `Term` tokens or an explicit wire/decode error.

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

Implement a closed, well-typed canonical NEX term that consumes accepted v0.3 `Term` tokens and emits canonical v0.3 `Bits`.

The encoder must reconstruct constructor prefixes and `U(n)` payloads from the token representation itself. Host code may build test applications and observe results, but may not supply missing encoding decisions through callbacks.

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

Before Stage 5.12 can be called Complete, add at least one precisely defined small complete class, frozen before aggregate execution, using explicit bounds such as:

- maximum AST node count;
- bounded Var/Nat/Prim payload ranges;
- all six constructors where the node bound permits them.

For every admitted term in that class:

- direct Go and Python canonical encodings agree;
- NEX `encodeTerm` agrees extensionally with canonical wire;
- NEX `decodeTerm` accepts canonical wire and returns exact v0.3 Term tokens;
- round-trip observations agree;
- malformed cases remain separately classified.

This is bounded evidence, not a global proof.

## Gate 7 — one-shot hold-out

Only after:

- full-codec interface frozen;
- workloads frozen;
- candidate artifacts frozen;
- development pass frozen;
- full historical checkpoint green;

may the unchanged candidate be executed once against the preregistered Stage 5.12 completion hold-out.

A hold-out failure rejects that candidate version. The same version may not be tuned against the revealed hold-out.

## Gate 8 — Stage 5.12 completion review

Stage 5.12 may be marked **Complete** only when all of the following are true:

- [x] Gate 0: Stage 5.11 formally Complete under accepted operational v0.3;
- [x] NEX integer wire codec prerequisites exist;
- [x] functional bit-stream representation checkpoint exists;
- [x] bounded NEX stream parser checkpoint exists;
- [x] exact operational Term representation frozen and validated by Stage 5.11 v0.3;
- [ ] exact full-codec interface/result contract frozen;
- [ ] full-codec development + hold-out workloads preregistered;
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

The immediate next action is **Gate 1**: freeze the exact full-codec interface/result contract against accepted `meta-representation-v0.3`.

No `decodeTerm` or `encodeTerm` implementation should be executed before Gate 1 and Gate 2 are committed and reviewed.
