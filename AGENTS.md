# AI agent instructions

This repository is the source of truth. Do not rely on prior chat history when repository state is available.

Before making changes, read at least:

1. `README.md`
2. `docs/NEX-1-v0.1.md`
3. `docs/ARCHITECTURE.md`
4. `docs/DOMAIN.md`
5. `docs/WORKFLOW.md`
6. `docs/TESTING.md`
7. `docs/SOURCES.md`
8. `docs/RESEARCH-DISSERTATION.md`
9. relevant files in `docs/adr/`
10. `docs/STATUS.md`

## Required working behavior

- Inspect the current branch and HEAD before editing.
- Preserve accepted ADR decisions unless the task explicitly introduces a superseding ADR.
- Work from problem and invariant to test/vector, implementation, verification, and diff review.
- Keep changes small and single-purpose.
- Do not mix unrelated refactors into functional work.
- Do not claim behavior is correct without executable evidence where such evidence is possible.
- Do not invent benchmark values, test results, or implementation status.
- Distinguish `verified`, `inferred`, `hypothesis`, and `not yet tested`.
- Prefer one canonical representation over convenience duplicates.
- Update `docs/STATUS.md` after a meaningful project stage.

## Research source policy

Per ADR-0004, `docs/SOURCES.md` is the canonical registry of external research sources used by the project.

When work materially relies on a new external theorem, algorithm, encoding, standard, language model, implementation baseline, or empirical result, the same change MUST add or update the corresponding source entry in `docs/SOURCES.md`.

AI agents MUST:

- prefer primary papers, official standards, and author-maintained technical material where practical;
- verify bibliographic identity and stable links/DOIs before registering a source;
- record what NEX actually uses from the source;
- distinguish the source's established result from NEX-specific inference or hypothesis;
- record exact versions/commit identifiers when an external implementation becomes a benchmark baseline;
- recheck mutable/living specifications when current content materially affects a decision.

Do not add a link merely because it was read during research. The registry is for sources that materially influence project work.

## Living research dissertation policy

Per ADR-0012, `docs/RESEARCH-DISSERTATION.md` is the canonical scholarly synthesis of the project and `docs/RESEARCH-DISSERTATION.ru.md` is its required Russian mirror.

The dissertation is not a substitute for the normative specification, ADRs, conformance artifacts, benchmark JSON, or tests. It synthesizes them into the durable research argument.

A change MUST update the dissertation in the same pull request, or explicitly state why no dissertation update is needed, when it produces a defensible new:

- reproducible measurement that changes or materially refines a conclusion;
- research-significant accepted/rejected/deferred architecture decision;
- external baseline or primary source materially used by the project;
- independent conformance result;
- formal proof, counterexample, falsification, or limitation;
- stage-completion conclusion;
- estimate/model for `S`, `B`, `P`, or total `C`;
- contradiction or qualification of an earlier hypothesis.

Dissertation text MUST preserve the distinction among external established result, NEX design decision, reproducible NEX measurement, inference from evidence, and open hypothesis/unknown.

Do not invent verbatim quotations. Direct quotation may be used only after checking the exact source wording; otherwise paraphrase and cite the primary source.

## Documentation language policy

English is the canonical documentation language.

Per ADR-0003 and ADR-0012, semantic changes to any of these primary documents should update the Russian mirror in the same pull request:

- `README.md` <-> `README.ru.md`;
- `docs/NEX-1-vX.Y.md` <-> `docs/NEX-1-vX.Y.ru.md`;
- `docs/ARCHITECTURE.md` <-> `docs/ARCHITECTURE.ru.md`;
- `docs/RESEARCH-DISSERTATION.md` <-> `docs/RESEARCH-DISSERTATION.ru.md`.

If a mirror cannot be updated immediately, explicitly mark it out of date in the pull request and in `docs/STATUS.md`.

Russian translations are informative; the English document is authoritative when wording differs.

## NEX-specific constraints

- NEX-1 Core v0.1 is normative in `docs/NEX-1-v0.1.md`.
- Architectural rationale is normative through Accepted ADRs.
- Human-friendly syntax is not the wire language.
- Bound variable names are not part of canonical terms.
- Machine/environment behavior must not leak into Core without an explicit architectural decision.
- Claims of compactness or optimality require measurements against stated baselines.

## Completion report

Use this structure when handing work back:

```text
Changed:
Verified:
Not verified:
Next:
```

Detailed architectural reasoning belongs in an ADR rather than being lost in a transient completion message.
