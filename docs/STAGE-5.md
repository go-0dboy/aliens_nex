# Stage 5 — Independent reconstruction and receiver-neutral bootstrap

**Status:** Planned; not started  
**Prerequisite:** Stage 4 complete  
**Primary purpose:** test whether NEX-1 v0.1 can be reconstructed independently from its specification/conformance artifacts and begin replacing the unknown bootstrap term `B` with explicit, assumption-conditioned artifacts rather than host-language proxies.

Stage 5 is an evidence stage, not a NEX-1 v0.2 redesign stage.

The two highest-value unresolved questions after Stage 4 are:

1. does the published NEX specification determine wire/static/dynamic behavior independently of the Go reference implementation?;
2. what information would a receiver actually need before NEX programs can be decoded, validated, typed, and evaluated, and can any of that information be represented as a measurable receiver-neutral bootstrap artifact?

The total-information objective remains:

```text
C = S + B + P
```

Stage 5 MUST NOT set `B = 0`, MUST NOT substitute Go/Rust/C source size for `B`, and MUST NOT claim an unconditional receiver-neutral `B` if the artifact still depends on undeclared assumptions.

## Stage 5.0 — independence protocol

Before writing a second implementation, freeze what the independent implementer is allowed to use.

Create a versioned **conformance packet** containing only the material intended to determine NEX behavior, for example:

```text
canonical NEX-1 v0.1 specification
relevant accepted ADRs
primitive IDs / schemes / arities as normative data
wire conformance vectors
static conformance vectors
evaluation conformance vectors
packet manifest + hashes
```

The first independent implementation MUST NOT be developed by translating `reference/go` source code.

The protocol must record:

- exact packet version/hash;
- selected implementation language/toolchain;
- what external literature may be consulted;
- what repository paths are excluded during the initial implementation;
- when comparison with the Go reference becomes allowed;
- how ambiguities/disagreements are classified.

A new ADR is required for the independence protocol and second-implementation language choice if that choice materially affects the research method.

## Stage 5.1 — conformance packet completeness audit

Before independent implementation, audit whether the packet contains enough information to reconstruct:

```text
U(n)
Term AST
canonical wire encode/decode
closed de Bruijn scope rules
Type / TypeScheme
primitive schemes
instantiation/generalization
unification + occurs check
Algorithm W behavior
primitive validity
dynamic WHNF semantics
primitive forcing behavior
fix/resource-limit distinction
```

Missing information must be repaired in the canonical specification/conformance artifacts before being treated as an implementation detail.

The packet itself should be reproducible from the repository by one command and should have a machine-readable manifest.

## Stage 5.2 — independent wire implementation

Using only the frozen packet and allowed external theory, implement independently:

```text
U(n) encode/decode
six-term AST
canonical term encode/decode
DecodeOne / exact-decoding equivalent
malformed-input classification
implementation resource-limit separation
```

Success criterion:

- all packet wire vectors pass;
- generated round trips/property tests pass in the independent implementation;
- no Go reference code was used as implementation guidance before the checkpoint.

Any disagreement is evidence, not something to hide by copying Go behavior.

## Stage 5.3 — independent static semantics

Implement from the specification/packet:

```text
closed-scope validation
type representation and schemes
free type variables
substitutions
unification + occurs check
primitive schemes
fresh instantiation
generalization
Algorithm W
principal type normalization for conformance
```

Success criterion:

- all static conformance vectors pass;
- independently inferred normalized principal schemes agree with the packet;
- negative cases preserve error-class distinctions where the packet defines them.

## Stage 5.4 — independent dynamic semantics

Implement the normative weak call-by-name evaluator from the specification, including:

```text
Var / Lam / App / Let / Nat / Prim
curried primitives
unit / succ / pred / ifz
pair / fst / snd
inl / inr / case
fix
selective forcing
WHNF observation
resource-limit separation
```

Call-by-need may be studied later, but MUST NOT replace the normative independent CBN implementation during the conformance proof.

Success criterion:

- all evaluation conformance vectors pass;
- laziness-sensitive cases pass;
- terminating `fix` examples pass;
- bounded refusal for non-terminating/resource-heavy examples remains distinguishable from invalidity.

## Stage 5.5 — differential conformance after independence freeze

Only after the first independent implementation is frozen at a declared checkpoint may it be compared directly with `reference/go`.

Run both implementations against:

```text
wire-v0.1 conformance
static-v0.1 conformance
eval-v0.1 conformance
frozen benchmark corpus v0.3
new deterministic generated terms where useful
```

Compare architecture-neutral outputs only:

```text
encoded bits
decoded canonical term
scope validity
normalized principal type scheme
observable WHNF
portable error class where specified
```

Do not compare host-specific allocation counts, object layouts, pointer identity, or runtime internals as conformance criteria.

Every discrepancy must be classified as one of:

```text
specification ambiguity / omission
Go reference bug
independent implementation bug
conformance-vector gap
deliberately unspecified implementation behavior
```

The classification and resolution become research evidence and must update the living dissertation under ADR-0012.

## Stage 5.6 — specification ambiguity audit and conformance hardening

The main value of a second implementation is not merely another green test suite. It is to reveal behavior that the first implementation may have assumed implicitly.

For every discovered ambiguity:

1. write the smallest reproducing term/bit stream;
2. state the competing interpretations;
3. determine whether v0.1 already has a defensible intended meaning;
4. clarify the canonical specification/ADR if necessary;
5. add a language-neutral conformance vector;
6. verify both implementations independently.

Do not resolve an ambiguity with the rule “match Go” unless the normative specification already supports that behavior.

If the audit requires an incompatible semantic/wire change, record it as future-version work; do not silently mutate NEX-1 v0.1.

## Stage 5.7 — receiver-assumption model for bootstrap

Before trying to assign a bit count to `B`, define exactly what the receiver is assumed to know.

Create a dependency/assumption model that separates at least:

```text
physical/channel assumptions
binary symbol/order assumptions
message framing / exact-length assumptions
basic mathematical assumptions
integer/self-delimiting-code assumptions
tree/term representation assumptions
binding/type/evaluation semantics
host-machine assumptions (which should not be hidden inside B)
```

The model may define several explicit assumption sets, for example `A0`, `A1`, `A2`, rather than pretending that one universally correct alien prior is known.

A bootstrap cost measured under assumptions `A` must be written conditionally:

```text
B | A
```

not simply `B`.

This is required to avoid claiming receiver neutrality while silently relying on terrestrial conventions.

## Stage 5.8 — first measurable bootstrap artifact

Design at least one concrete bootstrap candidate whose transmitted representation can be counted exactly under a declared assumption set.

The artifact must be more receiver-neutral than Go source and must explicitly expose every dependency needed to interpret it.

Possible forms may be investigated, but none is preselected as the answer:

```text
a tiny mathematical abstract machine
a minimal combinator/calculus bootstrap
a layered decoder -> validator -> evaluator description
a compact executable bootstrap notation with its own explicitly measured decoder base
```

The stage must guard against circular accounting. If a bootstrap artifact `X` requires an interpreter `Y`, the cost/assumption for `Y` cannot disappear from the model.

At least one report should attempt to decompose:

```text
B_decode
B_static
B_eval
B_total_candidate
```

under the declared assumption set.

If a defensible receiver-neutral candidate cannot yet be produced, that negative result is acceptable and must be recorded instead of substituting a host proxy.

## Stage 5.9 — research decision gate

At the end of Stage 5, answer separately:

### Independent reconstruction

- did a second implementation reproduce NEX behavior from the packet?;
- which ambiguities or hidden assumptions were discovered?;
- did the canonical specification/conformance suite require clarification?;
- is NEX-1 v0.1 now better supported as independently reconstructable?

### Bootstrap

- what receiver assumptions were made explicit?;
- is there a measurable bootstrap candidate?;
- is its cost unconditional or only `B | A`?;
- which portions of `S` and `B` remain unknown?;
- can total `C` be computed under any explicitly stated assumption set without substituting host-source proxies?

The decision gate must determine whether the next work should prioritize:

```text
specification repair
bootstrap refinement
broader independent implementations
formal verification
or only then a NEX-1 v0.2 compactness redesign
```

## Pull-request decomposition

Stage 5 should use multiple PRs with one dominant reason each rather than one very large PR. A recommended decomposition is:

1. **PR A — independence protocol + conformance packet**;
2. **PR B — independent wire/static implementation**;
3. **PR C — independent evaluator + differential conformance**;
4. **PR D — receiver-assumption model + bootstrap candidate**;
5. **PR E — Stage 5 research report / decision gate**.

Exact boundaries may change if evidence suggests a cleaner split, but independent implementation work must remain distinguishable from bootstrap-model work.

## Scope guard

Stage 5 MUST NOT introduce merely to make the work easier:

- NEX-1 v0.2 wire changes;
- new normative Core constructors/primitives;
- mutable memory/system profile;
- production frontend/parser;
- native compiler/backend;
- self-hosting claims before a receiver-neutral bootstrap contract exists;
- optimization of `Prim`/other wire fields based on Stage 4 before independent reconstruction is complete.

Experimental helper tools are allowed if they do not change normative v0.1 behavior.

## Definition of done

Stage 5 is complete only when all applicable items are true:

- an independence protocol and versioned conformance packet exist;
- a second implementation has been produced without translating `reference/go`;
- wire, static, and dynamic conformance pass independently;
- differential comparison with Go is performed only after the independence checkpoint;
- every discrepancy is classified and resolved or explicitly left open;
- discovered specification ambiguities produce specification/conformance hardening where appropriate;
- receiver assumptions for bootstrap are explicit and versioned;
- at least one measurable bootstrap candidate exists under explicit assumptions, or the inability to construct one is documented as a negative research result;
- `B` is never replaced with host-language source size;
- the Stage 5 decision gate records what is established, conditional, contradicted, and still unknown;
- `docs/RESEARCH-DISSERTATION.md` and `.ru.md` are enriched with all material Stage 5 evidence per ADR-0012;
- no prohibited NEX-1 v0.2/system/frontend work entered the stage.

## Starting gate

Do **not** start the independent implementation until the Stage 5 plan is reviewed and the independence protocol is accepted. The first implementation action should be Stage 5.0/5.1, not coding a second evaluator from memory.
