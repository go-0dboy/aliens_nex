# Stage 5.12 closeout — self wire codec completed before Stage 5.13

**Status:** Complete  
**Date:** 2026-09-19  
**Core:** NEX-1 v0.1 unchanged  
**Parent decision:** ADR-0018  
**Stage 6:** Planned  

## Sequencing rule

The project followed the strict order:

```text
5.11 Complete
  -> 5.12 Complete
     -> 5.13 may be planned next
```

No Stage 5.13 implementation was introduced while Stage 5.12 was incomplete. This closeout does not implement Stage 5.13; it only removes the predecessor block after the Stage 5.12 evidence gate is satisfied.

## Result

Stage 5.12 required NEX-written canonical wire support for:

```text
encodeU / decodeU
encodeTerm / decodeTerm
```

with the laws:

```text
decodeTerm(encodeTerm(term)) == term
encodeTerm(decodeTerm(bits)) == canonical(bits)
```

The integer prerequisites were established earlier in Stage 5.12c. The full `Term` codec is now accepted as `full-codec-v0.3` under the accepted Stage 5.11 operational representation:

```text
FiniteBits      = (N -> N) * N
FiniteNatTokens = (N -> N) * N
CodecResult     = N * ((N -> N) * N)
```

No NEX-1 v0.1 constructor, primitive, type former, wire rule, normative evaluation rule, mutable state, host callback, or native backend was added.

## Gate 0 — predecessor audit

**Complete.**

Stage 5.11 is Complete under `meta-representation-v0.3`.

Durable evidence:

```text
stage5/selfhost/meta-representation-v0.3.json
stage5/selfhost/validate_meta_representation_v0_3.py
docs/experiments/stage5-selfhost-5.11-completion-audit.md
docs/experiments/stage5-selfhost-meta-representation-v0.3.md
```

The accepted `Term` representation is the canonical finite natural-token prefix tree:

```text
Var(k)   -> [0,k]
Lam(t)   -> [1] ++ t
App(a,b) -> [2] ++ a ++ b
Let(v,b) -> [3] ++ v ++ b
Nat(n)   -> [4,n]
Prim(p)  -> [5,p]
```

## Gates 1–2 — full-codec contract and preregistration

**Complete.**

The project froze exact codec interfaces, status/error classes, round-trip laws, forbidden shortcuts, development surfaces, bounded exhaustive class, resource budgets, and separately preregistered hold-outs before executing each candidate version.

Frozen sharing budgets remained:

```text
Python call-by-need  5,000,000 transitions / depth 8,000
Go call-by-need      5,000,000 transitions / depth 20,000
Go normative CBN     5,000,000 transitions / depth 20,000
```

Anti-tuning rules were preserved:

- no budget increase after observing a candidate result;
- no failed-case deletion within the same version;
- algorithmic change after execution requires a new candidate version;
- a revealed hold-out is never reused as the next candidate's hold-out;
- failed candidates remain immutable negative evidence.

## Candidate lineage

### full-codec v0.1 — rejected on one-shot hold-out

v0.1 passed frozen development and the complete 27-Term class, then failed its one-shot preregistered hold-out:

```text
case                         law2:deepmixed:stream
Python need transitions     5,000,001
frozen transition limit     5,000,000
```

The candidate was rejected. The limit was not raised and the revealed hold-out was not used to retune v0.1.

### full-codec v0.2 — rejected on frozen development

v0.2 preregistered a local algorithmic improvement: binary selectors carried residual indices rather than pre-counting the left subtree on each query. Its first semantic development execution still failed the now-historical `deepmixed` case at the same frozen limit:

```text
case                         law2:deepmixed:stream
Python need transitions     5,000,001
frozen transition limit     5,000,000
```

This established that the dominant cost was not merely left-subtree pre-counting. The decoded token stream still behaved as a random-access view that reparsed original wire across distinct token queries.

v0.2 was rejected before its preregistered hold-out was opened.

### full-codec v0.3 — accepted

v0.3 was preregistered before implementation with a fresh unseen hold-out. It preserved the same public carriers, canonical wire, Core, and resource budgets.

Its algorithm constructs compositional functional fragments once during recursive traversal. Later indexed observations query these already-built fragments rather than reparsing the source for every token/bit index.

Frozen candidate identity:

```text
decodeTerm   6,198 bits
sha256       b20d12f94bb91efc4adcb73c55cfd9db5dfc3ecd625d9421be4d67e64fedb6d8

encodeTerm   6,124 bits
sha256       cea3472c4a819f41d7857b5cc3457cf92090f248fd101c3a40d0cfe951313ed4

total       12,322 bits as two separately serialized closed terms
```

Both infer:

```text
(((N -> N) * N) -> (N * ((N -> N) * N)))
```

## Gates 3–5 — decodeTerm, encodeTerm, and round-trip laws

**Complete on the frozen bounded surfaces.**

Official v0.3 semantic run:

```text
workflow  35440628434
job       105890683686
head      6947523cceb5e41c62d297f1f6934a3bf4c9de26
```

Development result:

```text
valid terms                          24
decode error cases                   12
encode error cases                   12
compound forced Nat observations    120
Python need refusals                   0
Go need refusals                       0
Go CBN refusals                       94
Python/Go need matches           120/120
largest Python need transitions  265,933  law2:deepmixed
largest Go need transitions      117,098  law2:deepmixed
```

Both required laws were checked extensionally, including stream contents and sentinel behavior. Function-valued results were not accepted merely because their outer observation was `Function`.

## Gate 6 — bounded exhaustive and differential strengthening

**Complete.**

The complete class frozen before aggregate execution is:

```text
AST nodes        1..3
leaf set         Var(0), Nat(0), Prim(0)
constructors     Var, Lam, App, Let, Nat, Prim where the bound permits
complete terms   27
```

Result:

```text
Direct Python canonical round trips          27/27
Direct Go canonical round trips/token checks 27/27
NEX forced law observations                 108/108
Python need refusals                              0
Go need refusals                                  0
Go CBN refusals                                  99
largest Python need transitions              32,764  law2:term-18
largest Go need transitions                  14,894  law2:term-18
```

The controls cover Direct Python, Direct Go, NEX-on-Python, and NEX-on-Go on the declared surface.

This is bounded empirical evidence, not a global proof of codec correctness.

## Pre-holdout historical checkpoint

**Complete.**

Before opening the v0.3 hold-out, workflow run `35441259575`, job `105892338355` completed green.

It reproduced or validated:

- Stage 5.12a arithmetic foundation;
- Stage 5.12b meta-sequence evidence;
- Stage 5.12c integer codec;
- Stage 5.12d negative result;
- Stage 5.12e negative/accepted stream evidence;
- Stage 5.12f parser evidence;
- immutable full-codec v0.1 and v0.2 negative results;
- frozen v0.3 identity, development, and exhaustive checks;
- independent Python implementation;
- Go reference and frozen Stage 4 evidence.

The frozen record is:

```text
stage5/selfhost/full-codec-preholdout-result-v0.3.json
```

## Gate 7 — one-shot preregistered hold-out

**Complete.**

The unchanged v0.3 candidate was executed once against its new preregistered unseen hold-out:

```text
workflow  35441600023
job       105893253759
head      f312910282e444b38953d869ee780f9c2488e965
```

The guard verified frozen identities before execution:

```text
candidate artifact     c5fb6836564262f7fafece2a06c06949a1cbe1dd
contract               e2205ee622c895eca1057960917fe0be22fca17c
development manifest   4c57a4d873d18b77f80a0efb62bb38865d86a17e
holdout workload       eed66f0150b1718b9cbad50548b9a14b97554da2
```

Hold-out result:

```text
valid terms                           7
decode error cases                    3
encode error cases                    3
compound forced Nat observations     34
Python need refusals                  0
Go need refusals                      0
Go CBN refusals                      30
Python/Go need matches            34/34
largest Python need transitions  487,579  law2:v3-deep3
largest Go need transitions      212,893  law2:v3-deep3
round-trip laws                     7/7 valid terms
```

Decision: accepted.

The 30 normative Go CBN resource refusals remain explicit operational-cost evidence. They were not converted into values or hidden by the sharing-control acceptance rule.

Durable evidence:

```text
stage5/selfhost/full-codec-holdout-result-v0.3.json
stage5/selfhost/verify_full_codec_result_v0_3.py
docs/experiments/stage5-selfhost-full-codec-v0.3.md
```

The accepted one-shot hold-out is represented by its frozen result and is not rerun as an ordinary regression test.

## CI optimization applied during closeout

The evidence surface was preserved while eliminating repeated expensive work:

- fast `stage5-self-sufficiency` validates active/frozen invariants rather than replaying historical runtime evidence;
- static and active full-codec workflows are explicit latest-commit trigger jobs, preventing cumulative PR path matching from rerunning heavy experiments on unrelated commits;
- v0.1/v0.2 full-codec failures are checked as immutable result artifacts rather than re-executed;
- historical regression runs only when `checkpoint-trigger.txt` changes;
- each hold-out runs only on its matching one-shot trigger;
- v0.3 development uses compound extensional assertions so status, length, every element, and sentinel are checked inside one NEX evaluation instead of several duplicated evaluations.

These changes reduce runner work without weakening expected semantics, deleting cases, changing budgets, or reclassifying failures.

## Gate 8 — completion review

The Stage 5.12 completion checklist is satisfied as follows:

- [x] Stage 5.11 formally Complete under accepted operational v0.3;
- [x] NEX integer wire codec prerequisites exist;
- [x] functional bit-stream representation checkpoint exists;
- [x] bounded NEX stream parser checkpoint exists;
- [x] exact operational Term representation frozen and validated;
- [x] exact full-codec interface/result contract frozen;
- [x] full-codec development and separate hold-out workloads preregistered;
- [x] NEX `decodeTerm` exists and passes frozen development evidence;
- [x] NEX `encodeTerm` exists and passes frozen development evidence;
- [x] both required round-trip/canonicalization laws pass on frozen surfaces;
- [x] Direct Go / Direct Python / NEX-on-Go / NEX-on-Python controls agree where required;
- [x] complete bounded 27-Term codec class passes;
- [x] unchanged v0.3 candidate passes the preregistered one-shot hold-out;
- [x] negative/resource outcomes are preserved rather than hidden;
- [x] NEX-1 v0.1 is unchanged;
- [x] `docs/STATUS.md` marks 5.12 Complete and 5.13 Planned;
- [x] both living dissertation versions incorporate the completed 5.12 result and limitations;
- [x] PR changed-file audit finds no normative Core-spec change and no Stage 5.13 implementation;
- [x] heavy CI was optimized without weakening the frozen evidence contract;
- [x] final Stage 5.12 historical regression is green on the closeout evidence head.

The final trigger-only historical regression completed successfully on the Stage 5.12 closeout evidence head:

```text
head      4977e87feb53a04c98f9f60feed9c4847524c788
workflow  35442303266
job       105895125195
result    success
```

It reproduced/validated Stage 5.12a–f, immutable v0.1/v0.2 negative evidence, frozen v0.3 identity/development/exhaustive evidence, the accepted one-shot holdout result without rerunning the holdout, independent Python, and Go/frozen Stage 4 evidence. Subsequent documentation-only reconciliation does not alter candidate code, contracts, workloads, result artifacts, or the evidence head recorded above.

## Stage boundary after closeout

After the successful final checkpoint:

```text
Stage 5.11  Complete
Stage 5.12  Complete
Stage 5.13  Planned; predecessor complete
Stage 6     Planned; still blocked by the 5.20 gate
```

Stage 5.12 does not establish structural scope/primitive validation, HM inference, evaluator correctness, integrated self-hosting, self-processing, or global metatheory. Those remain sequential later substages.
