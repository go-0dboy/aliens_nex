# aliens_nex

Experimental repository for **NEX-1**: a minimal, architecture-neutral, statically typed language for compact transmission of programs between systems that do not share a programming language, processor architecture, ABI, operating system, or textual notation.

## Current status

The project is at the specification stage.

The normative draft is:

- [NEX-1 Core v0.1 specification](docs/NEX-1-v0.1.md)

NEX-1 v0.1 currently defines:

- six Core term constructors: `Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`;
- zero-based de Bruijn indices, so bound variable names are not transmitted;
- Hindley-Milner style rank-1 let-polymorphism;
- natural numbers, functions, products, sums, and unit;
- explicit general recursion through `fix`;
- eleven fixed Core primitives;
- a canonical prefix-free binary wire encoding;
- weak call-by-name reference semantics;
- a strict separation between the universal Core and machine/environment profiles.

## Design goal

NEX does not try to minimize only the interpreter or only source-code syntax. The intended optimization target is the total information cost:

```text
cost = specification + bootstrap implementation + transmitted programs
```

This is why the project does not simply reduce everything to SKI combinators or machine instructions. The hypothesis is that a small typed lambda core with de Bruijn indices and direct binary data representation can provide a better overall trade-off.

## Important non-goals for v0.1

Core v0.1 intentionally does not define:

- pointers or mutable machine memory;
- files, sockets, display, keyboard, or operating-system calls;
- Unicode or strings;
- floating point;
- threads or atomics;
- exceptions, objects, classes, or modules;
- a human-oriented source language.

These belong in libraries, frontends, or explicit execution profiles rather than the universal Core.

## Next milestone

Build a reference implementation that can:

1. decode the canonical NEX bit stream;
2. validate de Bruijn scope;
3. infer types using Algorithm W / unification with occurs check;
4. evaluate well-typed closed programs;
5. encode terms back to the canonical wire form;
6. measure bit size, AST size, reduction count, and memory use for a fixed benchmark corpus.

The first benchmark corpus should include identity, addition, multiplication, factorial, Fibonacci, pair/sum processing, a small parser or recognizer, and eventually a NEX decoder and type checker written in NEX itself.

## Research basis

NEX-1 is an experimental design built from established ideas including:

- de Bruijn indices;
- Binary Lambda Calculus;
- Hindley-Milner type inference;
- PCF-style typed general recursion;
- separation of portable computation from host/environment embedding.

Primary references are listed in the specification.

## Repository policy at this stage

Until measurements exist, claims such as “smallest language”, “smallest compiler”, or fixed bootstrap sizes should be treated as hypotheses, not project facts.
