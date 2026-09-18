# ADR-0001: Adopt Architecture Decision Records

- **Status:** Accepted
- **Date:** 2026-09-18

## Context

NEX is being designed through a sequence of research and engineering decisions. The project must preserve why a decision was made, not only the final state of the specification. Without this history, later work risks repeating earlier debates, reintroducing rejected ideas, or changing architecture without understanding the consequences.

This risk is amplified when development continues across separate AI-assisted sessions: chat history is not a reliable project memory or source of truth.

## Decision drivers

- Architectural reasoning must survive individual chats and contributors.
- Accepted, rejected, and deferred alternatives must remain visible.
- New work must be able to recover project context from the repository alone.
- Claims must distinguish external fact, inference, hypothesis, and measured evidence.
- Major decisions must be reviewable as repository changes.

## Decision

The project will use ADRs stored in `docs/adr/`.

An ADR is required for decisions that materially affect Core semantics, type system, wire representation, evaluation, primitive set, profile boundaries, compatibility, bootstrap architecture, or repository-wide development rules.

Accepted ADRs are append-only historical records. If a decision materially changes, a later ADR supersedes the earlier one; the earlier record is not deleted.

## Consequences

### Positive

- Project reasoning becomes recoverable without relying on chat history.
- Rejected and deferred alternatives remain explicit.
- Architectural changes become intentional and reviewable.
- Future experiments can point back to the hypothesis or decision they validate.

### Cost

- Architectural changes require a small amount of documentation work.
- Some decisions will remain marked `Deferred` until measurements exist.

The cost is accepted because design stability and traceability are primary requirements for this research project.

## Alternatives considered

### Keep reasoning only in issues, pull requests, or chat

Rejected. These surfaces are useful discussion records but are too fragmented to serve as the durable architectural index.

### Keep only the latest architecture document

Rejected. A living architecture document explains the current system but normally loses the historical reason why competing approaches were declined.

### Encode every small implementation choice as an ADR

Rejected. ADRs are for durable architectural or process decisions. Local implementation details belong in code, tests, commits, and pull requests.

## Follow-up validation

The ADR process is successful if a new contributor or AI session can determine, using only the repository:

1. what the current architecture is;
2. why major alternatives were rejected or deferred;
3. which questions are still open;
4. what evidence would justify changing a decision.
