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

## Status values

Each ADR MUST use one of these statuses:

- `Proposed` — under active consideration;
- `Accepted` — current project decision;
- `Rejected` — considered and explicitly declined;
- `Deferred` — intentionally postponed pending evidence;
- `Superseded` — replaced by a later ADR.

A superseded ADR MUST remain in the repository and link to the ADR that replaces it.

## Required structure

Every ADR SHOULD contain:

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

## Review rule

A change that contradicts an Accepted ADR MUST either:

- update that ADR only if the original decision itself has not materially changed, or
- add a new ADR that supersedes it.

Silent architectural drift is not allowed.
