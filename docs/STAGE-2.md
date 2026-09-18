# Stage 2 — Static validation

**Status:** Complete  
**Completed by:** PR `#4 stage2: complete static validation and principal type inference`  
**Merge commit:** `cefe889d90a275897de31aa23c4b9742a388ec8f`

Stage 2 begins after the wire layer is already proven executable and repeatable. Its job is to determine whether a decoded NEX term is a valid closed, statically typed NEX-1 Core program **without executing it**.

The completed pipeline is:

```text
bits
  -> decode                Stage 1
  -> Term
  -> scope validation      Stage 2
  -> type inference
  -> principal TypeScheme
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

The reference implementation represents:

```text
T ::= a
    | 1
    | N
    | T -> T
    | T * T
    | T + T

S ::= forall a1 ... an. T
```

Internal type-variable identity does not depend on human-readable names such as `a`, `b`, or `T17`.

### 2.3 — substitutions and free type variables

Implemented:

- substitution application to types, schemes, and environments;
- free type variables for types, schemes, and environments;
- substitution composition;
- property tests for substitution composition.

### 2.4 — unification with occurs check

Structural unification is implemented for type variables, `1`, `N`, function, product, and sum types.

Unification performs the occurs check. For example:

```text
T0 ~ T0 -> T1
```

fails rather than constructing an infinite type.

The tested core property is:

```text
if unify(A, B) = S
then apply(S, A) == apply(S, B)
```

### 2.5 — primitive type schemes and primitive validity

One authoritative Core primitive table contains IDs `0..10`, names, and type schemes from NEX-1 v0.1.

Core-only static validation rejects unknown, reserved, and profile primitive IDs when no external profile is explicitly selected.

Type inference and future evaluation must derive primitive metadata from this authoritative table rather than maintaining incompatible independent definitions.

### 2.6 — instantiation and generalization

Implemented:

- fresh instantiation of quantified variables for each scheme use;
- direct alpha-renaming during instantiation;
- let-generalization over variables not free in the outer environment;
- monomorphic lambda-bound variables;
- no polymorphic recursion in v0.1.

### 2.7 — Algorithm W style inference

Inference is implemented for the six Core constructors:

```text
Var
Lam
App
Let
Nat
Prim
```

The public `InferClosed(term)` entry point operates on a closed Core term, validates Core primitive IDs, performs HM-style inference, and returns the principal type scheme.

### 2.8 — language-neutral type conformance

Conformance is part of Stage 2 design, not an afterthought.

The project maintains implementation-independent vectors containing, as applicable:

```text
Term
expected principal type
expected static error class
```

Type-variable names are not semantically significant. Before comparison, inferred principal types are canonicalized by first occurrence, for example:

```text
T17 -> T17       => T0 -> T0
T42 -> T9 -> T42 => T0 -> T1 -> T0
```

The current corpus contains 15 scope vectors and 19 type vectors, including identity, constant function, `succ`, application, products/sums, `fix`, polymorphic `let` reuse, out-of-scope variables, function/non-function mismatches, incompatible types, occurs-check failure, and unknown primitive IDs.

### 2.9 — properties, fuzzing, CI, and completion review

Stage 2 completion verification includes:

- all static conformance vectors;
- independent scope tests;
- substitution/unification properties;
- Algorithm W and let-polymorphism tests;
- deterministic malformed static-program rejection;
- clean-checkout CI;
- final diff review confirming evaluator/runtime behavior did not leak into Stage 2.

`reference/go/verify.sh` runs:

```text
gofmt check
go vet ./...
go test ./...
1s FuzzSubstitutionComposition
1s FuzzUnifyProducesEqualAppliedTypes
1s FuzzInferenceSuccessfulSchemeIsClosedAndStable
```

Final pre-merge PR CI evidence includes run `35360079519` and final head run `35360245915`, both successful.

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

The comparison must use a stated corpus and measurement method. If an explicit/certificate design wins materially, changing canonical type transmission requires a new ADR and a new specification revision.

See ADR-0007.

## Scope guard

Stage 2 did **not** implement:

- beta reduction or evaluator semantics;
- execution of `fix`, `succ`, `pred`, `ifz`, products, or sums;
- a human source parser;
- optimizer passes;
- mutable memory or system profiles;
- native/bytecode compilation;
- self-hosting.

Knowing that `succ : N -> N` is a typing fact. Computing `succ 5 -> 6` belongs to Stage 3 or later.

## Definition of done — satisfied

The reference implementation can take a Stage-1-decoded Core term and deterministically produce exactly one of:

```text
principal type scheme
scope error
primitive validity error
type/unification error
```

with implementation-independent conformance vectors and repeatable CI evidence.

Stage 2 is therefore complete.