# Stage 5.12f — functional-stream wire cursor/parser contract

**Status:** preregistered before NEX parser implementation  
**Date:** 2026-09-19  
**Core:** NEX-1 v0.1 unchanged

## Why this experiment follows 5.12e

Stage 5.12e established, on a frozen development workload and a separately preregistered hold-out, that finite bit data can be represented practically as a fixed rank-1 HM function:

```text
BitStream = N -> N
0/1 = bits
2   = EOF
```

That result does not yet provide a `Term` value. The next question is deliberately narrower: can unchanged NEX traverse the exact canonical wire recursively while carrying only a functional bit stream and a numeric cursor?

The experiment therefore does **not** reintroduce a packed-natural AST and does not yet claim complete `decodeTerm`.

## Fixed interface

The bit cursor is simply a natural offset:

```text
Cursor = N
```

Every parser operation returns the same fixed product type:

```text
ParserResult = N * (N * (N * N))
             = (status, a, b, nextOffset)
```

This uses existing Core `Product`; no recursive type is introduced.

Status codes are frozen as:

```text
0 Ok
1 UnexpectedEOF
2 TrailingData
```

Constructor kinds are frozen as:

```text
0 Var
1 Lam
2 App
3 Let
4 Nat
5 Prim
```

## Operations under test

### `decodeUAt`

```text
BitStream -> Cursor -> ParserResult
```

On success:

```text
(Ok, decodedNatural, 0, nextOffset)
```

It parses the existing NEX `U(n)` code directly from the functional bit stream.

### `readHead`

```text
BitStream -> Cursor -> ParserResult
```

On success:

```text
(Ok, constructorKind, payload, nextOffset)
```

`Var`, `Nat`, and `Prim` decode their `U(n)` payload. `Lam`, `App`, and `Let` use payload `0`.

### `skipTerm`

```text
BitStream -> Cursor -> ParserResult
```

It recursively traverses exactly one canonical term according to constructor arity and returns:

```text
(Ok, nodeCount, 0, nextOffset)
```

Frozen arities:

```text
Var  0
Lam  1
App  2
Let  2
Nat  0
Prim 0
```

### `exactTerm`

It runs the full term traversal and requires the next stream symbol to be EOF. Additional data produces:

```text
(TrailingData, nodeCount, 0, endOfFirstTerm)
```

## Explicit non-goals

5.12f does not test:

- de Bruijn scope validity;
- whether a primitive ID is known;
- type inference;
- evaluation;
- a materialized recursive AST value;
- self-processing.

Those claims remain for later checkpoints.

## Frozen workloads

Development workload:

```text
stage5/selfhost/parser-development-v0.1.json
```

It contains 27 cases covering:

- several `U(n)` values and truncated gamma codes;
- all six constructor headers;
- nested `Lam`, `App`, and `Let` traversal;
- missing children / truncated payloads;
- exact single-term framing and trailing data.

Separate hold-out:

```text
stage5/selfhost/parser-holdout-v0.1.json
```

It contains 12 additional cases with different integer values, different nested terms, truncations, and trailing-data cases.

The hold-out is preregistered but must not be executed against a NEX parser candidate until candidate v0.1 passes the development workload unchanged.

## Independent oracle before implementation

```text
stage5/selfhost/validate_parser_contract.py
```

is a small host mathematical oracle that checks both frozen workload files before any NEX parser candidate exists. This validation confirms that the expected observations are internally consistent with NEX-1 v0.1 wire rules.

Validating expected hold-out answers with the host oracle is not a candidate hold-out execution: no NEX parser candidate exists yet, and the hold-out remains classified `preregistered_unexecuted` for candidate acceptance.

## Frozen resource budgets

The experiment inherits the previously frozen anti-tuning budgets unchanged:

```text
Python call-by-need  5,000,000 transitions / depth 8,000
Go call-by-need      5,000,000 transitions / depth 20,000
Go normative CBN     5,000,000 transitions / depth 20,000
```

The same versioning discipline applies:

- no limit increase after seeing a candidate result;
- no failing-case deletion from the same candidate version;
- any algorithmic parser change after first execution requires candidate v0.2;
- candidate v0.2 would require a newly preregistered hold-out.

## Acceptance rule

Parser candidate v0.1 may be accepted for this narrow checkpoint only if:

1. the candidate artifact is canonical and reproducible;
2. principal types match the frozen interface;
3. all 27 development cases match the frozen oracle observations;
4. Python and Go call-by-need both have zero resource refusals under the frozen budgets;
5. their returned observations agree;
6. the candidate wire is frozen before hold-out execution;
7. the unchanged candidate passes the 12-case preregistered hold-out once under the same budgets.

Go CBN remains a separately reported resource measurement for this representation experiment.

## Meaning of a future pass

A pass would show that unchanged NEX-1 v0.1 can traverse complete canonical term framing over a functional stream and maintain a cursor without materializing a recursively packed natural AST.

It would still **not** be complete `decodeTerm`: no reusable decoded recursive `Term` object would yet exist. The result would justify the next decision point: either construct a flat/folded term representation over this parser, or fuse later validation with recursive wire traversal.
