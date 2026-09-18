# Stage 5.7 receiver-assumption model

This directory defines what a receiver may be assumed to know **before** NEX specification/bootstrap bits are transmitted.

The purpose is not to guess one true alien prior. The purpose is to prevent hidden priors from disappearing from the accounting.

## Core rule

Bootstrap is conditional:

```text
B | A
```

`A` is shared prior knowledge/capability. It is not part of the measured transmission. That does **not** mean `A` has zero information content.

The current profiles form a deliberate assumption ladder:

```text
A0  digital transport only
 |
 v
A1  + discrete mathematical metalanguage
 |
 v
A2(U) + one exact fixed universal binary machine U
```

A separate control profile exists:

```text
A_host(H) = A1 + a concrete terrestrial host H
```

`A_host(H)` is useful for engineering comparisons but cannot support a receiver-neutral bootstrap claim.

## Why A0 starts after the physical channel

NEX currently studies digital representation and executable semantics, not how an unknown civilization discovers radio modulation, clock recovery, symbol timing, synchronization, error-correcting codes, or message boundaries from raw physics.

`A0` therefore says: assume those problems have already produced one exact finite ordered binary frame.

This is a model boundary, not a claim that the physical layer is free. `assumptions-v0.1.json` explicitly records that the cost below `A0` is **not** zero; it is simply outside the current experiment.

## Why A2 is parameterized

There is no machine-independent executable-program length. A bootstrap program can only be counted after the receiver's machine semantics are fixed.

Therefore Stage 5.7 defines `A2(U)` rather than selecting a supposedly natural universal machine. Stage 5.8 must name and freeze a concrete candidate `U` before reporting a numeric `B | A2(U)`.

A useful result may eventually look like:

```text
B_decode | A2(Ux) = ... bits
B_static | A2(Ux) = ... bits
B_eval   | A2(Ux) = ... bits
```

but those numbers are not transferable to another `U` without a new measurement.

## No double counting

The historical research objective is:

```text
C = S + B + P
```

For exact Stage 5 accounting, every transmitted bit must appear once in a ledger.

If specification and bootstrap are physically separate, the additive form is valid:

```text
C | A = (S | A) + (B | A,S) + P
```

If a compact executable artifact simultaneously defines the language and executes it, report the inseparable portion as `SB | A`:

```text
C | A = (SB | A) + P
```

Never count the same artifact once as specification and again as bootstrap.

## Cross-profile comparisons

A numerically smaller bootstrap under a stronger prior is not automatically a better total solution.

For example:

```text
100 bits | A2(U)
```

cannot be declared superior to:

```text
500 bits | A1
```

unless the extra prior knowledge in `A2(U)` is explicitly normalized or priced by a later research model.

Stage 5.7 therefore freezes assumption structure, not a probability distribution over alien knowledge.

## Machine-readable source

`assumptions-v0.1.json` is canonical for the profile/atom registry. Run:

```text
python stage5/validate_receiver_assumptions.py
```

The validator checks profile inheritance, category boundaries, host exclusion, and the accounting invariants.
