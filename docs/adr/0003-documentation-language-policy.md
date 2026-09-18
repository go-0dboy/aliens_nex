# ADR-0003: English canonical documentation with Russian mirrors

- **Status:** Accepted
- **Date:** 2026-09-18

## Context

NEX is intended to be understandable and usable beyond one language community, so the canonical project documentation should remain in English. At the same time, the project is being designed and reviewed with a Russian-speaking primary maintainer, and the language design, goals, and architecture should be fully accessible in Russian without relying on external translation.

Maintaining every internal/process document in two languages would create unnecessary synchronization cost and increase the risk of contradictory project rules.

## Decision drivers

- English should remain the canonical project language for external interoperability and future contributors.
- The project goal and NEX language specification must be fully accessible in Russian.
- Architectural overview should also be available in Russian.
- Translation drift must be detectable and explicitly handled.
- Internal process documentation should not be duplicated unless the value justifies the maintenance cost.

## Decision

English remains the authoritative/canonical language of NEX documentation.

The following primary documents MUST have maintained Russian mirrors:

- `README.md` -> `README.ru.md`;
- `docs/NEX-1-vX.Y.md` -> `docs/NEX-1-vX.Y.ru.md`;
- `docs/ARCHITECTURE.md` -> `docs/ARCHITECTURE.ru.md`.

The Russian specification is an informative translation. If wording differs or becomes ambiguous, the English specification controls until both documents are synchronized.

A change that modifies the meaning of a mirrored primary document SHOULD update the corresponding Russian mirror in the same pull request. If this is temporarily impossible, the pull request and `docs/STATUS.md` MUST explicitly mark the translation as out of date.

ADRs, workflow instructions, test strategy, status checkpoints, source code, identifiers, commit messages, and other internal engineering documents remain English-only by default. They MAY receive translations later when there is a concrete need.

## Consequences

### Positive

- Project goals, language semantics, and architecture are accessible in both English and Russian.
- English remains a single normative reference for resolving ambiguity.
- Translation maintenance is concentrated on the documents most valuable to readers.

### Cost

- Every semantic change to the specification or architecture requires translation maintenance.
- Review must consider whether both language versions still describe the same design.

## Alternatives considered

### Russian-only documentation

Rejected. It would create an unnecessary barrier for external contributors and research comparison.

### Duplicate every project document in Russian

Rejected for now. The synchronization cost would be high, especially for volatile workflow/status documents, with limited benefit.

### English-only documentation

Rejected. It does not meet the project's accessibility requirement for the primary maintainer and Russian-speaking readers.

### Treat English and Russian as equally normative

Rejected. Two independently normative natural-language specifications create ambiguity when translations diverge. One canonical source is required.

## Follow-up validation

Primary-document pull requests should be reviewed for translation parity. Once automated documentation checks exist, the repository may add a simple check ensuring required mirror files are present and linked, but semantic translation equivalence remains a review responsibility.
