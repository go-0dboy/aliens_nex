# Stage 4.6 — Call-by-name versus call-by-need

Status: experimental, non-normative.

## Question

Measure whether sharing/memoization reduces work in the project reference evaluator for the already accepted NEX-1 v0.1 programs without changing their portable Core observation.

The experiment does **not** change NEX-1 v0.1 semantics. Weak call-by-name remains normative. Call-by-need is only an implementation strategy permitted when it preserves observable Core results.

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
- explicitly non-normative.

## Correctness gate

For every program in frozen `benchmarks/corpus-v0.3.json`:

1. reference CBN completes under the accepted default resource budget;
2. experimental call-by-need completes under that implementation's accepted budget;
3. both observations equal the corpus expected WHNF;
4. therefore both portable observations agree.

The literature supplies strong precedent for call-by-need preserving call-by-name observational behavior in standard lambda calculi [SRC-0012, SRC-0013, SRC-0023]. That does not by itself prove equivalence for NEX's exact `fix`, naturals, sums/products, and forcing rules; the project result remains experimental until a NEX-specific proof exists.

## Metrics

Reference-implementation counters:

```text
CBN transitions
CBN maximum evaluation depth
call-by-need transitions
call-by-need maximum evaluation depth
call-by-need thunk forces
call-by-need thunk evaluations
call-by-need memo hits
```

In the current Go implementations, the main `transitions` counter is incremented by the instrumented evaluator step path. Therefore the accepted aggregate result

```text
226151 -> 2484
98.90% reduction
```

means **98.90% fewer counted evaluator transitions under this instrumentation**.

It does **not** mean 98.90% lower wall-clock time, CPU instructions, allocations, peak memory, energy, or bootstrap size. Memoization itself adds state and bookkeeping that the transition counter does not convert into a common physical-work unit.

## Interpretation limits

- Lower transition count does not prove a smaller bootstrap implementation.
- Sharing requires additional runtime state.
- The corpus is small and frozen; results are workload-specific evidence, not a performance theorem.
- The experiment does not make call-by-need normative.
- A formal NEX-specific observational-equivalence theorem is still open.

## Reproduction

From `reference/go/`:

```sh
go run ./cmd/nexstrategy -corpus ../../benchmarks/corpus-v0.3.json -pretty=false
```

The same experiment is included in `verify.sh`; accepted values require a clean-checkout CI pass.
