#!/usr/bin/env python3
"""Validate meta-representation-v0.2 without rewriting the frozen v0.1 checkpoint."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V1 = ROOT / "stage5" / "selfhost" / "meta-representation-v0.1.json"
V2 = ROOT / "stage5" / "selfhost" / "meta-representation-v0.2.json"

TAGGED_REPRESENTATIONS = {
    "Term",
    "Type",
    "PortableObservation",
    "StaticResult",
    "ToolRequest",
    "ToolResult",
}


def fail(message: str) -> None:
    raise SystemExit(f"stage5.11 meta-representation v0.2 invalid: {message}")


def pair(a: int, b: int) -> int:
    if a < 0 or b < 0:
        fail("pair arguments must be naturals")
    return (1 << a) * (2 * b + 1) - 1


def main() -> None:
    old = json.loads(V1.read_text(encoding="utf-8"))
    new = json.loads(V2.read_text(encoding="utf-8"))

    if old.get("version") != "0.1" or new.get("version") != "0.2":
        fail("unexpected version lineage")
    if old.get("schema") != new.get("schema"):
        fail("schema changed while resolving tagged encoding")
    if old.get("core_version") != new.get("core_version") or new.get("core_version") != "NEX-1 v0.1":
        fail("Core target changed")
    if old.get("core_dependencies") != new.get("core_dependencies"):
        fail("Core dependencies changed")
    if old.get("tag_sets") != new.get("tag_sets"):
        fail("tag sets changed")
    if old.get("forbidden_dependencies") != new.get("forbidden_dependencies"):
        fail("forbidden-dependency guard changed")

    old_foundation = old.get("numeric_foundation", {})
    new_foundation = new.get("numeric_foundation", {})
    if old_foundation.get("pair") != new_foundation.get("pair"):
        fail("pair representation changed")
    if old_foundation.get("sequence") != new_foundation.get("sequence"):
        fail("sequence representation changed")

    tagged = new_foundation.get("tagged")
    expected_tagged = {
        "id": "pair-tag-v0.1",
        "carrier": "N x N -> N",
        "definition": "tagged(tag,payload) = pair(tag,payload)",
        "inverse": "unpair(code) = (tag,payload)",
        "canonical_rule": "tag must belong to the declared dense tag set; payload must satisfy the selected tag payload rule",
    }
    if tagged != expected_tagged:
        fail("exact tagged representation contract mismatch")

    old_reps = old.get("representations", {})
    new_reps = new.get("representations", {})
    if set(old_reps) != set(new_reps):
        fail("representation inventory changed")

    for name, spec in new_reps.items():
        if spec.get("carrier") != "N":
            fail(f"{name} no longer uses N carrier")
        if name in TAGGED_REPRESENTATIONS:
            if spec.get("form") != "tagged":
                fail(f"{name} must remain tagged")
            if spec.get("tagged_encoding") != "pair-tag-v0.1":
                fail(f"{name} does not reference pair-tag-v0.1")
        elif "tagged_encoding" in spec:
            fail(f"{name} unexpectedly declares tagged encoding")

    term_tags = new["tag_sets"]["term_tags"]
    for example in new.get("bounded_examples", {}).get("tagged_terms", []):
        constructor = example["constructor"]
        payload = example["payload"]
        expected = example["code"]
        try:
            tag = term_tags[constructor]
        except KeyError:
            fail(f"unknown constructor in tagged example: {constructor}")
        actual = pair(tag, payload)
        if actual != expected:
            fail(
                f"tagged example {constructor}({payload}) expected {expected}, got {actual}"
            )

    # The v0.2 change is intentionally narrow: old bounded pair/sequence examples
    # stay byte-for-byte equal; new evidence only makes the previously implicit
    # outer tagged encoding exact.
    for key in ("pairs", "sequences"):
        if old.get("bounded_examples", {}).get(key) != new.get("bounded_examples", {}).get(key):
            fail(f"historical bounded {key} examples changed")

    print("stage5.11 meta-representation v0.2: valid")
    print("Core/tag sets/pair/sequence: unchanged from v0.1")
    print("tagged(tag,payload)=pair(tag,payload): explicit and checked")
    print(f"tagged representation families: {len(TAGGED_REPRESENTATIONS)}")
    print(f"tagged Term examples: {len(new['bounded_examples']['tagged_terms'])}")


if __name__ == "__main__":
    main()
