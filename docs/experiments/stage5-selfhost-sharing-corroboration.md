# Stage 5.12b — second sharing-control corroboration

**Date:** 2026-09-19  
**Status:** verified checkpoint  
**Core:** NEX-1 v0.1 unchanged

## Purpose

The first 5.12b measurement showed that the N-only pow2-adic pair/sequence representation is executable but very expensive under pure call-by-name, while the Go call-by-need control completed all 37 frozen cases.

Because one sharing implementation is weak evidence for an implementation-strategy conclusion, a second memoizing evaluator was implemented in Python under:

```text
stage5/selfhost/python_need.py
```

It is deliberately outside `independent/python`. The historical Stage 5 independent implementation remains frozen and unchanged.

## Frozen workload

The exact same 37 pair/sequence cases and canonical NEX terms from the first 5.12b run were reused. No cases were removed or weakened after seeing the first result.

The updated full report from workflow run `35428624295` has SHA-256:

```text
4f6baafe007f785f2a274abd6905f4961dfa49b3eabebe85835c32d51f58683b
```

Durable compact result:

```text
stage5/selfhost/meta-sequence-measurement-summary-v0.2.json
```

## Result

```text
measurement cases                     37
Python CBN resource refusals           8
Python call-by-need refusals            0
Go CBN resource refusals               5
Go call-by-need refusals                0
Python/Go need observation mismatches   0
```

Both memoizing implementations returned the expected portable `Nat` observation on every frozen case.

The transition counters are implementation-specific and should not be expected to match numerically. The relevant portable result is that the two independently implemented runtime controls agree on all 37 returned observations and neither reaches the declared resource budget.

## Decision

The Stage 5.11 N-only representation is retained as the working 5.12 representation **with an explicit sharing condition for practical execution**.

This decision means:

- proceed to NEX-written `encodeU/decodeU` and term-wire processing using the frozen representation;
- continue recording pure-CBN resource outcomes rather than hiding them;
- keep call-by-need as an implementation strategy, not a new Core semantics;
- do not claim a formal CBN/call-by-need equivalence theorem from this experiment;
- do not classify the CBN cost as a Core defect.

The later 5.19 metatheory work still owes a NEX-specific observational-preservation argument for allowed sharing implementations.
