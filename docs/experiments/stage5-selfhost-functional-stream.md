# Stage 5.12e — fixed-type functional stream candidates

**Status:** v0.1 rejected on frozen development budget; v0.2 passed frozen development and preregistered hold-out workloads  
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
stage5/selfhost/functional-stream-v0.2-development-result-v0.1.json
stage5/selfhost/functional-stream-v0.2-holdout-result-v0.1.json
```

The 10 effective terms occupy 1,634 bits when counted separately. The two changed terms are:

```text
stream_repeat  134 bits   (v0.1: 221)
repeat_query   236 bits   (v0.1: 323)
```

At the time the experiment protocol was frozen, v0.2 had **not yet been runtime-executed by CI**.

### First runtime execution after protocol freeze

Workflow run `35432007845`, job `105868178140`, executed v0.2 only after the protocol and the separate hold-out file had already been committed.

The candidate artifact was unchanged after freeze. Result:

```text
canonical functions                         10
canonical bits, counted as separate terms  1,634
execution cases                              26
Python call-by-need resource refusals         0
Go call-by-need resource refusals             0
Go CBN resource refusals                      0
Python/Go need values matched               26/26
```

Largest measured sharing costs:

```text
repeat(1,128)(127)
Python need transitions  13,855
Go need transitions       6,418
frozen transition limit 5,000,000
```

Thus v0.2 passes the previously observed development workload under the frozen budgets. This remains development evidence, not hold-out evidence.

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

The candidate Git blob SHA was frozen as:

```text
7f35e453b7234e9078cf7cf2ca1e962b32e4ed3d
```

and the hold-out blob SHA as:

```text
3ca4ccb6406b5ab7f30edb005a55e2a139b2b8a5
```

After the development pass, the historical checkpoint regression completed successfully, including reproduction of the earlier negative interleaving and functional-stream-v0.1 results. The unchanged v0.2 candidate was then evaluated exactly once against the preregistered hold-out by workflow run `35432186658`, job `105868647658`.

Result:

```text
hold-out cases                              11
Python call-by-need resource refusals        0
Go call-by-need resource refusals            0
Go CBN resource refusals                     0
Python/Go need values matched              11/11
```

Largest hold-out costs:

```text
repeat(1,127)(126)
Python need transitions  13,747
Go need transitions       6,368
frozen transition limit 5,000,000
```

No candidate wire, hold-out input, expected semantic observation, or resource budget was changed between preregistration and execution.

## Decision at this checkpoint

`functional-stream-v0.2` is **accepted provisionally as the finite-bit-stream representation checkpoint for the tested surface**.

What this supports:

- dynamically sized finite bit data can be represented with the fixed rank-1 HM type `N -> N`;
- stream-producing and stream-transforming programs can be written in unchanged NEX-1 v0.1;
- on the frozen development and preregistered hold-out workloads, both sharing controls and the Go CBN control return the expected observations without resource refusal;
- the previous failures were properties of the tested numeric/cons-chain representations, not evidence that dynamically sized finite data is impossible in the Core.

What this does **not** establish:

- complete `Term` decoding or encoding;
- a practical representation for type environments, substitutions, or evaluator state;
- complete self-hosting;
- a NEX-specific proof that call-by-need preserves all CBN observations;
- receiver-neutral bootstrap or any new value for `B | A` or `C | A`.

## Next experiment

The next Stage 5.12 experiment should build a cursor/parser layer directly over the accepted stream interface rather than first packing the whole recursive syntax tree into one natural number.

Before implementation, that parser experiment must freeze:

1. the exact parser/cursor interface and result representation;
2. development inputs and expected observations;
3. resource budgets;
4. a separate hold-out set that is not executed during development;
5. the rule for versioning any algorithmic change after the first execution.

Only after those items are committed should parser code be executed for acceptance evidence.
