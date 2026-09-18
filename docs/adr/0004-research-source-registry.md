# ADR-0004: Maintain a research source registry

- **Status:** Accepted
- **Date:** 2026-09-18

## Context

NEX is a research-oriented language project that relies on external theory, papers, standards, encoding techniques, and comparative systems. If those sources remain only in chat history or are cited ad hoc, later work can lose track of which external claims are actually established, which project decisions merely draw inspiration from them, and which comparisons still require verification.

The project therefore needs a durable, reviewable registry of external sources tied to concrete NEX usage.

## Decision drivers

- Research claims must be traceable to primary or official material where practical.
- New sessions must be able to recover the project's theoretical basis from the repository alone.
- Project-specific inference must not be confused with what an external source actually proves.
- Living standards need explicit recheck dates.
- Benchmark baselines must identify exact external implementations/specifications when measurements begin.

## Decision

The project will maintain `docs/SOURCES.md` as the canonical external research source registry.

Each materially used source receives a stable `SRC-xxxx` ID.

A pull request MUST add or update an entry in `docs/SOURCES.md` when it materially relies on a new external:

- theorem or theoretical result;
- algorithm;
- encoding;
- programming-language model;
- standard or specification;
- external implementation used as a benchmark baseline;
- empirical result that influences a project decision.

The entry must state:

1. bibliographic identity and stable link/DOI when available;
2. source class (primary paper, official standard, author-maintained reference, secondary background, etc.);
3. what NEX uses from that source;
4. the current project impact;
5. important limits on what the source does **not** establish for NEX.

Primary research papers, official standards, and author-maintained technical sources are preferred. Secondary material is acceptable for orientation but should not remain the sole support for an important technical claim when a primary source can reasonably be located.

## Consequences

### Positive

- The theoretical basis of NEX becomes auditable.
- ADR reasoning can refer to stable source IDs instead of rediscovering references.
- The project can distinguish external fact from NEX-specific inference and hypothesis.
- Future comparative benchmarks can record exact baselines rather than vague product names.

### Cost

- Research-affecting PRs require modest source-maintenance work.
- Living specifications require periodic review when relevant decisions depend on current text.

The cost is accepted because research traceability is part of correctness for this project.

## Alternatives considered

### Keep references only at the end of the language specification

Rejected. Sources also influence ADRs, benchmarks, testing methodology, and future system profiles; a specification bibliography is too narrow.

### Rely on links in PRs/issues/chat

Rejected. Those are discussion surfaces, not a durable project-wide research index.

### Maintain a plain bibliography without usage notes

Rejected. A citation alone does not distinguish what the source establishes from what NEX infers or changes.

### Duplicate source metadata in every ADR

Rejected. ADRs should cite the relevant `SRC-xxxx` IDs and explain the decision; canonical bibliographic metadata belongs in one registry.

## Follow-up validation

The policy is working if a future contributor can answer from the repository alone:

1. which external works NEX currently depends on;
2. what claim or design idea each source supports;
3. whether a source is primary, official, or secondary;
4. what project conclusions remain hypotheses rather than established external results;
5. which exact external baselines must be used when comparisons are reproduced.
