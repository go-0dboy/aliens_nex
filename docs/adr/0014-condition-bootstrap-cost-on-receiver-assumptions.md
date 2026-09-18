# ADR-0014: Condition bootstrap cost on explicit receiver assumptions

**Status:** Accepted  
**Date:** 2026-09-18  
**Post-Stage-5 clarification:** 2026-09-19, see ADR-0016 and `assumptions-v0.2.json`

## Context

Stage 4 established that host/reference proxy `R` is not bootstrap cost `B`. Stage 5 then showed that NEX-1 v0.1 can be reconstructed independently from a frozen specification/conformance packet, but that result still does not determine what an unrelated receiver knows before any specification or executable bootstrap is transmitted.

A bootstrap length is therefore not meaningful in isolation. The same evaluator can be short under a strong pre-agreed machine and much larger under weaker prior assumptions. Description-length literature likewise treats lengths relative to a description method/model rather than as an unconditional machine-free scalar [SRC-0016, SRC-0017, SRC-0019].

## Decision drivers

- do not hide terrestrial conventions inside an unpriced `B`;
- keep physical/channel assumptions separate from NEX semantics;
- make stronger priors visible instead of treating them as free;
- prevent double counting when one transmitted artifact both specifies and executes semantics;
- require an exact interpretation before accepting a numerical bootstrap length;
- keep historical Stage 5 evidence immutable while allowing the assumption taxonomy to be corrected.

## Decision

All receiver-neutral bootstrap claims MUST be conditioned on an explicit, versioned assumption profile `A`.

The project uses:

```text
B | A
S | A
C | A
```

A receiver assumption is prior shared knowledge/capability not transmitted inside the measured message. Conditional does not mean zero-information; it means the claim is stated relative to that prior.

Exact total-cost claims SHOULD be phrased as the bit length of a concrete transmitted object:

```text
C | A = |M_A|
```

where `M_A` is fully serialized under the declared profile.

If the transmitted object has defensibly disjoint roles:

```text
C | A = (S | A) + (B | A,S) + (P | A,S,B)
```

If one artifact inseparably serves specification and executable-bootstrap roles:

```text
C | A = (SB | A) + (P | A,SB)
```

Every transmitted bit is counted exactly once.

## Historical v0.1 model

The Stage 5.7 artifact `stage5/receiver-assumptions/assumptions-v0.1.json` is preserved unchanged as historical evidence. It defined:

```text
A0
A1
A2(U)
A_host(H)
```

and placed the ability to interpret deterministic finite/recursive rule descriptions inside `A1`.

The post-Stage-5 literature audit judged that one atom too strong: an executable recursive-rule language itself needs exact syntax, operational semantics, recursion/binding conventions, and serialization. Hiding that capability inside a generic mathematical prior weakens the accounting boundary.

## Current v0.2 model

`stage5/receiver-assumptions/assumptions-v0.2.json` is the current taxonomy:

### `A0` — digital transport prior

`A0` assumes only that the physical/channel problem has already yielded one exact finite ordered binary frame: two distinguished logical symbols, order, exact boundary/length, and no residual bit errors inside the model.

Physical signal discovery, modulation, synchronization, error correction, and the cost of establishing the binary abstraction remain below the current NEX boundary; they are out of scope, not zero-cost.

### `A1` — elementary discrete-mathematics prior

`A1` extends `A0` only with explicitly listed mathematical concepts such as non-negative integers and finite sequences.

It does **not** assume an executable rule language, recursion semantics, NEX grammar, HM inference, a universal computer, or a terrestrial host.

### `A1(R)` — exact formal-rule-calculus prior

`A1(R)` extends `A1` with one exact formal calculus `R` whose syntax, binding/substitution rules if any, operational interpretation, recursion convention, and binary serialization are already shared.

`R` is a parameter. A numerical `B | A1(R)` is invalid unless the exact version of `R` is fixed before measurement.

### `A2(U)` — fixed universal-machine prior

`A2(U)` extends `A1` with one exactly specified universal binary abstract machine `U` and exact program/data/self-delimiting input convention.

`U` is a parameter, not a privileged universal constant. A valid claim names the machine explicitly, for example:

```text
B | A2(U_candidate_v1) = ... bits
```

### `A_host(H)` — terrestrial engineering control

A concrete Go/Python/WebAssembly/x86/POSIX-style host may be modeled as `A_host(H)` for engineering controls. It is ineligible for a receiver-neutral claim.

## Relationship among profiles

The corrected model has:

```text
A0 < A1 < A1(R)
A0 < A1 < A2(U)
A0 < A1 < A_host(H)
```

`A1(R)` and `A2(U)` are **different branches**. No numeric ordering between their prior strengths is assumed merely from the number of listed atoms.

Assumption atoms themselves are not assigned a bit-equivalent cost here. Numeric results from different profiles MUST NOT be ranked as total-cost winners unless the differing priors are explicitly normalized or priced by a later model.

## Accepted consequences

- There is still no unconditional scalar `B` in current NEX evidence.
- `P` is an exact canonical NEX wire length after the NEX contract is established, not an unconditional machine-free description length.
- A smaller `B | A2(U)` does not automatically dominate a larger value under weaker/different prior assumptions.
- The exact machine/calculus choice becomes part of the experiment and must be frozen before comparison.
- Host source size remains an engineering proxy, not `B`.
- Stage 5's negative bootstrap result remains valid; the corrected `A1` boundary makes that result more explicit rather than overturning it.

## Alternatives rejected

### Treat Go or Python implementation size as `B`

Rejected: this silently assumes a terrestrial runtime/platform.

### Choose one universal machine and call its cost absolute

Rejected: the reference machine is prior information and must be named as `U`.

### Keep recursive-rule interpretation inside generic `A1`

Rejected after the literature re-audit: this hides a computational formalism inside an apparently mathematical prior.

### Set receiver priors to zero information

Rejected: conditional assumptions are outside the measured message, not necessarily cheap or universal.

### Fold physical signalling into current bootstrap accounting

Deferred: important but separate from the present digital-semantic experiment.

## Evidence and references

- SRC-0015 Shannon: communication-system boundary.
- SRC-0016 Kolmogorov: description-method relativity.
- SRC-0017 Chaitin: program-size reasoning requires a specified interpretation.
- SRC-0019 Rissanen: shortest-description reasoning includes the chosen model/description framework.
- ADR-0016: post-Stage-5 correction and full literature audit.

## Validation

`stage5/validate_receiver_assumptions.py` validates both:

- historical frozen v0.1;
- current corrected v0.2.

The historical artifact is not rewritten to make the experiment look cleaner after the fact.
