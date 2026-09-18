# NEX Stage 5 independent conformance packet v0.1

This directory defines the frozen information boundary for the first independent NEX-1 implementation experiment.

## Purpose

The packet is intended to answer a narrow research question:

> Can a second implementation reconstruct NEX-1 v0.1 wire, static semantics, and normative weak-call-by-name behavior without translating or inspecting the existing Go reference implementation?

This packet is **not** a bootstrap artifact and is **not** an estimate of `B`.

## Frozen source snapshot

The packet is anchored to repository commit:

```text
4f9c50aed13cdbdf72c9ce6510521477d49c05a5
```

`manifest.json` records the exact Git blob SHA for every allowed repository source file.

The snapshot is intentionally older than the Stage 5 branch. Stage 5 protocol/audit files are packet-local additions layered on top of that frozen NEX-1 snapshot.

## Allowed implementation inputs

The implementation may use only:

1. files listed in `manifest.json` under `source_files`;
2. packet-local files in this directory;
3. external theory explicitly allowlisted by ADR-0013 / `allowed_external_source_ids`;
4. Python 3.12+ standard-library documentation needed to use the chosen host language.

The implementer must not inspect excluded NEX repository paths until the independent checkpoint is frozen.

## Why ADR-0008 is excluded

ADR-0008 describes how the Go reference evaluator is organized internally. NEX v0.1 does not require an implementation to use the same closure/environment/thunk representation. The independent implementation should recover observable weak-call-by-name behavior from the normative specification rather than duplicate the Go runtime architecture.

## Packet-specific observation rules

`OBSERVATIONS.md` defines only portable comparison formatting that the main specification does not completely fix, especially canonical textual rendering of principal type schemes.

These rules do not add new term constructors, type rules, reduction rules, or primitive semantics.

## Completeness audit

`AUDIT.md` records the Stage 5.1 audit. Any discovered omission is classified before implementation starts. The packet must not silently use `reference/go` to fill missing semantics.

## Reproduction

From a checkout containing the exact frozen source files, run:

```text
python3 stage5/build_packet.py --verify
```

To materialize a standalone directory:

```text
python3 stage5/build_packet.py --output /tmp/nex1-packet-v0.1
```

The builder verifies Git-blob content hashes from `manifest.json`, copies only allowlisted source files plus packet-local files, and writes a generated manifest containing SHA-256 hashes of the materialized packet contents.

## Independence checkpoint

The second implementation must freeze a commit after wire, static semantics, and normative dynamic semantics pass this packet. Only then may its author compare implementation code or generated behavior directly with `reference/go`.
