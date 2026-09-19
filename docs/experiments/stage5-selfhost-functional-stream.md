# Stage 5.12e — fixed-type functional stream candidate

**Status:** Runtime experiment in progress  
**Date:** 2026-09-19  
**Core:** NEX-1 v0.1 unchanged

## Motivation

Two N-only recursive-data strategies have now exposed complementary problems:

1. pow2-adic pairing is executable for small objects but recursive AST codes can explode in bit length because a subtree code becomes an exponent;
2. bit interleaving keeps recursive codes compact but needs repeated parity/halving over the packed natural and hits the frozen sharing depth budget on moderate examples.

Before treating this as a Core limitation, the project must test a representation that uses higher-order functions already present in NEX rather than packing recursive data into one `N`.

## Candidate

A finite bit stream is represented by the fixed HM type:

```text
Stream = N -> N
```

with the semantic convention:

```text
0 = bit 0
1 = bit 1
2 = EOF
```

For a valid finite stream, indices before its end return 0 or 1, and the end index plus all later indices return 2.

The basic constructors are ordinary NEX functions:

```text
nil  : N -> N
cons : N -> (N -> N) -> (N -> N)
head : (N -> N) -> N
tail : (N -> N) -> (N -> N)
drop : N -> (N -> N) -> (N -> N)
```

Conceptually:

```text
nil(i) = 2

cons(x, tail)(i) =
  if i == 0 then x
  else tail(i - 1)

tail(s)(i) = s(i + 1)
```

No recursive type is required because every stream has the same simple function type.

## Critical construction test

The candidate includes a recursive producer:

```text
repeat : N -> N -> (N -> N)
```

where `repeat(bit,count)` returns a stream closure of `count` copies of `bit` followed by EOF.

This is a stronger test than embedding a fixed sequence in generated source. The NEX program must dynamically create and return a finite structure whose length is only known at runtime.

Frozen execution cases include:

```text
repeat(1,8)(7)     = 1
repeat(1,8)(8)     = 2
repeat(0,32)(31)   = 0
repeat(0,32)(32)   = 2
repeat(1,128)(127) = 1
repeat(1,128)(128) = 2
```

The candidate also tests `tail` and `drop` returning streams.

## Artifacts

```text
stage5/selfhost/build_functional_stream.py
stage5/selfhost/functional-stream-v0.1.json
stage5/selfhost/verify_functional_stream.py
```

The exact artifact freezes 10 closed canonical NEX terms. Their combined size, counted as separate terms, is 1,808 bits.

## Acceptance rule

The candidate is supported for the next representation experiment only if:

1. artifact generation is reproducible;
2. every term round-trips through canonical NEX wire;
3. Python and Go infer the frozen principal types;
4. all frozen fully-applied cases return the expected natural result;
5. Python and Go call-by-need return the same values on all cases;
6. neither sharing implementation refuses a frozen case under the declared 5,000,000-transition budgets;
7. normative Go CBN refusals, if any, are recorded separately from semantic correctness.

Passing this checkpoint does **not** yet promote a complete new Stage-5 meta-representation and does not establish self-hosting. It only demonstrates that dynamically sized finite data can be represented and traversed with existing rank-1 HM functions/closures without recursive numeric packing.

## If supported

The next experiment should use functional streams directly as the internal representation of canonical NEX wire and implement a cursor/parser layer over them. A term need not first be converted into a recursively packed numeric AST; structural validation, type inference, and evaluation may instead operate over stream handles/cursors or other fixed-type functional interfaces.

## If rejected

Record the exact typing or runtime barrier. A failure caused by inability to give dynamically constructed streams a stable HM type would be materially stronger evidence of a Core expressiveness limitation than the previous numeric-representation failures. A pure resource failure would instead motivate another representation/cost experiment before any successor-Core proposal.
