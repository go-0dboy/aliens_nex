#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "stage5" / "receiver-assumptions" / "assumptions-v0.1.json"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    data = json.loads(MODEL.read_text(encoding="utf-8"))
    if data.get("schema") != "nex-receiver-assumptions-v0.1":
        fail("unexpected receiver-assumption schema")

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
    required_profiles = {"A0", "A1", "A2(U)", "A_host(H)"}
    if set(profile_by_id) != required_profiles:
        fail(f"profiles must be exactly {sorted(required_profiles)}")

    for profile in profiles:
        for atom_id in profile.get("adds", []):
            if atom_id not in atom_by_id:
                fail(f"profile {profile['id']} references unknown atom {atom_id}")
        parent = profile.get("extends")
        if parent is not None and parent not in profile_by_id:
            fail(f"profile {profile['id']} extends unknown profile {parent}")

    def effective(profile_id: str, trail: tuple[str, ...] = ()) -> set[str]:
        if profile_id in trail:
            fail("profile inheritance cycle: " + " -> ".join((*trail, profile_id)))
        profile = profile_by_id[profile_id]
        result = set(profile.get("adds", []))
        parent = profile.get("extends")
        if parent is not None:
            result |= effective(parent, (*trail, profile_id))
        return result

    a0 = effective("A0")
    a1 = effective("A1")
    a2 = effective("A2(U)")
    ahost = effective("A_host(H)")
    if not (a0 < a1 < a2):
        fail("expected strict assumption ladder A0 < A1 < A2(U)")

    if any(atom_by_id[x]["category"] != "transport" for x in a0):
        fail("A0 may contain transport atoms only")
    if any(atom_by_id[x]["category"] == "host" for x in a2):
        fail("A2(U) must not contain host assumptions")
    if "H_PLATFORM_H" not in ahost or profile_by_id["A_host(H)"].get("receiver_neutral_candidate") is not False:
        fail("A_host(H) must contain the host atom and be non-neutral")
    if profile_by_id["A2(U)"].get("parameter", {}).get("name") != "U":
        fail("A2(U) must declare parameter U")

    accounting = data.get("accounting", {})
    if "SB | A" not in accounting.get("joint_artifact", ""):
        fail("joint specification/bootstrap accounting rule is missing")
    if "exactly once" not in accounting.get("rule", ""):
        fail("ledger must state that every transmitted bit is counted exactly once")

    print("receiver-assumption model verified")
    for profile_id in ("A0", "A1", "A2(U)", "A_host(H)"):
        print(f"{profile_id}: {len(effective(profile_id))} effective assumption atoms")


if __name__ == "__main__":
    main()
