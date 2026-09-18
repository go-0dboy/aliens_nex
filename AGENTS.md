# AI agent instructions

This repository is the source of truth. Do not rely on prior chat history when repository state is available.

Before making changes, read at least:

1. `README.md`
2. `docs/NEX-1-v0.1.md`
3. `docs/ARCHITECTURE.md`
4. `docs/DOMAIN.md`
5. `docs/WORKFLOW.md`
6. `docs/TESTING.md`
7. relevant files in `docs/adr/`
8. `docs/STATUS.md`

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
