#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}:{label}: expected exactly one occurrence, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_after_once(path: Path, anchor: str, addition: str, label: str) -> None:
    replace_once(path, anchor, anchor + addition, label)


# README mirrors: current operational state, not the superseded all-N 5.11 candidate.
replace_once(
    ROOT / "README.md",
    "A post-Stage-5 **Core self-sufficiency workstream (5.10–5.20)** is now active under ADR-0018. It tests whether the unchanged NEX-1 v0.1 Core can express a complete implementation of its own portable wire, static, and dynamic semantics before the teaching experiment begins. Stage 6 remains **Planned**.",
    "A post-Stage-5 **Core self-sufficiency workstream (5.10–5.20)** is active under ADR-0018. It tests whether the unchanged NEX-1 v0.1 Core can express a complete implementation of its own portable wire, static, and dynamic semantics before the teaching experiment begins. Stages 5.10–5.12 are **Complete**; Stage 5.13 structural validation is the next **Planned** substage. Stage 6 remains **Planned** until the 5.20 gate permits activation.",
    "readme-current-status",
)
replace_once(
    ROOT / "README.md",
    "The first 5.11 candidate represents every frozen meta-object through NEX `N`, using numeric encodings for finite products, sequences, terms, types, schemes, and results. This deliberately tests the existing Core before considering recursive types or new primitives.",
    "The accepted Stage 5.11 operational representation uses finite functional carriers `FiniteBits = (N -> N) * N` and `FiniteNatTokens = (N -> N) * N`; recursive internal objects use canonical natural-token streams rather than recursively packed naturals. Stage 5.12 then accepted NEX-written full Term codec v0.3 on its frozen bounded surfaces without changing the Core, wire, carriers, or resource budgets.",
    "readme-accepted-representation",
)
replace_once(
    ROOT / "README.ru.md",
    "Сейчас активен **post-Stage-5 цикл проверки самодостаточности Core (5.10–5.20)** по ADR-0018. Он проверяет, способен ли неизменённый NEX-1 v0.1 выразить полную реализацию собственной переносимой бинарной, статической и динамической семантики до начала эксперимента по обучению. Этап 6 остаётся **запланированным**.",
    "Сейчас активен **post-Stage-5 цикл проверки самодостаточности Core (5.10–5.20)** по ADR-0018. Он проверяет, способен ли неизменённый NEX-1 v0.1 выразить полную реализацию собственной переносимой бинарной, статической и динамической семантики до начала эксперимента по обучению. Этапы 5.10–5.12 **завершены**; Stage 5.13 structural validation — следующий **запланированный** подэтап. Этап 6 остаётся **запланированным** до разрешающего решения gate 5.20.",
    "readme-ru-current-status",
)
replace_once(
    ROOT / "README.ru.md",
    "Первый кандидат 5.11 представляет все зафиксированные метаобъекты через `N`, используя числовые кодировки конечных произведений, последовательностей, термов, типов, схем и результатов. Это сознательно проверяет существующий Core до обсуждения рекурсивных типов или новых примитивов.",
    "Принятое operational representation Stage 5.11 использует конечные функциональные carriers `FiniteBits = (N -> N) * N` и `FiniteNatTokens = (N -> N) * N`; рекурсивные внутренние объекты представлены каноническими потоками натуральных tokens, а не одним рекурсивно упакованным натуральным. Затем Stage 5.12 принял NEX-written full Term codec v0.3 на замороженной bounded surface без изменения Core, wire, carriers или ресурсных бюджетов.",
    "readme-ru-accepted-representation",
)

# Architecture mirrors: ADR-0018 is part of the current logical architecture.
arch_note = "\n\n## Pre-Stage-6 Core self-sufficiency gate\n\nADR-0018 inserts the post-Stage-5 extension 5.10–5.20 before Stage 6 may become Active. This experimental layer tests self-implementation while preserving the normative NEX-1 v0.1 Core. The current boundary is: 5.10–5.12 Complete, 5.13 structural validation Planned, and Stage 6 Planned until the 5.20 decision gate. Accepted Stage 5.11/5.12 operational representations and codec programs are research/self-implementation artifacts, not new Core constructors, primitives, types, or wire rules.\n"
append_after_once(
    ROOT / "docs/ARCHITECTURE.md",
    "The canonical NEX-1 Core remains unchanged unless a later evidence-backed Core-version ADR explicitly changes it.",
    arch_note,
    "architecture-self-sufficiency-gate",
)
replace_once(
    ROOT / "docs/ARCHITECTURE.md",
    "Stage 6 introduces a research layer above the Core. It owns experimental artifacts for:",
    "Stage 6, if activated after the 5.20 gate, introduces a research layer above the Core. It owns experimental artifacts for:",
    "architecture-stage6-status",
)
arch_ru_note = "\n\n## Ворота самодостаточности Core перед Stage 6\n\nADR-0018 вставляет post-Stage-5 расширение 5.10–5.20 до возможной активации Stage 6. Этот экспериментальный слой проверяет self-implementation, сохраняя нормативный NEX-1 v0.1 Core неизменным. Текущая граница: 5.10–5.12 Complete, Stage 5.13 structural validation Planned, Stage 6 остаётся Planned до решения gate 5.20. Принятые operational representation и codec-программы Stage 5.11/5.12 являются исследовательскими/self-implementation артефактами, а не новыми конструкторами, примитивами, типами или правилами wire Core.\n"
append_after_once(
    ROOT / "docs/ARCHITECTURE.ru.md",
    "NEX-1 Core остаётся неизменным, пока отдельный ADR о новой версии, подкреплённый экспериментальными данными, явно не изменит его.",
    arch_ru_note,
    "architecture-ru-self-sufficiency-gate",
)
replace_once(
    ROOT / "docs/ARCHITECTURE.ru.md",
    "Этап 6 вводит исследовательский слой над Core. Он отвечает за экспериментальные артефакты:",
    "Stage 6, если gate 5.20 разрешит его активацию, вводит исследовательский слой над Core. Он отвечает за экспериментальные артефакты:",
    "architecture-ru-stage6-status",
)

# Stage 6 is planning-only until ADR-0018 5.20 permits activation.
replace_once(
    ROOT / "docs/STAGE-6.md",
    "**Status:** Planned / protocol checkpoint  \n**Date:** 2026-09-19  \n**Prerequisite:** Stages 0–5 complete; post-Stage-5 re-audit merged  \n**Decision:** ADR-0017",
    "**Status:** Planned; blocked by the ADR-0018 Stage 5.20 gate  \n**Date:** 2026-09-19  \n**Prerequisite:** Stage 5.20 outcome explicitly permits Stage 6 activation; Stages 5.11 and 5.12 are Complete, Stage 5.13 is the next Planned self-sufficiency substage  \n**Decisions:** ADR-0017 teaching/Core separation; ADR-0018 pre-Stage-6 self-sufficiency gate",
    "stage6-prerequisite",
)
replace_once(
    ROOT / "docs/STAGE-6.md",
    "Stage 6 keeps NEX-1 v0.1 stable. It investigates a separate teaching layer above the Core rather than changing the Core merely for pedagogical convenience.",
    "Stage 6 keeps NEX-1 v0.1 stable. It investigates a separate teaching layer above the Core rather than changing the Core merely for pedagogical convenience. ADR-0018 delays execution of this plan until the 5.10–5.20 self-sufficiency extension reaches its decision gate; completion of 5.11 and 5.12 does not by itself activate Stage 6.",
    "stage6-adr0018-note",
)

# Historical audit: preserve original recommendation, explicitly annotate later sequencing decision.
audit_note = "\n**Subsequent sequencing note (2026-09-19):** this audit predates ADR-0018. Its recommendation to proceed directly toward Stage 6 teaching was later superseded **only in sequencing** by the mandatory post-Stage-5 self-sufficiency extension 5.10–5.20. The audit's Stage 0–5 findings remain historical evidence. Current continuation is defined by `docs/STATUS.md`; Stage 5.11 and 5.12 are Complete, Stage 5.13 is Planned next, and Stage 6 remains Planned until the 5.20 gate.  \n"
append_after_once(
    ROOT / "docs/RESEARCH-AUDIT-2026-09-19.md",
    "**Decision record:** ADR-0016.",
    audit_note,
    "audit-sequencing-note",
)
audit_ru_note = "\n**Последующее решение о порядке работ (19.09.2026):** этот аудит предшествует ADR-0018. Его рекомендация непосредственно переходить к исследованию Stage 6 позже была superseded **только в части последовательности** обязательным post-Stage-5 расширением самодостаточности 5.10–5.20. Выводы аудита по этапам 0–5 сохраняются как исторические evidence. Текущая точка продолжения определяется `docs/STATUS.md`: Stage 5.11 и 5.12 Complete, Stage 5.13 Planned следующим, Stage 6 остаётся Planned до gate 5.20.  \n"
append_after_once(
    ROOT / "docs/RESEARCH-AUDIT-2026-09-19.ru.md",
    "**Решение:** ADR-0016.",
    audit_ru_note,
    "audit-ru-sequencing-note",
)

# Historical Stage 5 handoff remains intact, with later ADR-0018 noted.
append_after_once(
    ROOT / "docs/STAGE-5.md",
    "## Handoff to Stage 6",
    "\n\n> **Subsequent sequencing note:** this handoff records the conclusion of historical Stage 5. ADR-0018 was accepted later and inserted the separate 5.10–5.20 Core self-sufficiency extension before Stage 6 activation, without reopening Stage 5. Current continuation is in `docs/STATUS.md`; 5.11 and 5.12 are Complete and 5.13 is Planned next.",
    "stage5-handoff-note",
)

# ADR-0017 remains accepted; ADR-0018 changes activation timing, not the teaching/Core separation decision.
append_after_once(
    ROOT / "docs/adr/0017-separate-teaching-protocol-from-core.md",
    "**Date:** 2026-09-19",
    "\n\n**Follow-up sequencing decision:** ADR-0018 was accepted later on the same date and inserts the mandatory 5.10–5.20 Core self-sufficiency gate before Stage 6 may become Active. ADR-0017 remains Accepted: its teaching/Core separation is unchanged; only activation timing is controlled by ADR-0018. Current continuation: 5.11 and 5.12 Complete, 5.13 Planned.",
    "adr0017-followup",
)

# Stage 5.12 closeout is no longer contingent: the final trigger-only regression succeeded.
replace_once(
    ROOT / "docs/STAGE-5.12-CLOSEOUT.md",
    "**Status:** Complete, contingent only on the final trigger-only regression associated with the Stage 5.12 closeout head  ",
    "**Status:** Complete  ",
    "closeout-status",
)
replace_once(
    ROOT / "docs/STAGE-5.12-CLOSEOUT.md",
    "- [ ] final Stage 5.12 historical regression is green on the closeout head.",
    "- [x] final Stage 5.12 historical regression is green on the closeout evidence head.",
    "closeout-final-checkbox",
)
replace_once(
    ROOT / "docs/STAGE-5.12-CLOSEOUT.md",
    "The final unchecked item is deliberately satisfied by a **last trigger-only commit** changing `stage5/selfhost/checkpoint-trigger.txt`. That commit does not alter candidate code, contracts, workloads, results, or documentation. If that historical regression is green, this document's `Status: Complete` condition is satisfied without any post-regression branch mutation.",
    "The final trigger-only historical regression completed successfully on the Stage 5.12 closeout evidence head:\n\n```text\nhead      4977e87feb53a04c98f9f60feed9c4847524c788\nworkflow  35442303266\njob       105895125195\nresult    success\n```\n\nIt reproduced/validated Stage 5.12a–f, immutable v0.1/v0.2 negative evidence, frozen v0.3 identity/development/exhaustive evidence, the accepted one-shot holdout result without rerunning the holdout, independent Python, and Go/frozen Stage 4 evidence. Subsequent documentation-only reconciliation does not alter candidate code, contracts, workloads, result artifacts, or the evidence head recorded above.",
    "closeout-final-result",
)
replace_once(
    ROOT / "docs/STAGE-5.12-CLOSEOUT.md",
    "Once the final checkpoint is green:",
    "After the successful final checkpoint:",
    "closeout-boundary-wording",
)

# Historical full-codec v0.1 note: preserve its pre-execution body but prevent it from looking current.
replace_once(
    ROOT / "docs/experiments/stage5-selfhost-full-codec.md",
    "**Status:** candidate v0.1 frozen; first development execution in progress  ",
    "**Status:** Historical v0.1 record; candidate later rejected on its one-shot preregistered holdout  ",
    "full-codec-v01-status",
)
append_after_once(
    ROOT / "docs/experiments/stage5-selfhost-full-codec.md",
    "**Prerequisite:** Stage 5.11 Complete (`meta-representation-v0.3`)  ",
    "\n**Subsequent status:** v0.1 was rejected on holdout; v0.2 was rejected on frozen development; v0.3 was accepted and Stage 5.12 is Complete. The body below preserves the v0.1 freeze-time design and planned gate for provenance. Current completion evidence is in `docs/experiments/stage5-selfhost-full-codec-v0.3.md` and `docs/STAGE-5.12-CLOSEOUT.md`.  ",
    "full-codec-v01-subsequent-status",
)
replace_once(
    ROOT / "docs/experiments/stage5-selfhost-full-codec.md",
    "## Remaining gate",
    "## Historical remaining gate at v0.1 freeze time",
    "full-codec-v01-gate-heading",
)

# Accepted v0.3 evidence should include the final closeout regression.
append_after_once(
    ROOT / "docs/experiments/stage5-selfhost-full-codec-v0.3.md",
    "## Stage boundary",
    "\n\n## Final closeout regression\n\nAfter the one-shot holdout was frozen as immutable evidence and documentation/diff review was completed, the final trigger-only historical regression succeeded:\n\n```text\nhead      4977e87feb53a04c98f9f60feed9c4847524c788\nworkflow  35442303266\njob       105895125195\nresult    success\n```\n\nThe run reproduced/validated historical Stage 5.12a–f, immutable full-codec v0.1/v0.2 negative evidence, frozen v0.3 identity/development/exhaustive evidence, the accepted holdout result without rerunning the one-shot holdout, independent Python, and Go/frozen Stage 4 evidence.\n",
    "full-codec-v03-final-regression",
)

# Historical checkpoints: add current continuation notes without rewriting the point-in-time conclusions.
append_after_once(
    ROOT / "docs/experiments/stage5-selfhost-5.11-completion-audit.md",
    "Stage 5.13 remains Planned and blocked until Stage 5.12 is Complete.",
    "\n\n## Subsequent status\n\nThe sequencing condition recorded above was later satisfied: Stage 5.12 is now Complete with accepted full-codec v0.3, and Stage 5.13 is Planned as the next sequential substage. This note does not rewrite the audit's point-in-time reasoning.",
    "511-audit-subsequent-status",
)
append_after_once(
    ROOT / "docs/experiments/stage5-selfhost-stream-parser.md",
    "The next research step must not silently broaden this result into a complete decoder. Before further implementation, the project should explicitly choose and preregister the representation/interface required to carry structural information from the wire traversal into Stage 5.13 structural validation while preserving the anti-tuning and versioning rules established in 5.12e–f.",
    "\n\n## Subsequent status\n\nThis remains the historical Stage 5.12f parser checkpoint. The later operational meta-representation v0.3 and accepted full-codec v0.3 completed Stage 5.12 under the same anti-tuning discipline. The current next substage is Stage 5.13 structural validation; the parser checkpoint itself is not reinterpreted as proof of that later stage.",
    "stream-parser-subsequent-status",
)

# Living testing strategy: bounded exhaustive testing is no longer only future work.
replace_once(
    ROOT / "docs/TESTING.md",
    "The post-Stage-5 literature audit makes this a high-priority future layer.",
    "This is now an established evidence layer as well as a future workstream: Stage 5.12 used a precisely complete frozen 27-Term class for the full codec. Broader scope/static/evaluation classes and stronger function-application contexts remain future work.",
    "testing-bounded-exhaustive-status",
)

# Cross-document consistency audit.
required = {
    "docs/STATUS.md": ["5.12 self wire codec                   Complete; full codec v0.3 accepted", "5.13 self structural validation        Planned; predecessor complete"],
    "docs/STAGE-5-EXTENSION.md": ["## 5.12 — self wire codec", "**Stage 5.12 result: Complete.**", "**Status:** Planned; Stage 5.12 predecessor complete."],
    "docs/STAGE-5.12-CLOSEOUT.md": ["**Status:** Complete", "workflow  35442303266", "job       105895125195"],
    "docs/RESEARCH-DISSERTATION.md": ["Stage 5.12 is now Complete", "Stage 5.13 structural validation is now the next Planned sequential substage"],
    "docs/RESEARCH-DISSERTATION.ru.md": ["Stage 5.12 теперь Complete", "Stage 5.13 structural validation теперь является следующим Planned последовательным подэтапом"],
    "docs/STAGE-6.md": ["blocked by the ADR-0018 Stage 5.20 gate"],
    "docs/ARCHITECTURE.md": ["## Pre-Stage-6 Core self-sufficiency gate"],
    "docs/ARCHITECTURE.ru.md": ["## Ворота самодостаточности Core перед Stage 6"],
    "docs/experiments/stage5-selfhost-full-codec-v0.3.md": ["workflow  35442303266", "result    success"],
}
for rel, needles in required.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"{rel}: missing required current marker: {needle!r}")

historical_markers = {
    "docs/RESEARCH-AUDIT-2026-09-19.md": "Subsequent sequencing note",
    "docs/RESEARCH-AUDIT-2026-09-19.ru.md": "Последующее решение о порядке работ",
    "docs/STAGE-5.md": "Subsequent sequencing note",
    "docs/adr/0017-separate-teaching-protocol-from-core.md": "Follow-up sequencing decision",
    "docs/experiments/stage5-selfhost-full-codec.md": "Subsequent status",
    "docs/experiments/stage5-selfhost-5.11-completion-audit.md": "## Subsequent status",
    "docs/experiments/stage5-selfhost-stream-parser.md": "## Subsequent status",
}
for rel, marker in historical_markers.items():
    if marker not in (ROOT / rel).read_text(encoding="utf-8"):
        raise SystemExit(f"{rel}: historical/current-status marker missing")

# Stale phrases are errors in living docs; in explicitly historical files they require the marker above.
stale_patterns = [
    "The first 5.11 candidate represents every frozen meta-object",
    "Первый кандидат 5.11 представляет все зафиксированные метаобъекты",
    "Stage 5.12 remains Active",
    "Stage 5.12 is still Active",
    "Stage 5.12 remains active",
    "Stage 5.13 remains Planned and blocked until Stage 5.12",
    "Stage 5.13 remains blocked until Stage 5.12",
    "candidate v0.1 frozen; first development execution in progress",
]
known_historical = set(historical_markers)
paths = [ROOT / "README.md", ROOT / "README.ru.md"] + sorted((ROOT / "docs").rglob("*.md"))
for path in paths:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    hits = [p for p in stale_patterns if p in text]
    if hits and rel not in known_historical:
        raise SystemExit(f"{rel}: stale current-state phrase(s): {hits}")
    if hits and rel in known_historical and historical_markers[rel] not in text:
        raise SystemExit(f"{rel}: stale phrase without historical supersession marker")

print("documentation Stage 5.12 consistency audit: passed")
print("living current state: 5.11 Complete -> 5.12 Complete -> 5.13 Planned")
print("historical documents retain point-in-time text with explicit subsequent-status markers")
