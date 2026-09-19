# Stage 5.12b — N-only pair/sequence execution experiment

**Date:** 2026-09-19  
**Status:** measured checkpoint  
**Core:** NEX-1 v0.1 unchanged  
**Candidate:** `pow2-adic-pair-v0.1 / nat-sequence-v0.1`

## Question

The Stage 5.11 meta-representation uses only the NEX natural-number carrier `N` for finite meta-objects. Its basic product encoding is:

```text
pair(a,b) = 2^a * (2*b + 1) - 1
```

and finite sequences use:

```text
nil = 0
cons(head,tail) = 1 + pair(head,tail)
```

The representation is mathematically injective and was already bounded-round-trip checked at 5.11. The new question is operational:

> Is this representation practical enough to serve as the data foundation for a NEX-written wire codec under the existing evaluation strategies?

## Executable artifact

Stage 5.12b adds seven closed canonical NEX-1 terms:

```text
meta_pair
v2
unpair_left
unpair_right
seq_cons
seq_head
seq_tail
```

Their exact wire representations are frozen in:

```text
stage5/selfhost/meta-sequence-v0.1.json
```

The readable generator is engineering notation only:

```text
stage5/selfhost/build_meta_sequence.py
```

The seven terms occupy 3,290 canonical bits when counted independently. This is an engineering measurement, not `B | A`, not `C | A`, and not the size of the future integrated implementation.

## Method

The same 37 bounded applications were executed through:

1. the frozen independent Python call-by-name evaluator;
2. the Go normative call-by-name evaluator with transition/depth statistics;
3. the existing experimental Go call-by-need evaluator with memoization statistics.

Budgets:

```text
Python CBN max steps       5,000,000
Python CBN max depth             700
Go CBN max transitions    5,000,000
Go CBN max depth               20,000
Go need max transitions   5,000,000
Go need max depth              20,000
```

Resource refusal remains distinct from malformed input, static invalidity, semantic mismatch, and proof of divergence.

The full generated measurement report from GitHub Actions run `35428386585` has SHA-256:

```text
3ed5a2d7cab8fe85133934cb442999941dec41f5112baa78863acacb74a9bd9d
```

A durable compact summary is stored in:

```text
stage5/selfhost/meta-sequence-measurement-summary-v0.1.json
```

## Results

```text
measurement cases                    37
Python CBN resource refusals          8
Go CBN resource refusals              5
Go call-by-need resource refusals     0
portable mismatches on returned values 0
```

Go CBN exhausted the 5,000,000-transition budget on:

```text
meta_pair(2,3)
meta_pair(3,2)
unpair_left(39)
unpair_right(39)
seq_cons(1,6)
```

The strongest successful contrast was:

```text
unpair_right(27)
CBN transitions       4,857,667
call-by-need              1,793
ratio                  ~2709.24x
```

Other representative successful cases:

```text
unpair_left(27)   219,662 vs 1,128   ~194.74x
seq_tail(26)      593,517 vs 1,377   ~431.02x
seq_head(26)       21,708 vs   834    ~26.03x
```

All 37 call-by-need cases completed with the expected `Nat` observation. Whenever call-by-name returned a value, it agreed with the mathematical contract and with call-by-need.

## Interpretation

### Verified

- the seven generated objects are closed canonical NEX-1 v0.1 terms;
- their principal types match the declared contracts;
- all returned observations match the mathematical pair/sequence contract;
- the Go sharing evaluator completed every bounded case under the declared budget;
- historical Stage 5 and Stage 4 regression gates remain green on the measurement head.

### Inferred

The N-only representation is still a valid expressiveness construction, but naive normative call-by-name execution is already operationally poor on small encoded values. Sharing changes the practical feasibility by orders of magnitude on the tested cases.

### Not established

This experiment does **not** establish:

- that NEX-1 Core is defective;
- that the representation is globally optimal or globally impractical;
- a NEX-specific proof that every call-by-need implementation preserves CBN observations;
- that one Go sharing implementation is sufficient independent evidence for the future NEX-in-NEX toolchain;
- the final 5.20 classification.

## Decision for the next checkpoint

Do not discard `meta-representation-v0.1` merely because the reference CBN evaluator reaches resource limits. That would confuse an implementation-cost result with semantic invalidity.

Do not build the entire self wire codec on the current candidate without additional corroboration either.

Before `encodeU/decodeU` and recursive term-wire processing become the main implementation path, add a second sharing-capable execution control outside the frozen historical Stage 5 implementation and rerun the same frozen 37-case workload. If the sharing result is reproduced, the representation may proceed as a sharing-conditioned engineering basis while the NEX-specific CBN/call-by-need preservation argument remains explicit supporting work.
