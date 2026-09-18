# ADR-0006: Keep decoder resource limits separate from wire validity

- **Status:** Accepted
- **Date:** 2026-09-18

## Context

NEX-1 defines mathematical natural numbers and recursively nested terms without a fixed maximum size. Every real implementation, however, has finite memory, stack, time, and integer capacity.

If an implementation reports an input as malformed merely because it exceeds local limits, the implementation silently changes the language: the same canonical bit string could become valid on one machine and invalid on another.

At the same time, an unconstrained decoder is unsuitable for untrusted input because a long integer prefix or deeply nested term can consume excessive resources.

## Decision

Reference decoders MAY impose implementation resource limits including:

- maximum decoded integer bit length;
- maximum term nesting depth;
- maximum decoded node count.

Exceeding such a limit MUST be reported as a **resource-limit refusal**, distinct from syntax errors such as truncation, invalid bits, or trailing data.

Resource-limit refusal does **not** imply that the canonical NEX bit string is malformed or semantically invalid.

The Stage 1 reference API therefore distinguishes:

```text
DecodeOne(bits, limits)   -> term + consumed bits | syntax/resource error
DecodeExact(bits, limits) -> term | syntax/resource/trailing error
```

A zero limit in the Go reference implementation means unlimited for that particular resource. Production embeddings SHOULD set explicit limits appropriate to their environment.

Byte-container padding is not handled by `DecodeExact`; the caller must provide the exact valid Core bit length before decoding, consistent with the v0.1 specification.

## Consequences

### Positive

- NEX wire validity remains architecture-independent.
- Implementations can defend against resource-exhaustion inputs without redefining the format.
- Conformance tests can distinguish malformed data from locally unsupported size.

### Cost

- Decoder APIs need an additional error class and limits object.
- Two conforming implementations may have different maximum accepted sizes while still agreeing on the syntax below both limits.

## Alternatives considered

### No implementation limits

Rejected. It is not realistic for untrusted or adversarial input and confuses mathematical unboundedness with finite implementation resources.

### Define fixed maxima in NEX-1 Core

Rejected for v0.1. A fixed global maximum would introduce an arbitrary implementation-oriented bound into an otherwise architecture-neutral mathematical format.

### Treat limit exhaustion as malformed input

Rejected. That would make syntactic validity depend on the receiver's resources.

## Follow-up validation

Stage 1 tests must demonstrate that:

- truncated `U(n)` and term encodings produce syntax errors;
- depth/node/integer limits produce `ResourceLimitError`;
- the same valid encoded term succeeds when sufficient limits are supplied;
- trailing bits are reported separately from both categories.
