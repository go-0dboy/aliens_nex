# Stage 5 self-hosting experiment protocol

**Status:** Frozen protocol v0.1  
**Date:** 2026-09-19  
**Applies from:** Stage 5.12e onward  
**Core:** NEX-1 v0.1 unchanged

## Why this protocol was added

The first Stage 5.12 experiments correctly exposed several different failure modes, but the development loop became too easy to read as benchmark chasing: run a candidate, observe a limit, change the implementation, rerun. The project therefore freezes the experimental rules before executing the next candidate.

The purpose of this protocol is not to make the self-hosting gate pass. It is to make either a positive or a negative result interpretable.

## Historical evidence is not relabeled

Everything already observed before this protocol remains development or historical evidence. In particular:

- the arithmetic foundation is a verified checkpoint;
- the pow2-adic pair/sequence work is a verified expressiveness/resource checkpoint;
- the integer codec is a verified checkpoint;
- the interleaved-pair candidate is rejected under the frozen budgets and its negative result is reproducible;
- `functional-stream-v0.1` is a development candidate that exceeded the Python call-by-need 5,000,000-transition budget on repeat queries at lengths 32 and 128.

None of those already observed cases may later be described as hold-out evidence.

## Frozen resource budgets

The following limits are fixed before the first runtime execution of `functional-stream-v0.2`:

```text
Python call-by-need
  transitions  5,000,000
  depth            8,000

Go call-by-need
  transitions  5,000,000
  depth           20,000

Go normative CBN
  transitions  5,000,000
  depth           20,000
```

These budgets are not increased after seeing a candidate result.

A normative-CBN resource refusal is recorded separately. For the representation experiments it is not by itself a semantic failure, because the existing evidence already shows large operational differences between CBN and sharing implementations. A call-by-need mismatch or refusal is an acceptance failure for the active representation candidate under this protocol.

## Candidate versioning rule

A candidate version is immutable once its frozen workload has been executed.

Allowed after a result:

- documentation corrections;
- a verifier/infrastructure correction that does **not** alter canonical candidate wire, workload inputs, expected semantic observations, or resource budgets.

Not allowed on the same version after a result:

- changing the algorithm;
- deleting a failing input;
- weakening an expected result;
- increasing resource limits;
- replacing a representation detail that affects semantics or cost.

Any such change requires a new candidate version.

## Active candidate at protocol freeze

The active candidate is:

```text
stage5/selfhost/functional-stream-v0.2.json
stage5/selfhost/build_functional_stream_v0_2.py
stage5/selfhost/verify_functional_stream_v0_2.py
```

Its canonical wire already existed before this protocol was committed, but it had **not yet been executed by CI**. The representation remains:

```text
Stream = N -> N
0 = bit 0
1 = bit 1
2 = EOF
```

The only algorithmic change from v0.1 is `repeat`: v0.1 recursively materialized a `cons` chain, while v0.2 performs direct indexed recursion over `(count,index)`.

## Development workload

The tests embedded in `functional-stream-v0.2.json` are explicitly classified as **development/frozen regression workload**. They were inherited from already observed v0.1 work and therefore are not hold-out.

The v0.2 development acceptance conditions are:

1. reproducible artifact generation;
2. exact canonical wire round-trip;
3. frozen principal types reproduced by Python and Go;
4. all fully-applied test cases return the frozen natural observation;
5. Python and Go call-by-need report zero resource refusals under the frozen budgets;
6. Python and Go call-by-need agree on every observation;
7. Go CBN outcomes are measured separately.

## Preregistered hold-out

Before the first runtime execution of v0.2, a separate workload is frozen in:

```text
stage5/selfhost/functional-stream-holdout-v0.1.json
```

The hold-out is not executed until v0.2 first passes its development workload unchanged.

If v0.2 fails the hold-out, v0.2 is rejected. The project must not modify v0.2 and rerun the same hold-out. Any algorithmic successor becomes v0.3 and requires a new hold-out set registered before execution.

This rule prevents the loop:

```text
see hidden failure -> tune same candidate -> retry same hidden cases
```

from being reported as independent confirmation.

## CI tiers

The self-hosting CI is split conceptually into two tiers:

### Active-candidate tier

Fast enough to run on each active-candidate change:

```text
artifact reproducibility
static/type checks
active development workload
Python sharing control
Go sharing control
CBN measurement
```

### Historical/checkpoint regression tier

The expensive historical chain verifies frozen Stage 4/5 evidence and earlier Stage 5.12 checkpoints. It is required at explicit research checkpoints and before merge, but it should not be the feedback loop for every small active-candidate edit.

The distinction changes CI scheduling only. It does not weaken the final merge gate.

## Interpretation rule

The goal is to classify NEX-1 v0.1, not to force a positive outcome.

Valid eventual outcomes remain:

```text
supported
supported_but_impractical
core_limitation_discovered
inconclusive
```

A failed candidate is evidence. It is not permission to change NEX-1 v0.1 for convenience.
