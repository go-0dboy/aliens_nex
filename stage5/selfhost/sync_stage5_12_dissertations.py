#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one occurrence, found {count}")
    return text.replace(old, new, 1)


def patch(path: Path, replacements: list[tuple[str, str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    for label, old, new in replacements:
        text = replace_once(text, old, new, f"{path.name}:{label}")
    path.write_text(text, encoding="utf-8")


EN = ROOT / "docs" / "RESEARCH-DISSERTATION.md"
RU = ROOT / "docs" / "RESEARCH-DISSERTATION.ru.md"

patch(EN, [
    (
        "horizon",
        "**Evidence horizon:** Stages 0–5 complete; post-Stage-5 literature re-audit incorporated; Stage 5.11 operational meta-representation complete; pre-Stage-6 Core self-sufficiency work active through the accepted Stage 5.12f bounded stream-parser checkpoint as of 2026-09-19  ",
        "**Evidence horizon:** Stages 0–5 complete; post-Stage-5 literature re-audit incorporated; Stage 5.11 operational meta-representation complete; Stage 5.12 self wire codec complete with accepted full-codec v0.3 after frozen development, a complete bounded 27-Term class, a green pre-holdout historical checkpoint, and a one-shot preregistered hold-out; Stage 5.13 planned as the next sequential substage as of 2026-09-19  ",
    ),
    (
        "abstract-current-state",
        "The immediate research question remains Core self-sufficiency, not yet the teaching curriculum. Stage 5.12 is still Active and must complete the full NEX-written `decodeTerm`/`encodeTerm` contract before Stage 5.13 begins. Stage 6 remains planned and becomes active only after the 5.10–5.20 decision gate has enough evidence to classify the unchanged Core.",
        "Stage 5.12 is now Complete. Two full-codec predecessors remain negative evidence: v0.1 passed development and the bounded exhaustive class but failed its one-shot preregistered hold-out at `law2:deepmixed:stream`, while v0.2 failed frozen development on the same historical case; both reached `5,000,001 > 5,000,000` Python call-by-need transitions. The preregistered v0.3 successor retained the same Core, wire, carriers, and budgets but constructs compositional functional fragments once during recursive traversal instead of exposing a random-access decoded view that reparses the source across distinct index queries. It passed 120/120 development sharing observations, all 27 terms in the frozen complete small-term class with 108/108 NEX law observations, a green pre-holdout historical checkpoint, and a one-shot unseen hold-out with 34/34 Python/Go sharing matches and zero sharing refusals. The heaviest unseen law used 487,579 Python and 212,893 Go need transitions; 30 Go normative-CBN hold-out refusals remain explicitly recorded as operational-cost evidence.\n\nThe immediate research question remains Core self-sufficiency, not yet the teaching curriculum. Stage 5.13 structural validation is now the next Planned sequential substage, but no Stage 5.13 implementation is part of the Stage 5.12 closeout. Stage 6 remains planned and becomes active only after the 5.10–5.20 decision gate has enough evidence to classify the unchanged Core.",
    ),
    (
        "methodology-sequencing",
        "A later sequencing audit established an additional project rule: numbered self-sufficiency substages are not skipped. Stage 5.11 was therefore formally reopened for audit and closed only after operational representation v0.3 reconciled the successful functional-stream route with the original representation obligations. Stage 5.12 remains active until its complete codec contract is satisfied; Stage 5.13 is not implementation-active before that point.",
        "A later sequencing audit established an additional project rule: numbered self-sufficiency substages are not skipped. Stage 5.11 was therefore formally reopened for audit and closed only after operational representation v0.3 reconciled the successful functional-stream route with the original representation obligations. Stage 5.12 then followed the same rule: full-codec v0.1 was rejected on its preregistered hold-out, v0.2 was rejected on frozen development, and v0.3 was preregistered before implementation with a fresh hold-out. Only after v0.3 passed frozen development, the complete 27-Term class, a green historical checkpoint, and the one-shot hold-out was Stage 5.12 marked Complete. Stage 5.13 is therefore the next Planned sequential substage, but it is not implementation-active in this closeout.",
    ),
    (
        "rq10",
        "**RQ10.** Partially supported. NEX-written arithmetic and integer-wire machinery are executable; a fixed-type finite-stream representation and NEX-written cursor/parser passed frozen development plus separately preregistered hold-outs; and Stage 5.11 now has a complete operational representation contract v0.3 for Bits, Term, Type, Scheme, Substitution, TypeEnvironment, observations, and result/request classes. Full NEX-written `decodeTerm`/`encodeTerm`, structural validation, HM inference, evaluator, integrated toolchain, and self-processing remain unconstructed.",
        "**RQ10.** Partially supported, with the wire-codec portion now established on bounded frozen surfaces. NEX-written arithmetic and integer-wire machinery are executable; a fixed-type finite-stream representation and NEX-written cursor/parser passed frozen development plus separately preregistered hold-outs; Stage 5.11 has a complete operational representation contract v0.3; and Stage 5.12 now has an accepted NEX-written full `decodeTerm`/`encodeTerm` codec v0.3 that passed 120/120 development sharing observations, a complete frozen 27-Term class, a green historical pre-holdout checkpoint, and a one-shot preregistered 34/34 unseen hold-out without Core, wire, carrier, or budget changes. Structural validation, HM inference, evaluator, integrated toolchain, self-processing, and the 5.20 classification remain unconstructed/open.",
    ),
    (
        "threat-parser",
        "- The parser hold-out validates cursor-based structural traversal, not the complete Stage 5.12 codec or static checker.",
        "- The parser hold-out validates cursor-based structural traversal; complete Stage 5.12 codec evidence now exists separately and remains bounded rather than a global proof.\n- The accepted full-codec v0.3 hold-out reduces tuning risk but remains bounded empirical evidence; Go normative CBN resource refusals remain material operational-cost evidence even where both sharing controls complete.",
    ),
    (
        "contribution19",
        "18. a completed Stage 5.11 operational meta-representation v0.3 that replaces impractical recursive numeric packing for active work with finite functional bit/token streams while preserving v0.1/v0.2 historical evidence.",
        "18. a completed Stage 5.11 operational meta-representation v0.3 that replaces impractical recursive numeric packing for active work with finite functional bit/token streams while preserving v0.1/v0.2 historical evidence;\n19. an accepted NEX-written full Term wire codec v0.3, reached after preserving v0.1/v0.2 failures, and validated by frozen development, a complete 27-Term class, a green historical pre-holdout checkpoint, and a one-shot preregistered unseen hold-out under unchanged budgets and unchanged NEX-1 v0.1.",
    ),
    (
        "research-order",
        "```text\n5.11 Complete\n        -> complete 5.12 self wire codec\n        -> then 5.13–5.20 Core self-sufficiency evidence\n        -> classify NEX-1 v0.1 at the 5.20 gate\n        -> if the target remains supportable, activate Stage 6 teaching/bootstrap work\n```",
        "```text\n5.11 Complete\n        -> 5.12 Complete\n        -> next: 5.13 structural validation\n        -> then 5.14–5.20 Core self-sufficiency evidence\n        -> classify NEX-1 v0.1 at the 5.20 gate\n        -> if the target remains supportable, activate Stage 6 teaching/bootstrap work\n```",
    ),
    (
        "next-question",
        "The immediate next technical question is **not** Stage 5.13. It is Stage 5.12 Gate 1: freeze the exact full-codec interface/result contract against accepted v0.3 `Bits` and `Term`, preregister full-codec development/hold-out workloads, and only then implement NEX `decodeTerm`/`encodeTerm` and their round-trip/canonicalization laws.",
        "The immediate next technical question is Stage 5.13 structural validation: de Bruijn scope validity, Core primitive-ID validity, closed-program validity, and the required structural rejection classes over the accepted v0.3 Term representation. This is the next Planned substage only; no Stage 5.13 implementation is included in the Stage 5.12 closeout.",
    ),
    (
        "conclusion-last",
        "The immediate research task is therefore to finish Stage 5.12 completely: freeze its full codec contract and workloads, construct NEX-written `decodeTerm` and `encodeTerm` over v0.3, verify both required round-trip/canonicalization laws, strengthen the evidence with a bounded complete small-term class and differential controls, and only then open Stage 5.13. After 5.20, if the unchanged Core remains supportable, Stage 6 can construct the finite transmitted teaching artifact. Once a complete teaching/bootstrap artifact exists, its exact bit length can replace speculative bootstrap proxies.",
        "Stage 5.12 is therefore complete on its declared bounded evidence surface. Its accepted v0.3 codec demonstrates that the unchanged Core can transform canonical wire into the accepted internal Term representation and reconstruct canonical wire from that representation under the frozen experimental discipline; the preserved CBN refusals also show that operational cost remains a serious constraint. The immediate next research task is Stage 5.13 structural validation, followed sequentially by self HM inference, evaluation, integration, self-processing, broader validation, metatheory, and the 5.20 classification. After 5.20, if the unchanged Core remains supportable, Stage 6 can construct the finite transmitted teaching artifact. Once a complete teaching/bootstrap artifact exists, its exact bit length can replace speculative bootstrap proxies.",
    ),
])

patch(RU, [
    (
        "horizon",
        "**Граница учтённых результатов:** этапы 0–5 завершены; повторный аудит литературы учтён; Stage 5.11 operational meta-representation завершён; pre-Stage-6 проверка самодостаточности Core активна и учтена до принятого bounded checkpoint Stage 5.12f stream-parser по состоянию на 19.09.2026  ",
        "**Граница учтённых результатов:** этапы 0–5 завершены; повторный аудит литературы учтён; Stage 5.11 operational meta-representation завершён; Stage 5.12 self wire codec завершён принятием full-codec v0.3 после frozen development, полного bounded класса из 27 Term, зелёного pre-holdout historical checkpoint и одноразового preregistered hold-out; Stage 5.13 запланирован как следующий последовательный подэтап по состоянию на 19.09.2026  ",
    ),
    (
        "abstract-current-state",
        "Непосредственный исследовательский вопрос по-прежнему — самодостаточность Core, а не curriculum. Stage 5.12 остаётся Active и должен полностью закрыть NEX-written `decodeTerm`/`encodeTerm` до начала Stage 5.13. Stage 6 остаётся Planned и может стать Active только после достаточного результата gate 5.10–5.20.",
        "Stage 5.12 теперь Complete. Два предшествующих full-codec кандидата сохранены как отрицательные свидетельства: v0.1 прошёл development и bounded exhaustive class, но провалил одноразовый preregistered hold-out на `law2:deepmixed:stream`; v0.2 был отклонён уже на frozen development на том же историческом случае; оба дошли до `5 000 001 > 5 000 000` переходов Python call-by-need. Preregistered-преемник v0.3 сохранил тот же Core, wire, carriers и budgets, но один раз строит композиционные functional fragments при рекурсивном проходе вместо random-access decoded view, повторно разбирающего источник для разных индексов. Он прошёл 120/120 development sharing-наблюдений, все 27 термов полного frozen small-term class с 108/108 NEX law observations, зелёный pre-holdout historical checkpoint и одноразовый unseen hold-out с 34/34 совпадениями Python/Go sharing и нулём sharing-refusals. Самый тяжёлый unseen law потребовал 487 579 переходов Python need и 212 893 Go need; 30 отказов нормативного Go CBN на hold-out сохранены как явное свидетельство операционной стоимости.\n\nНепосредственный исследовательский вопрос по-прежнему — самодостаточность Core, а не curriculum. Stage 5.13 structural validation теперь является следующим Planned последовательным подэтапом, но никакая реализация Stage 5.13 не входит в closeout Stage 5.12. Stage 6 остаётся Planned и может стать Active только после достаточного результата gate 5.10–5.20.",
    ),
    (
        "methodology-sequencing",
        "Позднейший аудит порядка работ добавил ещё одно правило: нумерованные подэтапы self-sufficiency не перескакиваются. Поэтому Stage 5.11 был формально повторно проверен и закрыт только после того, как operational representation v0.3 согласовал успешную функционально-потоковую ветку с исходными обязательствами representation stage. Stage 5.12 остаётся Active до полного выполнения codec-контракта; Stage 5.13 до этого не является implementation-active.",
        "Позднейший аудит порядка работ добавил ещё одно правило: нумерованные подэтапы self-sufficiency не перескакиваются. Поэтому Stage 5.11 был формально повторно проверен и закрыт только после того, как operational representation v0.3 согласовал успешную функционально-потоковую ветку с исходными обязательствами representation stage. Stage 5.12 затем прошёл ту же дисциплину: full-codec v0.1 был отклонён на preregistered hold-out, v0.2 — на frozen development, а v0.3 был preregistered до реализации с новым hold-out. Только после прохождения v0.3 frozen development, полного 27-Term class, зелёного historical checkpoint и одноразового hold-out Stage 5.12 был отмечен Complete. Поэтому Stage 5.13 является следующим Planned последовательным подэтапом, но не становится implementation-active в рамках этого closeout.",
    ),
    (
        "rq10",
        "**RQ10.** Частично поддержан. NEX-written арифметика и integer-wire machinery исполняются; fixed-type finite-stream representation и NEX-written cursor/parser прошли замороженные development workload и отдельно preregistered hold-out; Stage 5.11 теперь имеет завершённый operational representation contract v0.3 для Bits, Term, Type, Scheme, Substitution, TypeEnvironment, observations и классов request/result. Полные NEX-written `decodeTerm`/`encodeTerm`, structural validation, HM inference, evaluator, integrated toolchain и self-processing ещё не построены.",
        "**RQ10.** Частично поддержан, причём wire-codec часть теперь установлена на bounded frozen surfaces. NEX-written арифметика и integer-wire machinery исполняются; fixed-type finite-stream representation и NEX-written cursor/parser прошли frozen development и отдельно preregistered hold-outs; Stage 5.11 имеет завершённый operational representation contract v0.3; Stage 5.12 теперь имеет принятый NEX-written full `decodeTerm`/`encodeTerm` codec v0.3, прошедший 120/120 development sharing-наблюдений, полный frozen 27-Term class, зелёный historical pre-holdout checkpoint и одноразовый preregistered unseen hold-out 34/34 без изменений Core, wire, carrier или budgets. Structural validation, HM inference, evaluator, integrated toolchain, self-processing и классификация 5.20 остаются не построенными/открытыми.",
    ),
    (
        "threat-parser",
        "- Parser hold-out проверяет cursor-based structural traversal, а не полный Stage 5.12 codec или static checker.",
        "- Parser hold-out проверяет cursor-based structural traversal; отдельные evidence полного Stage 5.12 codec теперь существуют, но остаются bounded, а не глобальным доказательством.\n- Принятый hold-out full-codec v0.3 уменьшает риск подгонки, но остаётся bounded empirical evidence; ресурсные отказы нормативного Go CBN остаются существенным свидетельством операционной стоимости даже там, где обе sharing-реализации завершаются.",
    ),
    (
        "contribution19",
        "18. завершённый Stage 5.11 operational meta-representation v0.3, который для активной работы заменяет непрактичный recursive numeric packing на конечные functional bit/token streams, сохраняя v0.1/v0.2 как исторические evidence.",
        "18. завершённый Stage 5.11 operational meta-representation v0.3, который для активной работы заменяет непрактичный recursive numeric packing на конечные functional bit/token streams, сохраняя v0.1/v0.2 как исторические evidence;\n19. принятый NEX-written full Term wire codec v0.3, полученный с сохранением провалов v0.1/v0.2 и проверенный frozen development, полным 27-Term class, зелёным historical pre-holdout checkpoint и одноразовым preregistered unseen hold-out при неизменных budgets и неизменённом NEX-1 v0.1.",
    ),
    (
        "research-order",
        "```text\n5.11 Complete\n        -> полностью закрыть 5.12 self wire codec\n        -> только затем 5.13–5.20 Core self-sufficiency evidence\n        -> классифицировать NEX-1 v0.1 в gate 5.20\n        -> если цель остаётся поддерживаемой, активировать Stage 6 teaching/bootstrap\n```",
        "```text\n5.11 Complete\n        -> 5.12 Complete\n        -> далее 5.13 structural validation\n        -> затем 5.14–5.20 Core self-sufficiency evidence\n        -> классифицировать NEX-1 v0.1 в gate 5.20\n        -> если цель остаётся поддерживаемой, активировать Stage 6 teaching/bootstrap\n```",
    ),
    (
        "next-question",
        "Непосредственный следующий технический вопрос — **не** Stage 5.13. Это Gate 1 Stage 5.12: заморозить точный full-codec interface/result contract для принятых v0.3 `Bits` и `Term`, preregister full-codec development/hold-out workloads и только затем реализовывать NEX `decodeTerm`/`encodeTerm` и проверять round-trip/canonicalization laws.",
        "Непосредственный следующий технический вопрос — Stage 5.13 structural validation: корректность de Bruijn scope, допустимость Core primitive-ID, closed-program validity и необходимые structural rejection classes поверх принятого v0.3 Term representation. Это только следующий Planned подэтап; никакая реализация Stage 5.13 не входит в closeout Stage 5.12.",
    ),
    (
        "conclusion-last",
        "Поэтому непосредственная исследовательская задача — **полностью завершить Stage 5.12**: зафиксировать full-codec contract и workloads, построить NEX-written `decodeTerm` и `encodeTerm` поверх v0.3, проверить обе обязательные round-trip/canonicalization laws, усилить evidence bounded complete small-term class и differential controls и только затем открывать Stage 5.13. После 5.20, если неизменённый Core остаётся поддерживаемым, Stage 6 сможет перейти к конечному передаваемому teaching artifact. Когда полный teaching/bootstrap artifact появится, его точная битовая длина сможет заменить косвенные оценки bootstrap cost.",
        "Stage 5.12 тем самым завершён на объявленной bounded evidence surface. Принятый codec v0.3 показывает, что неизменённый Core способен преобразовывать canonical wire в принятое внутреннее Term representation и восстанавливать canonical wire из этого представления при frozen experimental discipline; сохранённые CBN refusals одновременно показывают, что операционная стоимость остаётся серьёзным ограничением. Непосредственная следующая исследовательская задача — Stage 5.13 structural validation, затем последовательно self HM inference, evaluation, integration, self-processing, более широкая validation, metatheory и классификация 5.20. После 5.20, если неизменённый Core остаётся поддерживаемым, Stage 6 сможет перейти к конечному передаваемому teaching artifact. Когда полный teaching/bootstrap artifact появится, его точная битовая длина сможет заменить косвенные оценки bootstrap cost.",
    ),
])

print("Stage 5.12 dissertation sync patch applied successfully")
