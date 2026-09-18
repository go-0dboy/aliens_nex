# Go reference implementation

This directory contains the first executable reference implementation of the NEX-1 wire layer.

It is **not** the language specification. The normative source is `../../docs/NEX-1-v0.1.md`; architecture decisions are recorded in ADR-0005 and ADR-0006.

## Stage 1 scope

Implemented here:

- `U(n)` encode/decode with arbitrary-precision naturals;
- the six Core term constructors;
- canonical term encoder/decoder;
- exact versus prefix decoding;
- explicit resource limits;
- language-neutral conformance vectors;
- unit and fuzz/property tests.

Not implemented here yet:

- de Bruijn scope validation;
- primitive/profile semantic validation;
- type inference;
- evaluator;
- byte transport framing/padding container.

## Run verification

From the repository root:

```bash
cd reference/go
sh verify.sh
```

The script checks `gofmt`, runs `go vet ./...`, and then `go test ./...`.

The equivalent commands can also be run individually:

```bash
gofmt -l nex/*.go
go vet ./...
go test ./...
```

Optional fuzzing:

```bash
go test -run '^$' -fuzz=FuzzTermRoundTrip -fuzztime=10s ./nex
```

The module intentionally uses no third-party dependencies.
