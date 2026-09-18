# Stage 5 differential conformance

This directory compares the frozen independent Python reconstruction against the existing Go reference **after** the independent checkpoint has been frozen.

The comparison is intentionally limited to portable observations:

- canonical wire bits;
- principal type scheme or portable static error class;
- observable WHNF or portable evaluation error class.

It does **not** compare runtime representation, fresh-variable IDs, transition counts, allocation behavior, closure/thunk layout, or other implementation details.

`run.py` executes four deterministic groups:

1. the frozen Stage 4 corpus v0.3 (17 programs, including inherited v0.1 programs);
2. generated closed/well-typed templates covering naturals, functions, `Let`, pairs, sums and conditionals;
3. generated single-defect static cases for scope, unknown primitives, mismatch and occurs check;
4. generated arbitrary well-shaped wire terms, including large naturals/indices/primitive IDs, supplied to the Go side as encoded bits to exercise independent decoding.

A semantic/portable mismatch is a failing result. If one implementation reaches a finite implementation resource limit while the other produces a result, the runner records a `resource_asymmetry` rather than relabeling it as a language-semantic mismatch. Such asymmetries remain research findings and must be reviewed.

Run from the repository root after materializing the frozen packet into `independent/python/packet`:

```bash
python stage5/differential/run.py --report /tmp/nex-stage5-differential.json
```
