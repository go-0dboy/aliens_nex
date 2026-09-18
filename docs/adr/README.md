# Architecture Decision Records

NEX uses Architecture Decision Records (ADRs) to preserve not only final decisions, but also reasoning, alternatives, rejected/deferred options, later corrections, and consequences.

## Why ADRs exist here

NEX is a research-oriented language project. Choices such as SKI, Binary Lambda Calculus, Hindley-Milner, System F, PCF, recursive types, explicit memory, DAG transport, bootstrap machines, receiver priors, and teaching protocols can look attractive in isolation. ADRs prevent repeated debates and silent architectural drift.

An ADR is required for decisions that materially change or reinterpret one or more of:

- Core semantics;
- type system;
- wire format;
- evaluation strategy;
- primitive set;
- execution/profile boundary;
- compatibility rules;
- bootstrap/teaching/accounting architecture;
- repository-wide development/research process;
- a material research claim when later evidence narrows or corrects it.

## Current ADRs

- [ADR-0001: Adopt Architecture Decision Records](0001-adopt-architecture-decision-records.md)
- [ADR-0002: NEX-1 Core v0.1 design basis](0002-nex-core-v0.1-design-basis.md)
- [ADR-0003: English canonical documentation with Russian mirrors](0003-documentation-language-policy.md)
- [ADR-0004: Maintain a research source registry](0004-research-source-registry.md)
- [ADR-0005: Use Go for the first reference implementation](0005-go-reference-implementation.md)
- [ADR-0006: Keep decoder resource limits separate from wire validity](0006-decoder-resource-limits.md)
- [ADR-0007: Keep ordinary type annotations out of the NEX-1 v0.1 canonical wire format](0007-erased-type-annotations-v0.1.md)
- [ADR-0008: Use an environment-based weak call-by-name reference evaluator](0008-environment-based-call-by-name-reference-evaluator.md)
- [ADR-0009: Keep evaluator resource limits separate from NEX semantics and validity](0009-separate-evaluation-resource-limits-from-semantics.md)
- [ADR-0010: Freeze the measurement contract and benchmark corpus before optimization](0010-freeze-measurement-contract-before-optimization.md)
- [ADR-0011: Hold NEX-1 v0.1 stable after the Stage 4 evidence gate](0011-stage4-evidence-gate.md)
- [ADR-0012: Maintain a living research dissertation](0012-maintain-living-research-dissertation.md)
- [ADR-0013: Freeze the Stage 5 independence protocol and use Python for the first independent implementation](0013-stage5-independence-protocol.md)
- [ADR-0014: Condition bootstrap cost on explicit receiver assumptions](0014-condition-bootstrap-cost-on-receiver-assumptions.md)
- [ADR-0015: Close Stage 5 with a negative complete-bootstrap result](0015-stage5-decision-gate.md)
- [ADR-0016: Correct research claims after the post-Stage-5 literature re-audit](0016-post-stage5-literature-reaudit-corrections.md)
- [ADR-0017: Separate the NEX teaching/bootstrap protocol from the stable NEX-1 Core](0017-separate-teaching-protocol-from-core.md)

## Status values

Each ADR MUST use one of:

- `Proposed` — under active consideration;
- `Accepted` — current project decision;
- `Rejected` — considered and explicitly declined;
- `Deferred` — intentionally postponed pending evidence;
- `Superseded` — replaced by a later ADR.

A superseded ADR remains in the repository and links to its replacement. A factual clarification may also be recorded by a later ADR while the original architectural choice remains Accepted.

## Required structure

An ADR SHOULD contain:

1. Title
2. Status
3. Date
4. Context / problem
5. Decision drivers
6. Decision
7. Accepted consequences
8. Alternatives considered
9. Why alternatives were rejected or deferred
10. Evidence / references
11. Follow-up validation

## Numbering

ADRs use monotonically increasing four-digit numbers and IDs are never reused.

## Rule for research claims

An ADR MUST distinguish among:

- established external fact;
- project design decision;
- project inference;
- hypothesis;
- experimentally verified result;
- unresolved unknown.

A hypothesis MUST NOT become a fact merely through repetition. When later literature or experiments narrow an Accepted rationale, the correction must be explicit and historically traceable.

External research used materially by an ADR belongs in `docs/SOURCES.md` under a stable source ID.

## Review rule

A change that contradicts an Accepted ADR MUST either:

- add a new ADR that supersedes or corrects the relevant part; or
- update the older ADR only to add a clearly dated clarification pointing to the later decision, unless the older file is part of a frozen experiment packet whose byte identity must be preserved.

Frozen experimental source snapshots MUST NOT be rewritten merely to improve current wording. A later ADR records the correction instead.

Silent architectural or research-claim drift is not allowed.
