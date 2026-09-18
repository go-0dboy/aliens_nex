# Stage 4.6 — Call-by-name versus call-by-need

Status: experimental, non-normative.

## Question

Measure whether sharing/memoization can reduce reference-runtime work for the already accepted NEX-1 v0.1 programs without changing their observable Core result.

The experiment does **not** change NEX-1 v0.1 semantics. Weak call-by-name remains the normative reference semantics. Call-by-need is evaluated only as an implementation strategy permitted when it preserves observable results.

## Compared implementations

### Reference CBN

`nex.EvaluateClosedWithStats`:

- environment/closure evaluator;
- non-memoizing thunks;
- weak call-by-name semantics;
- normative Stage 3 reference behavior.

### Experimental call-by-need

`experiment.EvaluateCallByNeed`:

- same Core term grammar and primitive forcing behavior;
- memoizing thunks;
- shared environment bindings;
- explicitly non-normative Stage 4 implementation experiment.

## Correctness gate

For every program in frozen `benchmarks/corpus-v0.3.json`:

1. reference CBN must complete under the accepted default resource budget;
2. experimental call-by-need must complete under the same transition/depth budget;
3. both observations must equal the corpus expected WHNF;
4. therefore both observations must equal each other.

A strategy result is not accepted if this observable agreement gate fails.

## Metrics

Reference-only metrics:

```text
CBN transitions
CBN maximum evaluation depth
call-by-need transitions
call-by-need maximum evaluation depth
call-by-need thunk forces
call-by-need thunk evaluations
call-by-need memo hits
```

Derived metrics:

```text
transition savings = CBN transitions - call-by-need transitions
transition savings percent = savings / CBN transitions
```

These are implementation counters. They are **not** portable NEX Core costs and must not be added directly to transmitted-program bit cost `P`.

## Interpretation limits

- A lower transition count does not prove a smaller bootstrap implementation.
- Memoization requires additional runtime state; Stage 4.7 must account for implementation/bootstrap complexity separately.
- The accepted corpus is small and intentionally frozen; results are evidence for this workload set, not a universal performance theorem.
- The experiment does not make call-by-need normative.

## Reproduction

From `reference/go/`:

```sh
go run ./cmd/nexstrategy -corpus ../../benchmarks/corpus-v0.3.json -pretty=false
```

The same command is part of `verify.sh`; accepted results require a clean-checkout CI pass.
