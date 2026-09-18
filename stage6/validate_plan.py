#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "stage6" / "curriculum-plan-v0.1.json"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    data = json.loads(PLAN.read_text(encoding="utf-8"))

    if data.get("schema") != "nex-stage6-curriculum-plan-v0.1":
        fail("unexpected Stage 6 curriculum schema")
    if data.get("status") != "planning-contract-not-transmitted-artifact":
        fail("planning artifact must not masquerade as transmitted teaching content")
    if data.get("core_target") != "NEX-1 Core v0.1":
        fail("Stage 6 planning must target stable NEX-1 Core v0.1")
    if data.get("decision") != "ADR-0017":
        fail("Stage 6 plan must reference ADR-0017")

    profile = data.get("receiver_profile", {})
    if profile.get("selected") is not False:
        fail("planning checkpoint must not pretend the first receiver profile is already selected")
    allowed = set(profile.get("allowed_profiles", []))
    if allowed != {"A0", "A1", "A1(R)", "A2(U)"}:
        fail("unexpected receiver-profile candidate set")

    expected_competence = {"decode", "encode", "static", "evaluate", "construct", "self_test"}
    competence = set(data.get("competence_categories", []))
    if competence != expected_competence:
        fail("competence categories must include decode/encode/static/evaluate/construct/self_test exactly")

    teaching_goal = data.get("teaching_goal", {})
    if set(teaching_goal) != expected_competence or not all(teaching_goal.values()):
        fail("all Stage 6 competence goals must be enabled")

    constraints = data.get("hard_constraints", {})
    required_true = {
        "nex1_core_must_remain_unchanged",
        "teaching_representation_may_differ_from_canonical_wire",
        "undeclared_terrestrial_prose_is_not_receiver_neutral",
        "heldout_construction_tasks_required",
        "exact_bits_for_plan_are_not_bootstrap_cost",
        "receiver_proxy_results_are_not_alien_cognition_claims",
    }
    if set(constraints) != required_true or not all(constraints.values()):
        fail("Stage 6 hard constraints are missing or weakened")

    lessons = data.get("lessons", [])
    if not lessons:
        fail("curriculum plan must contain lessons")

    ids = [lesson.get("id") for lesson in lessons]
    if any(not item for item in ids) or len(ids) != len(set(ids)):
        fail("lesson IDs must be non-empty and unique")

    orders = [lesson.get("order") for lesson in lessons]
    if orders != list(range(len(lessons))):
        fail("lesson order must be contiguous and match list order")

    by_id = {lesson["id"]: lesson for lesson in lessons}
    order_by_id = {lesson["id"]: lesson["order"] for lesson in lessons}

    for lesson in lessons:
        if not lesson.get("concepts_introduced"):
            fail(f"lesson {lesson['id']} introduces no concepts")
        if not lesson.get("goal"):
            fail(f"lesson {lesson['id']} has no goal")
        for prereq in lesson.get("prerequisites", []):
            if prereq not in by_id:
                fail(f"lesson {lesson['id']} references unknown prerequisite {prereq}")
            if order_by_id[prereq] >= lesson["order"]:
                fail(f"lesson {lesson['id']} depends on non-earlier prerequisite {prereq}")

    if lessons[-1]["id"] != "L13-heldout-competence":
        fail("held-out competence gate must be the final planning step")
    if lessons[-1].get("status") != "experiment_only_not_transmitted_lesson":
        fail("held-out competence tasks must not be transmitted as teaching examples")

    measurement = data.get("measurement_plan", {})
    if measurement.get("publish_T_bits_before_exact_serialization") is not False:
        fail("T_bits must remain unpublished before exact serialization")
    if measurement.get("heldout_tasks_counted_in_T") is not False:
        fail("held-out tasks must remain outside the teaching artifact")
    for key in ("lesson_bits", "self_test_bits", "receiver_success_by_category", "assumption_leaks", "curriculum_revision_count"):
        if measurement.get(key) is not True:
            fail(f"measurement plan must require {key}")

    raw = PLAN.read_text(encoding="utf-8")
    forbidden_scalar_claims = ["\"T_bits\":", "\"bootstrap_bits\":", "\"total_bits\":"]
    if any(marker in raw for marker in forbidden_scalar_claims):
        fail("planning artifact must not publish a premature exact bit-count field")

    print("Stage 6 curriculum planning contract verified")
    print(f"lessons: {len(lessons)}")
    print("competence categories: " + ", ".join(sorted(competence)))
    print("receiver profile selected: false")
    print("exact teaching bits known: false")


if __name__ == "__main__":
    main()
