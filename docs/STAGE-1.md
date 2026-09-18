# Stage 1 — Wire foundation

**Status:** Complete  
**Completed:** 2026-09-18  
**Completed by:** PR `#3 stage1: implement NEX wire foundation`  
**Merge commit:** `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`

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
8. round-trip and fuzz/property tests;
9. repeatable repository verification through GitHub Actions.

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

Verification entry point:

```text
cd reference/go
sh verify.sh
```

The same command is executed by `.github/workflows/wire-foundation.yml` after a clean GitHub checkout.

## Conformance artifact

Language-neutral vectors live in:

```text
conformance/wire-v0.1.json
```

At Stage 1 completion the corpus contains:

- 17 `U(n)` integer vectors, including code-length boundaries and a value above 64-bit range;
- 12 canonical term vectors covering all six constructors and nested combinations;
- 15 invalid exact-input vectors covering truncation and trailing data.

A future second implementation must consume the same vectors rather than copying expected values into its own test source.

## Verification evidence

The final Stage 1 branch passed:

```text
gofmt check    PASS
go vet ./...   PASS
go test ./...  PASS
```

GitHub Actions run `35348259779` executed from a clean checkout and completed successfully.

A final one-second `FuzzTermRoundTrip` run completed 27,289 generated executions without a failure. This is empirical test evidence, not a formal proof of correctness.

## Definition of done — result

All Stage 1 completion conditions were satisfied:

- `U(n)` vectors pass;
- term golden vectors pass;
- `decode(encode(term)) == term` is exercised by generated/fuzzed terms;
- malformed/truncated inputs are rejected deterministically;
- resource-limit errors are distinct from malformed input;
- `DecodeOne` reports consumed bit count correctly;
- `DecodeExact` rejects trailing bits;
- conformance vectors are implementation-independent;
- reference verification is repeatable from the repository;
- CI repeats the verification from a clean checkout;
- no type inference or evaluator logic leaked into the wire package;
- the final PR diff was reviewed against the Stage 1 scope.

## Remaining limitations

Stage 1 does not claim:

- a formal proof of decoder correctness;
- independent confirmation by a second implementation;
- de Bruijn scope validity;
- primitive/profile semantic validity;
- type correctness;
- evaluator correctness;
- comparative size superiority over BLC, SKI/Jot, WebAssembly, or stack bytecode.

Those claims require later stages or separate experiments.

## Next layer after Stage 1

Stage 2 may now be planned around static validation:

```text
de Bruijn scope validation
  -> type representation
  -> substitutions/unification
  -> Algorithm W
```

Stage 2 should be specified and reviewed before its implementation begins.
