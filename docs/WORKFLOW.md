# Development workflow

This project treats the repository as the shared memory between humans and AI-assisted development sessions.

Chat history is not a source of truth. A new session should be able to continue from repository state without reconstructing architecture from conversation logs.

## 1. Shared language before implementation

Before implementing a new subsystem, define the relevant vocabulary, contracts, and invariants in the repository.

Use:

- `docs/DOMAIN.md` for shared terminology and domain invariants;
- `docs/ARCHITECTURE.md` for current component boundaries;
- `docs/adr/` for durable design decisions and rejected/deferred alternatives;
- `docs/TESTING.md` for verification strategy;
- `docs/STATUS.md` for the current continuation point;
- `docs/RESEARCH-DISSERTATION.md` for the cumulative scholarly synthesis of research questions, evidence, measurements, limitations, and conclusions.

If a term has two plausible meanings, resolve it in documentation before allowing both meanings to spread through code.

## 2. Work unit

Each implementation unit should follow this order:

```text
Problem
  -> Contract
  -> Invariant
  -> Failing test / executable example
  -> Implementation
  -> Verification
  -> Diff review
  -> Refactor only if justified
  -> Status checkpoint
  -> Research synthesis checkpoint when evidence changed
```

### Problem

State the concrete gap or failure. Do not begin from a preferred implementation.

### Contract

Define externally observable behavior and inputs/outputs.

### Invariant

State what must remain true even when implementation changes.

### Failing test or executable example

Where practical, demonstrate the missing behavior before implementing it. For specification work, use normative examples or conformance vectors instead of pretending prose is a test.

### Implementation

Make the smallest coherent change that satisfies the contract.

### Verification

Run the relevant tests, type checks, format/lint checks, conformance vectors, and build steps. A change is not "done" because the code looks plausible.

### Diff review

Review what actually changed. Look for:

- accidental architecture drift;
- duplicated concepts;
- hidden assumptions;
- unrequested refactors;
- behavior not covered by verification;
- comments or documentation that claim more than tests prove.

### Refactor

Refactor only after behavior is proven and only when the refactor has a clear reason. Do not combine unrelated cleanup with a functional change.

### Status checkpoint

Update `docs/STATUS.md` with:

- what is now proven;
- what remains unverified;
- relevant branch/PR/commit;
- blockers;
- exactly one next recommended step.

### Research synthesis checkpoint

Per ADR-0012, ask after every meaningful evidence checkpoint:

```text
Did this work create or materially change a defensible research result,
conclusion, limitation, baseline, source, decision, falsification,
independent conformance result, or S/B/P/C accounting claim?
    |
    +-- no  -> no dissertation edit is required
    |
    +-- yes -> update docs/RESEARCH-DISSERTATION.md
               and docs/RESEARCH-DISSERTATION.ru.md in the same PR
```

This checkpoint is mandatory at stage-completion gates and after benchmark/measurement results that affect interpretation.

The dissertation update should not merely append a success statement. It must preserve the research meaning of the result, including negative/null findings, experimental conditions, limitations, and whether the evidence confirms, contradicts, or leaves a hypothesis unresolved.

## 3. One change, one reason

A pull request should have one dominant reason to exist.

Do not mix, for example:

- wire-format changes;
- type-system changes;
- evaluator optimizations;
- large naming cleanup;
- unrelated documentation restructuring.

If one decision logically requires another, make that dependency explicit.

## 4. Architecture before local cleverness

Prefer modules with small public contracts and deeper internal implementations over many shallow cross-coupled helpers.

Before adding a shortcut, ask whether it creates a second representation of an existing concept. NEX especially needs one canonical representation for terms, types, primitive IDs, and wire encoding.

## 5. Feedback loops

The primary feedback loop is deterministic:

```text
spec/contract -> test/vector -> implementation -> automated result -> diff review
```

When debugging, start from the first concrete failure rather than redesigning multiple layers at once.

For compiler/language work, useful feedback includes:

- golden encode/decode vectors;
- malformed-input rejection tests;
- type inference tests;
- property tests for round trips;
- evaluator examples;
- cross-implementation conformance tests;
- size/performance benchmark reports.

For research conclusions, useful feedback additionally includes:

- frozen corpora and explicitly versioned measurement inputs;
- machine-generated aggregate reports;
- externally sourced baselines with documented translation assumptions;
- negative or resource-limit checkpoints that are preserved rather than discarded;
- independent implementations or formal proofs where feasible.

## 6. AI-assisted work rules

AI agents working in this repository MUST:

1. inspect the current branch/HEAD, relevant docs, ADRs, tests, CI, and current dissertation before changing code;
2. not repeat work already present in the repository;
3. distinguish verified facts from hypotheses;
4. not invent passing tests, benchmark numbers, implementation status, bibliographic claims, or quotations;
5. not silently change an Accepted ADR;
6. avoid broad refactors unless the task specifically requires one;
7. prefer concrete diffs and verification results over long speculative explanations;
8. leave a continuation checkpoint after each meaningful stage;
9. update the dissertation when ADR-0012's evidence trigger applies.

AI agents SHOULD surface contradictions early instead of coding around them.

## 7. Definition of done

A code change is done only when all applicable items are true:

- contract is explicit;
- invariants are preserved;
- tests/conformance vectors cover the change;
- relevant tests pass;
- type/lint/build checks pass when present;
- documentation matches actual behavior;
- ADR is added or updated when architecture changed;
- `docs/STATUS.md` identifies the next state accurately;
- the living dissertation has been updated when the change produced research-significant evidence under ADR-0012.

A research result is done only when the measurement procedure and limitations are recorded alongside the result, and when material conclusions are integrated into the living dissertation rather than left only in a PR/chat/status note.

## 8. Communication style

Implementation reports should be concise and evidence-based:

```text
Changed:
Verified:
Not verified:
Next:
```

Do not replace verification with a long narrative. Detailed reasoning belongs in ADRs when it affects future design; cumulative research interpretation belongs in the dissertation.
