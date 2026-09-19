# Stage 5.12f — NEX-written cursor/parser over functional bit streams

**Status:** accepted bounded checkpoint  
**Date:** 2026-09-19  
**Core:** NEX-1 v0.1 unchanged

## Question

After Stage 5.12e established that dynamically sized finite bit streams can be represented as ordinary NEX functions of fixed rank-1 HM type,

```text
BitStream = N -> N
0/1       = bit values
2         = EOF
```

the next question was deliberately narrower than full `decodeTerm`:

> Can unchanged NEX-1 v0.1 traverse its own canonical wire recursively through a cursor over a functional bit stream, without first packing a recursive AST into one natural number and without adding recursive types or new primitives?

This checkpoint tests only wire traversal. It does not claim a materialized `Term` representation, static semantics, evaluation, or self-hosting.

## Preregistered contract

Before parser implementation, the following were frozen and host-oracle validated:

```text
stage5/selfhost/parser-contract-v0.1.json
stage5/selfhost/parser-development-v0.1.json
stage5/selfhost/parser-holdout-v0.1.json
stage5/selfhost/validate_parser_contract.py
```

The fixed interface is:

```text
BitStream    = N -> N
Cursor       = N
ParserResult = N * (N * (N * N))
             = (status, a, b, nextOffset)
```

Status codes:

```text
0 Ok
1 UnexpectedEOF
2 TrailingData
```

Constructor-kind codes:

```text
0 Var
1 Lam
2 App
3 Let
4 Nat
5 Prim
```

Four operations were frozen:

```text
decodeUAt : BitStream -> Cursor -> ParserResult
readHead  : BitStream -> Cursor -> ParserResult
skipTerm  : BitStream -> Cursor -> ParserResult
exactTerm : BitStream -> Cursor -> ParserResult
```

Their roles are:

- `decodeUAt` — decode canonical `U(n)` from a cursor;
- `readHead` — decode one constructor header and immediate `U` payload when present;
- `skipTerm` — recursively traverse one complete term according to constructor arity and return its node count and next cursor;
- `exactTerm` — require that the traversed term is followed immediately by EOF.

The preregistered development workload contains 27 cases. The separately preregistered hold-out contains 12 cases. All expected results were checked by an independent host oracle **before** any NEX parser candidate was executed.

Resource budgets were inherited unchanged from `experiment-protocol-v0.1.json`:

```text
Python call-by-need   5,000,000 transitions / depth 8,000
Go call-by-need       5,000,000 transitions / depth 20,000
Go normative CBN      5,000,000 transitions / depth 20,000
```

Go CBN is measurement-only for this checkpoint. Acceptance requires both independently implemented sharing controls to return the frozen values without resource refusal.

## Candidate v0.1

Artifacts:

```text
stage5/selfhost/build_stream_parser.py
stage5/selfhost/stream-parser-v0.1.json
stage5/selfhost/verify_stream_parser.py
```

The candidate consists of four closed canonical NEX terms:

```text
decodeUAt    752 bits
readHead    2165 bits
skipTerm    3964 bits
exactTerm   4480 bits
-------------------
total      11361 bits
```

The total is the engineering size of four separately serialized terms. It is not `B | A`, not total `C | A`, and not a minimal self-hosting library size.

All four terms infer the same fixed principal type:

```text
(N -> N) -> N -> (N * (N * (N * N)))
```

No constructor, primitive, type former, wire rule, mutable store, host AST object, or hidden callback was added to NEX-1.

## Development result

The first official development execution was GitHub Actions run `35433974244`, job `105873398120`.

Frozen candidate Git blob:

```text
44b9d85f8bbe522d8b637c977c3fb39520c2c10f
```

Result:

```text
development cases                         27
projected ParserResult fields            108
Python call-by-need resource refusals      0
Go call-by-need resource refusals          0
Go normative CBN resource refusals        16
Python/Go need values matched            108/108
largest Python need transitions          7,339  skip-nested:a
largest Go need transitions              3,171  skip-nested:a
```

The verifier forces all four fields of every `ParserResult`. Merely observing the outer `Pair` constructor is therefore insufficient to pass.

The development result is frozen in:

```text
stage5/selfhost/stream-parser-development-result-v0.1.json
```

## Historical checkpoint before hold-out

Before revealing the hold-out to the candidate, the explicit historical regression was run as Actions run `35434076839` and completed successfully.

It reproduced or validated:

- Stage 5.12a arithmetic foundation;
- Stage 5.12b pair/sequence measurements;
- Stage 5.12c integer codec;
- Stage 5.12d negative interleaved-pair result;
- Stage 5.12e negative v0.1 and accepted v0.2 stream evidence;
- Stage 5.12f development result;
- independent Python reconstruction checkpoint;
- Go reference and frozen Stage 4 evidence.

Only after that green checkpoint was the parser hold-out trigger changed.

## Preregistered hold-out result

The unchanged candidate was executed once against the 12 preregistered cases in Actions run `35434195939`, job `105873992224`.

Before execution, the verifier required these exact Git blob identities:

```text
candidate  44b9d85f8bbe522d8b637c977c3fb39520c2c10f
hold-out   352e37b682230f196b3b4414932b7625dd24bfa7
```

Result:

```text
hold-out cases                            12
projected ParserResult fields             48
Python call-by-need resource refusals      0
Go call-by-need resource refusals          0
Go normative CBN resource refusals        18
Python/Go need values matched             48/48
largest Python need transitions          15,151  skip-let-complex:a
largest Go need transitions               6,392  skip-let-complex:a
```

No candidate wire, workload case, expected value, or resource budget was changed between development and hold-out.

The durable result is:

```text
stage5/selfhost/stream-parser-holdout-result-v0.1.json
stage5/selfhost/verify_stream_parser_result.py
```

`verify_stream_parser_result.py` checks the recorded result and Git blob identities without re-executing the one-shot hold-out.

## Interpretation

Accepted conclusion:

> On the frozen development and preregistered hold-out surfaces, unchanged NEX-1 v0.1 can decode canonical integer fields, distinguish all six term constructors, recursively traverse complete canonical term structure, detect premature EOF/trailing data, and carry the traversal cursor using only a fixed-type functional bit stream and existing Core features.

This materially strengthens the 5.12e result: the functional stream is not merely constructible and indexable; it can support recursive traversal of actual NEX canonical term wire.

The conclusion remains bounded. The checkpoint does **not** establish:

- a materialized recursive `Term` value inside NEX;
- complete `decodeTerm` / `encodeTerm` round trips;
- scope validation;
- primitive-ID validation;
- principal HM inference;
- evaluation;
- an integrated NEX-in-NEX implementation;
- self-processing of that implementation;
- receiver-neutral bootstrap.

## CBN qualification

Normative Go CBN refused 16 development projections and 18 hold-out projections under the fixed 5,000,000-transition budget, while both sharing controls completed every acceptance observation.

This is not interpreted as semantic invalidity. It is further evidence that sharing is an engineering feasibility condition for the current self-sufficiency construction. NEX-specific CBN/call-by-need observational-preservation metatheory remains open.

## Decision

`stream-parser-v0.1` is **accepted as the Stage 5.12f bounded canonical-wire traversal checkpoint**.

NEX-1 v0.1 remains unchanged.

The next research step must not silently broaden this result into a complete decoder. Before further implementation, the project should explicitly choose and preregister the representation/interface required to carry structural information from the wire traversal into Stage 5.13 structural validation while preserving the anti-tuning and versioning rules established in 5.12e–f.

## Subsequent status

This remains the historical Stage 5.12f parser checkpoint. The later operational meta-representation v0.3 and accepted full-codec v0.3 completed Stage 5.12 under the same anti-tuning discipline. The current next substage is Stage 5.13 structural validation; the parser checkpoint itself is not reinterpreted as proof of that later stage.
