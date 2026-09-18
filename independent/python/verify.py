#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent
PACKET = ROOT / "packet"


def die(message: str) -> None:
    print(f"verification error: {message}", file=sys.stderr)
    raise SystemExit(2)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        die(f"cannot parse {path.relative_to(ROOT)}: {exc}")


def verify_packet() -> dict[str, int]:
    generated = load_json(PACKET / "PACKET-MANIFEST.generated.json")
    if generated.get("schema") != "nex-stage5-materialized-packet-v0.1":
        die("unexpected generated packet manifest schema")
    if generated.get("packet_id") != "nex1-independent-conformance-packet-v0.1":
        die("unexpected packet id")

    for entry in generated.get("files", []):
        rel = entry["path"]
        path = PACKET / rel
        if not path.is_file():
            die(f"packet file missing: {rel}")
        data = path.read_bytes()
        if len(data) != entry["bytes"]:
            die(f"packet byte length mismatch: {rel}")
        actual = hashlib.sha256(data).hexdigest()
        if actual != entry["sha256"]:
            die(f"packet sha256 mismatch: {rel}")

    manifest = load_json(PACKET / "stage5/conformance-packet-v0.1/manifest.json")
    if manifest.get("schema") != "nex-stage5-conformance-packet-manifest-v0.1":
        die("unexpected packet-local manifest schema")
    if manifest.get("source_commit") != generated.get("frozen_source_commit"):
        die("source commit mismatch between packet manifests")
    target = manifest.get("implementation_target", {})
    if target.get("language") != "Python" or target.get("minimum_version") != "3.12":
        die("packet implementation target is not Python 3.12+")
    if target.get("dependencies") != "standard-library-only":
        die("packet dependency target is not standard-library-only")

    wire = load_json(PACKET / "conformance/wire-v0.1.json")
    static = load_json(PACKET / "conformance/static-v0.1.json")
    evaluation = load_json(PACKET / "conformance/eval-v0.1.json")
    if wire.get("schema") != "nex-wire-conformance-v0.1":
        die("wire vector schema mismatch")
    if static.get("schema") != "nex-static-conformance-v0.1":
        die("static vector schema mismatch")
    if evaluation.get("schema") != "nex-eval-conformance-v0.1":
        die("evaluation vector schema mismatch")
    versions = {wire.get("core_version"), static.get("core_version"), evaluation.get("core_version")}
    if versions != {"NEX-1 Core v0.1"}:
        die(f"inconsistent conformance core versions: {versions}")

    return {
        "wire_integer": len(wire["integer_vectors"]),
        "wire_term": len(wire["term_vectors"]),
        "wire_invalid": len(wire["invalid_exact_vectors"]),
        "scope": len(static["scope_vectors"]),
        "type": len(static["type_vectors"]),
        "evaluation": len(evaluation["evaluation_vectors"]),
    }


def main() -> int:
    counts = verify_packet()
    print(
        "packet verified: "
        f"wire={counts['wire_integer']} integer + {counts['wire_term']} term + {counts['wire_invalid']} invalid, "
        f"scope={counts['scope']}, type={counts['type']}, evaluation={counts['evaluation']}"
    )
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
