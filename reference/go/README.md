# Go reference implementation

This directory contains the first executable reference implementation of NEX-1 Core wire and static-validation layers.

It is **not** the language specification. The normative source is `../../docs/NEX-1-v0.1.md`; architectural decisions are recorded in ADRs.

## Implemented

### Stage 1 — wire foundation

- `U(n)` encode/decode with arbitrary-precision naturals;
- the six Core term constructors;
- canonical term encoder/decoder;
- exact versus prefix decoding;
- explicit decoder resource limits;
- language-neutral wire conformance vectors.

### Stage 2 — static validation

- zero-based de Bruijn closed-scope validation;
- monotypes and rank-1 type schemes;
- free type variables;
- substitutions and substitution composition;
- structural unification with occurs check;
- one authoritative Core primitive metadata/type table for IDs `0..10`;
- primitive validity checking without an external profile;
- fresh scheme instantiation and let-generalization;
- Algorithm-W-style inference for `Var`, `Lam`, `App`, `Let`, `Nat`, and `Prim`;
- canonical principal-type rendering independent of internal type-variable IDs;
- language-neutral positive/negative static conformance vectors;
- unit, property, and fuzz tests.

Still outside this implementation stage:

- evaluator/reduction semantics;
- execution of Core primitives;
- byte transport framing/padding container;
- external machine/system profiles;
- frontend source syntax;
- optimizer/compiler/self-hosting.

## Run verification

From the repository root:

```bash
cd reference/go
sh verify.sh
```

The script checks formatting and static analysis, runs the complete unit/conformance suite, and performs short property fuzz runs for substitutions, unification, and inference stability.

Equivalent core checks:

```bash
gofmt -l nex/*.go
go vet ./...
go test ./...
```

The module intentionally uses no third-party dependencies.
