# Stage 5.7 receiver-assumption model

This directory defines what a receiver may be assumed to know **before** NEX specification/bootstrap bits are transmitted.

The purpose is not to guess one true alien prior. The purpose is to prevent hidden priors from disappearing from the accounting.

## Current model

`assumptions-v0.2.json` is the current corrected model. `assumptions-v0.1.json` remains frozen historical evidence.

The v0.2 correction separates elementary discrete mathematics from the stronger assumption that a receiver already knows how to interpret an exact recursively executable rule calculus.

The current profiles are:

```text
A0        exact binary-frame prior
 |
 v
A1        elementary discrete-mathematics prior
 |\
 | +--> A1(R) exact formal-rule-calculus prior
 |
 +----> A2(U) fixed universal-binary-machine prior
 |
 +----> A_host(H) terrestrial host control
```

More exactly:

- `A0` gives two distinguished binary symbols, finite order, exact frame boundaries/length, and error-free delivery at the model boundary;
- `A1` adds non-negative integers and finite sequences as mathematical concepts;
- `A1(R)` adds one exact, versioned formal rule calculus `R`, including its syntax, semantics, recursion/binding conventions, and binary serialization;
- `A2(U)` adds one exact, fixed universal binary machine `U` plus exact program/data framing;
- `A_host(H)` adds a concrete terrestrial host/runtime/platform and is an engineering control, not a receiver-neutral bootstrap profile.

Neither `A1(R)` nor `A2(U)` is silently included in plain `A1`.

## Core rule

Bootstrap is conditional:

```text
B | A
```

`A` is shared prior knowledge/capability. It is not part of the measured transmission. That does **not** mean `A` has zero information content.

Cross-profile numerical ranking is not valid without an explicit model for the additional prior knowledge. A smaller `B | A2(U)` is therefore not automatically a better total communication solution than a larger `B | A1`.

## Why A0 starts after the physical channel

NEX currently studies digital representation and executable semantics, not how an unknown civilization discovers radio modulation, clock recovery, symbol timing, synchronization, error-correcting codes, or message boundaries from raw physics.

`A0` therefore assumes those lower-level problems have already produced one exact finite ordered binary frame. This is a model boundary, not a claim that the physical layer is free. v0.2 explicitly records that the cost below `A0` is outside the current experiment rather than zero.

## Why A1(R) is separate

The historical v0.1 `A1` profile implicitly bundled elementary mathematics with the ability to interpret recursively defined formal rules. The post-Stage-5 literature audit judged that assumption too computationally strong to hide inside a generic mathematical prior.

v0.2 therefore keeps plain `A1` limited to elementary discrete mathematical concepts and introduces `A1(R)` for experiments that deliberately assume an exact rule calculus.

Any claim of `B | A1(R)` must name and freeze `R` first.

## Why A2 is parameterized

There is no machine-independent executable-program length. A bootstrap program can only be counted after the receiver's machine semantics are fixed.

Therefore the model uses `A2(U)` rather than selecting a supposedly natural universal machine. Any numeric `B | A2(U)` claim must name and freeze an exact versioned `U` and its binary input convention first.

A useful result may eventually look like:

```text
B_decode | A2(Ux) = ... bits
B_static | A2(Ux) = ... bits
B_eval   | A2(Ux) = ... bits
```

but those numbers are conditional on that exact `U`.

## No double counting

The historical conceptual objective is:

```text
C = S + B + P
```

Exact accounting is receiver-conditioned and message-based:

```text
C | A = |M_A|
```

If transmitted roles are genuinely disjoint:

```text
C | A = (S | A) + (B | A,S) + (P | A,S,B)
```

If one artifact jointly specifies and executes the language:

```text
C | A = (SB | A) + (P | A,SB)
```

Every transmitted bit is counted exactly once. Never count the same artifact once as specification and again as bootstrap.

## Machine-readable sources

Current model:

```text
stage5/receiver-assumptions/assumptions-v0.2.json
```

Historical predecessor:

```text
stage5/receiver-assumptions/assumptions-v0.1.json
```

Validate the model with:

```text
python stage5/validate_receiver_assumptions.py
```

The validator checks profile inheritance, category boundaries, host exclusion, and the accounting invariants.
