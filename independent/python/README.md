# Independent NEX-1 v0.1 Python implementation

This directory is an independent reconstruction of NEX-1 Core v0.1 from the frozen `nex1-independent-conformance-packet-v0.1` packet only. It targets Python 3.12+ and uses only the standard library.

## Contents

- `nex/term.py` — six-constructor Core AST.
- `nex/wire.py` — `U(n)`, canonical term encoding, prefix/exact decoding, consumed-bit reporting, syntax/resource distinction.
- `nex/scope.py` — closed zero-based de Bruijn scope validation.
- `nex/typesys.py` — HM rank-1 inference, schemes, substitutions, unification, occurs check, let-generalization, Core primitive schemes, canonical type observation.
- `nex/eval.py` — weak call-by-name evaluator with delayed arguments/fields/payloads, all Core primitives, partial application, and separate execution resource refusal.
- `packet/` — the frozen conformance packet used as the information boundary.
- `tests/` — conformance and independent unit/property-style tests.
- `AMBIGUITIES.md` — ambiguities/omissions encountered.
- `IMPLEMENTATION-NOTES.md` — independent design choices.
- `INDEPENDENCE-DECLARATION.md` — experiment provenance and independence statement.

## Verification

From this directory:

```bash
python verify.py
```

`verify.py` first checks packet manifests, SHA-256 file digests, vector schemas, and the Core version. It then runs all conformance and additional tests and exits nonzero on any failure.

No third-party package installation is required.
