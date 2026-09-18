# Architecture Decision Records

NEX uses Architecture Decision Records (ADRs) to preserve not only the final decision, but also the reasoning, alternatives, rejected options, deferred options, and consequences.

## Why ADRs exist here

NEX is a research-oriented language project. Many choices can look attractive in isolation: SKI, Binary Lambda Calculus, Hindley-Milner, System F, PCF, recursive types, linear types, stack bytecode, explicit memory, DAG transport, and others. Repeating the same debate in each new session wastes time and makes the design unstable.

An ADR is therefore required for any decision that materially changes one or more of:

- Core semantics;
- type system;
- wire format;
- evaluation strategy;
- primitive set;
- execution/profile boundary;
- compatibility rules;
- bootstrap architecture;
- repository-wide development process.

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

## Status values

Each ADR MUST use one of these statuses:

- `Proposed` — under active consideration;
- `Accepted` — current project decision;
- `Rejected` — considered and explicitly declined;
- `Deferred` — intentionally postponed pending evidence;
- `Superseded` — replaced by a later ADR.

A superseded ADR MUST remain in the repository and link to the ADR that replaces it.

## Required structure

Each ADR SHOULD contain:

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

ADRs use monotonically increasing four-digit numbers:

```text
0001-title.md
0002-title.md
...
```

Numbers are never reused.

## Rule for research claims

An ADR MUST distinguish among:

- established external fact;
- project inference;
- hypothesis;
- experimentally verified result.

A hypothesis MUST NOT be rewritten later as a fact merely because it has been repeated in project documentation.

External research used materially by an ADR should be registered in `docs/SOURCES.md` and referenced by its stable source ID where useful.

## Review rule

A change that contradicts an Accepted ADR MUST either:

- update that ADR only if the original decision itself has not materially changed, or
- add a new ADR that supersedes it.

Silent architectural drift is not allowed.
