# Stage 5.12a — First executable NEX-in-NEX arithmetic foundation

## Status

Candidate implementation checkpoint under ADR-0018. This is the first substep of Stage 5.12; it is **not yet the self wire codec**.

Artifacts:

```text
stage5/selfhost/build_foundation.py
stage5/selfhost/foundation-v0.1.json
stage5/selfhost/verify_foundation.py
```

## Problem

The Stage 5.11 N-only meta-representation is useful only if NEX itself can perform the finite natural-number operations required to navigate it. Host arithmetic must not be mistaken for the eventual NEX-in-NEX implementation.

Before implementing `encodeU`, `decodeU`, or recursive term wire processing, Stage 5.12 therefore starts with a small executable arithmetic foundation written entirely as ordinary NEX-1 v0.1 programs.

## Engineering source versus research object

`build_foundation.py` uses readable local names only as generator notation. It lowers those names to zero-based de Bruijn indices and serializes the resulting six-constructor Core terms according to the normative NEX wire grammar.

The generator is not part of the self-hosted implementation. The research objects are the exact canonical bit strings stored in `foundation-v0.1.json`.

The artifact is reproducibility-checked against the generator so a source edit cannot silently change the frozen bits.

## First foundation functions

The candidate contains:

```text
add          : N -> N -> N
mul          : N -> N -> N
odd          : N -> N        # 0 for even, 1 for odd
halve        : N -> N        # floor(n / 2)
pow2         : N -> N        # 2^n
shift_right  : N -> N -> N  # floor(n / 2^k)
```

They use only existing v0.1 constructs, principally `fix`, `succ`, `pred`, `ifz`, `Lam`, `App`, `Let`, and `Nat`.

No arithmetic helper is added as a Core primitive.

## Verification contract

`verify_foundation.py` independently consumes the frozen canonical bits through both existing implementations.

For each foundation function it checks:

1. Python exact decode/re-encode preserves the frozen wire bits;
2. Python infers the expected principal type;
3. Python evaluates fixed small applications to the expected `Nat` observation;
4. Go `nexdiffprobe` decodes/re-encodes the same frozen bits;
5. Go infers the same expected principal type;
6. Go evaluates the same fixed applications to the same expected `Nat` observation.

The tests intentionally remain small. Their purpose is to establish executable building blocks, not to make a performance claim or prove arithmetic correctness for all naturals.

## Research meaning

A successful checkpoint supports only this local statement:

> Several derived natural-number operations needed by the 5.11 representation can be expressed as closed, statically valid canonical NEX-1 programs and agree across the independent Go/Python controls on the declared examples.

It does not establish:

- correctness for all natural inputs;
- efficiency of the N-only representation;
- correctness of `pair/unpair`;
- a self wire codec;
- a self-interpreter;
- self-hosting.

## Resource warning to measure, not hide

The normative Core exposes `succ`, `pred`, and zero testing rather than machine-level bit/arithmetic instructions. Derived arithmetic can therefore cause substantial evaluator work, especially under call-by-name when a computed value is referenced repeatedly.

This is a measurement target for later 5.12/5.18 work. It is not currently classified as a Core defect and is not a reason to introduce new primitives before evidence is collected.

## Next step

After this foundation passes branch-level Go/Python verification, implement and measure the exact meta-pair/sequence operations from `meta-representation-v0.1.json`. Only then freeze the representation as the basis for NEX-written `encodeU/decodeU` and term wire processing.
