# Stage 4 external baseline comparison

**Status:** Experimental, non-normative  
**Applies to:** Stage 4.5 only

The goal is to compare transmitted program representations without pretending that different computational models have identical built-ins or bootstrap costs.

## Binary Lambda Calculus baseline

Source: John Tromp's Binary Lambda Calculus [SRC-0002].

For an identical pure lambda term, the baseline uses Tromp's exact encoding:

```text
lambda M    -> 00 BLC(M)
M N         -> 01 BLC(M) BLC(N)
index i     -> 1^i 0
```

BLC indices are one-based, so NEX `Var(k)` maps to BLC index `k+1`.

Only frozen-corpus programs containing exclusively `Var`, `Lam`, and `App` are included in this direct comparison. Stage 4.5 does not silently Church-encode NEX `Nat` or `Prim`, because doing so would mix syntax cost with a choice of library/built-in assumptions.

This is a direct same-term comparison, not a shortest-BLC-program search.

## Jot baseline

Source: Chris Barker's archived primary Iota/Jot page [SRC-0014]. Barker defines:

```text
K   -> 11100
S   -> 11111000
AB  -> 1 {A} {B}
```

For the same pure lambda subset used by BLC, the project applies one fixed translation:

1. convert de Bruijn binders to unique internal names;
2. use standard unoptimized SK bracket abstraction:
   - `[x]x = I`, represented as `S K K`;
   - if `x` is not free in `M`, `[x]M = K M`;
   - `[x](M N) = S ([x]M) ([x]N)`;
3. encode the resulting closed S/K tree with Barker's Jot mapping above.

This translation is deterministic and reproducible. It is intentionally **not** described as minimal Jot. For example, Jot's empty program already denotes identity, while this fixed bracket translation produces `S K K`; the experiment measures translation cost, not shortest program complexity.

## Tiny postfix structural stack baseline

This baseline is project-defined rather than an external standard. It exists to test whether NEX's prefix structural representation is materially different from a simple uniform postfix stack representation while keeping the same term constructors, integer code, primitive IDs, static rules, and semantics.

Exact experimental code:

```text
Var(k)   -> 000 U(k)
Nat(n)   -> 001 U(n)
Prim(p)  -> 010 U(p)
Lam(M)   -> STACK(M) 011
App(F,X) -> STACK(F) STACK(X) 100
Let(V,B) -> STACK(V) STACK(B) 101
110      reserved
111      reserved
```

The exact transport bit length terminates the stream. A structural decoder reads tokens left-to-right using a term stack; leaf instructions push one term, `Lam` consumes one term, and `App`/`Let` consume two terms and push one result. A valid complete stream ends with exactly one reconstructed term, which is then subject to the same NEX static semantics for this experiment.

This baseline therefore isolates **program structural encoding**. It is not an independent machine bootstrap and must not be used to claim a smaller total `B`.

## Comparison rules

Reports MUST keep these comparisons separate:

- `NEX vs BLC`: identical pure lambda subset only;
- `NEX vs Jot`: identical pure lambda subset passed through the fixed bracket translation;
- `NEX vs tiny stack`: full frozen corpus, same term semantics and payload integers.

No result from these measurements is a claim about globally shortest programs. Interpreter/decoder/type-system/bootstrap assumptions remain separate from program payload size.