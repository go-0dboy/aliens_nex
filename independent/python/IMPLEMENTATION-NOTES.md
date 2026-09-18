# Independent implementation notes

## Term representation

The six Core constructors are immutable Python dataclasses: `Var`, `Lam`, `App`, `Let`, `Nat`, and `Prim`. Python `int` is used only as the host representation of mathematical arbitrary-precision naturals and indices.

## Wire decoder

The decoder operates on exact strings of `0`/`1` bits. `decode_one` returns `(term, consumed_bits)` and `decode_exact` additionally rejects trailing bits. Integer-bit-length, term-depth, and node-count limits are optional host resource guards; limit refusal has a separate exception class from malformed/truncated/trailing input.

## Scope validation

Scope is represented by a mathematical binder depth, not by a bounded index type. `Lam.body` increments depth. `Let.value` uses the outer depth, while `Let.body` increments it by one.

## Type representation

Types are immutable nodes for variable, unit, natural, function, product, and sum. Environments are lists of type schemes with the nearest de Bruijn binding first. Substitutions are maps from internal integer IDs to monotypes.

Primitive type-scheme variables use private negative IDs; inference-generated fresh variables use non-negative IDs. This avoids accidental aliasing while keeping internal numbering non-observable. Successful top-level types are generalized and rendered by first occurrence according to `OBSERVATIONS.md`.

## Inference strategy

The checker uses an Algorithm-W-style recursive inference procedure with explicit substitutions, free-variable calculation, fresh instantiation, let-generalization, structural unification, and occurs check. A closed-scope pass is run before inference.

## Evaluator runtime model

The evaluator uses environments plus **non-memoizing delayed thunks**, intentionally implementing call-by-name rather than call-by-need. Lambdas are closures. Unsaturated primitives are runtime function values carrying delayed arguments. Pairs and sum constructors carry delayed fields/payloads.

Selective forcing is encoded directly in primitive rules: `pair`/`inl`/`inr` force nothing; projections force only the selected field after exposing the constructor; `ifz` forces only the discriminant and selected branch; `case` forces the sum and selected function while preserving payload laziness.

`fix` is represented by a dedicated recursive thunk that re-applies the delayed function to a fresh recursive occurrence when demanded. No reduction occurs under a lambda before application.

## Resource limits

Evaluation has implementation-specific maximum-step and depth guards. Exceeding them raises `EvaluationResourceLimitError`; it is not treated as malformed input, scope/type invalidity, unknown primitive, a normal result, or proof of divergence. A host `RecursionError` is also translated into the same resource-refusal class.
