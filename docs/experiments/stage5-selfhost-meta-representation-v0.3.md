# Stage 5.11 — accepted operational meta-representation v0.3

**Date:** 2026-09-19  
**Status:** Accepted; Stage 5.11 Complete  
**Core:** NEX-1 v0.1 unchanged

## Problem

The historical v0.1/v0.2 contracts established that all required self-hosting meta-objects can be encoded using natural numbers, but later Stage 5.12 experiments showed that recursively packing trees into one `N` is not a practical operational route under the frozen budgets.

The successful Stage 5.12e/5.12f path instead established a functional finite stream:

```text
BitStream = N -> N
0/1 = data
2   = EOF
```

Stage 5.11 therefore remained incomplete until the representation contract was reconciled with the successful operational evidence.

## Decision

v0.3 keeps the external canonical NEX wire as finite functional bits but changes the internal recursive meta-object carrier to a finite functional stream of natural-number tokens.

```text
FiniteBits      = (N -> N) * N
FiniteNatTokens = (N -> N) * N
```

The second component is the exact finite length. Equality is extensional on the declared finite interval; closure identity is irrelevant.

### Term

`Term` is no longer one recursively packed natural and is not an opaque reference to original wire bits.

```text
Var(k)   -> [0,k]
Lam(t)   -> [1] ++ t
App(a,b) -> [2] ++ a ++ b
Let(v,b) -> [3] ++ v ++ b
Nat(n)   -> [4,n]
Prim(p)  -> [5,p]
```

The representation is a canonical prefix token tree. Children are located by token cursor plus structural skip. Therefore no recursive Core type or host AST is required.

This is intentionally non-trivial for Stage 5.12:

```text
decodeTerm : canonical Bits -> Term tokens
encodeTerm : Term tokens -> canonical Bits
```

The accepted contract explicitly forbids satisfying `encodeTerm` by returning or copying an opaque captured input wire value.

### Other recursive meta-objects

The same `FiniteNatTokens` carrier is frozen for:

```text
Type
Scheme
Substitution
TypeEnvironment
PortableObservation
StaticResult
ToolRequest
ToolResult
```

Each family has an exact prefix/count grammar in `meta-representation-v0.3.json`.

A separate first-class runtime state is not required at Stage 5.11 because Stage 5.15 may use source-level substitution over `Term`. If a later evaluator requires additional closure/environment state, that state must receive a new versioned representation contract before use.

## Preserved distinctions

v0.3 keeps separate:

- malformed internal meta-representation;
- malformed/truncated canonical wire;
- invalid de Bruijn scope;
- unknown primitive ID;
- HM/type errors;
- portable evaluation observations;
- implementation resource refusal.

Resource refusal is never serialized as semantic invalidity.

## Historical lineage

- v0.1 remains the original N-only candidate.
- v0.2 remains the exact N-only/tagged contract and expressiveness evidence.
- v0.3 supersedes v0.2 **only for active operational self-hosting work**.

The failures discovered in Stage 5.12d are preserved as evidence; v0.3 does not rewrite them.

## Executable validation

Machine-readable contract:

```text
stage5/selfhost/meta-representation-v0.3.json
```

Validator:

```text
python stage5/selfhost/validate_meta_representation_v0_3.py
```

The validator checks:

1. unchanged NEX-1 v0.1 constructors, type formers, and primitive IDs;
2. unchanged semantic tag sets from v0.2;
3. exact functional carriers;
4. all ten required representation roles;
5. exact Term/Type token grammars;
6. the anti-identity `Term`/wire relation;
7. bounded examples for Bits, Term, Type, Scheme, Substitution, TypeEnvironment, and PortableObservation;
8. a complete generated Term class for 1–4 AST nodes under the validator's frozen leaf set;
9. token round trips and canonical-wire reconstruction for every generated term;
10. zero token collisions and zero canonical-wire collisions in that bounded class;
11. the forbidden-dependency guard;
12. version gating for any later additional runtime-state representation.

The accepted candidate passed both the `accepted-checkpoint` and `selfhost-contract` jobs in workflow run `35436125965` before the status was promoted from candidate to accepted. The accepted-status artifact is required to pass the same validator again before closeout is considered final.

## Stage 5.11 conclusion

Stage 5.11 is **Complete** under the v0.3 operational contract.

This conclusion means only that the self-hosting workstream now has finite, exact, versioned representation contracts expressible with existing NEX-1 v0.1 values. It does not claim that the Stage 5.12 full `encodeTerm/decodeTerm` implementation already exists.

At the Stage 5.11 closeout, the next permitted work was the remaining Stage 5.12 codec gates and Stage 5.13 was still blocked by that predecessor. That sequencing condition has since been satisfied: Stage 5.12 is now Complete with accepted full-codec v0.3, and Stage 5.13 is Planned as the next sequential substage. This navigation update does not alter the Stage 5.11 evidence or decision.
