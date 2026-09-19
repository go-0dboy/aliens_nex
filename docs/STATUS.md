# Project status

**Date:** 2026-09-19  
**Baseline branch:** `main`  
**Active work:** Post-Stage-5 NEX Core self-sufficiency extension (5.10–5.20)  
**Current state:** `Stages 0–5 complete; 5.10 accepted; 5.11 representation work versioned; 5.12a/b/c verified; 5.12d interleaved pair rejected under frozen budgets; 5.12e functional-stream v0.1 rejected; v0.2 passed frozen development and preregistered hold-out workloads and is accepted provisionally for the tested finite-bit-stream surface; Stage 6 remains Planned; NEX-1 v0.1 unchanged`  
**Active decision:** ADR-0018  
**Living dissertation:** `docs/RESEARCH-DISSERTATION.md` / `docs/RESEARCH-DISSERTATION.ru.md`

## Stable historical evidence

- Stage 0 — project/specification/ADR baseline — Complete.
- Stage 1 — canonical wire format — Complete, PR #3.
- Stage 2 — static validation and rank-1 HM inference — Complete, PR #4.
- Stage 3 — weak call-by-name dynamic semantics — Complete, PR #5.
- Stage 4 — empirical validation and benchmarking — Complete, PR #6.
- Stage 5 — independent reconstruction and receiver-conditioned bootstrap evidence — Complete.

Historical Stage 5.0–5.9 remains closed under ADR-0015. The 5.10–5.20 numbering is a **post-Stage-5 extension** and does not rewrite the blind-reconstruction/bootstrap experiment or its negative result.

The normative NEX-1 v0.1 Core remains unchanged:

```text
Var Lam App Let Nat Prim
zero-based de Bruijn binding
rank-1 HM Let polymorphism
Core primitives 0..10
weak call-by-name semantics
canonical binary wire
```

No new Core constructor, primitive, type former, wire rule, host callback, mutable-memory model, or native backend is authorized by the self-sufficiency workstream.

### Stage 4 frozen corpus

```text
programs   17
AST nodes  345
wire bits  1371

Prim  460
Var   286
App   264
Nat   244
Lam    84
Let    33
```

The Stage 4 call-by-need experiment preserved all 17 accepted observations while reducing the project-defined transition counter from 226,151 CBN transitions to 2,484 need transitions. The 98.90% figure is a transition-counter reduction, not a wall-clock claim.

### Stage 5 independent reconstruction

```text
cases total           942
portable matches      942
semantic mismatches     0
resource asymmetries    0
```

Composition:

```text
17   frozen corpus programs
325  valid cases = 25 parameter sets x 13 templates
100  static-error cases = 25 parameter sets x 4 families
500  randomized term shapes tested at wire level
```

This remains strong differential-conformance evidence on the tested surface, not a proof of semantic correctness or specification completeness.

### Receiver assumptions and bootstrap

Current research uses the corrected model:

```text
A0        exact binary-frame prior
A1        elementary discrete mathematics only
A1(R)     A1 + exact formal rule calculus R
A2(U)     A1 + exact universal binary machine U and framing
A_host(H) non-neutral terrestrial host control
```

Historical `assumptions-v0.1.json` remains frozen; current work uses `assumptions-v0.2.json`.

Bootstrap status is unchanged:

```text
accepted complete bootstrap candidates  0
full B | A known                        false
full SB | A known                       false
total C | A computable                  false
```

Python/Go implementations remain engineering controls, not receiver-neutral bootstrap.

## Post-Stage-5 Core self-sufficiency extension

ADR-0018 inserts an executable evidence gate before Stage 6 activation:

```text
5.10 contract and gate                 accepted
5.11 NEX-in-NEX meta-representation   versioned/validated checkpoints
5.12 self wire codec                   active
5.13 self structural validation        planned
5.14 self HM type inference            planned
5.15 self evaluator                    planned
5.16 integrated NEX-in-NEX toolchain  planned
5.17 self-processing                   planned
5.18 bounded/differential validation   planned
5.19 supporting metatheory             planned
5.20 decision gate                     planned
```

Reserved 5.20 outcomes remain:

```text
supported
supported_but_impractical
core_limitation_discovered
inconclusive
```

Difficulty is evidence to record; it does not authorize a NEX-1 v0.1 redesign.

## 5.11 — meta-representation checkpoints

The historical N-only candidate is frozen in:

```text
stage5/selfhost/meta-representation-v0.1.json
stage5/selfhost/validate_meta_representation.py
```

Every frozen meta-object there uses mathematical `N` as the physical Core carrier. No recursive type, list primitive, host AST, host byte array, new Core primitive, or wire change is assumed.

During 5.12 it became clear that v0.1 did not explicitly freeze the outer tagged-value formula. Historical v0.1 remains unchanged. `meta-representation-v0.2.json` explicitly records the candidate rule `tagged(tag,payload)=pair(tag,payload)` and is independently validated.

The later 5.12 experiments show that this numeric representation is useful as an expressiveness construction but is not automatically a practical recursive AST representation.

## 5.12a — executable arithmetic foundation

Frozen NEX-written helpers:

```text
add          : N -> N -> N
mul          : N -> N -> N
odd          : N -> N
halve        : N -> N
pow2         : N -> N
shift_right  : N -> N -> N
```

Verified:

```text
canonical functions                         6
canonical bits, counted as separate terms  756
test applications per implementation        22
Python/Go wire/type/Nat observations        matched
```

The 756-bit figure is an engineering size, not bootstrap cost and not `B | A` or `C | A`.

## 5.12b — N-only pair/sequence and sharing

Seven closed canonical NEX terms implement:

```text
meta_pair
v2
unpair_left
unpair_right
seq_cons
seq_head
seq_tail
```

Frozen workload result:

```text
canonical bits                           3290
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

Accepted interpretation: the bounded representation is executable, naive CBN is operationally poor, and two separately implemented sharing controls agree on the tested observations. This is not a NEX-specific equivalence proof and not a Core-defect finding.

## 5.12c — NEX-written integer codec

The integer part of canonical NEX wire has been implemented in NEX itself.

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

The single Python sharing refusal is an implementation-resource outcome; Go sharing and both direct host codec controls corroborate the returned semantics. This checkpoint is not yet complete `Term` encode/decode.

## 5.12d — recursive numeric pairing alternatives

The pow2-adic pair

```text
pair(a,b) = 2^a * (2*b+1) - 1
```

is mathematically valid but unsuitable for recursively materialized AST codes because the outer bit length can depend on the **numeric value** of an already encoded subtree.

A bit-interleaving candidate avoids the code-size explosion, but its NEX implementation requires repeated derived parity/halving operations.

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

The interleaved candidate is therefore **rejected as the primary recursive representation under the frozen budgets**. Its negative result is reproducibly checked. No resource limit was raised to make it pass.

This is evidence about the representation and available derived operations, not yet a fundamental Core limitation.

## 5.12e — fixed-type functional bit streams

To avoid packing recursive data into one large natural, the next experiment used:

```text
Stream = N -> N
0 = bit 0
1 = bit 1
2 = EOF
```

### v0.1 — rejected development candidate

The first producer recursively materialized a `cons` chain. It is structurally reproducible and typeable, but four development cases hit the frozen Python need transition limit:

```text
repeat(0,32)(31)
repeat(0,32)(32)
repeat(1,128)(127)
repeat(1,128)(128)

5,000,001 > 5,000,000 transitions
```

The negative result is preserved by `verify_functional_stream_v0_1_result.py`; the limit was not raised and the cases were not removed.

### Anti-tuning protocol

Before executing the successor candidate, the project froze:

```text
stage5/selfhost/experiment-protocol-v0.1.json
stage5/selfhost/validate_experiment_protocol.py
docs/experiments/stage5-selfhost-experiment-protocol.md
stage5/selfhost/functional-stream-holdout-v0.1.json
```

Rules include:

- previously observed cases are development/historical evidence, never retroactive hold-out;
- Python need: 5,000,000 transitions / depth 8,000;
- Go need and Go CBN: 5,000,000 transitions / depth 20,000;
- budgets cannot be increased after seeing a candidate result;
- failed cases cannot be deleted from the same candidate version;
- an algorithmic change after first execution requires a new candidate version;
- a hold-out failure rejects that version; tuning the same version against the same hold-out is forbidden.

### v0.2 — accepted finite-stream checkpoint on tested surface

v0.2 retains the same stream contract but changes `repeat` to direct indexed recursion over `(count,index)` rather than materializing a `cons` chain.

At protocol freeze, v0.2 had not yet been runtime-executed. Its candidate blob and the separately registered hold-out were frozen before execution.

Development run `35432007845` / job `105868178140`:

```text
canonical functions                         10
canonical bits, counted as separate terms  1,634
execution cases                              26
Python need resource refusals                 0
Go need resource refusals                     0
Go CBN resource refusals                      0
Python/Go need values matched               26/26
largest Python need transitions             13,855
largest Go need transitions                  6,418
```

The historical checkpoint regression then completed successfully, reproducing the prior positive and negative checkpoints.

The unchanged candidate was subsequently executed once against the preregistered 11-case hold-out in workflow run `35432186658`, job `105868647658`:

```text
hold-out cases                              11
Python need resource refusals                0
Go need resource refusals                    0
Go CBN resource refusals                     0
Python/Go need values matched              11/11
largest Python need transitions            13,747
largest Go need transitions                 6,368
```

Decision: `functional-stream-v0.2` is **accepted provisionally as the finite-bit-stream representation checkpoint for the tested surface**.

This supports the claim that dynamically sized finite bit data can be represented and queried with unchanged rank-1 HM functions/closures under the frozen budgets. It does **not** establish complete `Term` representation, type environments, substitutions, evaluator state, self-hosting, or receiver-neutral bootstrap.

Durable evidence:

```text
stage5/selfhost/functional-stream-v0.2-development-result-v0.1.json
stage5/selfhost/functional-stream-v0.2-holdout-result-v0.1.json
docs/experiments/stage5-selfhost-functional-stream.md
```

## CI structure after the protocol checkpoint

Fast active feedback and expensive historical checks are separated.

```text
stage5-self-sufficiency.yml
  -> protocol/contracts/reproducibility
  -> active candidate

stage5-self-sufficiency-regression.yml
  -> cheap trigger job on ordinary commits
  -> heavy historical regression only when latest commit changes checkpoint-trigger.txt

stage5-self-sufficiency-holdout.yml
  -> cheap trigger job on ordinary commits
  -> hold-out execution only when latest commit changes holdout-trigger-v0.1.txt
```

The latest-commit trigger behavior has been verified: ordinary commits run only the cheap trigger job and skip the heavy regression/hold-out job.

This changes scheduling only; the final merge gate still requires current historical evidence and research synthesis.

## Required final implementation target

The workstream still targets an exact canonical NEX implementation `I` with:

```text
Decode
Encode
Validate
Infer
Evaluate
```

plus self-processing checks over `code(I)`.

A native `NEX -> x86/ARM/WASM` compiler is not part of this gate; any such backend requires a separately declared target/profile.

## Stage 6 — teaching NEX

ADR-0017 remains Accepted. Stage 6 remains **Planned**, not Active, while the 5.10–5.20 gate is unresolved.

The retained pipeline is:

```text
receiver prior A
    -> NEX Teaching / Bootstrap Message T
    -> reconstructed NEX-1 competence
    -> conformance / self-test
    -> canonical NEX programs P
```

Existing Stage 6 planning artifacts remain planning artifacts, not accepted teaching messages and not sources of `T_bits`.

## Research synthesis / next step

The next technical experiment is **not** another unregistered representation tweak. Before code, Stage 5.12 must define and freeze a cursor/parser experiment over `Stream = N -> N`:

1. exact cursor/parser interface;
2. exact result representation compatible with unchanged NEX-1 v0.1;
3. development inputs and expected observations;
4. frozen resource budgets;
5. separate preregistered hold-out;
6. versioning rule for any post-execution algorithmic change.

Only after that contract is committed should the parser be executed for acceptance evidence.

Both living dissertation versions must incorporate ADR-0018, the pre-Stage-6 self-sufficiency question, the sharing qualification, the rejected numeric representations, and the accepted functional-stream checkpoint before PR #16 can leave draft.
