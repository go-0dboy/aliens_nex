# NEX-1 v0.1

**Status:** Draft specification  
**Version:** 0.1  
**Date:** 2026-09-18

NEX-1 is a minimal, architecture-neutral, statically typed language intended for compact transmission of programs between systems that do not share a programming language, processor architecture, ABI, operating system, or textual notation.

The design goal is not to minimize only the interpreter. NEX-1 aims to minimize the combined information cost:

```text
cost = specification + bootstrap implementation + transmitted programs
```

The core therefore keeps lambda abstraction and application instead of reducing every program to a tiny combinator basis when that would make programs larger.

---

## 1. Design principles

NEX-1 Core follows these rules:

1. Programs have a canonical binary representation.
2. Bound variable names are never transmitted.
3. Programs are statically typed before execution.
4. Most type annotations are not transmitted; types are inferred.
5. The core is independent of machine word size, byte order, pointers, operating systems, files, networks, displays, and character encodings.
6. General recursion is explicit and part of the core.
7. Machine interaction is defined by optional profiles, not by the core language.
8. A receiver must be able to reject malformed or ill-typed programs before execution.

The mathematical basis is an unannotated lambda calculus with de Bruijn indices, Hindley-Milner style rank-1 let-polymorphism, natural numbers, algebraic product/sum types, and a typed fixed-point primitive.

---

## 2. Notation

This document uses readable names such as `Lam`, `App`, `fix`, and `succ`. These names are documentation only. They are not part of the canonical wire representation.

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

---

## 3. Types

The core type grammar is:

```text
T ::= a
    | 1
    | N
    | T -> T
    | T * T
    | T + T
```

where:

- `a` is a type variable;
- `1` is the unit type;
- `N` is the mathematical type of arbitrary-precision natural numbers;
- `A -> B` is a function type;
- `A * B` is a product type;
- `A + B` is a sum type.

Type schemes are:

```text
S ::= forall a1 ... an. T
```

Universal quantification exists in the type system only. `forall` is not a term constructor and is not transmitted in ordinary terms.

### 3.1 Examples

```text
N -> N
N * N
1 + N
forall a. a -> a
forall a b. a * b -> b * a
```

`1 + A` can be used as an optional value without introducing a special `Option` type.

---

## 4. Core terms

A NEX-1 Core program uses exactly six term constructors:

```text
Term ::= Var(index)
       | Lam(body)
       | App(function, argument)
       | Let(value, body)
       | Nat(value)
       | Prim(id)
```

No other term constructor exists in NEX-1 Core v0.1.

In particular, the core has no dedicated syntax nodes for:

```text
if, while, for, return, struct, enum, pair, switch,
+, -, *, class, method, exception, pointer, module
```

Such concepts are expressed through primitives, functions, libraries, or future profiles.

---

## 5. Variables and de Bruijn indices

NEX-1 uses zero-based de Bruijn indices.

Inside a binder:

```text
0 = nearest enclosing binder
1 = next enclosing binder
2 = next enclosing binder
...
```

Readable expression:

```text
\x -> \y -> x
```

Canonical tree:

```text
Lam(
  Lam(
    Var(1)
  )
)
```

Readable expression:

```text
\x -> \y -> y
```

Canonical tree:

```text
Lam(
  Lam(
    Var(0)
  )
)
```

Variable names are therefore never required on the wire.

A top-level NEX-1 program MUST be closed: every `Var(k)` MUST refer to an enclosing `Lam` or `Let` binder.

---

## 6. Lambda abstraction

`Lam(body)` introduces one bound value. Within `body`, that value is `Var(0)`.

Readable form:

```text
\x -> x
```

Canonical form:

```text
Lam(Var(0))
```

Its principal type is:

```text
forall a. a -> a
```

---

## 7. Application

`App(f, x)` applies `f` to `x`.

Readable form:

```text
f x
```

Multiple applications associate to the left:

```text
f a b c
```

means:

```text
(((f a) b) c)
```

---

## 8. Let binding

`Let(value, body)` means a polymorphic let-binding.

Readable form:

```text
let x = value in body
```

Within `body`, `x` is represented by `Var(0)`.

`Let` is a primitive AST constructor because Hindley-Milner generalization occurs at let-bindings. Replacing every `let x = a in b` with `App(Lam(b), a)` would change typing behavior.

Dynamic evaluation of `Let` is non-strict. Conceptually:

```text
Let(value, body) -> body[0 := value]
```

`value` MUST NOT be evaluated merely because the binding is created. An environment-based implementation may instead extend the runtime environment for `body` with a delayed binding for `value`.

---

## 9. Natural numbers

`Nat(n)` contains a natural number:

```text
n >= 0
```

`N` has arbitrary mathematical precision. It is not defined as a host `int`, `uint32`, `uint64`, or machine word.

Large values are encoded directly in binary form by the wire integer code described later; NEX-1 does not use Church numerals as the canonical numeric representation.

---

## 10. Core primitive table

NEX-1 Core v0.1 reserves primitive IDs `0..10` exactly as follows.

| ID | Name | Arity | Type scheme |
|---:|---|---:|---|
| 0 | `fix` | 1 | `forall a. (a -> a) -> a` |
| 1 | `succ` | 1 | `N -> N` |
| 2 | `pred` | 1 | `N -> N` |
| 3 | `ifz` | 3 | `forall a. N -> a -> a -> a` |
| 4 | `pair` | 2 | `forall a b. a -> b -> a * b` |
| 5 | `fst` | 1 | `forall a b. a * b -> a` |
| 6 | `snd` | 1 | `forall a b. a * b -> b` |
| 7 | `inl` | 1 | `forall a b. a -> a + b` |
| 8 | `inr` | 1 | `forall a b. b -> a + b` |
| 9 | `case` | 3 | `forall a b c. (a + b) -> (a -> c) -> (b -> c) -> c` |
| 10 | `unit` | 0 | `1` |

Primitive IDs `11..31` are reserved for future Core revisions and MUST NOT be assigned by external profiles.

Profile-specific primitives MUST use IDs `>= 32`.

---

## 11. Primitive semantics

Core primitives are curried. A primitive supplied with fewer arguments than its arity is a function value in weak-head normal form. Supplied arguments are delayed until the saturated primitive rule requires them.

### 11.1 Natural numbers

```text
succ n       -> n + 1
pred 0       -> 0
pred (n + 1) -> n
```

`succ` and `pred` force their argument far enough to obtain a natural number.

### 11.2 Zero branch

```text
ifz 0       z s -> z
ifz (n + 1) z s -> s
```

`ifz` forces its first argument far enough to distinguish zero from a positive natural. It MUST evaluate only the selected branch; the unselected branch MUST NOT be evaluated merely by the `ifz` rule.

### 11.3 Products

Conceptually, `pair a b` is a product value.

```text
fst (pair a b) -> a
snd (pair a b) -> b
```

Constructing `pair a b` MUST NOT force either field. `fst` and `snd` force the pair expression far enough to expose the pair constructor and then demand only the selected field. The unselected field MUST NOT be evaluated merely by projection.

### 11.4 Sums

Conceptually:

```text
inl a : A + B
inr b : A + B
```

Constructing `inl a` or `inr b` MUST NOT force the payload.

Reduction:

```text
case (inl a) f g -> f a
case (inr b) f g -> g b
```

`case` forces the scrutinee far enough to expose `inl` or `inr`. It MUST evaluate only the selected branch function. The unselected branch MUST NOT be evaluated by the `case` rule. The selected payload is passed to the selected function according to ordinary call-by-name application and therefore remains delayed until that function demands it.

### 11.5 Fixed point

```text
fix f -> f (fix f)
```

`fix` provides general recursion and therefore permits non-terminating programs. The recursive argument `fix f` is passed according to ordinary call-by-name application and MUST NOT be pre-evaluated merely by the fixed-point rule.

### 11.6 Unit

`unit` is an immediate value of type `1` and has arity zero.

---

## 12. Evaluation strategy

The reference semantics is **weak call-by-name**.

A function argument is substituted without being evaluated first.

The principal beta rule is conceptually:

```text
App(Lam(body), argument) -> body[0 := argument]
```

The corresponding `Let` rule is conceptually:

```text
Let(value, body) -> body[0 := value]
```

Neither rule requires evaluating the substituted expression first.

Implementations SHOULD avoid literal capture-prone substitution and MAY use environments, closures, explicit substitutions, graph reduction, or call-by-need.

An implementation MAY use call-by-need memoization provided that the observable Core result is the same as the reference semantics.

Evaluation does not reduce under `Lam` until the lambda is applied.

### 12.1 Weak-head normal forms

Reference evaluation is required only to expose the outer computational form. The observable Core weak-head forms are:

```text
lambda/function
natural number
unit
pair constructor with delayed fields
inl constructor with delayed payload
inr constructor with delayed payload
unsaturated primitive function
```

A conforming implementation MAY represent these forms using host-specific closures, environments, thunks, heaps, or other internal objects. Those runtime representations are not part of the NEX wire format and are not portable observations.

### 12.2 Primitive forcing

The normative forcing behavior is summarized below.

| Primitive | Forced by the rule | Remains delayed unless later demanded |
|---|---|---|
| `fix f` | `f` only as required for ordinary application | recursive `fix f` argument |
| `succ n` | `n` to `N` | — |
| `pred n` | `n` to `N` | — |
| `ifz n z s` | `n`, then selected branch | unselected branch |
| `pair a b` | nothing | both fields |
| `fst p` | `p` to pair WHNF, then selected field | right field |
| `snd p` | `p` to pair WHNF, then selected field | left field |
| `inl a` | nothing | payload |
| `inr b` | nothing | payload |
| `case s f g` | `s` to sum WHNF, then selected function | unselected function; payload until selected function demands it |
| `unit` | nothing | — |

### 12.3 Divergence and implementation resource limits

Because `fix` permits general recursion, a valid well-typed program may diverge.

A practical evaluator MAY impose implementation resource limits such as transition/fuel, recursion-depth, memory, or allocation limits. Exceeding such a limit is an implementation refusal. It MUST NOT be reported as a malformed wire term, scope error, type error, unknown primitive, or normal Core result.

Finite resource exhaustion does not in general prove that a program diverges: the same valid program may terminate with larger resources.

The exact step/fuel counting convention is implementation-specific and is not a portable Core observable. Conformance tests MUST NOT require different evaluators to exhaust a resource budget after the same number of internal steps.

---

## 13. Typing

A conforming receiver MUST type-check a decoded closed term before execution.

NEX-1 v0.1 uses Hindley-Milner style rank-1 let-polymorphism.

### 13.1 Variable

For `Var(k)`, obtain the `k`-th binding from the typing environment and instantiate its type scheme with fresh type variables.

### 13.2 Lambda

For:

```text
Lam(body)
```

assign a fresh monotype `A` to the new binder. If:

```text
body : B
```

then:

```text
Lam(body) : A -> B
```

### 13.3 Application

For:

```text
App(f, x)
```

infer:

```text
f : A
x : B
```

create a fresh type variable `C`, then unify:

```text
A ~ B -> C
```

If unification fails, the term is ill-typed.

### 13.4 Let

For:

```text
Let(value, body)
```

1. infer the monotype of `value`;
2. apply the current substitution;
3. generalize type variables not free in the outer environment;
4. add the resulting type scheme as the nearest binding for `body`;
5. infer `body`.

### 13.5 Primitive

`Prim(id)` is instantiated from the primitive table's type scheme.

An unknown primitive ID is invalid unless it belongs to an explicitly selected external profile.

### 13.6 Occurs check

Unification MUST perform an occurs check. A type variable MUST NOT be unified with a type containing itself.

---

## 14. Program validity

A Core payload is valid only if all of the following are true:

1. the bit stream decodes to exactly one complete term;
2. no trailing non-padding term bits remain;
3. every de Bruijn index is in scope;
4. every Core primitive ID is defined;
5. type inference succeeds;
6. the top-level term is closed.

Termination is not required. A valid NEX-1 program may diverge because `fix` provides general recursion.

Evaluator resource exhaustion is not a validity condition. A valid program remains valid if a particular implementation refuses to continue because of an implementation resource limit.

---

## 15. Self-delimiting natural number code U(n)

NEX-1 uses a self-delimiting code `U(n)` for non-negative integers.

Let:

```text
m = n + 1
```

Write `m` in ordinary binary without leading zeroes. Let its bit length be `L`.

Then:

```text
U(n) = (L - 1 zero bits) followed by binary(m)
```

Examples:

| n | U(n) |
|---:|---|
| 0 | `1` |
| 1 | `010` |
| 2 | `011` |
| 3 | `00100` |
| 4 | `00101` |
| 5 | `00110` |
| 6 | `00111` |
| 7 | `0001000` |

This is equivalent to Elias gamma coding of `n + 1`.

---

## 16. Canonical wire encoding

A Core term is encoded recursively with the following prefix grammar:

```text
00   U(k)   Var(k)
01   T      Lam(T)
10   T T    App(T, T)
110  T T    Let(T, T)
1110 U(n)   Nat(n)
1111 U(p)   Prim(p)
```

The constructor prefixes are prefix-free:

```text
00
01
10
110
1110
1111
```

Therefore no parentheses, separators, identifiers, whitespace, or textual keywords are required.

The canonical Core object is a **bit string**, not a byte string.

---

## 17. Byte packing

When a NEX bit string must be stored in octets:

1. bits are packed from the most significant bit to the least significant bit of each octet;
2. the final octet is padded with zero bits on the right when necessary;
3. the transport container MUST carry the exact valid bit length, because padding zeroes are not part of the Core term.

The transport container itself is outside NEX-1 Core v0.1.

---

## 18. Encoding examples

### 18.1 Identity

Readable form:

```text
\x -> x
```

AST:

```text
Lam(Var(0))
```

Encoding:

```text
Lam     = 01
Var     = 00
U(0)    = 1
```

Result:

```text
01001
```

Length: **5 bits**.

Principal type:

```text
forall a. a -> a
```

The type is inferred and is not transmitted with the term.

### 18.2 Successor function

Readable form:

```text
\x -> succ x
```

AST:

```text
Lam(
  App(
    Prim(1),
    Var(0)
  )
)
```

Encoding:

```text
01           Lam
10           App
1111 010     Prim(1)
00 1         Var(0)
```

Result:

```text
01101111010001
```

Length: **14 bits**.

Inferred type:

```text
N -> N
```

---

## 19. Derived functions

The following examples are readable notation, not additional Core syntax.

### 19.1 Addition

```text
add =
  fix (\self ->
    \a ->
      \b ->
        ifz b
          a
          (succ (self a (pred b))))
```

Type:

```text
N -> N -> N
```

### 19.2 Multiplication

```text
mul =
  fix (\self ->
    \a ->
      \b ->
        ifz b
          0
          (add a (self a (pred b))))
```

Type:

```text
N -> N -> N
```

### 19.3 Factorial

```text
fact =
  fix (\self ->
    \n ->
      ifz n
        1
        (mul n (self (pred n))))
```

Type:

```text
N -> N
```

### 19.4 Swap

```text
swap = \p -> pair (snd p) (fst p)
```

Principal type:

```text
forall a b. a * b -> b * a
```

---

## 20. Optional values

A conventional optional value can be represented as:

```text
Option A = 1 + A
```

Readable conventions:

```text
None   = inl unit
Some x = inr x
```

No special optional-value feature is required in the core language.

---

## 21. What is deliberately not in Core v0.1

The following are outside the normative Core specification:

```text
bytes
fixed-width machine integers
floating point
mutable memory
pointers
files
networking
Unicode
threads
atomics
exceptions
objects
modules
recursive algebraic data types
linear types
content-addressed references
DAG transport
compression dictionaries
debug symbols
```

Their absence does not imply that they cannot be implemented or added by profiles. It means that a receiver does not need to understand them in order to implement NEX-1 Core.

---

## 22. Computational completeness

The combination of:

```text
lambda abstraction
application
natural numbers
zero test
successor/predecessor
typed fixed point
```

forms a PCF-like general recursive language. NEX-1 therefore intentionally allows non-termination and is suitable as a basis for universal computation.

This is distinct from simply typed lambda calculus without general recursion, which is strongly normalizing and therefore insufficient as the sole basis for an unrestricted general-purpose programming language.

---

## 23. Bootstrap model

A minimal receiver needs four logical components:

```text
bit decoder
scope validator
type inference / unification
evaluator + primitive table
```

The bootstrap process is:

```text
bit stream
   -> decode Core term
   -> validate de Bruijn scope
   -> infer/check types
   -> evaluate
```

After a first implementation exists, a NEX implementation can itself be expressed as a NEX program. Self-hosting is therefore a project goal, not a requirement for a v0.1 conforming implementation.

---

## 24. External profiles

NEX-1 Core does not define machine I/O.

A profile MAY add primitive IDs `>= 32` and type atoms needed by a particular execution environment.

A profile MUST NOT change the meaning of Core primitive IDs `0..10` or Core constructor encodings.

A program requiring an external profile is valid only when that profile is explicitly selected by the transport or execution environment.

This separation allows the same Core language to target unrelated systems without making pointers, files, sockets, displays, or host ABIs part of the universal specification.

---

## 25. Experimental SYS0 direction (non-normative)

The first system profile is expected to explore byte-addressable memory while keeping effects explicit.

Candidate profile-specific types:

```text
Byte
Mem
```

Candidate primitive range starting at ID 32:

```text
byte      : N -> Byte
nat       : Byte -> N
and8      : Byte -> Byte -> Byte
or8       : Byte -> Byte -> Byte
xor8      : Byte -> Byte -> Byte
shl8      : Byte -> N -> Byte
shr8      : Byte -> N -> Byte
memNew    : N -> Mem
memSize   : Mem -> N
memLoad   : Mem -> N -> (1 + Byte)
memStore  : Mem -> N -> Byte -> (1 + Mem)
```

This section is intentionally non-normative in v0.1. SYS0 requires separate analysis of resource semantics, efficient implementation, and interaction with polymorphism before it becomes a profile specification.

---

## 26. Conformance classes

### 26.1 Decoder

A conforming **NEX-1 Decoder** MUST:

- decode the canonical term grammar;
- decode `U(n)` exactly;
- detect incomplete or structurally invalid streams;
- report consumed bit length.

### 26.2 Type checker

A conforming **NEX-1 Type Checker** MUST:

- validate de Bruijn scope;
- implement rank-1 let-polymorphism;
- perform unification with occurs check;
- instantiate primitive schemes correctly;
- reject ill-typed terms.

### 26.3 Evaluator

A conforming **NEX-1 Evaluator** MUST:

- accept only valid, well-typed closed Core terms;
- implement the Core primitive semantics and arities;
- preserve the forcing/non-strictness rules in sections 11 and 12;
- treat unsaturated primitives as function weak-head forms;
- produce results observationally equivalent to the reference weak call-by-name semantics for terminating Core programs;
- keep implementation resource-limit refusal distinct from Core validity and normal results.

---

## 27. Open questions for v0.2

The following questions are intentionally unresolved:

1. Is `Let` worth its wire cost compared with alternative polymorphism encodings?
2. Should `Nat` remain arbitrary precision in every implementation, or should a system profile introduce efficient fixed-width words?
3. Is call-by-name the best reference semantics, or would call-by-value reduce bootstrap complexity enough to justify the change?
4. Should recursive algebraic data types be added to Core, or kept as encoded/library-level structures?
5. Should a future canonical transport use DAG sharing and content-addressed references?
6. What is the measured total information cost versus BLC, SKI/Jot, a tiny stack machine, and WebAssembly?
7. What is the smallest self-hosting decoder/type-checker/evaluator that can be written in NEX itself?

No answer to these questions is part of v0.1.

---

## 28. Required experimental corpus

Before promoting NEX-1 beyond v0.1, implementations SHOULD measure at least:

```text
identity
constant function
function composition
addition
multiplication
factorial
Fibonacci
pair/sum processing
binary data traversal
parser or recognizer
a small interpreter
NEX decoder
NEX type checker
```

For each program record:

```text
wire bit length
AST node count
evaluation steps
peak runtime memory
implementation size
```

These measurements are needed to determine whether NEX actually minimizes the intended total information cost rather than merely having an attractive small core.

---

## 29. Research basis

NEX-1 is a new experimental design, but the individual foundations are established ideas:

- N. G. de Bruijn, *Lambda Calculus Notation with Nameless Dummies, a Tool for Automatic Formula Manipulation* (1972): nameless bound variables / de Bruijn indices.
- John Tromp, *Binary Lambda Calculus*: compact prefix-free binary encoding of lambda terms using de Bruijn-style representation.
- Robin Milner, *A Theory of Type Polymorphism in Programming* (1978): polymorphic static type inference.
- Luis Damas and Robin Milner, *Principal Type-Schemes for Functional Programs* (1982): principal type schemes for Hindley-Milner style typing.
- Gordon Plotkin, PCF and related work on typed functional computation with natural numbers and fixed points.
- Gordon Plotkin, *Call-by-name, call-by-value and the lambda-calculus* (1975): operational distinction between evaluation strategies.
- John Launchbury, *A Natural Semantics for Lazy Evaluation* (1993): lazy evaluation with sharing.
- Peter Sestoft, *Deriving a Lazy Abstract Machine* (1997): environment/closure-based lazy machine derivation and call-by-need implementation background.
- WebAssembly Core Specification: a modern example of separating a portable computational core from embedding/environment interaction.

Useful primary references:

- https://doi.org/10.1016/1385-7258(72)90034-0
- https://tromp.github.io/cl/Binary_lambda_calculus.html
- https://doi.org/10.1016/0022-0000(78)90014-4
- https://doi.org/10.1145/582153.582176
- https://doi.org/10.1016/0304-3975(75)90017-1
- https://doi.org/10.1145/158511.158618
- https://doi.org/10.1017/S0956796897002712
- https://www.w3.org/TR/wasm-core/

---

## 30. Versioning rule

The exact constructor prefix codes and primitive assignments in this document define **NEX-1 Core v0.1**.

Any incompatible change to:

- term constructor encoding;
- integer encoding `U(n)`;
- de Bruijn indexing convention;
- type inference rules;
- primitive IDs `0..10`;
- primitive semantics;

requires a new Core version.

Additive external profiles do not change the Core version.
