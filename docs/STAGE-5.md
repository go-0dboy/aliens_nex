# Stage 5 — Independent reconstruction and receiver-neutral bootstrap

**Status:** In progress — Stage 5.0–5.5 verified; 5.6 current audit conclusion recorded; bootstrap work 5.7–5.9 not started  
**Active branch:** `stage5/independent-differential`  
**Prerequisite:** Stage 4 complete  
**Primary purpose:** test whether NEX-1 v0.1 can be reconstructed independently from specification/conformance artifacts and replace the unknown bootstrap term `B` with explicit assumption-conditioned evidence rather than host-language proxies.

Stage 5 is an evidence stage, not a NEX-1 v0.2 redesign stage.

The two highest-value questions after Stage 4 are:

1. does the published NEX specification determine wire/static/dynamic behavior independently of the Go reference implementation?;
2. what information would a receiver actually need before NEX programs can be decoded, validated, typed, and evaluated, and can that information be represented as a measurable receiver-neutral bootstrap artifact?

The total-information objective remains:

```text
C = S + B + P
```

Stage 5 MUST NOT set `B = 0`, MUST NOT substitute Go/Python/Rust/C source size for `B`, and MUST NOT claim an unconditional receiver-neutral `B` while the artifact depends on undeclared assumptions.

## Current checkpoint — 2026-09-18

### Protocol/packet

Stage 5.0 and 5.1 were completed by PR #7 and squash-merged as:

```text
04f4f84cce50a15638802babbe934b70e495911c
```

Post-merge `stage5-independence` run `35383798779` passed.

ADR-0013 fixes the independence protocol:

- frozen NEX source snapshot `4f9c50aed13cdbdf72c9ce6510521477d49c05a5`;
- Python 3.12+ standard-library-only as the first independent target;
- `reference/go/**` and implementation-revealing material excluded during blind implementation;
- ADR-0008 intentionally excluded because it documents Go evaluator architecture rather than portable NEX runtime structure;
- a fresh isolated model/context or different implementer required for independent evidence;
- direct Go comparison allowed only after a declared independent checkpoint is frozen.

The standalone packet is identified as:

```text
nex1-independent-conformance-packet-v0.1
```

and is reproducibly materialized by `stage5/build_packet.py` from exact Git-blob hashes.

The Stage 5.1 audit found two presentation gaps, resolved only as packet observation conventions:

1. canonical alpha-normalized principal-scheme rendering `T0`, `T1`, ...;
2. JSON `kind/value/a/b` mapping for conformance fixtures.

Neither changes NEX-1 v0.1 semantics or canonical wire syntax.

### Independent reconstruction checkpoint

A separate model/context received the frozen packet and returned:

```text
nex1-independent-python-v0.1.zip
```

Frozen received archive:

```text
sha256:
783e4186f9a8c024f00a732deae33b547c81ed4d7639c610a1e8bc5997eb3fbe

ZIP comment / external checkpoint marker:
a594b73b711998df04b45eec296086d5577fba2f
```

Before `reference/go` was opened for comparison, the implementation independently passed:

```text
17 / 17 integer wire vectors
12 / 12 term wire vectors
15 / 15 invalid exact-wire vectors
15 / 15 scope vectors
19 / 19 type vectors
21 / 21 evaluation vectors
23 / 23 independent tests
```

Additional pre-comparison audit exercised 20,000 generated wire round trips, large arbitrary-precision integers, typing/laziness cases, and resource-refusal separation without detecting a failure.

The frozen author-written source/tests/notes are imported under `independent/python/`. The canonical packet itself is re-materialized in CI rather than duplicated as an editable repository copy.

`stage5/independent-checkpoints/python-v0.1.json` records the received archive identity and exact SHA-256/byte length for every frozen imported file. `stage5/verify_independent_checkpoint.py` ensures later work cannot silently modify the independent implementation.

### Post-freeze differential result

Only after the archive identity was frozen was `reference/go` opened for direct comparison.

The comparison layer is outside the frozen Python subtree and compares portable observations only:

```text
canonical wire bits
normalized principal type / portable static error class
observable WHNF / portable evaluation error class
```

It does not compare runtime representation, fresh IDs, transition counts, object layout, allocations, closure/thunk machinery, or other host-specific details.

Accepted clean-checkout evidence:

```text
reference-go       run 35384938291 — success
stage5-independence run 35384938418 — success
stage5-differential run 35384938381 — success
```

Differential report:

```text
schema              nex-stage5-differential-report-v0.1
seed                20260918
cases total         942
corpus v0.3          17
generated valid     325
generated static    100
generated wire      500
portable matches    942
mismatches            0
resource asymmetries  0
success             true
```

Artifact:

```text
id      10563821507
digest  sha256:bda41629934f1c7b8f2554726002c3af5186d8cb19df649d8fab72129f8ba62a
```

This provides strong empirical evidence that NEX-1 v0.1 wire, static semantics and observable CBN behavior can be reconstructed from the frozen specification/conformance packet without translating the Go implementation. It is not a formal completeness proof and does not prove agreement for every possible valid or invalid program.

One independent ambiguity remains deliberately non-portable: for a term containing multiple independent static defects, the specification does not define a global diagnostic precedence. The Python implementation uses a scope-first validation order, and post-freeze inspection found that Go currently does likewise, but that coincidence is not promoted to NEX semantics because no portable need has been demonstrated.

## Stage 5.0 — independence protocol — Complete

Before a second implementation is written, freeze what it is allowed to observe.

Required protocol data:

```text
packet version/hash
implementation language/toolchain
allowlisted theory
excluded repository paths
independent-freeze boundary
discrepancy classification rules
```

Result: ADR-0013 and packet v0.1 satisfy this requirement.

## Stage 5.1 — conformance packet completeness audit — Complete

The packet must determine enough behavior to reconstruct:

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
WHNF / weak CBN semantics
primitive selective forcing
fix
resource-refusal separation
```

Result: no known missing Core semantic rule blocked the independent reconstruction. F1/F2 presentation conventions were made explicit without changing v0.1 semantics.

## Stage 5.2 — independent wire implementation — Complete for first independent implementation

Success criteria achieved:

- all packet wire vectors pass;
- generated round trips pass;
- arbitrary-precision naturals are supported;
- malformed input and implementation resource refusal remain distinct;
- implementation was frozen before Go comparison.

## Stage 5.3 — independent static semantics — Complete for first independent implementation

Independently reconstructed:

```text
closed scope validation
type/scheme representation
free type variables
substitutions
unification + occurs check
primitive schemes
fresh instantiation
generalization
Algorithm-W-style inference
canonical principal-scheme observation
```

All packet static vectors pass.

## Stage 5.4 — independent dynamic semantics — Complete for first independent implementation

Independently reconstructed normative weak call-by-name behavior including:

```text
Var / Lam / App / Let / Nat / Prim
partial primitive application
unit / succ / pred / ifz
pair / fst / snd
inl / inr / case
fix
selective forcing
WHNF observation
resource-refusal separation
```

All packet evaluator vectors and independent laziness/resource tests pass.

The Python runtime is not required to reproduce Go runtime internals. Its use of a dedicated recursive `FixThunk` is one concrete example of an independently chosen representation.

## Stage 5.5 — differential conformance after independence freeze — Complete for current evidence set

The first accepted differential set contains 942 deterministic cases and produced:

```text
942 portable matches
0 semantic mismatches
0 resource asymmetries
```

Any future enlargement of the differential corpus must remain versioned/reproducible and must not mutate the frozen independent checkpoint.

## Stage 5.6 — specification ambiguity audit and conformance hardening — Current audit complete; no normative change required

Every discrepancy, when found, must be classified as one of:

```text
specification ambiguity / omission
Go reference bug
independent implementation bug
conformance-vector gap
deliberately unspecified implementation behavior
```

Current evidence produced no semantic discrepancy requiring v0.1 repair.

The known multi-error diagnostic-precedence question remains intentionally unspecified because:

- it does not alter successful program semantics;
- existing conformance does not require a global precedence;
- both current implementations happen to choose scope-first, but agreement alone is not a normative argument.

If later testing exposes a portable ambiguity, add the smallest reproducer and language-neutral vector. Do not resolve ambiguities by the rule “match Go”.

## Stage 5.7 — receiver-assumption model for bootstrap — Next

Before assigning a bit count to `B`, define exactly what the receiver is assumed to know.

The assumption model must separate at least:

```text
physical/channel assumptions
binary symbol/order assumptions
message framing / exact-length assumptions
basic mathematical assumptions
integer/self-delimiting-code assumptions
tree/term representation assumptions
binding/type/evaluation assumptions
host-machine assumptions that must not be hidden
```

The model may define explicit assumption sets such as `A0`, `A1`, `A2`.

A bootstrap cost under assumptions `A` must be written:

```text
B | A
```

not simply `B`.

## Stage 5.8 — first measurable bootstrap artifact — Planned

Design at least one concrete bootstrap candidate whose transmitted representation can be counted exactly under a declared assumption set.

Possible forms may be explored but none is assumed correct in advance:

```text
tiny mathematical abstract machine
minimal combinator/calculus bootstrap
layered decoder -> validator -> evaluator description
compact executable bootstrap notation with explicitly accounted decoder base
```

Avoid circular accounting: if artifact `X` requires interpreter `Y`, then `Y` must either be declared in assumptions or accounted for.

Attempt to decompose at least:

```text
B_decode
B_static
B_eval
B_total_candidate
```

under a declared assumption set.

If no defensible candidate can be built, record that as a negative research result rather than substituting host source size.

## Stage 5.9 — research decision gate — Planned

At Stage 5 completion answer separately:

### Independent reconstruction

- can another implementation reproduce NEX from the frozen packet?;
- which ambiguities/hidden assumptions were exposed?;
- did v0.1 require clarification?;
- how strong is the evidence for independent reconstructability?

Current provisional answer: the first independent Python implementation reproduced the accepted portable evidence and matched Go on all 942 post-freeze differential cases, with no known semantic discrepancy.

### Bootstrap

- what receiver assumptions are explicit?;
- is there a measurable bootstrap candidate?;
- what is `B | A`?;
- which parts of `S` and `B` remain unknown?;
- can `C` be evaluated under any explicit assumption set without host-source proxies?

No answer is yet accepted for this half.

## Pull-request decomposition

Stage 5 uses multiple PRs with one dominant reason each:

1. **PR #7 — independence protocol + conformance packet** — merged;
2. **PR #8 — frozen independent implementation + differential conformance** — in progress;
3. **next PR — receiver-assumption model**;
4. **next PR — bootstrap candidate/measurement**;
5. **final Stage 5 PR — research decision gate / closeout**.

Exact later boundaries may change if evidence suggests a cleaner decomposition.

## Scope guard

Stage 5 MUST NOT introduce merely to make the work easier:

- NEX-1 v0.2 wire changes;
- new normative Core constructors/primitives;
- mutable memory/system profile;
- production frontend/parser;
- native compiler/backend;
- self-hosting claims before a receiver-neutral bootstrap contract exists;
- compactness redesign based on Stage 4 before independent reconstruction is complete.

Experimental helper tools are allowed if they do not change normative v0.1 behavior.

## Definition of done

Stage 5 is complete only when all applicable items are true:

- [x] independence protocol and versioned conformance packet exist;
- [x] a second implementation has been produced without translating `reference/go`;
- [x] wire, static, and dynamic conformance pass independently;
- [x] differential comparison with Go occurs only after the independent checkpoint;
- [x] current differential discrepancies are classified (none found in accepted 942-case run);
- [x] current ambiguity audit is recorded and does not silently promote implementation behavior to semantics;
- [ ] receiver assumptions for bootstrap are explicit and versioned;
- [ ] at least one measurable bootstrap candidate exists under explicit assumptions, or inability to construct one is documented as a negative result;
- [x] `B` has never been replaced with host-language source size;
- [ ] Stage 5 final decision gate records established, conditional, contradicted, and unknown results;
- [ ] living dissertation EN/RU includes all material Stage 5 evidence;
- [x] no prohibited NEX-1 v0.2/system/frontend work has entered the stage so far.

## Next starting gate

Do not redesign NEX after the successful independent reconstruction. The next implementation task is **Stage 5.7: define versioned receiver-assumption sets**.

Before creating any bootstrap artifact, specify what is free/assumed and what must be transmitted. Only then may a candidate `B | A` be measured.
