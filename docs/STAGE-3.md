# Stage 3 — Dynamic semantics and evaluator

**Status:** In progress  
**Branch:** `stage3/dynamic-semantics`

Stage 3 begins after wire decoding and static validation are already complete. Its job is to define and implement the observable execution semantics of a valid NEX-1 Core program without expanding into a frontend, optimizer, machine profile, compiler, or self-hosting system.

The target pipeline is:

```text
bits
  -> decode                  Stage 1
  -> Term
  -> static validation       Stage 2
  -> well-typed closed Term
  -> evaluation to WHNF      Stage 3
  -> observable Core result
```

## Stage 3 design baseline

NEX-1 v0.1 keeps the existing reference strategy:

```text
weak call-by-name
```

Arguments are delayed. The reference evaluator does not memoize them. A conforming optimized implementation MAY use call-by-need sharing only if the observable Core result is unchanged.

The first reference evaluator uses an environment-based runtime rather than literal de Bruijn substitution:

```text
Environment   nearest binder first
Thunk         suspended Term + Environment
Closure       Lam body + Environment
Value         WHNF runtime result
```

This runtime representation is an implementation technique. It is not transmitted on the NEX wire.

## Stage 3.0 — dynamic-semantics contract audit

Before evaluator code is treated as authoritative, clarify the existing v0.1 semantics in four places:

1. dynamic behavior of `Let(value, body)`;
2. the WHNF forms observable under weak evaluation;
3. primitive arity, partial application, and argument forcing;
4. separation of divergence from implementation resource-limit refusal.

The audit must update the canonical English specification and Russian mirror before Stage 3 is merged.

### Let

Runtime `Let` is non-strict and operationally behaves like substitution without changing its separate HM typing role:

```text
Let(value, body) -> body[0 := value]
```

An environment implementation extends the body environment with a thunk for `value`; `value` is not evaluated merely because the binding is created.

### Weak-head normal forms

Evaluation is only required to expose the outer computational form. Reference WHNF categories are:

```text
lambda/function closure
natural number
unit
pair constructor with delayed fields
inl constructor with delayed payload
inr constructor with delayed payload
unsaturated primitive function
```

Evaluation does not reduce a lambda body merely because the lambda itself is the result.

### Primitive arities

```text
fix   1
succ  1
pred  1
ifz   3
pair  2
fst   1
snd   1
inl   1
inr   1
case  3
unit  0
```

An unsaturated primitive is a function WHNF. Supplied primitive arguments remain delayed until the saturated primitive rule requires them.

### Primitive forcing contract

| Primitive | Forced arguments | Delayed / unselected parts |
|---|---|---|
| `fix f` | evaluate `f` only as required for ordinary application | recursive argument `fix f` is delayed |
| `succ n` | `n` to a natural | — |
| `pred n` | `n` to a natural | — |
| `ifz n z s` | `n`, then selected branch to the requested WHNF | unselected branch MUST NOT be evaluated |
| `pair a b` | none | both fields remain delayed |
| `fst p` | `p` to pair WHNF, then selected field | unselected field MUST NOT be evaluated |
| `snd p` | `p` to pair WHNF, then selected field | unselected field MUST NOT be evaluated |
| `inl a` | none | payload remains delayed |
| `inr b` | none | payload remains delayed |
| `case s f g` | `s` to sum WHNF; selected function only | unselected function MUST NOT be evaluated |
| `unit` | none | — |

## Stage 3.1 — runtime value, environment, and thunk model

Implement explicit runtime structures for:

```text
Thunk(term, environment)
Closure(body, environment)
NatValue(n)
UnitValue
PairValue(leftThunk, rightThunk)
InlValue(payloadThunk)
InrValue(payloadThunk)
PrimitiveValue(id, suppliedArguments)
```

Reference thunks are non-memoizing. Sharing/memoization is deferred to a later optimization experiment.

The environment order MUST match Stage 2 de Bruijn rules: index `0` is the nearest runtime binder.

## Stage 3.2 — lambda/let evaluator core

Implement weak call-by-name evaluation for:

```text
Var
Lam
App
Let
Nat
```

Core rules:

- `Lam` returns a closure without evaluating its body;
- `App` evaluates only the function position far enough to obtain a callable WHNF;
- a lambda argument is inserted as a thunk without pre-evaluation;
- `Var(k)` evaluates the referenced thunk when demanded;
- `Let(value, body)` extends the body environment with a delayed `value` thunk.

Required examples include:

```text
(\x -> x) 42                -> 42
(\x -> 7) divergingTerm     -> 7
let x = divergingTerm in 7  -> 7
```

## Stage 3.3 — primitive application spine

Extend the authoritative Core primitive metadata so runtime arity belongs to the same source of truth as primitive ID/name/type scheme.

`Prim(id)` and partially supplied primitives are callable runtime values. Primitive execution starts only when arity is reached.

Do not create a second independent primitive-ID table for the evaluator.

## Stage 3.4 — natural/unit primitive execution

Implement and test:

```text
unit
succ
pred
ifz
```

Required laziness vector:

```text
ifz 0 42 divergingTerm -> 42
```

## Stage 3.5 — product and sum execution

Implement and test:

```text
pair
fst
snd
inl
inr
case
```

Required non-strictness examples include:

```text
fst (pair 1 divergingTerm) -> 1
case (inl 5) (\x -> x) divergingFunction -> 5
```

Constructor creation MUST NOT force stored fields/payloads.

## Stage 3.6 — fixed point and divergence

Implement:

```text
fix f -> f (fix f)
```

without pre-evaluating the recursive argument.

General recursion means some valid programs diverge. Reference tests therefore require implementation resource controls so test execution cannot hang forever.

A resource-limit refusal is not a NEX semantic result and MUST NOT reclassify a valid program as malformed or ill-typed.

## Stage 3.7 — language-neutral evaluation conformance

Create `conformance/eval-v0.1.json`.

Vectors compare observable WHNF behavior rather than Go-internal runtime objects. Portable observations include:

```text
Nat(n)
Unit
Lambda/function
Pair constructor
Inl constructor
Inr constructor
```

Function behavior is tested by application rather than by serializing host closures. Lazy fields/payloads are tested by projections/case operations rather than by forcing them merely for comparison.

Required corpus includes:

- beta application;
- non-strict ignored argument;
- non-strict `Let`;
- `succ`/`pred` edge cases;
- both `ifz` branches with divergent unselected alternatives;
- pair projection without forcing the other field;
- both sum branches;
- partial primitive application;
- representative `fix` recursion such as addition/factorial where practical.

## Stage 3.8 — properties, resource controls, fuzzing, and CI

Add deterministic implementation limits such as a transition/fuel budget and/or recursion-depth guard.

The exact internal step-counting convention is implementation-specific and is not a portable Core observable. Cross-implementation conformance therefore MUST NOT depend on an exact number of evaluator steps.

Properties should include where practical:

```text
same validated pure term + sufficient resources -> same observable result
successful evaluation of a Stage-2-valid term does not produce scope/type errors
constructor creation does not force delayed fields
unselected branches remain unevaluated
```

CI must run the normal unit/conformance suite and bounded evaluator fuzz/property checks from a clean checkout.

## Stage 3.9 — completion review

Before Stage 3 is complete:

- canonical English and Russian v0.1 docs contain the clarified dynamic contract;
- environment/thunk/closure reference model is implemented;
- all Core primitives execute according to the forcing table;
- `fix` supports terminating recursive examples and bounded detection/refusal of nontermination in tests;
- language-neutral evaluation vectors pass;
- clean-checkout CI passes;
- the final diff contains no frontend, optimizer, native/bytecode compiler, machine/system profile, mutable-memory system, or self-hosting implementation.

## Reference versus optimized evaluation

Reference Stage 3 is deliberately call-by-name without thunk memoization. This keeps the executable reference close to the normative reduction strategy.

Call-by-need is a permitted optimization candidate because the current specification already allows memoization when the observable result is unchanged. It is not part of the first reference evaluator. Any later memoizing implementation must be tested against the same language-neutral evaluation corpus.

## Scope guard

Stage 3 MUST NOT add:

- human source syntax/parser;
- optimizer passes;
- mutable memory;
- files/network/display/system calls;
- machine profiles;
- native or bytecode compilation;
- self-hosting compiler/interpreter work.

## Definition of done

Stage 3 is complete when a decoded, statically valid NEX-1 Core term can be evaluated according to the clarified weak call-by-name contract to an observable WHNF, or can diverge / be refused because of explicitly separate implementation resource limits, with implementation-independent evaluation vectors and repeatable CI evidence.
