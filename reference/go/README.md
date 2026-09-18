# Go reference implementation

This directory contains the first executable reference implementation of NEX-1 Core wire, static-validation, and dynamic-evaluation layers.

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

### Stage 3 — dynamic semantics

- environment-based weak call-by-name reference evaluation;
- non-memoizing `Thunk`, `Closure`, and de Bruijn runtime environments;
- non-strict lambda application and `Let`;
- weak-head runtime values for naturals, unit, functions, pairs, and sums;
- curried primitive application using arity stored in the authoritative primitive table;
- execution of all Core primitives `fix`, `succ`, `pred`, `ifz`, `pair`, `fst`, `snd`, `inl`, `inr`, `case`, and `unit`;
- delayed pair fields and sum payloads;
- branch/projection forcing only where required by the NEX-1 v0.1 contract;
- arbitrary-precision natural arithmetic;
- terminating recursion through `fix` and bounded resource refusal for demanded divergence;
- language-neutral evaluation conformance in `../../conformance/eval-v0.1.json`;
- evaluator determinism/property fuzzing.

The reference evaluator deliberately does **not** memoize thunks. A future call-by-need implementation may add sharing only if it remains observationally equivalent on Core programs.

Still outside this implementation stage:

- byte transport framing/padding container;
- external machine/system profiles;
- frontend source syntax;
- optimizer/compiler/self-hosting;
- call-by-need optimization/sharing implementation.

## Run verification

From the repository root:

```bash
cd reference/go
sh verify.sh
```

The script checks formatting and static analysis, runs the complete wire/static/evaluation unit and conformance suites, and performs short property fuzz runs for substitutions, unification, inference stability, and evaluation determinism.

Equivalent core checks:

```bash
gofmt -l nex/*.go
go vet ./...
go test ./...
```

The module intentionally uses no third-party dependencies.
