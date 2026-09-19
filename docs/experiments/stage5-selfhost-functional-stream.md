# Stage 5.12e — fixed-type functional stream candidates

**Status:** v0.1 rejected on frozen development budget; v0.2 frozen and not yet runtime-executed  
**Date:** 2026-09-19  
**Core:** NEX-1 v0.1 unchanged

## Motivation

Two N-only recursive-data strategies exposed complementary problems:

1. pow2-adic pairing is executable for small objects but recursive AST codes can explode in bit length because a subtree code becomes an exponent;
2. bit interleaving keeps recursive codes compact but needs repeated parity/halving over the packed natural and hits the frozen sharing depth budget on moderate examples.

Before treating this as a Core limitation, the project tests a representation that uses higher-order functions already present in NEX rather than packing recursive data into one `N`.

## Shared representation contract

A finite bit stream is represented by the fixed HM type:

```text
Stream = N -> N
```

with the semantic convention:

```text
0 = bit 0
1 = bit 1
2 = EOF
```

For a valid finite stream, indices before its end return 0 or 1, and the end index plus all later indices return 2.

The basic functions are ordinary NEX terms:

```text
nil  : N -> N
cons : N -> (N -> N) -> (N -> N)
head : (N -> N) -> N
tail : (N -> N) -> (N -> N)
drop : N -> (N -> N) -> (N -> N)
```

`nil` actually has the more general principal scheme `forall T0. T0 -> N`; this is ordinary rank-1 HM polymorphism and it instantiates to `N -> N` when used as a stream.

No recursive type is required because every stream has the same simple function type.

## v0.1 — cons-chain producer

Artifacts:

```text
stage5/selfhost/build_functional_stream.py
stage5/selfhost/functional-stream-v0.1.json
stage5/selfhost/verify_functional_stream.py
stage5/selfhost/verify_functional_stream_v0_1_result.py
```

The artifact freezes 10 closed canonical NEX terms occupying 1,808 bits when counted separately.

Its recursive producer constructs a runtime chain conceptually equivalent to:

```text
repeat(bit,count) =
  if count == 0 then nil
  else cons(bit, repeat(bit,count-1))
```

The candidate is structurally reproducible and typeable, but the frozen development workload produces four Python call-by-need transition refusals at the unchanged 5,000,000-transition budget:

```text
repeat(0,32)(31)
repeat(0,32)(32)
repeat(1,128)(127)
repeat(1,128)(128)
```

Each reaches transition `5,000,001 > 5,000,000`.

This is recorded as a negative runtime result for v0.1. The limits are not raised and the failing cases are not deleted.

## v0.2 — direct indexed producer

v0.2 keeps the same `Stream = N -> N` contract and the same already observed development workload, but changes only the implementation of `repeat`.

Conceptually it computes a queried index directly:

```text
repeat(bit,count)(i) =
  if count == 0 then EOF
  else if i == 0 then bit
  else repeat(bit,count-1)(i-1)
```

It therefore does not first materialize a recursive `cons` chain.

Artifacts:

```text
stage5/selfhost/build_functional_stream_v0_2.py
stage5/selfhost/functional-stream-v0.2.json
stage5/selfhost/verify_functional_stream_v0_2.py
```

The 10 effective terms occupy 1,634 bits when counted separately. The two changed terms are:

```text
stream_repeat  134 bits   (v0.1: 221)
repeat_query   236 bits   (v0.1: 323)
```

At the time the experiment protocol was frozen, v0.2 had **not yet been runtime-executed by CI**.

## Anti-tuning protocol

The rules are frozen in:

```text
stage5/selfhost/experiment-protocol-v0.1.json
docs/experiments/stage5-selfhost-experiment-protocol.md
stage5/selfhost/validate_experiment_protocol.py
```

Important consequences:

- all cases seen before the protocol, including the v0.1/v0.2 embedded workload, are development evidence and are never relabeled as hold-out;
- Python need remains limited to 5,000,000 transitions / depth 8,000;
- Go need and Go CBN remain limited to 5,000,000 transitions / depth 20,000;
- limits are not increased after observing a result;
- a failed case is not removed from the same candidate version;
- verifier-only fixes are allowed only if candidate wire, workload, expected results and budgets are unchanged;
- an algorithmic change after execution requires a new candidate version.

## Preregistered hold-out for v0.2

Before v0.2's first runtime execution, 11 additional `repeat_query` cases were frozen in:

```text
stage5/selfhost/functional-stream-holdout-v0.1.json
```

They are intentionally **not** part of the development run.

The procedure is:

```text
v0.2 frozen development workload
        |
        +-- fail -> reject v0.2
        |
        +-- pass -> keep artifact unchanged
                    -> execute preregistered hold-out once
                         |
                         +-- fail -> reject v0.2; successor must be v0.3 with new hold-out
                         +-- pass -> accept this representation checkpoint provisionally
```

This prevents the same hidden workload from being used repeatedly to tune the same candidate.

## Acceptance meaning

Passing v0.2 development plus hold-out would establish only that dynamically sized finite bit data can be represented and queried with existing rank-1 HM functions/closures under the frozen sharing budgets.

It would **not** establish complete self-hosting, and it would not yet prove that the representation is appropriate for `Term`, HM environments, substitutions, or evaluator state.

If v0.2 is accepted, the next representation experiment may build a cursor/parser layer over functional streams rather than first converting canonical wire into a recursively packed natural-number AST.

If v0.2 is rejected, the exact barrier remains evidence for the eventual Stage 5.20 outcome; it does not authorize a NEX-1 v0.1 Core change.
