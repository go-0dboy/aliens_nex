# Testing and conformance strategy

NEX is a language/specification project. Tests are not only implementation checks; they are executable evidence that independent implementations interpret the specification the same way.

## 1. Test layers

### Unit tests

Cover local deterministic behavior:

- self-delimiting integer encoding/decoding;
- de Bruijn scope checks;
- substitutions and type substitutions;
- free-type-variable calculation;
- occurs check;
- unification;
- primitive lookup;
- individual reduction rules.

### Conformance vectors

Golden vectors connect specification text to observable behavior.

Each vector should record as applicable:

```text
name
canonical term
wire bits
expected decode result
expected principal type or expected type error
expected evaluation result or expected divergence classification if bounded
```

Initial vectors should include:

- identity;
- constant function;
- application;
- polymorphic `let` reuse;
- `succ` / `pred`;
- `ifz` branch laziness;
- pair/fst/snd;
- inl/inr/case;
- recursive arithmetic using `fix`;
- malformed wire prefixes;
- out-of-scope de Bruijn indices;
- unification failure;
- occurs-check failure.

### Property tests

Where the implementation language supports them, test invariants such as:

```text
decode(encode(term)) == term
encode(decode(bits)) == canonical(bits)
```

for valid generated closed terms within bounded size.

Typing-related generated tests should preserve the distinction between arbitrary syntax and well-typed syntax.

### Differential tests

When a second implementation exists, run the same vector corpus against both implementations and compare:

- acceptance/rejection;
- inferred type modulo renaming of type variables;
- canonical encoding;
- terminating evaluation results.

### Benchmarks

Benchmarks are separate from correctness tests.

For fixed programs record:

- encoded bit count;
- AST node count;
- type-check cost;
- evaluation/reduction work;
- peak implementation memory when reproducible;
- bootstrap binary/source size under a precisely stated measurement method.

Never treat one implementation's runtime performance as proof about the language's information-theoretic compactness.

## 2. Regression rule

Every discovered bug should produce the smallest practical regression test or conformance vector before or with the fix.

A bug fix without reproducible evidence risks becoming a transient patch.

## 3. Failure-first workflow

For implementation defects:

```text
reproduce -> failing test -> minimal fix -> full relevant suite -> diff review
```

Start with the first concrete failure. Do not redesign multiple modules simultaneously because one test failed.

## 4. Claims and evidence

Use precise language in reports:

- `verified`: reproduced by an executable check in the current work;
- `inferred`: follows from repository/spec reasoning but was not executed;
- `hypothesis`: needs experiment;
- `not verified`: explicitly unknown.

Do not write "all tests pass" unless the relevant complete suite was actually run on the commit being reported.

## 5. Initial definition of green

Once code exists, a pull request is expected to be green on all applicable checks:

```text
format
lint/static analysis
type/build
unit tests
conformance tests
```

Benchmark regressions may initially report rather than fail CI until stable thresholds are established by ADR.
