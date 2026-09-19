# Stage 5.12 full codec v0.3 — completion evidence

Date: 2026-09-19

## Decision

`full-codec-v0.3` is accepted as the Stage 5.12 NEX-written full Term wire codec on the frozen bounded surfaces.

This closes the Stage 5.12 codec requirement after final historical regression and documentation/diff review. It does not establish Stage 5.13 structural validation, HM inference, evaluation, integrated self-hosting, or receiver-neutral bootstrap.

NEX-1 v0.1 is unchanged.

## Interface

```text
FiniteBits      = (N -> N) * N
FiniteNatTokens = (N -> N) * N
CodecResult     = N * ((N -> N) * N)

decodeTerm : FiniteBits -> CodecResult
encodeTerm : FiniteNatTokens -> CodecResult
```

Term tokens remain the accepted Stage 5.11 v0.3 representation:

```text
Var(k)   -> [0,k]
Lam(t)   -> [1] ++ t
App(a,b) -> [2] ++ a ++ b
Let(v,b) -> [3] ++ v ++ b
Nat(n)   -> [4,n]
Prim(p)  -> [5,p]
```

## Candidate lineage

### v0.1

Passed development and the complete frozen 27-Term class, then was rejected on its one-shot preregistered holdout:

```text
case       law2:deepmixed:stream
Python need transitions  5,000,001
frozen limit             5,000,000
```

No limit was raised and the failed candidate was not tuned against the revealed holdout.

### v0.2

Preregistered successor replaced per-query left-subtree size pre-counts with residual-index traversal. Its first development execution was rejected on the same historical `deepmixed` case at the same frozen transition limit:

```text
case       law2:deepmixed:stream
Python need transitions  5,000,001
frozen limit             5,000,000
```

The failure showed that the dominant cost was higher-level: `decodeTerm` still exposed a random-access token view that reparsed the original wire across distinct token queries.

### v0.3

Before implementation, the project preregistered a new successor and a fresh unseen holdout. The public carrier and Core remained unchanged. The algorithm builds compositional functional fragments once during recursive traversal, so later indexed observations query already-constructed fragments rather than reparsing the source wire for every token/bit index.

Candidate identity:

```text
decodeTerm  6,198 bits
sha256      b20d12f94bb91efc4adcb73c55cfd9db5dfc3ecd625d9421be4d67e64fedb6d8

encodeTerm  6,124 bits
sha256      cea3472c4a819f41d7857b5cc3457cf92090f248fd101c3a40d0cfe951313ed4

total      12,322 bits as two separately serialized closed terms
```

Both infer:

```text
(((N -> N) * N) -> (N * ((N -> N) * N)))
```

## Development

Official semantic run:

```text
workflow  35440628434
job       105890683686
head      6947523cceb5e41c62d297f1f6934a3bf4c9de26
```

Results:

```text
valid terms                         24
decode error cases                  12
encode error cases                  12
compound forced Nat observations   120
Python need refusals                  0
Go need refusals                      0
Go CBN refusals                      94
Python/Go need matches          120/120
largest Python need transitions 265,933  law2:deepmixed
largest Go need transitions     117,098  law2:deepmixed
```

The previously failing `deepmixed` law is therefore below the unchanged 5,000,000-transition sharing budget by a wide margin.

## Bounded exhaustive class

The same frozen complete class used by earlier candidates was retained:

```text
AST nodes        1..3
leaf set         Var(0), Nat(0), Prim(0)
complete terms   27
```

Results:

```text
Direct Python canonical round trips          27/27
Direct Go round trips/token projections      27/27
NEX forced law observations                 108/108
Python need refusals                              0
Go need refusals                                  0
Go CBN refusals                                  99
largest Python need transitions              32,764  law2:term-18
largest Go need transitions                  14,894  law2:term-18
```

## Pre-holdout historical checkpoint

Before opening the new holdout, workflow run `35441259575`, job `105892338355` completed green.

It reproduced or validated:

- Stage 5.12a arithmetic foundation;
- Stage 5.12b meta-sequence evidence;
- Stage 5.12c integer codec;
- Stage 5.12d rejection;
- Stage 5.12e negative and accepted stream evidence;
- Stage 5.12f parser evidence;
- immutable full-codec v0.1 and v0.2 negative results;
- frozen v0.3 identity, development and exhaustive checks;
- independent Python implementation;
- Go reference and frozen Stage 4 evidence.

The frozen pre-holdout record is `stage5/selfhost/full-codec-preholdout-result-v0.3.json`.

## One-shot preregistered holdout

The v0.3 holdout was registered before candidate implementation and remained unexecuted until all preconditions passed.

One-shot run:

```text
workflow  35441600023
job       105893253759
head      f312910282e444b38953d869ee780f9c2488e965
```

Frozen identities observed by the holdout guard:

```text
candidate artifact     c5fb6836564262f7fafece2a06c06949a1cbe1dd
contract               e2205ee622c895eca1057960917fe0be22fca17c
development manifest   4c57a4d873d18b77f80a0efb62bb38865d86a17e
holdout workload       eed66f0150b1718b9cbad50548b9a14b97554da2
```

Results:

```text
valid terms                          7
decode error cases                   3
encode error cases                   3
compound forced Nat observations   34
Python need refusals                 0
Go need refusals                     0
Go CBN refusals                     30
Python/Go need matches           34/34
largest Python need transitions 487,579  law2:v3-deep3
largest Go need transitions     212,893  law2:v3-deep3
round-trip laws                    7/7 valid terms
```

Decision: accepted.

The 30 normative Go CBN resource refusals remain explicit operational-cost evidence. They are not converted into successful values and are not hidden by the sharing-control acceptance rule.

## Anti-tuning properties preserved

- no Core change;
- no wire change;
- no representation carrier change after Stage 5.11 v0.3 freeze;
- no resource-budget increase;
- no failed-case deletion;
- v0.1 holdout was not reused as the v0.2/v0.3 holdout;
- v0.2 rejection occurred before its holdout was opened;
- v0.3 holdout was new and registered before v0.3 candidate code;
- candidate wire did not change after first semantic execution;
- the successful holdout is now verified as immutable evidence and must not be rerun as an acceptance experiment.

## Stage boundary

## Final closeout regression

After the one-shot holdout was frozen as immutable evidence and documentation/diff review was completed, the final trigger-only historical regression succeeded:

```text
head      4977e87feb53a04c98f9f60feed9c4847524c788
workflow  35442303266
job       105895125195
result    success
```

The run reproduced/validated historical Stage 5.12a–f, immutable full-codec v0.1/v0.2 negative evidence, frozen v0.3 identity/development/exhaustive evidence, the accepted holdout result without rerunning the one-shot holdout, independent Python, and Go/frozen Stage 4 evidence.


The accepted evidence establishes the Stage 5.12 target:

- NEX-written `decodeTerm` converts canonical NEX wire into the accepted internal Term token representation;
- NEX-written `encodeTerm` reconstructs canonical NEX wire from that representation;
- both round-trip laws hold on development, bounded-exhaustive, and preregistered holdout surfaces;
- Direct Python, Direct Go, NEX-on-Python, and NEX-on-Go controls agree where required;
- malformed wire/meta cases preserve distinct status classes on the frozen surfaces;
- negative resource results from earlier candidates remain preserved.

Stage 5.13 remains a separate next stage. Stage 5.12 codec acceptance does not itself prove scope validation, primitive-ID validation, HM inference, evaluator correctness, full self-processing, or metatheory.
