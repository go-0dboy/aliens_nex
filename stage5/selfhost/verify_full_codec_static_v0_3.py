#!/usr/bin/env python3
"""Static-only validation of full-codec v0.3 before first semantic execution.

Builds canonical wire, checks Python/Go principal typing and prints immutable
identity. It never evaluates decodeTerm/encodeTerm on a workload.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PYTHON_IMPL = ROOT / "independent" / "python"
GO_IMPL = ROOT / "reference" / "go"
sys.path.insert(0, str(PYTHON_IMPL))

from nex.typesys import infer_principal, render_scheme  # noqa: E402
from nex.wire import decode_exact, encode_term  # noqa: E402
from build_foundation import encode_core, lower  # noqa: E402
from build_full_codec import EXPECTED_TYPE  # noqa: E402
from build_full_codec_v0_3 import source_terms_full_codec_v0_3  # noqa: E402


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12 full-codec v0.3 static verification failed: {message}")


def main() -> None:
    check = subprocess.run(
        [sys.executable, str(ROOT / "stage5/selfhost/validate_full_codec_contract_v0_3.py")],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if check.returncode != 0:
        fail(check.stderr.strip() or check.stdout.strip())

    rows = []
    requests = []
    for name, source in source_terms_full_codec_v0_3().items():
        bits = encode_core(lower(source))
        term = decode_exact(bits)
        if encode_term(term) != bits:
            fail(f"{name}: canonical Python wire round-trip failed")
        inferred = render_scheme(infer_principal(term))
        if inferred != EXPECTED_TYPE:
            fail(f"{name}: Python type {inferred!r} != {EXPECTED_TYPE!r}")
        digest = hashlib.sha256(bits.encode("ascii")).hexdigest()
        rows.append((name, len(bits), digest))
        requests.append({"id": f"static:{name}", "level": "static", "bits": bits})

    completed = subprocess.run(
        ["go", "run", "./cmd/nexselfhostprobe"], cwd=GO_IMPL,
        input=json.dumps(requests), text=True, capture_output=True, check=False,
    )
    if completed.returncode != 0:
        fail(f"Go static probe failed: {completed.stderr.strip()}")
    responses = {row["id"]: row for row in json.loads(completed.stdout)}
    for name, _length, _digest in rows:
        row = responses.get(f"static:{name}")
        if row is None or row.get("static_error"):
            fail(f"{name}: Go static rejection/missing response: {row}")
        if row.get("type") != EXPECTED_TYPE:
            fail(f"{name}: Go type {row.get('type')!r} != {EXPECTED_TYPE!r}")

    print("stage5.12 full codec v0.3: canonical identity and static typing verified")
    for name, length, digest in rows:
        print(f"{name}: {length} bits sha256={digest}")
    print(f"principal type: {EXPECTED_TYPE}")
    print("candidate semantic execution: NOT PERFORMED")
    print("v0.3 holdout: NOT READ / NOT EXECUTED")


if __name__ == "__main__":
    main()
