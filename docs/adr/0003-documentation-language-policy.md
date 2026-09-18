# ADR-0003: English canonical documentation with Russian mirrors

- **Status:** Accepted
- **Date:** 2026-09-18

## Context

NEX is intended to be understandable and usable beyond one language community, so the canonical project documentation should remain in English. At the same time, the project is being designed and reviewed with a Russian-speaking primary maintainer, and the language design, goals, and architecture should be fully accessible in Russian without relying on external translation.

Maintaining every internal/process document in two languages would create unnecessary synchronization cost and increase the risk of contradictory project rules.

A Russian mirror is useful only if it reads as technical Russian rather than as a word-for-word English calque. Literal sentence alignment is not a project goal. Semantic parity, terminological precision, and readability are more important than preserving English syntax or vocabulary.

## Decision drivers

- English should remain the canonical project language for external interoperability and future contributors.
- The project goal and NEX language specification must be fully accessible in Russian.
- Architectural overview should also be available in Russian.
- Translation drift must be detectable and explicitly handled.
- Russian mirrors should read naturally to a technically competent Russian-speaking reader.
- Internal process documentation should not be duplicated unless the value justifies the maintenance cost.

## Decision

English remains the authoritative/canonical language of NEX documentation.

The following primary documents MUST have maintained Russian mirrors:

- `README.md` -> `README.ru.md`;
- `docs/NEX-1-vX.Y.md` -> `docs/NEX-1-vX.Y.ru.md`;
- `docs/ARCHITECTURE.md` -> `docs/ARCHITECTURE.ru.md`.

The living research dissertation required by ADR-0012 also has a maintained Russian mirror:

- `docs/RESEARCH-DISSERTATION.md` -> `docs/RESEARCH-DISSERTATION.ru.md`.

The Russian specification is an informative translation. If wording differs or becomes ambiguous, the English specification controls until both documents are synchronized.

### Russian-mirror style rule

Russian mirrors MUST preserve meaning, identifiers, formulae, source references, measured values, and normative distinctions, but SHOULD NOT mechanically preserve English wording or sentence structure.

Use Russian technical prose by default. In particular:

- translate ordinary explanatory vocabulary when an established Russian equivalent exists;
- keep source-code identifiers, file paths, command names, formal grammar symbols, profile IDs such as `A0`, and names of external systems unchanged;
- at first use of an established English technical term that is useful for literature search, give a Russian term followed by the English form in parentheses when helpful, then prefer the Russian term or accepted abbreviation;
- avoid sentence-level code switching such as mixing Russian grammar with ordinary English nouns (`artifact`, `claim`, `receiver`, `exact`, `frozen`, `baseline`, `workflow`) when the English word is not an identifier or necessary term of art;
- do not translate proper names of languages, calculi, algorithms, standards, or cited works merely for stylistic uniformity;
- use the glossary to fix a stable Russian rendering for recurrent research terms.

The Russian mirror MAY be shorter or structurally smoother than the English canonical text if no research claim, limitation, measurement, source attribution, or normative distinction is lost. Semantic correspondence is required; literal paragraph-by-paragraph translation is not.

A change that modifies the meaning of a mirrored primary document SHOULD update the corresponding Russian mirror in the same pull request. If this is temporarily impossible, the pull request and `docs/STATUS.md` MUST explicitly mark the translation as out of date.

ADRs, workflow instructions, test strategy, status checkpoints, source code, identifiers, commit messages, and other internal engineering documents remain English-only by default. They MAY receive translations later when there is a concrete need.

## Consequences

### Positive

- Project goals, language semantics, and architecture are accessible in both English and Russian.
- English remains a single normative reference for resolving ambiguity.
- Russian readers receive an idiomatic technical text rather than a transliterated English draft.
- Translation maintenance is concentrated on the documents most valuable to readers.

### Cost

- Every semantic change to the specification or architecture requires translation maintenance.
- Review must consider both semantic parity and language quality.
- A good mirror may require editorial rewriting rather than mechanical translation.

## Alternatives considered

### Russian-only documentation

Rejected. It would create an unnecessary barrier for external contributors and research comparison.

### Duplicate every project document in Russian

Rejected for now. The synchronization cost would be high, especially for volatile workflow/status documents, with limited benefit.

### English-only documentation

Rejected. It does not meet the project's accessibility requirement for the primary maintainer and Russian-speaking readers.

### Treat English and Russian as equally normative

Rejected. Two independently normative natural-language specifications create ambiguity when translations diverge. One canonical source is required.

### Require literal paragraph-by-paragraph translation

Rejected. It encourages unnatural Russian syntax and unnecessary English vocabulary while providing little additional semantic safety. Semantic parity is reviewed directly instead.

## Follow-up validation

Primary-document pull requests should be reviewed for translation parity. Russian mirrors should also be reviewed for avoidable code switching and repeated calques from English. Once automated documentation checks exist, the repository may add simple checks ensuring required mirror files are present and linked, but semantic translation equivalence and language quality remain review responsibilities.
