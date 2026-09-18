# ADR-0014: Condition bootstrap cost on explicit receiver assumptions

**Status:** Accepted  
**Date:** 2026-09-18

## Context

Stage 4 established that the host/reference implementation proxy `R` is not bootstrap cost `B`. Stage 5.0–5.6 then showed that NEX-1 v0.1 can be reconstructed independently from a frozen specification/conformance packet, but that result still does not determine what a completely unrelated receiver is assumed to know before the packet or any executable bootstrap is transmitted.

A bootstrap length is therefore not meaningful in isolation. The same NEX evaluator can be tiny if the receiver already knows a strong universal machine, larger if only a mathematical metalanguage is shared, and not yet executable if the only shared object is an ordered bitstream.

This is consistent with two established external observations. Shannon separates the engineering communication system from message semantics and models sender/channel/receiver assumptions explicitly [SRC-0015]. Algorithmic descriptions are relative to a chosen description method/reference machine rather than absolutely machine-free [SRC-0016]. Self-delimiting program-size measures likewise require a specified computational interpretation [SRC-0017].

## Decision drivers

- do not hide terrestrial conventions inside an unpriced `B`;
- keep the physical/channel abstraction separate from NEX semantics;
- make stronger receiver priors visible rather than treating them as free;
- permit exact future bootstrap measurements without pretending there is one uniquely natural alien machine;
- prevent double-counting when one transmitted artifact simultaneously specifies and implements semantics;
- keep host-language source size as an engineering proxy only.

## Decision

All Stage 5 bootstrap claims MUST be conditioned on an explicit, versioned receiver-assumption profile `A`.

The project will use the notation:

```text
B | A
S | A
C | A
```

A receiver assumption is prior shared knowledge or capability that is **not transmitted in the measured message**. This does not mean its information cost is zero; it means the claim is conditional on that prior.

The first model is defined in `stage5/receiver-assumptions/assumptions-v0.1.json` and uses four profiles.

### `A0` — digital transport prior

`A0` assumes only that the physical/channel problem has already yielded one exact finite ordered binary frame: two distinguished logical symbols, a first-to-last order, an exact boundary/length, and no residual bit errors inside the model.

`A0` does **not** assume natural-number coding, Elias gamma, NEX constructors, de Bruijn indices, type theory, evaluation semantics, character encoding, a processor, a universal machine, or a terrestrial host.

Physical signal discovery, modulation, synchronization, error correction, and the cost of establishing the binary abstraction are below the current NEX model boundary. They are out of scope, not zero-cost.

### `A1` — discrete mathematical metalanguage prior

`A1` extends `A0` with explicitly listed elementary mathematical concepts: non-negative integers and basic arithmetic relations, finite sequences, and deterministic finite/recursive rule descriptions.

It still does not assume any NEX-specific grammar/code/semantics or a universal computer.

### `A2(U)` — fixed universal-machine prior

`A2(U)` extends `A1` with one **exactly specified** universal binary abstract machine `U` and its exact program/data and self-delimiting input convention.

`U` is a parameter, not a free universal constant. A future claim such as

```text
B = 731 bits
```

is invalid. The admissible form is, for example,

```text
B | A2(U_candidate_v1) = 731 bits
```

where `U_candidate_v1` is versioned and its semantics are fixed.

Stage 5.7 does not choose `U`; Stage 5.8 must instantiate and measure at least one candidate.

### `A_host(H)` — engineering control only

A concrete terrestrial host such as Go, Python, WebAssembly, x86-64, or POSIX may be represented as `A_host(H)` for engineering experiments. It is explicitly ineligible for a receiver-neutral bootstrap claim.

## Accounting rule

The conceptual project objective remains:

```text
C = S + B + P
```

but exact conditional accounting MUST use a transmitted-bit ledger.

Every transmitted bit is counted exactly once. If specification and executable bootstrap occupy disjoint segments, report:

```text
C | A = (S | A) + (B | A,S) + P
```

If one artifact simultaneously serves both specification and bootstrap roles and cannot be defensibly partitioned, report a joint segment instead:

```text
C | A = (SB | A) + P
```

and do not count the same bits once as `S` and again as `B`.

Assumption atoms themselves are not assigned a bit-equivalent cost in Stage 5.7. Therefore numeric results from different profiles MUST NOT be ranked as total-cost winners unless a later model explicitly prices or otherwise normalizes the differing priors.

## Accepted consequences

- There is no unconditional scalar `B` in current NEX evidence.
- A smaller `B | A2(U)` does not by itself dominate a larger `B | A1`; the former relies on a stronger prior.
- The choice of `U` becomes part of the experiment and must be frozen before optimization comparisons.
- A valid negative result is possible: under `A0` or `A1`, the project may be unable to construct a sufficiently receiver-neutral executable bootstrap yet.
- Host source size remains `R`, not `B`.
- Stage 5.8 must emit a ledger that identifies every transmitted bootstrap/specification segment and its exact bit length.

## Alternatives considered

### Treat the Go or Python implementation as `B`

Rejected. This silently assumes a terrestrial language/runtime/platform and contradicts the Stage 4 measurement contract.

### Choose one universal Turing machine and call its cost absolute

Rejected. Reference-machine choice is itself prior information. A fixed machine is allowed only as an explicit parameter `U` of `A2(U)`.

### Set all receiver priors to zero cost

Rejected. Conditional assumptions are not transmitted bits, but calling them zero-information would turn hidden conventions into a false receiver-neutral claim.

### Fold physical signalling into Stage 5 bootstrap

Deferred. Signal discovery, synchronization, modulation, noise coding, and physical units are legitimate problems, but mixing them into the NEX language-bootstrap experiment would prevent a clean digital-semantic measurement. `A0` names this boundary explicitly.

## Evidence and references

- [SRC-0015] Shannon (1948): communication system decomposition and separation of communication engineering from semantics.
- [SRC-0016] Kolmogorov (1965): algorithmic information/descriptions are defined relative to a chosen effective description method.
- [SRC-0017] Chaitin (1975): self-delimiting program-size information requires a specified program interpretation.
- Stage 4 measurement contract: `docs/STAGE-4.md`, ADR-0010, ADR-0011.
- Stage 5 independent reconstruction: `docs/STAGE-5.md` and PR #8 evidence.

## Follow-up validation

Stage 5.7 must:

1. keep the assumption registry machine-readable and CI-validated;
2. show that `A0 ⊂ A1 ⊂ A2(U)` by explicit atom inclusion, without assigning a numeric cost to that inclusion;
3. keep `A_host(H)` outside receiver-neutral claims;
4. update the living research dissertation with the conditional-cost model.

Stage 5.8 must select/freeze at least one concrete bootstrap representation and, where applicable, one concrete `U`, then measure transmitted bits under a declared profile without double-counting.
