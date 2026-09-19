# Stage 5.8 — Bootstrap feasibility audit

> **Subsequent clarification (2026-09-19):** this experiment used historical `assumptions-v0.1.json`. ADR-0016 later corrected the taxonomy: plain `A1` now contains only elementary discrete mathematics, while the stronger prior needed to interpret an exact recursive rule language is `A1(R)`. This correction does not overturn the negative Stage 5.8 result; it makes Candidate A's missing dependency more explicit. ADR-0018 later inserted the separate 5.10–5.20 Core self-sufficiency extension before Stage 6.

## Status

Negative research result for the first complete-bootstrap attempt.

Stage 5.8 asks for at least one exact, finite, receiver-assumption-conditioned bootstrap candidate, or for a documented failure to construct one without hiding an interpreter or substituting host-source size.

This experiment applies the acceptance contract in `stage5/bootstrap/attempt-v0.1.json`.

## Acceptance contract

A candidate may be reported as a complete `B | A` or `SB | A` only if all of the following are true:

1. the receiver profile is exact and versioned;
2. the transmitted artifact is finite and fixed;
3. its exact bit length is defined;
4. every interpreter/machine needed to use it is either explicitly inside `A` or inside the transmitted ledger;
5. the profile is eligible for receiver-neutral claims;
6. the artifact has been verified to realize the required NEX-1 wire, static, and dynamic behavior;
7. the reported length is not a host-source proxy.

A failed condition is not repaired by assigning the missing component zero cost.

## Candidate A — recursive rule description under historical v0.1 `A1`

The historical v0.1 `A1` profile assumed a discrete mathematical metalanguage including non-negative integers, finite sequences, and the ability to understand deterministic finite/recursive rule descriptions.

This appeared promising because NEX semantics can be written mathematically as recursive rules. However, Stage 5 did not define an exact receiver-neutral **binary syntax and operational semantics for the rule-description language itself**.

The existing forms are not admissible replacements:

- English Markdown assumes English, Unicode/UTF-8, Markdown, typography, and prose interpretation;
- JSON assumes JSON syntax and character encoding;
- Go/Python assumes a terrestrial language/runtime;
- simply saying “the receiver understands these rules” moves the missing interpreter into an undeclared prior.

Therefore no exact transmitted artifact and no defensible `SB | A1` bit count was accepted in Stage 5.8.

Under the corrected v0.2 taxonomy, the intended stronger prior is represented explicitly as `A1(R)`, where the exact rule calculus `R` must itself be frozen before any `B | A1(R)` claim. The historical rejection remains valid because no such exact `R` or complete transmitted artifact was present in Stage 5.8.

**Classification:** `rejected_incomplete`.

## Candidate B — Binary Lambda Calculus under `A2(U=BLC)`

Binary Lambda Calculus (SRC-0002) is a serious candidate for a fixed compact computational basis because it has an exact binary term representation and is computationally universal.

That does **not** by itself give NEX a bootstrap cost.

To accept `B | A2(U=BLC)`, the project would still need a frozen BLC program that implements at least the NEX-1 decoder, static semantics, and observable evaluator, together with exact input/output framing and conformance verification.

No such complete NEX-on-BLC program exists in the Stage 5 repository. Counting a BLC universal evaluator alone would measure BLC machinery, not the missing NEX interpreter.

Therefore Stage 5.8 does not publish a BLC bootstrap bit count.

**Classification:** `rejected_incomplete`.

## Candidate C — Python 3.12 host control

The frozen independent Python implementation is finite and functionally verified.

From `stage5/independent-checkpoints/python-v0.1.json`:

```text
NEX package source only             28,832 bytes
all frozen author-written files     52,859 bytes
```

These figures are useful engineering controls. They are **not** `B`.

Using them as bootstrap would assume Python 3.12, its execution model, integer semantics, library/runtime behavior, text/source representation, and a machine capable of running that environment. Those assumptions belong to `A_host(Python3.12)`, which ADR-0014 explicitly excludes from receiver-neutral bootstrap claims.

**Classification:** `engineering_control_only`.

## Result

No candidate passes the full acceptance contract.

```text
accepted complete bootstrap candidates  0
full B | A known                        false
full SB | A known                       false
total C | A computable                  false
```

This is the accepted Stage 5.8 result.

The result is deliberately negative: the research now knows **why** the missing bootstrap cannot yet be replaced by a defensible scalar without additional work.

The two principal missing constructions are now explicit in the corrected terminology:

1. define and freeze a receiver-neutral exact formal rule calculus `R` under `A1(R)`, then encode and verify the full NEX semantics in it; or
2. freeze an exact `U` under `A2(U)` and implement the complete NEX bootstrap as a verified program for that machine.

Those are subjects for later research. They must not be silently folded into a weaker prior after seeing a desired bit count.

## Reproducibility

Machine-readable historical record:

```text
stage5/bootstrap/attempt-v0.1.json
```

Validation command:

```text
python stage5/bootstrap/validate_attempt.py
```

The validator also recomputes the Python host-control byte totals from the frozen independent checkpoint rather than accepting hand-copied numbers.
