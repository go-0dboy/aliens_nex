# ADR-0009: Keep evaluator resource limits separate from NEX semantics and validity

**Status:** Accepted  
**Date:** 2026-09-18

## Context

NEX-1 v0.1 includes `fix`, so valid well-typed programs may diverge. A practical reference implementation and CI suite cannot allow unbounded evaluation to hang the process indefinitely.

The project already made the analogous distinction for wire decoding in ADR-0006: an implementation may refuse a resource-intensive valid input without redefining the wire language as malformed.

Stage 3 needs the same separation for execution.

## Decision drivers

- `fix` intentionally permits nontermination;
- test suites need bounded execution;
- host stack/memory/CPU limits are not Core semantics;
- different conforming implementations may count internal steps differently;
- conformance should compare observable program behavior, not implementation accounting details.

## Decision

Reference evaluation MAY be configured with implementation resource limits such as:

```text
MaxTransitions / fuel
MaxEvaluationDepth
host memory or allocation guards where needed
```

Exceeding such a limit produces a distinct implementation resource-limit refusal.

It MUST NOT be reported as:

```text
malformed wire
scope error
type error
unknown primitive
normal Core result
```

A program that exceeds a configured evaluation limit may still be a valid NEX program and may terminate with larger resources.

A truly diverging program and a terminating-but-expensive program are generally not distinguishable by a finite evaluator run. Therefore a resource-limit refusal MUST NOT claim that the program has been proven divergent.

## Portable conformance rule

The exact transition/fuel counting convention is implementation-specific.

Language-neutral conformance vectors MUST NOT require that two implementations hit a resource limit after the same number of internal steps.

Portable vectors should instead test terminating observable results and laziness cases where an unselected divergent expression must not be demanded.

Implementation-specific tests MAY use a bounded fuel limit to prove that direct recursive loops do not hang CI.

## Accepted consequences

- evaluator APIs must distinguish semantic results from implementation refusal;
- CI can safely exercise `fix` and known looping examples;
- a later optimized evaluator may consume a different number of internal steps while remaining conforming;
- resource metrics can still be benchmarked, but they are measurements rather than semantic truth.

## Alternatives considered

### Define one normative universal step counter

Rejected for v0.1. It would constrain implementation architecture and make environment, substitution, graph-reduction, and call-by-need implementations unnecessarily dependent on one machine-like accounting model.

### Treat fuel exhaustion as divergence

Rejected. Finite exhaustion cannot prove nontermination in general.

### Do not expose evaluator limits

Rejected for the reference implementation because recursive tests could hang indefinitely and make CI unreliable.

## Evidence / references

This ADR is primarily a project engineering/semantics-boundary decision. `fix` and valid divergence are already normative in NEX-1 v0.1. ADR-0006 provides the existing project precedent for separating implementation resource refusal from language validity.

## Follow-up validation

Stage 3 tests must demonstrate both:

```text
ifz 0 42 divergingTerm -> 42
```

without exhausting fuel, and a directly demanded recursive loop that ends only in an explicit evaluator resource-limit refusal under bounded test settings.
