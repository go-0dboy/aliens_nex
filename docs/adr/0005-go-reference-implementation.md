# ADR-0005: Use Go for the first reference implementation

- **Status:** Accepted
- **Date:** 2026-09-18

## Context

Stage 1 needs a small executable reference implementation of the NEX-1 wire grammar. The implementation language must not become part of NEX semantics, but it should make the reference easy to audit, test, and reproduce.

NEX `N` is arbitrary precision, so a host language with standard-library arbitrary-precision integers materially reduces implementation-specific complexity.

## Decision drivers

- static host-language typing;
- arbitrary-precision integer support without third-party dependencies;
- simple package/module model;
- built-in unit and fuzz/property testing support;
- straightforward readable code suitable as a reference rather than an optimized production implementation;
- reproducible builds with no external runtime libraries required by the codec.

## Decision

The first NEX reference implementation will be written in **Go** and live under:

```text
reference/go/
```

The module declares Go 1.23 compatibility and intentionally uses only stable language/library features available there. Current upstream Go documentation is reviewed from the current Go 1.27 line; compatibility with older Go is a project implementation choice, not a statement about the current Go release.

The implementation MUST use only the Go standard library during Stage 1. NEX arbitrary-precision naturals are represented with `math/big.Int`.

Go is an implementation vehicle only. No behavior is normative merely because the Go code behaves that way; the English NEX specification and accepted ADRs remain authoritative.

Relevant external documentation is registered as `SRC-0010`.

## Consequences

### Positive

- `math/big` avoids inventing or importing a bigint implementation for `N`.
- `testing` provides table tests and fuzzing through the standard toolchain.
- The reference codec can remain dependency-free.
- Static host typing catches many implementation-shape errors without changing NEX's own type system.

### Cost

- Go garbage collection and runtime behavior say nothing about future NEX bootstrap size or target runtime design.
- `big.Int` is an implementation representation and must not leak into the language specification.
- A second implementation in another language is still required before implementation independence can be demonstrated empirically.

## Alternatives considered

### Rust

Deferred as a future independent implementation. Rust is strongly typed and well suited to systems software, but arbitrary-precision integers are not provided by its standard library, so the first faithful `N` implementation would require either a third-party crate or extra bigint code. That is undesirable for the minimal reference baseline.

### Python

Rejected for the first reference implementation. Python provides arbitrary-precision integers and excellent prototyping speed, but its dynamic host typing gives weaker structural feedback for the reference model.

### C or C++

Rejected for the first reference implementation. Neither standard library directly provides the arbitrary-precision natural representation required by NEX, which would add implementation noise unrelated to Stage 1.

## Follow-up validation

- `go test ./...` must pass from `reference/go/`.
- `go vet ./...` must pass.
- Conformance data must live outside Go source code so another language can consume the same vectors.
- A future second implementation should be compared against the same conformance corpus.
