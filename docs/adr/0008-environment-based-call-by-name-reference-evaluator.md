# ADR-0008: Use an environment-based weak call-by-name reference evaluator

**Status:** Accepted  
**Date:** 2026-09-18

## Context

NEX-1 v0.1 already specifies weak call-by-name evaluation and explicitly permits implementations to avoid literal substitution by using environments, closures, explicit substitutions, graph reduction, or call-by-need.

Stage 3 needs one executable reference model. Literal de Bruijn substitution is possible but would mix evaluator correctness with index shifting/capture machinery and would make laziness harder to inspect. A call-by-need heap would be faster but would introduce sharing/mutation into the first evaluator even though memoization is only an allowed optimization, not the normative reference strategy.

The evaluator must also support non-strict `Let`, lazy products/sums, partial primitive application, and `fix`.

## Decision drivers

- stay close to the normative weak call-by-name strategy;
- preserve exact de Bruijn binder behavior without capture-prone substitution;
- make delayed evaluation explicit and testable;
- keep call-by-need memoization out of the first correctness oracle;
- keep runtime structures entirely outside the wire format;
- provide a model that can later be compared with an optimized lazy machine.

## Decision

The first NEX reference evaluator will be environment-based and non-memoizing.

Its conceptual runtime uses:

```text
Environment   ordered nearest de Bruijn binder first
Thunk         suspended Term + Environment
Closure       lambda body + Environment
Value         weak-head runtime result
```

A lambda application evaluates the function position to a callable WHNF, then extends the closure environment with a thunk for the unevaluated argument.

`Var(k)` demands the `k`-th runtime binding. Because the reference evaluator is call-by-name, demanding the same thunk again re-evaluates it rather than returning a memoized result.

`Let(value, body)` is dynamically non-strict: evaluation proceeds with `body` under an environment extended by a thunk for `value`. This is operationally equivalent to non-strict substitution while preserving `Let` as a distinct term for HM typing.

Runtime constructor values keep fields/payloads delayed:

```text
PairValue(leftThunk, rightThunk)
InlValue(payloadThunk)
InrValue(payloadThunk)
```

Primitives are curried runtime functions represented with their already supplied delayed arguments until their arity is reached.

## Primitive forcing decision

The reference evaluator forces only what is necessary to expose the rule result:

- `succ` / `pred`: force their numeric argument;
- `ifz`: force the discriminant and only the selected branch;
- `pair`: force neither field;
- `fst` / `snd`: force the pair constructor and only the selected field;
- `inl` / `inr`: force no payload;
- `case`: force the sum constructor and only the selected branch function;
- `fix`: apply the function to a delayed recursive fixed-point expression;
- `unit`: immediate unit value.

Partial primitive applications are function WHNFs.

## Accepted consequences

- The implementation is intentionally not optimized for repeated thunk use.
- Runtime environments/closures/thunks exist only in the reference implementation and are not NEX wire objects.
- De Bruijn lookup is direct and no runtime name resolution is required.
- Laziness can be tested explicitly using divergent unused arguments/branches.
- A later call-by-need implementation can share the same conformance vectors but needs separate implementation reasoning.

## Alternatives considered

### Literal de Bruijn substitution

Rejected for the first reference evaluator. It is closer to the textbook beta rule syntactically, but requires shifting/substitution code whose correctness is orthogonal to the semantic questions Stage 3 is trying to expose.

### Call-by-need from the start

Deferred. Launchbury and Sestoft provide strong foundations for lazy evaluation with sharing [SRC-0012, SRC-0013], and v0.1 permits memoization when observable results are unchanged. However, adding heap update/sharing to the initial oracle would make the reference implementation more complex than the normative call-by-name strategy.

### Call-by-value

Rejected because it contradicts the accepted v0.1 evaluation strategy and would change observable termination behavior, including `ifz`, lazy pairs, and ignored function arguments. Plotkin's call-by-name/call-by-value distinction is relevant background [SRC-0011].

## Evidence / references

- [SRC-0011] Plotkin 1975: call-by-name versus call-by-value operational distinction.
- [SRC-0012] Launchbury 1993: natural semantics for lazy evaluation with sharing.
- [SRC-0013] Sestoft 1997: lazy abstract machine derived from Launchbury; comparison to call-by-name Krivine-style evaluation.

These sources provide theory and implementation precedent. They do not define NEX primitive forcing rules; those rules are NEX project decisions derived from the existing v0.1 reduction intent.

## Follow-up validation

Stage 3 must prove through language-neutral vectors that:

- ignored lambda arguments can diverge without affecting the result;
- `Let` is non-strict;
- pair fields and sum payloads are delayed;
- unselected `ifz`/`case` branches are not evaluated;
- a memoizing implementation, if added later, agrees on observable Core results.
