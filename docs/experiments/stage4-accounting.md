# Stage 4.7 — Total-information accounting model

Status: experimental accounting model; refined after the Stage 5 literature re-audit.

## Objective

Keep the project goal

```text
C = S + B + P
```

useful without substituting convenient host-language quantities for unknown transmitted information.

The terms are:

```text
P  canonical program payload under an established NEX wire contract
S  transmitted specification / semantic contract
B  transmitted bootstrap needed to reconstruct/check/execute the representation
R  host reference implementation proxy, diagnostic only
```

## Post-Stage-5 clarification

`C = S + B + P` is a conceptual ledger, not an unconditional machine-free information scalar. Description length is meaningful only relative to an explicit interpretation/description framework [SRC-0016, SRC-0017, SRC-0019].

The preferred exact form is therefore:

```text
C | A = |M_A|
```

where `M_A` is one concrete transmitted object under declared receiver assumptions `A`.

If that object can be partitioned into disjoint transmitted roles:

```text
C | A = (S | A) + (B | A,S) + (P | A,S,B)
```

If specification and executable bootstrap are inseparable:

```text
C | A = (SB | A) + (P | A,SB)
```

Every transmitted bit is counted exactly once.

## P — exact conditional program payload

For a fixed corpus and the already-established NEX-1 v0.1 wire contract, `P` is exact: it is the sum of canonical wire bit lengths emitted by the normative encoder.

Thus Stage 4's `P = 1371 bits` for corpus v0.3 remains exact. The correction is interpretive: this is a description length **under the NEX wire contract**, not a machine-free absolute information quantity.

## S — specification proxy, not accepted transmission cost

No receiver-neutral transmission encoding of the NEX prose/formal specification has been defined. Stage 4 records UTF-8 Markdown size only as a transparent host-document proxy.

Markdown, English, UTF-8, notation, and URLs cannot be silently assumed by an unknown receiver, so this byte count is not accepted as `S | A`.

## R — reference implementation proxy

Stage 4 records the UTF-8 byte size of an explicit Go source manifest implementing the Core path. This value remains `R`, not `B`.

Go syntax, `math/big`, compiler/runtime, garbage collector, standard library, ABI, and host semantics are not receiver-neutral bootstrap assumptions.

Therefore:

```text
R != B
```

and no conversion factor is assumed.

## B — unknown until a dependency-closed bootstrap exists

Stage 5 preserved this conclusion and strengthened it with explicit receiver profiles. There is still no accepted complete receiver-neutral bootstrap artifact, so no full `B | A` or total `C | A` is numerically known.

The corrected receiver taxonomy is maintained in `stage5/receiver-assumptions/assumptions-v0.2.json` and ADR-0014.

## Comparing designs

For two designs under the **same declared receiver profile and compatible accounting boundary**:

```text
Delta C | A = Delta S | A + Delta B | A + Delta P | A
```

A repeated-program break-even may be written only after the corresponding setup terms are represented consistently. Cross-profile numeric comparisons are not total-cost rankings unless differing priors are themselves normalized or priced.

Examples:

- root-type transmission adds program bits; it is a total win only if a real checker/bootstrap reduction compensates for them;
- BLC saves 7 bits on the three-program pure-lambda subset, but relative setup/bootstrap costs are not measured;
- call-by-need changes no program bits and its evaluator-transition reduction is not a transmission-cost term.

## Machine-readable report

`reference/go/cmd/nexaccount` remains a Stage 4 report for:

- exact corpus `P`;
- raw specification proxy;
- explicit Go reference proxy `R`;
- `B.known = false`;
- `total_C_computable = false`.

It intentionally prevents an unknown bootstrap from being represented as zero.

## Reproduction

From `reference/go/`:

```sh
go run ./cmd/nexaccount \
  -corpus ../../benchmarks/corpus-v0.3.json \
  -repo-root ../.. \
  -pretty=false
```

The original numeric report remains a valid Stage 4 artifact. ADR-0016 and Stage 5's corrected receiver model refine only its interpretation.
