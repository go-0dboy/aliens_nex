# Stage 2 — Static validation

**Status:** In progress  
**Branch:** `stage2/static-validation`

Stage 2 begins after the wire layer is already proven executable and repeatable. Its job is to determine whether a decoded NEX term is a valid closed, statically typed NEX-1 Core program **without executing it**.

The target pipeline is:

```text
bits
  -> decode                Stage 1
  -> Term
  -> scope validation      Stage 2
  -> type inference
  -> verified typed Term
```

Execution remains outside Stage 2.

## Stage 2 sub-stages

### 2.1 — de Bruijn scope validation

Prove that every `Var(k)` refers to an enclosing binder.

Reference rules:

```text
Validate(term, depth)

Var(k)       valid iff k < depth
Lam(body)    validate body at depth + 1
App(f, x)    validate both at depth
Let(v, body) validate v at depth; validate body at depth + 1
Nat(n)       no binder effect
Prim(id)     no binder effect
```

`Let(value, body)` is non-recursive in v0.1: the new binder is in scope only in `body`, not in `value`.

Top-level validation starts at depth `0`, therefore a valid top-level Core program is closed.

### 2.2 — type representation and type schemes

Add an in-memory representation of:

```text
T ::= a
    | 1
    | N
    | T -> T
    | T * T
    | T + T

S ::= forall a1 ... an. T
```

Internal type-variable identity must not depend on human-readable names such as `a`, `b`, or `T17`.

### 2.3 — substitutions and free type variables

Implement:

- substitution application to types, schemes, and environments;
- free type variables for types, schemes, and environments;
- substitution composition.

The implementation must have property tests for substitution identity and composition.

### 2.4 — unification with occurs check

Implement structural unification for type variables, `1`, `N`, function, product, and sum types.

Unification MUST perform the occurs check. For example:

```text
T0 ~ T0 -> T1
```

must fail rather than construct an infinite type.

A core property to test is:

```text
if unify(A, B) = S
then apply(S, A) == apply(S, B)
```

### 2.5 — primitive type schemes and primitive validity

Create one authoritative Core primitive table for IDs `0..10`, including the schemes from NEX-1 v0.1.

The static validator must reject unknown Core primitive IDs when no external profile is explicitly selected.

Type inference and later evaluation must not maintain incompatible independent primitive definitions.

### 2.6 — instantiation and generalization

Implement:

- fresh instantiation of quantified variables for each scheme use;
- let-generalization over variables not free in the outer environment;
- monomorphic lambda-bound variables;
- no polymorphic recursion in v0.1.

### 2.7 — Algorithm W style inference

Implement inference for the six Core constructors:

```text
Var
Lam
App
Let
Nat
Prim
```

The public Stage 2 entry point operates on a closed term after scope validation.

### 2.8 — language-neutral type conformance

Conformance is part of Stage 2 design, not an afterthought.

The project must maintain implementation-independent vectors containing, as applicable:

```text
Term
expected principal type
expected static error class
```

Type-variable names are not semantically significant. Before comparison, inferred principal types must be canonicalized by first occurrence, for example:

```text
T17 -> T17       => T0 -> T0
T42 -> T9 -> T42 => T0 -> T1 -> T0
```

Required positive examples include identity, constant function, `succ`, application, products/sums, `fix`, and polymorphic `let` reuse.

Required negative examples include out-of-scope variables, function/non-function mismatches, incompatible types, occurs-check failure, and unknown primitive IDs.

### 2.9 — properties, fuzzing, CI, and completion review

Before Stage 2 is complete:

- all static conformance vectors pass;
- scope validation is independently tested;
- substitution/unification properties pass;
- Algorithm W examples and let-polymorphism pass;
- malformed static programs are rejected deterministically;
- CI executes the same verification from a clean checkout;
- the final diff is reviewed to confirm that evaluator/runtime behavior has not leaked into Stage 2.

## Type annotations policy during Stage 2

NEX-1 v0.1 ordinary canonical terms do **not** transmit term-level type annotations. Human-oriented frontends MAY support annotations, but a v0.1 frontend must erase them when producing the canonical Core term.

Stage 2 therefore implements inference for the current erased-type wire format.

This is a design baseline, not a claim that erased types are globally optimal for the project objective:

```text
cost = specification + bootstrap implementation + transmitted programs
```

A future experiment must compare at least:

```text
NEX-HM
  erased type information + larger inference bootstrap

versus

NEX-explicit
  compact transmitted type information/certificates + smaller checker bootstrap
```

The comparison must use a stated corpus and measurement method. If an explicit/certificate design wins materially, changing canonical type transmission requires a new ADR and a new specification revision; Stage 2 must not silently alter v0.1 wire terms.

See ADR-0007.

## Scope guard

Stage 2 MUST NOT implement:

- beta reduction or evaluator semantics;
- execution of `fix`, `succ`, `pred`, `ifz`, products, or sums;
- a human source parser;
- optimizer passes;
- mutable memory or system profiles;
- native/bytecode compilation;
- self-hosting.

Knowing that `succ : N -> N` is a typing fact. Computing `succ 5 -> 6` belongs to a later execution stage.

## Definition of done

Stage 2 is complete when the reference implementation can take a Stage-1-decoded Core term and deterministically produce exactly one of:

```text
principal type scheme
scope error
primitive validity error
type/unification error
resource-limit refusal (if configured)
```

with implementation-independent conformance vectors and repeatable CI evidence.
