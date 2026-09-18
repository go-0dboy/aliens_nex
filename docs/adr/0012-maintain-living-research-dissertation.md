# ADR-0012: Maintain a living research dissertation

**Status:** Accepted  
**Date:** 2026-09-18

## Context

NEX is no longer only a language-design sketch. Stages 0–4 produced a normative Core specification, wire encoding, static semantics, dynamic semantics, conformance artifacts, executable reference implementation, benchmark corpora, external baselines, and empirical results.

Those facts are currently distributed across specifications, ADRs, stage plans, status checkpoints, benchmark JSON, source registry entries, CI runs, and implementation code. That distribution is useful for engineering continuity but makes it difficult to see the research argument as one coherent body of work: problem statement, research questions, hypotheses, prior work, method, evidence, limitations, results, and conclusions.

A research project can also lose important negative or qualified findings if only implementation status is maintained. For example, Stage 4 found that Binary Lambda Calculus is smaller than NEX on the measured identical pure-lambda subset, that call-by-need dramatically reduces reference transition counts on some workloads without changing program bits, and that the total cost `C = S + B + P` cannot yet be numerically resolved because `B` is unknown. These findings must remain part of the durable scientific record rather than transient chat or PR commentary.

## Decision drivers

- preserve the full research argument, not only implementation state;
- keep conclusions traceable to reproducible artifacts and primary literature;
- retain negative, null, and qualified findings;
- make the project understandable to an external technical reader;
- prevent later sessions from silently rewriting hypotheses as established facts;
- keep English as the canonical research language while maintaining a Russian mirror;
- ensure new measurements and conclusions accumulate into the research record at the time they become defensible.

## Decision

The repository SHALL maintain a living dissertation-style research manuscript:

- canonical English: `docs/RESEARCH-DISSERTATION.md`;
- required Russian mirror: `docs/RESEARCH-DISSERTATION.ru.md`.

The manuscript is a research synthesis, not a substitute for the normative NEX specification, ADRs, benchmark artifacts, or tests.

The manuscript SHALL use a conventional scholarly structure appropriate to a technical dissertation-style work, including at least:

- abstract;
- research problem and motivation;
- object/subject, goal, research questions, and hypotheses;
- literature/theoretical background;
- methodology and evidence classification;
- staged development and experimental chapters;
- reproducible results and negative results;
- discussion and answers to research questions;
- threats to validity and limitations;
- contributions;
- future work;
- conclusion;
- glossary;
- bibliography;
- reproducibility/artifact appendix.

The manuscript SHALL cite primary or official sources where external theory or prior work materially supports a claim. Stable `SRC-xxxx` identifiers from `docs/SOURCES.md` SHOULD be shown alongside conventional bibliographic references where useful.

Direct quotation is not required for ordinary technical attribution. Verbatim quotations MAY be used only when their exact wording has been checked against the source; otherwise the manuscript SHALL paraphrase and cite the source rather than inventing quotation text.

### Living-research update rule

A change MUST update the dissertation in the same PR, or explicitly record why no dissertation change is needed, when it produces any of the following:

1. a new reproducible measurement that changes or materially refines a research conclusion;
2. a new accepted/rejected/deferred architectural decision with research significance;
3. a new external baseline or primary source materially used by the project;
4. a new conformance result from an independent implementation;
5. a new formal proof, counterexample, falsification, or limitation;
6. a stage completion that answers or materially changes a research question;
7. a revised estimate/model for `S`, `B`, `P`, or total `C`;
8. evidence that a previously stated hypothesis is unsupported, contradicted, or needs qualification.

Small implementation changes that do not alter research evidence, interpretation, or method do not require dissertation edits.

Every dissertation update MUST preserve the distinction among:

- external established result;
- NEX design decision;
- reproducible NEX measurement;
- inference from current evidence;
- open hypothesis / unknown.

The English manuscript is authoritative. Material research-semantic changes MUST update the Russian mirror in the same PR. If temporary desynchronization is unavoidable, it MUST be called out in the PR and `docs/STATUS.md`.

## Accepted consequences

- research conclusions become durable repository state rather than chat history;
- documentation work increases at meaningful evidence checkpoints;
- the manuscript may remain explicitly incomplete while the project is ongoing;
- the manuscript must preserve historical negative results instead of being rewritten only around the latest preferred design;
- institution-specific formatting, submission declarations, pagination, title-page rules, and jurisdiction-specific dissertation requirements remain out of scope until a target institution or standard is selected.

## Alternatives considered

### Keep only stage/status documents

Rejected. They are optimized for continuation and engineering checkpoints, not a coherent research argument or literature-grounded synthesis.

### Generate the dissertation only at the end

Rejected. Important rationale, negative results, and limitations would have to be reconstructed retrospectively and could be lost or distorted.

### Make Russian canonical

Rejected for repository consistency with ADR-0003. English remains canonical; Russian remains a maintained mirror for accessibility and review.

## Evidence / references

This decision is process-oriented and relies on the existing NEX research record rather than a new external theorem. External technical claims within the dissertation remain governed by ADR-0004 and `docs/SOURCES.md`.

## Follow-up validation

Future PR review should ask:

```text
Did this change create a defensible new research result, conclusion, limitation, or research-significant decision?
    |
    +-- no  -> dissertation update not required
    |
    +-- yes -> update English dissertation + Russian mirror in the same PR
```

The dissertation should be reviewed for internal consistency at every stage-completion gate.