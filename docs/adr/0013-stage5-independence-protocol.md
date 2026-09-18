# ADR-0013: Freeze the Stage 5 independence protocol and use Python for the first independent implementation

**Status:** Accepted  
**Date:** 2026-09-18

## Context

Stage 4 established that NEX-1 v0.1 has one complete Go reference implementation, reproducible conformance artifacts, and measured program-level behavior, but it did not establish that the published specification independently determines the same system. The specification and Go implementation were developed together, so shared assumptions could remain invisible.

Stage 5 therefore needs a second implementation whose evidentiary value comes from reconstructing NEX from a frozen specification/conformance packet rather than translating `reference/go`.

A methodological complication is explicit: the agent/session that helped develop the Go reference already has prior knowledge of that implementation. Work produced in that same contaminated context cannot honestly be labelled cognitively independent merely because it is written in another language.

## Decision drivers

- test specification completeness rather than ability to port Go code;
- make implementation-input material finite, versioned, and reviewable;
- prevent accidental leakage from `reference/go`, Stage 4 experiments, or benchmark-specific behavior;
- use a host language materially different from Go;
- avoid third-party libraries where possible;
- retain arbitrary-precision natural numbers without importing a big-integer package;
- distinguish independent-conformance evidence from receiver-neutral bootstrap evidence;
- preserve discovered ambiguities as research results.

## Decision

### 1. Frozen packet

The first independent implementation SHALL be based on `stage5/conformance-packet-v0.1/manifest.json`, whose source snapshot is pinned to repository commit:

```text
4f9c50aed13cdbdf72c9ce6510521477d49c05a5
```

The packet allowlist contains only:

- `docs/NEX-1-v0.1.md`;
- `conformance/wire-v0.1.json`;
- `conformance/static-v0.1.json`;
- `conformance/eval-v0.1.json`;
- ADR-0002 (Core v0.1 design basis);
- ADR-0006 (decoder resource limits versus validity);
- ADR-0007 (erased term annotations in v0.1);
- ADR-0009 (evaluator resource limits versus semantics).

ADR-0008 is intentionally **excluded** from the implementation packet. It specifies the architecture of the Go reference evaluator (`environment + closures + delayed bindings`), not a required NEX runtime representation. Including it would reduce implementation independence.

The packet also contains packet-specific observation rules needed only to compare portable conformance outputs, not to prescribe host runtime structures.

### 2. Excluded repository material before the independence checkpoint

The first independent implementer MUST NOT inspect or derive implementation guidance from:

```text
reference/go/**
reference/go/experiment/**
benchmarks/**
docs/experiments/**
docs/STAGE-1.md ... docs/STAGE-4.md
docs/STATUS.md
docs/RESEARCH-DISSERTATION*.md
PR discussions or commit diffs containing Go implementation details
```

The exclusion is about implementation guidance. Repository infrastructure needed only to build/extract the frozen packet may be used.

### 3. Allowed external theory

The independent implementer MAY consult the primary theory already underlying the normative design, specifically:

- de Bruijn (nameless variables / indices) — SRC-0001;
- Milner 1978 — SRC-0003;
- Damas & Milner 1982 — SRC-0004;
- Plotkin 1977 LCF/PCF background — SRC-0005;
- Elias 1975 integer coding — SRC-0006;
- Plotkin 1975 call-by-name/call-by-value — SRC-0011.

External sources must not be used to override explicit NEX v0.1 rules.

### 4. First independent implementation language

The first independent implementation SHALL target **Python 3.12+ using only the Python standard library**.

Rationale:

- Python is materially different from Go in type system, object model, control flow, and implementation style;
- Python integers provide arbitrary precision without a third-party big-integer dependency;
- the standard library is sufficient for JSON conformance, testing, dataclasses/structured values, and deterministic command-line tools;
- the implementation can remain small enough for specification review;
- host-language static typing is irrelevant to whether NEX's own static semantics are reconstructed correctly.

Python source size MUST NOT be interpreted as receiver-neutral bootstrap cost `B`.

### 5. Cognitive-independence requirement

A result may be labelled **independent implementation evidence** only if the implementation is produced in a fresh isolated context or by another implementer who receives the frozen packet and allowed theory but not the excluded NEX implementation material.

The current co-development context may:

- define the protocol;
- build and verify the packet;
- audit packet completeness;
- create test harness/infrastructure that does not encode hidden Go behavior.

It MUST NOT claim that code authored from prior Go implementation knowledge is independent evidence.

### 6. Comparison gate

Direct comparison with `reference/go` becomes allowed only after an independent checkpoint is frozen containing at least:

```text
wire codec
scope validation
principal type inference
normative weak-CBN evaluator
packet conformance results
implementation commit SHA
```

After that freeze, differential testing may classify discrepancies as:

```text
specification ambiguity / omission
Go reference bug
independent implementation bug
conformance-vector gap
deliberately unspecified implementation behavior
```

The rule "make the second implementation match Go" is not a valid resolution unless the specification independently supports the Go behavior.

## Accepted consequences

- Stage 5 begins with documentation and packet infrastructure rather than implementation code.
- A fresh implementation context is required before Stage 5.2 can produce strong independent evidence.
- Python becomes an experimental conformance platform, not a normative implementation architecture.
- Some ambiguities may require specification/conformance clarification before the independent implementation proceeds.
- Stage 5 may discover that existing vectors encode presentation conventions not yet stated normatively; those must be documented as observation conventions rather than inferred from Go.

## Alternatives considered

### Rust

Deferred for the first independent implementation. Rust would provide strong host-side invariants, but arbitrary-precision naturals require a non-standard dependency or a custom big integer, adding unrelated implementation surface. It remains a good candidate for a later third implementation.

### Another Go implementation

Rejected for the first independence experiment because language/runtime similarity would increase the chance of copying the reference architecture or reproducing the same assumptions.

### JavaScript / TypeScript

Deferred. Native JavaScript `BigInt` is sufficient numerically, but Python provides a simpler standard-library-only test/conformance environment for this experiment.

### Write the second implementation in the current co-development context

Rejected as evidence. It could still be useful engineering work, but it would not satisfy the cognitive-independence claim because this context already knows the Go design.

## Evidence / references

This ADR is primarily a research-method decision. The allowed theory corresponds to sources already registered in `docs/SOURCES.md`. No claim is made that Python is more receiver-neutral than Go; it is selected only to strengthen implementation independence.

## Follow-up validation

Stage 5.0 is complete when:

- this ADR is Accepted;
- the packet manifest is versioned and tied to the exact source commit/blobs;
- excluded/allowed material is explicit;
- the Python 3.12 standard-library-only choice is recorded;
- the cognitive-independence limitation is visible in `docs/STATUS.md` and the living dissertation.

Stage 5.1 must then audit whether the packet is sufficient without consulting `reference/go`.
