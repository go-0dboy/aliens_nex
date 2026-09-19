#!/usr/bin/env python3
"""Reproduce the frozen negative runtime result for functional-stream v0.1."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERIFIER = ROOT / "stage5" / "selfhost" / "verify_functional_stream.py"

EXPECTED = [
    "stage5.12e functional-stream verification failed: Python call-by-need refused candidate cases:",
    "repeat_query:5(0, 32, 31): transition limit exceeded: 5000001 > 5000000",
    "repeat_query:6(0, 32, 32): transition limit exceeded: 5000001 > 5000000",
    "repeat_query:7(1, 128, 127): transition limit exceeded: 5000001 > 5000000",
    "repeat_query:8(1, 128, 128): transition limit exceeded: 5000001 > 5000000",
]


def main() -> None:
    completed = subprocess.run(
        [sys.executable, str(VERIFIER)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = (completed.stdout + "\n" + completed.stderr).strip()
    if completed.returncode == 0:
        raise SystemExit("functional-stream v0.1 unexpectedly passed its frozen workload")
    missing = [fragment for fragment in EXPECTED if fragment not in output]
    if missing:
        raise SystemExit(
            "functional-stream v0.1 negative result changed; missing expected evidence: "
            + " | ".join(missing)
            + "\nactual output:\n"
            + output
        )
    print("stage5.12e functional-stream v0.1 negative result: reproduced")
    print("Python call-by-need frozen transition refusals: 4")
    print("candidate remains historical development evidence, not hold-out")


if __name__ == "__main__":
    main()
