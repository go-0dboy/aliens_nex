# Stage 5.12d result — bit-interleaving pair is not the primary representation

**Status:** Negative result, reproduced  
**Date:** 2026-09-19  
**Core:** NEX-1 v0.1 unchanged

The bit-interleaving candidate solved the recursive **code-size** pathology of the earlier pow2-adic pair, but it did not satisfy the pre-registered runtime acceptance rule under the frozen sharing budgets.

## Frozen evidence

Machine-readable result:

```text
stage5/selfhost/interleaved-pair-result-v0.1.json
```

Candidate and verifier:

```text
stage5/selfhost/interleaved-pair-v0.1.json
stage5/selfhost/verify_interleaved_pair.py
stage5/selfhost/verify_interleaved_pair_result.py
```

The raw candidate verifier is intentionally strict and exits non-zero when the acceptance rule is violated. The result verifier accepts only the exact frozen negative surface, so CI cannot become green because of an unrelated error.

## Measured result

```text
canonical functions                         3
canonical bits, separate terms          1,531
execution cases                            27
Python call-by-need resource refusals       6
Go call-by-need resource refusals           4
Go CBN resource refusals                   14
Python/Go need values compared             21
portable mismatches on returned values      0
```

Go call-by-need refused exactly:

```text
meta_pair_interleaved(27,39)
meta_pair_interleaved(95,111)
unpair_left_interleaved(14847)
unpair_right_interleaved(14847)
```

All four reached the frozen depth boundary:

```text
20001 > 20000
```

Python call-by-need additionally refused `unpair_left/right(2415)` at its smaller frozen depth boundary `4001 > 4000`.

## What the experiment says

The candidate's compactness result is real:

```text
(95,111): pow2-adic 103 bits -> interleaved 14 bits
(111,1):  pow2-adic 113 bits -> interleaved 13 bits
```

But accessing those compact numeric codes still requires derived parity and halving operations. In NEX-1 v0.1 these are ultimately constructed from `succ`, `pred`, `ifz`, and recursion. The measured runtime therefore grows with the numeric code strongly enough to hit the frozen sharing depth bound on moderate examples.

This is **not** a semantic counterexample: every returned result matched the independent mathematical oracle, and Python/Go sharing observations agreed wherever both returned.

It is also **not yet** a proof that the Core is insufficient. It rejects one representation strategy as the primary practical self-hosting basis.

## Decision

Do not promote bit interleaving to `meta-representation-v0.3`.

The next experiment changes representation class rather than changing the numeric pairing function again: finite data is represented by fixed-type functions/closures.

Initial bit stream candidate:

```text
Stream = N -> N
0/1    = data
2      = EOF
```

This avoids both recursive numeric pairing and a recursive Core type. If dynamic construction, tail/drop, and long finite streams work under the existing rank-1 HM checker and evaluators, it provides a new route to self wire parsing without packing the entire structure into one natural number.
