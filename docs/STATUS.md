# Project status

**Date:** 2026-09-19  
**Baseline branch:** `main`  
**Active work:** Post-Stage-5 NEX Core self-sufficiency extension (5.10–5.20)  
**Current state:** `Stages 0–5 complete; 5.10 accepted; 5.11 representation work versioned; 5.12a/b/c verified; 5.12d interleaved pair rejected under frozen budgets; 5.12e functional-stream v0.1 rejected on development resource budget; v0.2 frozen under anti-tuning protocol and awaiting first runtime execution; Stage 6 remains Planned; NEX-1 v0.1 unchanged`  
**Active decision:** ADR-0018  
**Living dissertation:** `docs/RESEARCH-DISSERTATION.md` / `docs/RESEARCH-DISSERTATION.ru.md`

## Completed stages

- Stage 0 — project/specification/ADR baseline — Complete.
- Stage 1 — canonical wire format — Complete, PR #3.
- Stage 2 — static validation and rank-1 HM inference — Complete, PR #4.
- Stage 3 — weak call-by-name dynamic semantics — Complete, PR #5.
- Stage 4 — empirical validation and benchmarking — Complete, PR #6.
- Stage 5 — independent reconstruction and receiver-conditioned bootstrap evidence — Complete.

Historical Stage 5.0–5.9 remains closed under ADR-0015. The new 5.10–5.20 numbering denotes a **post-Stage-5 extension** and does not rewrite the blind-reconstruction/bootstrap experiment or its negative result.

## Post-Stage-5 research audit

The 2026-09-19 re-audit remains recorded in:

- `docs/RESEARCH-AUDIT-2026-09-19.md`;
- `docs/RESEARCH-AUDIT-2026-09-19.ru.md`;
- `docs/RELATED-WORK.md` / `docs/RELATED-WORK.ru.md`;
- ADR-0016.

No reviewed issue invalidates the NEX-1 v0.1 wire/static/dynamic semantics or frozen Stage 4–5 measurements.

Important corrections remain accepted:

- typed combinatory logic is a legitimate competitor;
- exact total cost is conditional on explicit receiver assumptions and concrete serialization;
- current receiver assumptions use `A1(R)` rather than hiding an executable rule calculus in `A1`;
- `942/942` is strong differential-conformance evidence, not a proof;
- the 98.90% Stage 4 result is an evaluator transition-counter reduction, not wall-clock speedup;
- Lincos, DeVito–Oehrle, Lingua Cosmica, CosmicOS, and exosemiotic work are design inputs for teachability;
- historical novelty is not a project success criterion.

## Stable evidence

### NEX-1 Core

The normative v0.1 object remains unchanged:

```text
Var Lam App Let Nat Prim
zero-based de Bruijn binding
rank-1 HM Let polymorphism
Core primitives 0..10
weak call-by-name semantics
canonical binary wire
```

No new Core constructor, primitive, type former, wire rule, host callback, mutable memory model, or native backend is authorized by the self-sufficiency workstream.

### Stage 4 corpus

```text
programs   17
AST nodes  345
wire bits  1371
```

Constructor attribution remains:

```text
Prim  460
Var   286
App   264
Nat   244
Lam    84
Let    33
```

### Stage 5 independent reconstruction

```text
cases total           942
portable matches      942
semantic mismatches     0
resource asymmetries    0
```

Case composition remains:

```text
17   frozen corpus programs
325  valid cases = 25 parameter sets x 13 templates
100  static-error cases = 25 parameter sets x 4 families
500  randomized term shapes tested at wire level
```

Accepted meaning remains strong differential-conformance evidence of reconstructability on the tested surface, not a proof of semantic correctness or specification completeness.

### Receiver assumptions

Historical Stage 5 evidence remains frozen in `assumptions-v0.1.json`. Current research uses `assumptions-v0.2.json`:

```text
A0        exact binary-frame prior
A1        elementary discrete mathematics only
A1(R)     A1 + exact formal rule calculus R
A2(U)     A1 + exact universal binary machine U and framing
A_host(H) non-neutral terrestrial host control
```

These are experimental conditions, not claims about actual extraterrestrial cognition.

### Bootstrap status

```text
accepted complete bootstrap candidates  0
full B | A known                        false
full SB | A known                       false
total C | A computable                  false
```

The Python/Go host implementations remain engineering controls, not receiver-neutral bootstrap. The post-Stage-5 self-sufficiency experiment does not retroactively change this result.

## Post-Stage-5 Core self-sufficiency extension

ADR-0018 inserts an executable evidence gate before Stage 6 activation:

```text
5.10 contract and gate                 accepted in ADR-0018
5.11 NEX-in-NEX meta-representation   versioned/validated checkpoints
5.12 self wire codec                   active; integer codec verified; recursive representation under controlled experiment
5.13 self structural validation        planned
5.14 self HM type inference            planned
5.15 self evaluator                    planned
5.16 integrated NEX-in-NEX toolchain  planned
5.17 self-processing                   planned
5.18 bounded/differential validation   planned
5.19 supporting metatheory             planned
5.20 decision gate                     planned
```

### 5.11 meta-representation checkpoints

The original candidate is:

```text
stage5/selfhost/meta-representation-v0.1.json
stage5/selfhost/validate_meta_representation.py
```

Every frozen meta-object uses only NEX mathematical naturals `N` as its physical Core carrier. No recursive type, list primitive, host AST, host byte array, new Core primitive, or wire change is assumed.

During 5.12 it became clear that v0.1 fixed tag inventories and payload shapes but did not explicitly freeze the outer tagged-value formula. Historical v0.1 remains unchanged. `meta-representation-v0.2.json` makes the candidate formula explicit as `tagged(tag,payload)=pair(tag,payload)` and is separately validated.

This versioning records clarification rather than silently rewriting prior evidence.

### 5.12a executable arithmetic foundation

Frozen artifacts:

```text
stage5/selfhost/build_foundation.py
stage5/selfhost/foundation-v0.1.json
stage5/selfhost/verify_foundation.py
docs/experiments/stage5-selfhost-foundation.md
```

The six derived NEX functions are:

```text
add          : N -> N -> N
mul          : N -> N -> N
odd          : N -> N
halve        : N -> N
pow2         : N -> N
shift_right  : N -> N -> N
```

Verified result:

```text
canonical functions                         6
canonical bits, counted as separate terms  756
test applications per implementation        22
Python/Go wire/type/Nat observations        matched
```

The `756` figure is a local engineering size, not bootstrap cost and not `B | A` or `C | A`.

### 5.12b N-only pair/sequence execution and sharing checkpoint

Seven canonical NEX terms implement the first pair/sequence candidate:

```text
meta_pair
v2
unpair_left
unpair_right
seq_cons
seq_head
seq_tail
```

They occupy 3,290 canonical bits when counted separately.

Frozen workload result:

```text
measurement cases                          37
Python CBN resource refusals                8
Go CBN resource refusals                    5
Python call-by-need resource refusals       0
Go call-by-need resource refusals           0
Python/Go need observation mismatches       0
```

Largest successful Go contrast:

```text
unpair_right(27)
CBN transitions       4,857,667
call-by-need              1,793
ratio                  ~2709.24x
```

Accepted interpretation remains:

- the representation is executable on the bounded workload;
- naive normative CBN is operationally poor;
- two independently implemented sharing controls agree on all 37 returned observations;
- sharing is an engineering feasibility condition for this representation;
- this is not a proof of CBN/call-by-need equivalence and not a Core-defect finding.

### 5.12c NEX-written integer codec

The self-hosting workstream then implemented the integer part of canonical NEX wire in NEX itself.

Artifacts:

```text
stage5/selfhost/build_integer_codec.py
stage5/selfhost/integer-codec-v0.1.json
stage5/selfhost/verify_integer_codec.py
docs/experiments/stage5-selfhost-integer-codec.md
```

Verified measurements:

```text
canonical functions                         6
canonical bits, counted as separate terms  11,881
canonical encodeU bits                      3,860
canonical decodeU bits                      4,249
NEX execution cases                            25
Python call-by-need resource refusals           1
Go call-by-need resource refusals               0
Go CBN resource refusals                       13
Python/Go need observations                 matched wherever Python returned
Python/Go direct U(n) host controls          matched
```

The single Python sharing refusal remains an implementation-resource outcome; the Go sharing control and both direct host codec controls corroborate the returned semantics. This checkpoint does not yet include complete `Term` encode/decode.

### 5.12d recursive numeric pairing alternatives

Attempting to extend numeric pairing from small sequences to recursive ASTs exposed a distinct problem.

For the original pow2-adic pair,

```text
pair(a,b) = 2^a * (2*b+1) - 1
```

recursive use can make the bit length of an outer code depend on the **numeric value** of an already encoded subtree. This is operationally unsuitable for materializing realistic self ASTs.

A bit-interleaving bijection was therefore implemented as a versioned executable candidate. It avoids the size explosion, but its NEX implementation depends on repeated parity/halving of packed naturals.

Frozen result:

```text
canonical functions                     3
canonical bits                        1,531
execution cases                          27
Python call-by-need resource refusals     6
Go call-by-need resource refusals         4
Go CBN resource refusals                 14
Python/Go need values compared            21
returned semantic mismatches               0
```

The Go sharing refusals are depth refusals on the predeclared workload, including `pair(27,39)`, `pair(95,111)` and unpairing `14847`.

Decision: the interleaved candidate is **rejected as the primary recursive representation under the frozen budgets**. The rejection is reproduced by `verify_interleaved_pair_result.py`; limits were not raised to make the candidate pass.

This is evidence about the representation/available derived operations, not yet evidence of a fundamental NEX Core limitation.

### 5.12e functional-stream representation experiment

To avoid packing recursive data into one huge natural, the next candidate uses functions already present in NEX:

```text
Stream = N -> N
0 = bit 0
1 = bit 1
2 = EOF
```

#### v0.1 — cons-chain development candidate

The v0.1 artifact is structurally reproducible and typeable. Its recursive `repeat` producer materializes a `cons` chain.

Under the unchanged Python call-by-need budget of 5,000,000 transitions, the following development cases refuse at transition `5,000,001`:

```text
repeat(0,32)(31)
repeat(0,32)(32)
repeat(1,128)(127)
repeat(1,128)(128)
```

v0.1 is therefore a recorded negative development checkpoint. `verify_functional_stream_v0_1_result.py` preserves that exact result.

#### v0.2 — frozen indexed candidate, not yet runtime-executed

v0.2 keeps the same stream contract but replaces only `repeat` with direct indexed recursion over `(count,index)`; it does not build the recursive cons chain first.

Artifacts:

```text
stage5/selfhost/build_functional_stream_v0_2.py
stage5/selfhost/functional-stream-v0.2.json
stage5/selfhost/verify_functional_stream_v0_2.py
```

At the protocol checkpoint, its effective 10 terms occupy 1,634 bits counted separately; `stream_repeat` is 134 bits and `repeat_query` is 236 bits.

Crucially, v0.2 has not yet been runtime-executed. Before that first execution the experiment rules and a separate hold-out were preregistered.

### 5.12 experimental protocol — frozen before v0.2 runtime

Artifacts:

```text
stage5/selfhost/experiment-protocol-v0.1.json
stage5/selfhost/validate_experiment_protocol.py
docs/experiments/stage5-selfhost-experiment-protocol.md
stage5/selfhost/functional-stream-holdout-v0.1.json
```

Rules now enforced:

- all cases already observed before the protocol are development/historical evidence, never retroactive hold-out;
- Python need budget is fixed at 5,000,000 transitions / depth 8,000;
- Go need and Go CBN budgets are fixed at 5,000,000 transitions / depth 20,000;
- limits cannot be increased after seeing a candidate result;
- failing cases cannot be deleted from the same candidate version;
- algorithmic change requires a new candidate version;
- verifier-only repair is allowed only if candidate wire, inputs, expected semantics and budgets do not change;
- v0.2 must first pass the already observed development workload unchanged;
- only then may the preregistered 11-case hold-out be executed;
- a hold-out failure rejects v0.2; tuning the same v0.2 against that hold-out is forbidden.

This protocol was introduced specifically to prevent benchmark chasing and make either positive or negative evidence interpretable.

### CI scheduling after the protocol checkpoint

The expensive historical chain is no longer the feedback loop for every active-candidate edit.

```text
stage5-self-sufficiency.yml
  -> contract/protocol/reproducibility
  -> active candidate only

stage5-self-sufficiency-regression.yml
  -> explicit checkpoint / frozen-evidence regression
  -> 5.12a/b/c
  -> reproduced 5.12d rejection
  -> reproduced functional-stream v0.1 rejection
  -> independent Python / Go historical verification
```

`stage5/selfhost/checkpoint-trigger.txt` provides an explicit way to request a full historical checkpoint before merge or at a research boundary.

This changes scheduling, not the final quality gate.

## Required final implementation target

The workstream still targets an exact canonical NEX implementation `I` with:

```text
Decode
Encode
Validate
Infer
Evaluate
```

and self-processing checks over `code(I)`.

A native `NEX -> x86/ARM/WASM` compiler is not part of this gate. Such a backend requires a separately declared target/profile.

## Decision outcomes reserved for 5.20

```text
supported
supported_but_impractical
core_limitation_discovered
inconclusive
```

Difficulty during implementation is evidence to record; it does not itself authorize a NEX-1 v0.1 redesign.

## Stage 6 — teaching NEX

ADR-0017 remains Accepted and establishes the teaching/Core boundary:

```text
receiver prior A
    -> NEX Teaching / Bootstrap Message T
    -> reconstructed NEX-1 competence
    -> conformance / self-test
    -> canonical NEX programs P
```

Stage 6 remains **Planned**, not Active, while the 5.10–5.20 gate is unresolved.

Existing Stage 6 planning artifacts remain:

```text
docs/STAGE-6.md
stage6/curriculum-plan-v0.1.json
stage6/validate_plan.py
docs/adr/0017-separate-teaching-protocol-from-core.md
```

`curriculum-plan-v0.1.json` remains a planning artifact, not an accepted teaching message and not a source of `T_bits`.

## Supporting evidence work

The following remain important across the pre-Stage-6 workstream and later Stage 6:

- NEX-specific canonical forms / preservation / progress-or-safety metatheory;
- NEX-specific call-by-need observational-preservation reasoning;
- bounded exhaustive small-term comparison across independent implementations, including function application contexts;
- hold-out and independently specified workloads.

These support confidence in the target Core but do not replace either the self-sufficiency gate or the later teaching experiment.

## Research synthesis status

ADR-0018 and the 5.12 representation/resource findings are research-significant. Both living dissertation versions must incorporate the pre-Stage-6 self-sufficiency question, the sharing qualification, and the representation/resource results before this PR can leave draft.

## Next step — fixed by the protocol

1. validate the new experiment protocol and both functional-stream artifacts;
2. obtain a green historical checkpoint regression with the v0.1 negative result reproduced;
3. execute `functional-stream-v0.2` against the already observed development workload with frozen budgets;
4. if v0.2 fails, reject it without changing its limits or deleting cases;
5. if v0.2 passes, execute the preregistered 11-case hold-out **once** without changing v0.2;
6. only after that decision may the project choose the representation basis for the next `Term`/wire parser experiment.
