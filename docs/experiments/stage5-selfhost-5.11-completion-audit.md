# Stage 5.11 completion audit — representation contract before Stage 5.12 closeout

**Date:** 2026-09-19  
**Status:** Gate 0 closed — Stage 5.11 Complete  
**Core:** NEX-1 v0.1 unchanged

## Question

Before continuing Stage 5.12, verify whether Stage 5.11 satisfies its original representation contract strongly enough to serve as the representation basis required by Stage 5.12 and later self-hosting work.

Strict sequencing remains:

```text
5.11 Complete
  -> 5.12 Complete
     -> 5.13 may begin
```

## Historical state before the audit

`meta-representation-v0.2.json` was substantially complete as a **mathematical N-only representation contract**. It defined finite encodings for:

```text
Bits
Term
Type
Scheme
Substitution
TypeEnvironment
PortableObservation
StaticResult
ToolRequest
ToolResult
```

It also froze the pow2-adic pair, sequence encoding, exact tagged-value encoding, tag sets, canonicality rules, portable result classes, forbidden dependencies, and bounded examples.

The problem was therefore not a missing representation family.

The problem was that later Stage 5.12 evidence had moved to a different operational representation:

```text
v0.2:
  Bits : N
  Term : N
  recursive structure through numeric packing

accepted Stage 5.12e/5.12f path:
  BitStream = N -> N
  Cursor    = N
```

The N-only representations remain mathematically valid historical evidence, but recursive numeric packing was not the accepted practical path.

## Resolution — operational v0.3

The audit is closed by:

```text
stage5/selfhost/meta-representation-v0.3.json
stage5/selfhost/validate_meta_representation_v0_3.py
docs/experiments/stage5-selfhost-meta-representation-v0.3.md
```

v0.3 freezes two functional finite carriers:

```text
FiniteBits      = (N -> N) * N
FiniteNatTokens = (N -> N) * N
```

`FiniteBits` preserves the accepted `0/1/EOF` bit-stream semantics with exact length.

Recursive internal meta-data use canonical natural-token streams rather than one recursively packed natural.

### Operational Term

```text
Var(k)   -> [0,k]
Lam(t)   -> [1] ++ t
App(a,b) -> [2] ++ a ++ b
Let(v,b) -> [3] ++ v ++ b
Nat(n)   -> [4,n]
Prim(p)  -> [5,p]
```

This is a complete prefix token tree. Child addressing uses token cursors and structural skip. The contract explicitly requires Stage 5.12 `decodeTerm` to transform canonical wire bits into these tokens and `encodeTerm` to reconstruct canonical wire from the tokens; an opaque wire identity shortcut is forbidden.

### Other required roles

Exact token grammars are frozen for:

```text
Type
Scheme
Substitution
TypeEnvironment
PortableObservation
StaticResult
ToolRequest
ToolResult
```

A separate first-class runtime-state object is not required by Stage 5.11. A substitution-based evaluator may operate on `Term`. If Stage 5.15 later needs extra closure/environment state, a new versioned representation must be frozen before that state is used.

## Verification

The v0.3 validator checks:

- NEX-1 v0.1 constructor/type/primitive dependencies unchanged;
- semantic tags unchanged from v0.2;
- exact functional carrier types;
- all ten required representation families;
- exact Term and Type grammars;
- anti-identity Term/wire rule;
- canonicality and equality rules;
- bounded examples;
- complete generated Term class for 1–4 nodes under the frozen leaf set;
- token round trips;
- canonical-wire reconstruction;
- bounded injectivity/no collisions;
- forbidden dependencies;
- explicit future version gate for any extra runtime state.

The v0.3 candidate passed both `accepted-checkpoint` and `selfhost-contract` in workflow run `35436125965` before promotion to accepted status. The accepted-status artifact remains wired into the same mandatory CI validator.

## Stage 5.11 completion gate

- [x] historical v0.1 preserved;
- [x] exact v0.2 numeric/tagged contract preserved and validated;
- [x] practical failure modes of recursive numeric representation recorded;
- [x] functional BitStream feasibility established on frozen development + hold-out evidence;
- [x] operational v0.3 reconciles Bits/Term with the successful functional-stream path;
- [x] v0.3 covers every representation role required by the current 5.10–5.20 self-hosting contract;
- [x] exact canonicality/equality/error rules frozen;
- [x] machine-readable validation and bounded examples exist;
- [x] no hidden Core/host dependency introduced;
- [x] additional runtime-state needs are explicitly version-gated rather than silently assumed.

## Audit decision

**Stage 5.11 is Complete.**

Historical v0.1/v0.2 remain unchanged as evidence. v0.3 supersedes them only for active operational self-hosting work.

This completion does not imply that Stage 5.12 is complete. The next permitted work is Gate 1 onward in `docs/STAGE-5.12-CLOSEOUT.md`: freeze the exact full-codec interface/workloads, then implement and verify NEX-written `decodeTerm` and `encodeTerm` against the accepted v0.3 `Term` representation.

Stage 5.13 remains Planned and blocked until Stage 5.12 is Complete.
