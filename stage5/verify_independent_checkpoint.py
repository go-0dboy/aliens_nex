#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "stage5/independent-checkpoints/python-v0.1.json"


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema") != "nex-stage5-independent-checkpoint-v0.1":
        print("unexpected checkpoint manifest schema", file=sys.stderr)
        return 2
    failures: list[str] = []
    for entry in data.get("files", []):
        path = ROOT / entry["path"]
        if not path.is_file():
            failures.append(f"missing {entry['path']}")
            continue
        raw = path.read_bytes()
        if len(raw) != entry["bytes"]:
            failures.append(f"byte length mismatch {entry['path']}")
        actual = hashlib.sha256(raw).hexdigest()
        if actual != entry["sha256"]:
            failures.append(f"sha256 mismatch {entry['path']}: {actual}")
    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1
    print(
        f"independent checkpoint verified: {len(data['files'])} frozen files; "
        f"archive sha256={data['archive_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
