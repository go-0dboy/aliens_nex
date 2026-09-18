# Stage 1 — Wire foundation

**Status:** In progress  
**Branch:** `stage1/wire-foundation`

Stage 1 proves the canonical NEX-1 v0.1 wire grammar before type inference or evaluation is implemented.

## Scope

Stage 1 contains only:

1. `U(n)` encode/decode using the specification's Elias-gamma-of-`n+1` rule;
2. canonical in-memory representation of the six Core term constructors;
3. canonical `Term` encode/decode;
4. language-neutral conformance vectors;
5. exact-input and prefix-input decoder APIs;
6. deterministic malformed-input errors;
7. implementation resource limits reported separately from malformed input;
8. round-trip and fuzz/property tests.

Stage 1 explicitly excludes type inference, de Bruijn scope validation, evaluator semantics, frontends, optimizer passes, machine/system profiles, and self-hosting.

## Wire contract

The reference implementation exposes two decoding modes:

```text
DecodeOne(bits)   -> term + consumed bit count
DecodeExact(bits) -> exactly one term or trailing-bits error
```

`DecodeOne` is useful to embed NEX terms in an outer transport. `DecodeExact` is used for canonical Core payload validation when the exact valid bit length is already known.

Byte padding is not interpreted by the Core decoder. A transport container must remove padding by supplying the exact valid bit length first, as required by the v0.1 specification.

## Error classes

Stage 1 distinguishes:

- `truncated`: a syntactically incomplete prefix or integer code;
- `invalid bit`: an implementation bit sequence contains something other than `0` or `1`;
- `trailing bits`: `DecodeExact` decoded one complete term but input remains;
- `resource limit`: the implementation declined otherwise syntactically meaningful input because configured integer/depth/node limits were exceeded;
- `invalid in-memory term`: encoder input violates the six-constructor shape.

A resource-limit refusal is not evidence that the NEX bit string is malformed. See ADR-0006.

## Reference implementation

The first reference implementation is written in Go. See ADR-0005.

It is intentionally dependency-free outside the Go standard library. Arbitrary-precision NEX naturals are represented using `math/big.Int`.

Location:

```text
reference/go/
```

## Conformance artifact

Language-neutral vectors live in:

```text
conformance/wire-v0.1.json
```

They contain:

- `U(n)` vectors, including values above 64-bit range;
- term AST + canonical bit strings;
- invalid exact-input vectors with expected error class.

A future second implementation must consume the same vectors rather than copying expected values into its own test source.

## Definition of done

Stage 1 is complete when all of the following are true:

- `U(n)` vectors pass;
- term golden vectors pass;
- `decode(encode(term)) == term` is exercised by generated/fuzzed terms;
- malformed/truncated inputs are rejected deterministically;
- resource-limit errors are distinct from malformed input;
- `DecodeOne` reports consumed bit count correctly;
- `DecodeExact` rejects trailing bits;
- conformance vectors are implementation-independent;
- `go test ./...` and `go vet ./...` pass for the reference implementation;
- no type inference or evaluator logic has leaked into the wire package;
- `docs/STATUS.md` records verified results and remaining limitations.

## Next layer after Stage 1

Only after this stage is accepted should Stage 2 begin:

```text
de Bruijn scope validation
  -> type representation
  -> substitutions/unification
  -> Algorithm W
```
