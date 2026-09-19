#!/usr/bin/env python3
"""Static-only verification for Stage 5.12 full codec candidate v0.2.

No candidate evaluation occurs here. The script rechecks the preregistration,
canonical wire identity and independent Python/Go principal typing before the
first v0.2 development semantic run.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "stage5" / "selfhost" / "full-codec-v0.2.json"
PYTHON_IMPL = ROOT / "independent" / "python"
GO_IMPL = ROOT / "reference" / "go"

sys.path.insert(0, str(PYTHON_IMPL))

from nex.typesys import infer_principal, render_scheme  # noqa: E402
from nex.wire import decode_exact, encode_term  # noqa: E402
from build_full_codec import EXPECTED_TYPE  # noqa: E402
from build_full_codec_v0_2 import source_terms_full_codec_v0_2  # noqa: E402
from build_foundation import encode_core, lower  # noqa: E402


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12 full-codec v0.2 static verification failed: {message}")


def main() -> None:
    check = subprocess.run(
        [sys.executable, str(ROOT / "stage5" / "selfhost" / "validate_full_codec_contract_v0_2.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if check.returncode != 0:
        fail(check.stderr.strip() or check.stdout.strip())

    build = subprocess.run(
        [sys.executable, str(ROOT / "stage5" / "selfhost" / "build_full_codec_v0_2.py"), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if build.returncode != 0:
        fail(build.stderr.strip() or build.stdout.strip())

    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    if artifact.get("version") != "0.2" or artifact.get("core_version") != "NEX-1 v0.1":
        fail("candidate version/Core drifted")
    if artifact.get("status") != "stage5.12-development-candidate":
        fail("candidate status drifted")
    if artifact.get("contract") != "stage5/selfhost/full-codec-contract-v0.2.json":
        fail("contract reference drifted")
    if artifact.get("holdout_status") != "preregistered_unexecuted":
        fail("holdout must remain preregistered_unexecuted")

    sources = source_terms_full_codec_v0_2()
    items = artifact.get("functions", [])
    if [row.get("name") for row in items] != ["decodeTerm", "encodeTerm"]:
        fail("unexpected function inventory/order")

    requests = []
    for row in items:
        name = row["name"]
        bits = encode_core(lower(sources[name]))
        if len(bits) != row["wire_bit_length"]:
            fail(f"{name}: wire length drifted")
        digest = hashlib.sha256(bits.encode("ascii")).hexdigest()
        if digest != row["wire_sha256"]:
            fail(f"{name}: wire SHA-256 drifted")
        term = decode_exact(bits)
        if encode_term(term) != bits:
            fail(f"{name}: canonical Python wire round-trip failed")
        inferred = render_scheme(infer_principal(term))
        if inferred != EXPECTED_TYPE or inferred != row["expected_type"]:
            fail(f"{name}: Python type {inferred!r} != {EXPECTED_TYPE!r}")
        requests.append({"id": f"static-v02:{name}", "level": "static", "bits": bits})

    completed = subprocess.run(
        ["go", "run", "./cmd/nexselfhostprobe"],
        cwd=GO_IMPL,
        input=json.dumps(requests),
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"Go static probe failed: {completed.stderr.strip()}")
    try:
        responses = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        fail(f"cannot parse Go probe output: {exc}")
    by_id = {row["id"]: row for row in responses}
    for item in items:
        row = by_id.get(f"static-v02:{item['name']}")
        if row is None or row.get("static_error"):
            fail(f"{item['name']}: Go static rejection/missing response: {row}")
        if row.get("type") != EXPECTED_TYPE:
            fail(f"{item['name']}: Go type {row.get('type')!r} != {EXPECTED_TYPE!r}")

    print("stage5.12 full codec v0.2: canonical identity and static typing verified")
    for item in items:
        print(f"{item['name']}: {item['wire_bit_length']} bits sha256={item['wire_sha256']}")
    print(f"principal type: {EXPECTED_TYPE}")
    print("candidate semantic execution: NOT PERFORMED")
    print("holdout: NOT EXECUTED")


if __name__ == "__main__":
    main()
