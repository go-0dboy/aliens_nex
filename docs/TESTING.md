# Testing and conformance strategy

NEX is a language/specification research project. Tests are implementation checks and empirical evidence that independently built systems interpret specified observations the same way. They are **not** a substitute for a formal proof when the claim being made is a theorem about all programs.

## 1. Test layers

### Unit tests

Cover local deterministic behavior:

- self-delimiting integer encoding/decoding;
- de Bruijn scope checks;
- type substitutions and free-type-variable operations;
- occurs check and unification;
- primitive lookup;
- individual reduction/forcing rules.

### Conformance vectors

Golden vectors connect specification text to portable observations.

Each vector records as applicable:

```text
name
canonical term
wire bits
expected decode result
expected principal type or static error class
expected weak-head observation
```

Important families include identity, polymorphic `let`, naturals/control, pair/projection, sums/case, recursion, malformed wire, scope failure, type mismatch, and occurs-check failure.

Conformance observations deliberately exclude host closures, pointer identity, internal thunk shape, fresh type-variable IDs, and exact fuel/step conventions.

A top-level functional result is currently observed coarsely as `Function`; lambda closures and unsaturated primitive functions are not serialized as different host objects. Consequently, semantic confidence for function values must also come from applying functions in testing contexts. A future exhaustive/contextual suite should strengthen this area rather than treating `Function == Function` as full extensional equivalence.

### Property and generated tests

Useful invariants include:

```text
decode(encode(term)) == term
encode(decode(bits)) == canonical(bits)
```

Generated syntax must distinguish arbitrary terms from well-scoped and well-typed terms.

Random testing supplements, but does not replace, systematic structural coverage.

### Bounded exhaustive tests

This is now an established evidence layer as well as a future workstream: Stage 5.12 used a precisely complete frozen 27-Term class for the full codec. Broader scope/static/evaluation classes and stronger function-application contexts remain future work.

For a chosen size bound, enumerate all or a precisely defined complete class of small terms, then classify/filter by:

```text
wire validity
closed scope
static validity
termination within a declared non-semantic search bound
```

Compare all independent implementations on portable observations. Bounded exhaustive enumeration provides a different kind of evidence from random sampling or repeated numeric parameterizations of a few AST templates.

### Differential tests

When multiple implementations exist, compare common inputs on:

- canonical encoding;
- acceptance/rejection and portable error class;
- principal type modulo alpha-renaming;
- terminating weak-head observations;
- resource refusal only as a separate implementation outcome.

Differential agreement is evidence, not a correctness oracle. It cannot reveal an error shared by every implementation, and independently developed versions may still have correlated faults [SRC-0024, SRC-0027].

The Stage 5 report must therefore be described precisely. Its 942 cases consist of:

```text
17   frozen corpus programs
325  valid cases = 25 parameter sets x 13 fixed AST templates
100  static-error cases = 25 parameter sets x 4 error families
500  randomized term shapes tested at wire level
```

The accepted claim is **strong differential-conformance evidence of reconstructability on the tested surface**, not proof of semantic correctness or specification completeness.

### Formal metatheory

Tests cannot establish universally quantified language-safety theorems. Before NEX claims formal type safety, the project should provide a paper or mechanized proof covering the exact Core, including its primitives and `fix`, with at least:

```text
canonical forms
preservation / subject reduction
an appropriate progress-or-partial-computation safety theorem
```

Likewise, literature on standard call-by-need calculi motivates the optimization but does not automatically prove NEX's exact CBN/call-by-need equivalence. A NEX-specific proof or mechanization is required for that stronger claim.

### Benchmarks

Benchmarks are separate from correctness tests.

For fixed programs record, where meaningful:

- encoded bit count;
- AST node count;
- type-check cost;
- explicitly defined evaluator counters;
- peak memory or allocations when reproducible;
- exact bootstrap/transmission segments only under a declared measurement contract.

Never reinterpret one implementation's runtime counter as an architecture-neutral performance metric or information-theoretic compactness result.

The Stage 4 `226151 -> 2484` number is an evaluator-transition-counter change, not a measured 98.90% wall-clock speedup.

## 2. Corpus discipline

Freezing a corpus before optimization prevents post-result editing. It does not make a hand-designed corpus representative.

Future empirical work should distinguish:

```text
design corpus
hold-out corpus
externally specified tasks
bounded-exhaustive/generated program families
```

Constructor shares such as `Prim = 33.6%` are properties of a declared corpus, not language-wide frequency estimates.

## 3. Regression rule

Every discovered implementation bug should produce the smallest practical regression test or conformance case before or with the fix.

A research-claim correction may instead require:

- a new ADR;
- a new literature source entry;
- a revised limitation/threat-to-validity statement;
- a new experiment rather than a code patch.

Historical evidence must not be silently rewritten to make earlier experiments appear stronger.

## 4. Failure-first workflow

For implementation defects:

```text
reproduce -> failing test -> minimal fix -> relevant full suite -> diff review
```

For research inconsistencies:

```text
claim -> primary source / artifact -> contradiction or limitation -> correction ADR -> regression/re-audit gate
```

Do not redesign multiple modules merely because one test or claim fails.

## 5. Claims and evidence vocabulary

Use precise language:

- `verified`: reproduced by an executable check on the stated commit/artifact;
- `formally proved`: established by a reviewed proof covering the exact stated system;
- `inferred`: follows from repository/spec reasoning but was not executed/proved here;
- `hypothesis`: requires experiment or proof;
- `not verified` / `unknown`: explicitly unresolved.

Do not write "all tests pass" unless the relevant complete suite actually ran on the reported commit.

## 6. Research re-audit gate

After a material correction to the research interpretation, the repository-level `research-reaudit` workflow is expected to rerun, on one head:

```text
Go reference + Stage 4 verification
frozen Stage 5 packet verification
frozen independent source hashes
independent Python verification
receiver-assumption validators
bootstrap-feasibility validator
942-case Go/Python differential comparison
```

This gate checks that a documentary/methodological correction has not silently invalidated earlier executable evidence. It does not turn empirical evidence into a theorem.
