#!/usr/bin/env python3
"""Build/verify the frozen Stage 5 independent conformance packet.

This tool intentionally knows only packet paths and hashes. It does not inspect
or import the Go reference implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
PACKET_DIR = ROOT / "stage5" / "conformance-packet-v0.1"
MANIFEST_PATH = PACKET_DIR / "manifest.json"
GENERATED_MANIFEST = "PACKET-MANIFEST.generated.json"


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_manifest() -> dict[str, Any]:
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        manifest = json.load(f)
    if manifest.get("schema") != "nex-stage5-conformance-packet-manifest-v0.1":
        raise ValueError("unexpected packet manifest schema")
    if manifest.get("source_commit") != "4f9c50aed13cdbdf72c9ce6510521477d49c05a5":
        raise ValueError("unexpected frozen source commit")
    return manifest


def verify_source_files(manifest: dict[str, Any]) -> list[Path]:
    paths: list[Path] = []
    seen: set[str] = set()
    for item in manifest["source_files"]:
        rel = item["path"]
        if rel in seen:
            raise ValueError(f"duplicate source path: {rel}")
        seen.add(rel)
        path = ROOT / rel
        if not path.is_file():
            raise FileNotFoundError(rel)
        data = path.read_bytes()
        actual = git_blob_sha(data)
        expected = item["git_blob_sha"]
        if actual != expected:
            raise ValueError(
                f"frozen source mismatch for {rel}: expected {expected}, got {actual}"
            )
        paths.append(path)
    return paths


def verify_packet_local_files(manifest: dict[str, Any]) -> list[Path]:
    paths: list[Path] = []
    seen: set[str] = set()
    for rel in manifest["packet_local_files"]:
        if rel in seen:
            raise ValueError(f"duplicate packet-local path: {rel}")
        seen.add(rel)
        path = ROOT / rel
        if not path.is_file():
            raise FileNotFoundError(rel)
        paths.append(path)
    return paths


def verify_conformance_json(manifest: dict[str, Any]) -> None:
    required_schemas = {
        "conformance/wire-v0.1.json": "nex-wire-conformance-v0.1",
        "conformance/static-v0.1.json": "nex-static-conformance-v0.1",
        "conformance/eval-v0.1.json": "nex-eval-conformance-v0.1",
    }
    allowlisted = {item["path"] for item in manifest["source_files"]}
    for rel, expected_schema in required_schemas.items():
        if rel not in allowlisted:
            raise ValueError(f"required conformance file is not allowlisted: {rel}")
        with (ROOT / rel).open("r", encoding="utf-8") as f:
            payload = json.load(f)
        if payload.get("schema") != expected_schema:
            raise ValueError(
                f"unexpected schema for {rel}: {payload.get('schema')!r}"
            )


def materialize(manifest: dict[str, Any], output: Path) -> None:
    source_paths = verify_source_files(manifest)
    local_paths = verify_packet_local_files(manifest)
    verify_conformance_json(manifest)

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    copied: list[dict[str, Any]] = []
    for path in source_paths + local_paths:
        rel = path.relative_to(ROOT)
        destination = output / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        data = path.read_bytes()
        destination.write_bytes(data)
        copied.append(
            {
                "path": rel.as_posix(),
                "bytes": len(data),
                "sha256": sha256(data),
            }
        )

    generated = {
        "schema": "nex-stage5-materialized-packet-v0.1",
        "packet_id": manifest["packet_id"],
        "frozen_source_commit": manifest["source_commit"],
        "files": sorted(copied, key=lambda x: x["path"]),
    }
    encoded = (json.dumps(generated, indent=2, sort_keys=True) + "\n").encode("utf-8")
    (output / GENERATED_MANIFEST).write_bytes(encoded)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verify",
        action="store_true",
        help="verify the frozen allowlist and packet-local files without materializing",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="materialize a standalone packet directory",
    )
    args = parser.parse_args()

    if not args.verify and args.output is None:
        parser.error("specify --verify and/or --output")

    try:
        manifest = load_manifest()
        verify_source_files(manifest)
        verify_packet_local_files(manifest)
        verify_conformance_json(manifest)
        if args.output is not None:
            materialize(manifest, args.output.resolve())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"packet verification failed: {exc}", file=sys.stderr)
        return 1

    print(
        f"packet {manifest['packet_id']} verified at source commit "
        f"{manifest['source_commit']}"
    )
    if args.output is not None:
        print(f"materialized: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
