#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = [
    ROOT / "stage5" / "receiver-assumptions" / "assumptions-v0.1.json",
    ROOT / "stage5" / "receiver-assumptions" / "assumptions-v0.2.json",
]


def fail(message: str) -> None:
    raise SystemExit(message)


def load(path: Path) -> dict:
    if not path.exists():
        fail(f"missing receiver-assumption model: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_common(data: dict) -> tuple[dict[str, dict], dict[str, dict]]:
    principles = data.get("principles", {})
    required_principles = {
        "assumptions_are_transmitted": False,
        "assumption_bit_cost_measured_here": False,
        "cross_profile_numeric_ranking_allowed": False,
        "host_source_counts_as_receiver_neutral_bootstrap": False,
        "double_count_shared_spec_bootstrap_bits": False,
        "physical_layer_below_A0_is_zero_cost": False,
    }
    for key, expected in required_principles.items():
        if principles.get(key) is not expected:
            fail(f"principle {key} must be {expected!r}")
    if principles.get("conditional_claim_notation") != "B | A":
        fail("conditional bootstrap notation must be 'B | A'")

    atoms = data.get("atoms", [])
    atom_ids = [a.get("id") for a in atoms]
    if not atom_ids or len(atom_ids) != len(set(atom_ids)):
        fail("assumption atom IDs must be non-empty and unique")
    atom_by_id = {a["id"]: a for a in atoms}
    allowed_categories = {"transport", "mathematical", "computational", "host"}
    for atom in atoms:
        if atom.get("category") not in allowed_categories:
            fail(f"invalid category for atom {atom.get('id')}")
        if not atom.get("statement"):
            fail(f"missing statement for atom {atom.get('id')}")

    profiles = data.get("profiles", [])
    profile_by_id = {p.get("id"): p for p in profiles}
    if len(profile_by_id) != len(profiles):
        fail("profile IDs must be unique")
    for profile in profiles:
        for atom_id in profile.get("adds", []):
            if atom_id not in atom_by_id:
                fail(f"profile {profile['id']} references unknown atom {atom_id}")
        parent = profile.get("extends")
        if parent is not None and parent not in profile_by_id:
            fail(f"profile {profile['id']} extends unknown profile {parent}")

    accounting = data.get("accounting", {})
    if "SB | A" not in accounting.get("joint_artifact", ""):
        fail("joint specification/bootstrap accounting rule is missing")
    if "exactly once" not in accounting.get("rule", ""):
        fail("ledger must state that every transmitted bit is counted exactly once")
    return atom_by_id, profile_by_id


def effective(profile_by_id: dict[str, dict], profile_id: str, trail: tuple[str, ...] = ()) -> set[str]:
    if profile_id in trail:
        fail("profile inheritance cycle: " + " -> ".join((*trail, profile_id)))
    profile = profile_by_id[profile_id]
    result = set(profile.get("adds", []))
    parent = profile.get("extends")
    if parent is not None:
        result |= effective(profile_by_id, parent, (*trail, profile_id))
    return result


def validate_v01(data: dict) -> None:
    if data.get("schema") != "nex-receiver-assumptions-v0.1":
        fail("unexpected v0.1 receiver-assumption schema")
    atom_by_id, profiles = validate_common(data)
    required = {"A0", "A1", "A2(U)", "A_host(H)"}
    if set(profiles) != required:
        fail(f"v0.1 profiles must be exactly {sorted(required)}")
    a0, a1, a2 = (effective(profiles, p) for p in ("A0", "A1", "A2(U)"))
    if not (a0 < a1 < a2):
        fail("v0.1 expected strict assumption ladder A0 < A1 < A2(U)")
    if any(atom_by_id[x]["category"] != "transport" for x in a0):
        fail("v0.1 A0 may contain transport atoms only")


def validate_v02(data: dict) -> None:
    if data.get("schema") != "nex-receiver-assumptions-v0.2":
        fail("unexpected v0.2 receiver-assumption schema")
    atom_by_id, profiles = validate_common(data)
    required = {"A0", "A1", "A1(R)", "A2(U)", "A_host(H)"}
    if set(profiles) != required:
        fail(f"v0.2 profiles must be exactly {sorted(required)}")

    a0 = effective(profiles, "A0")
    a1 = effective(profiles, "A1")
    a1r = effective(profiles, "A1(R)")
    a2 = effective(profiles, "A2(U)")
    ahost = effective(profiles, "A_host(H)")
    if not (a0 < a1 < a1r and a0 < a1 < a2):
        fail("v0.2 expected A0 < A1 with stronger A1(R) and A2(U) branches")
    if a1r <= a2 or a2 <= a1r:
        fail("v0.2 A1(R) and A2(U) must be distinct branches, not an implicit strength ordering")
    if any(atom_by_id[x]["category"] != "transport" for x in a0):
        fail("v0.2 A0 may contain transport atoms only")
    if any(atom_by_id[x]["category"] == "computational" for x in a1):
        fail("v0.2 A1 must not hide a rule calculus or universal machine")
    if profiles["A1(R)"].get("parameter", {}).get("name") != "R":
        fail("v0.2 A1(R) must declare parameter R")
    if profiles["A2(U)"].get("parameter", {}).get("name") != "U":
        fail("v0.2 A2(U) must declare parameter U")
    if any(atom_by_id[x]["category"] == "host" for x in a1r | a2):
        fail("receiver-neutral candidate profiles must not contain host assumptions")
    if "H_PLATFORM_H" not in ahost or profiles["A_host(H)"].get("receiver_neutral_candidate") is not False:
        fail("A_host(H) must contain the host atom and be non-neutral")

    accounting = data.get("accounting", {})
    if "|M_A|" not in accounting.get("exact_message_form", ""):
        fail("v0.2 must define exact cost as length of a concrete transmitted object M_A")
    if data.get("principles", {}).get("description_length_is_unconditional") is not False:
        fail("v0.2 must reject unconditional machine-free description-length claims")


def main() -> None:
    v01, v02 = map(load, MODELS)
    validate_v01(v01)
    validate_v02(v02)
    print("receiver-assumption models verified")
    for label, data in (("v0.1 historical", v01), ("v0.2 current", v02)):
        profiles = {p["id"]: p for p in data["profiles"]}
        sizes = ", ".join(f"{p}={len(effective(profiles, p))}" for p in profiles)
        print(f"{label}: {sizes}")


if __name__ == "__main__":
    main()
