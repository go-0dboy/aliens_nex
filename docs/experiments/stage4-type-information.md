# Stage 4 type-information experiment

**Status:** Experimental, non-normative  
**Applies to:** Stage 4.4 only

NEX-1 v0.1 transmits ordinary Core terms without term-level type annotations and reconstructs principal types using Hindley-Milner inference. ADR-0007 deliberately left open whether this minimizes total information cost once bootstrap complexity is included.

Stage 4.4 begins with a deliberately narrow hybrid experiment rather than pretending to have a complete explicit-type replacement.

## Hybrid root principal-type envelope v0.1

For a closed NEX term:

1. infer its principal top-level `TypeScheme` using the existing v0.1 checker;
2. alpha-normalize quantified variables by first occurrence in the type body;
3. transmit an additional experimental type payload after/beside the unchanged canonical term;
4. measure the exact additional program bits.

Experimental scheme encoding:

```text
U(q)   monotype
```

where `q` is the number of quantified variables.

Experimental monotype prefixes:

```text
00 U(i)   quantified type variable i
010       1
011       N
100 A B   A -> B
101 A B   A * B
110 A B   A + B
111       reserved
```

This encoding is **not** part of NEX-1 v0.1 and MUST NOT be accepted by the v0.1 decoder.

## What this experiment can establish

It measures exactly, on a frozen corpus:

```text
P_HM      = canonical erased term bits
P_hybrid  = canonical erased term bits + root principal-type bits
Delta_P   = P_hybrid - P_HM
```

## What this experiment cannot establish

A root type alone does not eliminate the need to verify internal applications, let-generalization, primitive instantiation, or other typing judgments. Therefore this experiment does **not** prove that an explicit-type bootstrap is smaller, and it does not assign a numerical bootstrap saving.

Any claim that explicit/hybrid typing reduces `B` requires a distinct checker/verification design and a measured implementation or other clearly labelled bootstrap proxy.

The purpose of this first experiment is to obtain an exact transmitted-program overhead while preserving the distinction between measured `P` and currently unknown `B`.