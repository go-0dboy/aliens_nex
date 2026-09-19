# Project status

**Date:** 2026-09-19  
**Baseline branch:** `main`  
**Active work:** Post-Stage-5 NEX Core self-sufficiency extension (5.10–5.20)  
**Current state:** `Stages 0–5 complete; 5.10 accepted; 5.11 representation work versioned; 5.12a/b/c verified; 5.12d interleaved pair rejected under frozen budgets; 5.12e functional-stream v0.1 rejected and v0.2 accepted provisionally on frozen development+hold-out surfaces; 5.12f NEX-written stream parser passed frozen development and preregistered hold-out and is accepted for bounded canonical-wire traversal; Stage 6 remains Planned; NEX-1 v0.1 unchanged`  
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
5.12 self wire codec                   active; bounded stream traversal accepted
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

## 5.12f — NEX-written cursor/parser over functional streams

Before implementation, the project preregistered the parser interface, 27 development cases, 12 separate hold-out cases, unchanged resource budgets, and a host oracle:

```text
stage5/selfhost/parser-contract-v0.1.json
stage5/selfhost/parser-development-v0.1.json
stage5/selfhost/parser-holdout-v0.1.json
stage5/selfhost/validate_parser_contract.py
```

The fixed interface is:

```text
BitStream    = N -> N
Cursor       = N
ParserResult = N * (N * (N * N))
             = (status, a, b, nextOffset)
```

The four NEX-written operations are:

```text
decodeUAt
readHead
skipTerm
exactTerm
```

All infer:

```text
(N -> N) -> N -> (N * (N * (N * N)))
```

Frozen candidate size as separately serialized terms:

```text
decodeUAt    752 bits
readHead    2165 bits
skipTerm    3964 bits
exactTerm   4480 bits
-------------------
total      11361 bits
```

The 11,361-bit figure is an engineering size, not `B | A`, `C | A`, or a minimal self-hosting library.

### Development result

First official development run: workflow `35433974244`, job `105873398120`.

```text
development cases                         27
projected ParserResult fields            108
Python call-by-need resource refusals      0
Go call-by-need resource refusals          0
Go normative CBN resource refusals        16
Python/Go need values matched            108/108
largest Python need transitions          7,339  skip-nested:a
largest Go need transitions              3,171  skip-nested:a
```

All four `ParserResult` fields were forced and compared; observing only the outer `Pair` does not count as success.

The result was frozen together with candidate/contract/workload Git blob identities. A full historical checkpoint was then triggered. Workflow run `35434076839` completed successfully and reproduced 5.12a–f development evidence, independent Python, and Go/frozen Stage 4 evidence.

### Preregistered hold-out result

Only after that green checkpoint was the parser hold-out trigger changed. The unchanged candidate was executed once in workflow run `35434195939`, job `105873992224`.

Frozen identities verified immediately before execution:

```text
candidate  44b9d85f8bbe522d8b637c977c3fb39520c2c10f
hold-out   352e37b682230f196b3b4414932b7625dd24bfa7
```

Result:

```text
hold-out cases                            12
projected ParserResult fields             48
Python call-by-need resource refusals      0
Go call-by-need resource refusals          0
Go normative CBN resource refusals        18
Python/Go need values matched             48/48
largest Python need transitions          15,151  skip-let-complex:a
largest Go need transitions               6,392  skip-let-complex:a
```

Decision: `stream-parser-v0.1` is **accepted as the bounded canonical-wire traversal checkpoint on the frozen development and preregistered hold-out surfaces**.

This establishes that unchanged NEX-1 v0.1 can decode canonical `U(n)` fields, distinguish all six term constructors, recursively traverse complete canonical term structure, and detect premature EOF/trailing data using a functional `BitStream` and natural cursor.

It does **not** establish a materialized recursive `Term`, complete `decodeTerm`/`encodeTerm`, scope validation, primitive-ID validity, HM inference, evaluation, integrated self-hosting, self-processing, or receiver-neutral bootstrap.

Normative Go CBN refused 16 development projections and 18 hold-out projections under the frozen budget. Both sharing controls completed every acceptance observation. This is recorded as further evidence that sharing is an engineering feasibility condition, not as semantic invalidity or a Core defect.

Durable evidence:

```text
stage5/selfhost/stream-parser-v0.1.json
stage5/selfhost/stream-parser-development-result-v0.1.json
stage5/selfhost/stream-parser-holdout-result-v0.1.json
stage5/selfhost/verify_stream_parser_result.py
docs/experiments/stage5-selfhost-stream-parser.md
```

## CI structure after the protocol checkpoint

Fast accepted-checkpoint validation and expensive historical checks are separated.

```text
stage5-self-sufficiency.yml
  -> protocol/contracts/reproducibility
  -> validate frozen 5.12f result without rerunning hold-out

stage5-self-sufficiency-regression.yml
  -> cheap trigger job on ordinary commits
  -> heavy historical regression only when latest commit changes checkpoint-trigger.txt
  -> reproduce development evidence and validate frozen hold-out result

stage5-self-sufficiency-holdout.yml
  -> cheap trigger job on ordinary commits
  -> one-shot hold-out jobs only when the matching explicit trigger changes
```

The latest-commit trigger behavior has been verified. The parser hold-out is now represented by its frozen result and blob identities; ordinary regression does not re-execute the one-shot hold-out.

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

Stage 5.12f has closed the immediate question of whether a fixed-type functional stream can support bounded recursive traversal of actual canonical NEX term wire. The next step must not silently equate traversal with a complete decoder.

Before further implementation, the project must explicitly define how structural information produced by wire traversal will be represented and consumed by Stage 5.13 structural validation while preserving the existing anti-tuning discipline. In particular, the next contract must state whether validation will operate directly over `(BitStream, Cursor)`/parser results or whether a new versioned materialized representation is required.

Stage 6 remains Planned. Both living dissertation versions must include the accepted 5.12f checkpoint and its CBN/sharing qualification before PR #16 can leave draft.
