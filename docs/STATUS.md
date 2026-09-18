# Project status

**Date:** 2026-09-18  
**Baseline branch:** `main`  
**Current stage:** `Stage 4 — Empirical validation and benchmarking — In progress`  
**Stage 0 completed by:** PR `#1 docs: establish ADRs and project workflow`  
**Research source registry completed by:** PR `#2 docs: add research source registry`  
**Stage 1 completed by:** PR `#3 stage1: implement NEX wire foundation`  
**Stage 1 merge commit:** `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`  
**Stage 2 completed by:** PR `#4 stage2: complete static validation and principal type inference`  
**Stage 2 merge commit:** `cefe889d90a275897de31aa23c4b9742a388ec8f`  
**Stage 3 completed by:** PR `#5 stage3: complete dynamic semantics and reference evaluator`  
**Stage 3 merge commit:** `166cdc03282ea500263fdca7185f006f9b17a702`  
**Active Stage 4 branch:** `stage4/empirical-validation`

## Stages 0–3 — Complete

Stage 0 established the specification/process baseline. Stage 1 implemented canonical wire encode/decode. Stage 2 implemented closed-scope/static validation and principal HM type inference. Stage 3 implemented the complete weak-call-by-name v0.1 Core evaluator, synchronized EN/RU dynamic semantics, language-neutral evaluation conformance, resource separation, fuzz/property verification, and clean-checkout CI.

Detailed completion records remain in `docs/STAGE-1.md`, `docs/STAGE-2.md`, and `docs/STAGE-3.md`.

## Stage 4 — Empirical validation and benchmarking — In progress

Stage 4 is defined in `docs/STAGE-4.md`.

Accepted work order:

```text
4.0 measurement contract
4.1 frozen canonical benchmark corpus
4.2 NEX metrics/instrumentation
4.3 internal NEX design experiments
4.4 erased-HM versus explicit/hybrid type-information experiment
4.5 external baselines
4.6 call-by-name versus call-by-need experiment
4.7 bootstrap accounting model
4.8 reproducible experimental report
4.9 evidence-based decision gate
```

ADR-0010 requires the measurement contract and corpus to be fixed before optimization comparisons. Portable exact metrics, reference-only runtime metrics, and bootstrap/specification proxies must remain separately labelled.

The current Stage 4 objective is to make NEX's compactness claims measurable and falsifiable without changing NEX-1 v0.1 semantics or wire format.

## Remaining project-wide unverified claims

Still intentionally unverified:

- formal/exhaustive proof of decoder, type-inference, or evaluator correctness;
- conformance agreement with a second independent implementation;
- bootstrap/self-hosting feasibility and size;
- total-information-cost comparison against BLC, SKI/Jot, a typed stack machine, or an explicit-type NEX variant;
- practical cost of call-by-name versus call-by-need for representative NEX programs;
- any claim that NEX is globally optimal or the smallest possible language.

## Next recommended step

Implement Stage 4.1–4.2 without altering v0.1 semantics: freeze the first benchmark corpus, build deterministic exact NEX metrics from canonical terms, add explicitly labelled reference-evaluator counters, and make CI reproduce the report/checks from a clean checkout.
