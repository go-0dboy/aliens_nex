# Stage 5.12c — NEX-written self-delimiting integer codec

**Status:** Verified checkpoint  
**Date:** 2026-09-19  
**Core:** NEX-1 v0.1 unchanged  
**Representation basis:** `meta-representation-v0.1` with the sharing feasibility condition from 5.12b

## Question

Can closed canonical NEX-1 terms implement the canonical self-delimiting integer code `U(n)` used by the NEX wire format without delegating encode/decode semantics to the host language?

## Research objects

The exact generated artifact is:

```text
stage5/selfhost/integer-codec-v0.1.json
```

The reproducible construction and verifier are:

```text
stage5/selfhost/build_integer_codec.py
stage5/selfhost/verify_integer_codec.py
```

The six closed NEX functions are:

```text
seq_length
seq_reverse
binary_rev
prepend_zeros
encodeU
decodeU
```

Readable names exist only in generator notation. The measured research objects are their closed canonical NEX-1 wire encodings.

## Frozen result encoding

Internal `Bits` remains the N-only finite-sequence representation from 5.11/5.12b.

`decodeU` returns an N-only result:

```text
Ok(value, rest_bits) = pair(0, pair(value, rest_bits))
Truncated            = pair(1, 0)
MalformedBit         = pair(2, 0)
```

No new primitive, recursive type, byte-array value, host callback, or wire constructor was added.

## Differential controls

The NEX terms are executed by the post-Stage-5 sharing-capable controls. Their outputs are compared with the existing independent Python and Go host implementations of `U(n)`.

The verifier also checks:

- canonical wire round-trip of every generated helper term;
- principal type agreement;
- exact expected N result codes;
- exact `U(n)` bit strings;
- truncated and malformed-bit classifications;
- Go weak-CBN resource outcomes separately from semantic validity.

## Verified CI result

Successful workflow run:

```text
stage5-self-sufficiency run 35429440356
head commit 261e19689d2a2a35b58d7a90064f590cb4510b10
```

Measured checkpoint:

```text
canonical functions                         6
canonical bits, separate terms         11,881
canonical encodeU bits                  3,860
canonical decodeU bits                  4,249
NEX execution cases                        25
Python call-by-need resource refusals       1
Go call-by-need resource refusals           0
Go CBN resource refusals                   13
```

Where the Python sharing control returned a value, its portable observation matched the Go sharing control. Both direct host `U(n)` implementations matched the frozen NEX-written expected results.

## Interpretation

This checkpoint supports the claim that the current Core can express the canonical `U(n)` algorithm and its portable success/error classifications using only existing NEX-1 facilities.

It does **not** establish that the N-only representation is cheap under normative call-by-name. The resource evidence is the opposite: even this small codec already produces many bounded CBN refusals. One Python sharing-control case also exceeds its declared depth budget, while the Go sharing control completes the frozen set.

Those refusals are resource outcomes, not semantic invalidity. The verifier therefore fails on wrong returned values, wire/type mismatches, or disagreement with the host codec controls, but records bounded evaluator refusal separately.

## New contract issue discovered before 5.12d

Attempting to proceed from integer coding to `encodeTerm/decodeTerm` exposed an ambiguity in `meta-representation-v0.1`: the `Term` representation fixed the carrier, tag set, and payload shapes but did not state the exact outer tagged-value formula.

The historical v0.1 artifact is retained unchanged. `meta-representation-v0.2` resolves the ambiguity explicitly as:

```text
tagged(tag, payload) = pair(tag, payload)
```

for every tagged representation family. 5.12d must target v0.2 and its validator rather than silently choosing a formula in implementation code.

## Next step

Implement the canonical NEX term codec over the exact v0.2 representation:

```text
encodeTerm : TermCode -> EncodeResult

decodeTerm : Bits -> DecodeResult
```

with all six constructors, exact canonical wire prefixes, recursive subterm handling, malformed-meta rejection for encoding, and truncated/malformed-bit propagation for decoding.
