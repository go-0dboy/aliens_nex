# Stage 5.12d — Recursive meta-pairing alternatives before Term codec

**Status:** Active experiment  
**Date:** 2026-09-19  
**Core:** NEX-1 v0.1 unchanged

## Why this experiment exists

Stage 5.11 originally selected the bijection:

```text
pair(a,b) = 2^a * (2*b + 1) - 1
```

because it is exact, total, injective, invertible, and implementable over NEX naturals. Stage 5.12b showed that sharing makes small pair/sequence operations executable in practice, and 5.12c successfully built NEX-written `encodeU/decodeU` on that basis.

The next step, `encodeTerm/decodeTerm`, exposes a new requirement that the earlier sequence tests did not stress: pair payloads now recursively contain **already encoded AST subtrees**.

For the pow2-adic bijection, the binary length of `pair(a,b)` is roughly proportional to the *numeric value* of `a`, not merely to the binary length of `a`. Therefore recursive use can turn moderate subtree codes into explosive outer codes.

This is a meta-representation engineering problem, not currently a NEX Core limitation.

## Exact tagged contract issue

`meta-representation-v0.1` fixed the N carrier, tag sets, and payload shapes but did not state the exact outer tagged-value formula. The historical file remains unchanged.

`meta-representation-v0.2` resolves that ambiguity as:

```text
tagged(tag,payload) = pair(tag,payload)
```

and is separately machine-validated. This clarification is necessary before any term codec is meaningful, but it also makes the recursive size issue fully explicit.

## Growth examples under the existing pair

Using the v0.2 Term rule and the existing pair:

```text
Var(0)                         -> small
Lam(Var(0))                    -> small
Nat(3)                         -> 7-bit numeric code
Prim(1)                        -> 7-bit numeric code
App(Lam(Var(0)), Nat(3))       -> about 12-bit numeric code
App(Prim(1), Nat(3))           -> about 106-bit numeric code
Let(Nat(3), Lam(Var(0)))       -> about 117-bit numeric code
```

The sharp jump is not caused by NEX wire prefixes. It comes from using a subtree code as the exponent of two inside the meta-pair.

For a self-processing implementation, deeper left subtrees would compound this effect. Proceeding directly to a full self AST with this representation risks proving only theoretical expressibility while making `code(I)` impossible to materialize under any useful resource bound.

## Candidate alternative: bit-interleaving bijection

The candidate pair maps bits as follows:

```text
result bit 2*i     = bit i of a
result bit 2*i + 1 = bit i of b
```

The inverse simply collects even and odd bit positions.

This is a bijection:

```text
N x N <-> N
```

and its result bit length is bounded by roughly twice the larger input bit length rather than by an input's numeric value.

It is also directly expressible with already-derived NEX operations:

```text
odd
halve
add
fix
ifz
```

No new Core primitive or bitwise primitive is required.

## Frozen executable candidate

Artifacts:

```text
stage5/selfhost/build_interleaved_pair.py
stage5/selfhost/interleaved-pair-v0.1.json
stage5/selfhost/verify_interleaved_pair.py
```

The exact closed NEX candidate functions are:

```text
meta_pair_interleaved        : N -> N -> N
unpair_left_interleaved      : N -> N
unpair_right_interleaved     : N -> N
```

Their generator source notation is engineering-only; the JSON artifact freezes exact canonical NEX wire.

The verifier checks:

- artifact reproducibility;
- canonical wire round-trip;
- principal type agreement;
- an independent host mathematical oracle;
- bounded host round trips;
- Python sharing-control results;
- Go sharing-control results;
- Go normative-CBN resource outcomes separately.

## Pre-registered comparison points

The frozen candidate includes these size contrasts:

```text
(a,b)       pow2-adic pair bits    interleaved pair bits
(1,111)              9                     14
(95,111)           103                     14
(111,1)            113                     13
```

The first case deliberately shows that interleaving is not uniformly smaller. The question is recursive scaling and executable feasibility, not cherry-picked local compression.

## Decision rule

Do **not** switch the active meta-representation merely because the mathematical examples look better.

A successor representation is justified only if:

1. the NEX-written interleaving pair and both inverses are canonical and well-typed;
2. they return the frozen oracle results;
3. at least the Go sharing control completes the frozen candidate workload without semantic mismatch;
4. independent sharing evidence does not contradict it;
5. recursive Term-code size analysis confirms the pow2-adic representation is operationally unsuitable while interleaving avoids the pathological growth;
6. the change is versioned rather than silently modifying v0.1/v0.2 evidence.

If accepted, the next representation version will require rebuilding sequence and integer-codec prerequisites before the final `encodeTerm/decodeTerm` checkpoint. Historical 5.12b/5.12c results remain evidence about the earlier candidate and are not rewritten.
