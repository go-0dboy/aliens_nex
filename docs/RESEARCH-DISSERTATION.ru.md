# NEX-1: минимальное архитектурно-независимое типизированное ядро для информационно-эффективной передачи вычислений

## Проектирование, формализация, исполняемая семантика, эмпирическая оценка и протокол независимого восстановления

**Тип документа:** живая исследовательская рукопись в диссертационном стиле  
**Основной язык:** английский  
**Каноническая версия:** `RESEARCH-DISSERTATION.md`  
**Граница учтённых данных:** Stage 0–4 завершены; checkpoint Stage 5.0–5.1, 18.09.2026  
**Проект:** NEX / `aliens_nex`

> Эта рукопись является научным синтезом исследования, поддерживаемым непосредственно в репозитории. Она ещё не оформлена под требования конкретного университета, ВАК, национальной системы аттестации или библиографического стандарта. Нормативное определение языка остаётся в `docs/NEX-1-v0.1.md`, а архитектурные и исследовательско-методологические решения — в принятых ADR.

---

## Аннотация

В работе исследуется вопрос о том, может ли очень небольшое, архитектурно-независимое и статически типизированное вычислительное ядро уменьшить объём информации, необходимой для передачи исполняемого вычислительного знания между сторонами, которые не могут предполагать общий язык программирования, архитектуру процессора, ABI, операционную систему, текстовую нотацию или общую среду реализации. Объектом исследования является архитектурно-независимое представление и восстановление вычислений общего назначения в условиях крайне ограниченного канала передачи. Целевая функция определяется не только размером программ, а полной информационной стоимостью

```text
C = S + B + P
```

где `S` — информация, необходимая для задания вычислительной системы, `B` — receiver-neutral bootstrap-информация, необходимая получателю для её реализации, а `P` — объём передаваемых программ.

Экспериментальная система NEX-1 v0.1 использует шесть канонических конструкторов термов (`Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`), zero-based de Bruijn indices, rank-1 let-полиморфизм Hindley–Milner, прямые arbitrary-precision натуральные литералы, произведения и суммы через фиксированные примитивы, общую рекурсию через `fix`, самоделимитирующееся префиксное бинарное представление и weak call-by-name semantics. Теоретическая база включает безымянную lambda-нотацию de Bruijn [1], Binary Lambda Calculus как компактный бинарный baseline [2], вывод типов Hindley–Milner и principal type schemes [3,4], типизированную рекурсию в духе PCF/LCF [5], integer coding Elias [6] и классические различия между call-by-name и lazy sharing [9–11].

Stages 1–3 создали исполняемые wire-, static- и dynamic-semantics. Stage 4 заморозил measurement rules и benchmark corpora до оптимизации и выполнил воспроизводимые сравнения. На принятом корпусе v0.3 из 17 программ канонические NEX-термы занимают 1371 бит при 345 AST-узлах. Наибольший измеренный вклад дают ссылки на примитивы — 460 бит (33,6%), далее `Var` — 286 бит (20,9%), `App` — 264 бита (19,3%), `Nat` — 244 бита (17,8%), `Lam` — 84 бита (6,1%), `Let` — 33 бита (2,4%). Прямой `Nat(255)` использует 21 бит против 2300 бит у проверенной repeated-`succ` конструкции. `Let` демонстрирует измеримую точку окупаемости, а не является безусловно выгодным. Не-нормативный principal-root-type envelope добавляет 134 бита, или 9,77% program-payload overhead, не доказывая уменьшения bootstrap.

На одинаковом pure-lambda subset из трёх программ Binary Lambda Calculus оказался компактнее NEX: 30 против 37 бит. Следовательно, universal NEX program-size superiority не подтверждается. Проектный tiny postfix structural encoding использует 1529 бит на полном корпусе против 1371 у NEX, но переиспользует NEX integer/primitive conventions и не является независимым сравнением полной bootstrap-стоимости. Экспериментальный call-by-need evaluator сохраняет одинаковый observable WHNF на всех 17 программах и уменьшает Go-reference transitions с 226151 до 2484 в сумме (98,90%), главным образом на рекурсивных и повторно форсируемых вычислениях. Это evidence о реализации, а не о стоимости передачи.

Главный отрицательный результат сохраняется: полная информационная стоимость `C` пока численно неизвестна. `P` измеряется точно для выбранного корпуса, но Markdown size является только textual proxy для `S`, Go source — только host/reference proxy `R`, а реальный receiver-neutral bootstrap `B` неизвестен.

Stage 5 начинает проверку того, можно ли восстановить NEX независимо от Go reference. ADR-0013 фиксирует implementation-input boundary и выбирает Python 3.12 standard-library-only для первой независимой реконструкции. При этом «вторая реализация» не считается независимой только потому, что написана на другом языке: текущий co-development context уже знает устройство Go reference и поэтому является когнитивно загрязнённым. Сильное independent evidence требует свежего изолированного контекста или другого реализатора, который получает только frozen conformance packet и разрешённую первичную теорию. Аудит Stage 5.1 уже выявил два presentation-layer omission: канонический alpha-normalized text principal type schemes и явный JSON fixture mapping для шестиконструкторного AST. Оба оформлены как packet observation conventions без изменения NEX-1 v0.1 semantics.

Таким образом, основной вклад текущего этапа — не заявление о глобальной минимальности, а создание исполняемой, фальсифицируемой и потенциально независимо проверяемой исследовательской системы, в которой утверждения о компактности, воспроизводимости и полной информационной стоимости можно проверять, а не предполагать.

**Ключевые слова:** минимальный язык программирования, архитектурно-независимые вычисления, Binary Lambda Calculus, индексы de Bruijn, Hindley–Milner, кодирование программ, bootstrap, информационная стоимость, call-by-name, call-by-need, independent conformance, воспроизводимый benchmark.

---

# 1. Введение

## 1.1 Мотивация

Большинство языков программирования и форматов исполняемого кода предполагают общий контекст: кодировки символов, текстовый синтаксис, модель процессора, размер слова, object format, сервисы OS, соглашения компилятора или спецификацию VM. Для обычной земной разработки это естественно, но становится проблемой, если отправитель и получатель могут разделять только упорядоченный бинарный канал и базовые математические закономерности.

Мотивирующий мысленный эксперимент намеренно экстремален: как передать не просто данные, а повторно используемое вычислительное знание, если нельзя предполагать знание земного языка, CPU, ABI, OS или исходной нотации?

Минимизация длины программы недостаточна. Однобитная программа бесполезна, если для её понимания нужен огромный непереданный interpreter. И наоборот, сверхмалый interpreter может сделать все программы длиннее. Поэтому NEX исследует совместную функцию

```text
C = S + B + P
```

а не длину синтаксиса отдельно.

## 1.2 Научная проблема

Проблема состоит в определении того, может ли компактное типизированное функциональное ядро дать выгодный баланс полной информационной стоимости при передаче вычислений общего назначения без общей платформы реализации.

Связанные аспекты:

1. **компактность представления** — малые, однозначные, самоделитирующиеся бинарные программы;
2. **восстанавливаемость семантики** — scope, типы и смысл выполнения должны следовать из переданных правил;
3. **вычислительная выразительность** — общая рекурсия и композиционное построение данных;
4. **проверяемость** — детерминированное отклонение malformed и ill-typed программ;
5. **стоимость bootstrap** — экономия program bits не должна скрывать большой receiver implementation;
6. **эмпирическая фальсифицируемость** — compactness claims должны проверяться на frozen workloads и явных alternatives.

## 1.3 Объект и предмет

**Объект:** архитектурно-независимое представление и выполнение вычислений общего назначения в условиях крайне ограниченной передачи информации.

**Предмет:** компромиссы между размером specification, receiver bootstrap complexity, program payload, static verifiability, evaluation strategy и независимой воспроизводимостью минимального typed lambda-core.

## 1.4 Цель

Построить и эмпирически оценить минимальное исполняемое ядро, чья бинарная форма и семантика достаточно явны для независимого восстановления, а также разработать воспроизводимый метод проверки его полной communication cost относительно альтернатив.

## 1.5 Задачи

1. Определить минимальный architecture-neutral Core и его invariants.
2. Определить canonical self-delimiting wire format.
3. Реализовать executable encode/decode conformance.
4. Реализовать static scope/type semantics.
5. Реализовать dynamic semantics без скрытого machine behavior.
6. Создать language-neutral conformance artifacts.
7. Замораживать benchmark corpora до оптимизации.
8. Измерять constructor-level wire cost и design trade-offs.
9. Сравнивать selected baselines при явных assumptions.
10. Отделять точный program cost от specification/implementation/bootstrap proxies.
11. Проверить, может ли independent implementation восстановить то же поведение без доступа к Go source.
12. Явно определить receiver assumptions до назначения численного bootstrap cost.
13. Сохранять положительные, отрицательные, условные и нерешённые результаты в living research record.

## 1.6 Исследовательские вопросы

**RQ1.** Можно ли задать typed lambda-core детерминированное, architecture-neutral, self-delimiting binary representation с executable conformance?

**RQ2.** Можно ли восстанавливать static validity и principal types без ordinary term-level type annotations?

**RQ3.** Может ли semantics оставаться простой и non-strict, допуская существенно более эффективные реализации с теми же observables?

**RQ4.** Какие Core constructs доминируют в transmitted program cost и оправдывают ли себя `Let` и direct `Nat`?

**RQ5.** Как NEX program payload соотносится с selected alternatives в контролируемых сравнениях?

**RQ6.** Можно ли уже численно оценить `C = S + B + P`, а если нет — какие evidence отсутствуют?

**RQ7.** Определяют ли опубликованные specification и conformance packet поведение независимо от Go reference?

**RQ8.** При каких явных receiver assumptions можно определить measurable bootstrap `B | A`, не подменяя его host source size?

## 1.7 Рабочие гипотезы

**H1.** Nameless lambda representation с compact prefix encoding даёт малый и однозначный wire format.

**H2.** HM-style erased typing способен уменьшать `P`, но total benefit зависит от неизвестного bootstrap inference [3,4].

**H3.** Небольшое число дополнительных constructs, таких как direct naturals и `Let`, может уменьшать payload, даже увеличивая specification.

**H4.** Weak CBN способен служить простой normative semantics, а call-by-need sharing — observationally equivalent optimization [9–11].

**H5.** Нельзя заранее предполагать преимущество NEX над BLC на pure lambda terms [2].

**H6.** Program payload недостаточен для global superiority claim; нужны receiver-neutral `S` и `B`.

**H7.** Достаточно явные specification + language-neutral vectors должны позволить независимому реализатору восстановить те же portable observables без Go implementation guidance.

## 1.8 Научная новизна и значимость на текущей границе данных

Новизна не состоит в изобретении lambda calculus, de Bruijn indices, HM или lazy evaluation — это established foundations. Исследовательская новизна проекта заключается в объединении этих идей в явно information-accounted transmission experiment, где specification, bootstrap, program payload, conformance и implementation independence рассматриваются как единая фальсифицируемая система.

Практическая значимость текущего этапа включает executable conformance, reproducible measurements, frozen corpus discipline и protocol, способный выявлять hidden assumptions между co-developed specification и reference implementation.

---

# 2. Теоретическая база и связанные работы

## 2.1 de Bruijn indices

De Bruijn показал, что связанные переменные можно представлять числовыми ссылками вместо имён [1; SRC-0001]. NEX использует zero-based indices; alpha-renaming не несёт wire information.

## 2.2 Binary Lambda Calculus

BLC Тромпа демонстрирует компактное бинарное представление untyped lambda terms [2; SRC-0002] и служит внешним compactness baseline. NEX не копирует BLC: он добавляет static typing, `Let`, direct naturals и fixed primitives, поэтому Stage 4 сравнивает только identical pure-lambda subset.

## 2.3 Hindley–Milner

Milner задаёт decidable rank-1 polymorphic inference [3; SRC-0003], Damas–Milner — principal type schemes [4; SRC-0004]. NEX использует эти идеи для reconstruction типов. Результат Wells по System F [7; SRC-0007] напоминает, что более сильный implicit polymorphism нельзя автоматически считать сохраняющим decidability.

## 2.4 Typed recursion

Plotkin LCF/PCF даёт precedent малого typed functional language с naturals и fixed-point recursion [5; SRC-0005]. Точный primitive set и wire NEX являются проектными решениями.

## 2.5 Self-delimiting integers

Elias предложил universal integer codes [6; SRC-0006]. NEX определяет `U(n)` как gamma coding от `n + 1`.

## 2.6 Evaluation strategy

Plotkin формализовал различие CBN/CBV [9; SRC-0011]. Launchbury описал lazy semantics с sharing [10; SRC-0012], Sestoft — abstract-machine treatment [11; SRC-0013]. NEX использует weak CBN нормативно, а call-by-need изучает только как optimization.

## 2.7 Combinatory alternatives

Combinatory logic даёт альтернативные малые basis [8; SRC-0009]. Barker Iota/Jot задаёт Jot mapping, использованный в Stage 4 [12; SRC-0014]. Shortest-Jot claim не делается.

## 2.8 Portable core и embedding

WebAssembly Core служит примером отделения portable computational core от host embedding [13; SRC-0008], но NEX не заимствует его конкретную machine/memory/module model.

---

# 3. Методология исследования

## 3.1 Артефактно-экспериментальный цикл

```text
Problem
 -> Contract
 -> Invariant
 -> Failing test / executable example
 -> Implementation
 -> Verification
 -> Diff review
 -> Status checkpoint
 -> Research synthesis checkpoint
```

Долговременной памятью проекта является repository, а не chat history.

## 3.2 Классы evidence

Различаются:

1. established external result;
2. NEX design decision;
3. reproducible NEX measurement;
4. inference from current evidence;
5. open hypothesis / unknown.

## 3.3 Воспроизводимость

Используются wire/static/evaluation vectors, negative cases, unit/property/fuzz tests, frozen corpora, deterministic experiment CLIs и clean-checkout GitHub Actions.

## 3.4 Frozen-corpus rule

ADR-0010 делает corpus version immutable после публикации comparative results. Сохранённый v0.2 с `factorial-5`, превысившим default CBN budget, является примером сохранения неудобного результата.

## 3.5 Total-information accounting

```text
C = S + B + P
```

- `P` — exact canonical program bits;
- `S` — receiver-neutral specification cost, пока без accepted artifact;
- `B` — receiver-neutral bootstrap cost, неизвестен;
- `R` — host/reference proxy, который нельзя подменять под `B`.

## 3.6 Independence как экспериментальная переменная

Stage 5 вводит отдельное требование: independence implementation должна быть контролируемым условием.

Вторая реализация на новом host language не считается независимой, если implementer уже знает внутреннее устройство первой. ADR-0013 поэтому отделяет

```text
packet/protocol construction
        от
independent implementation evidence
```

Первая независимая реализация может использовать только frozen packet, selected primary theory и документацию Python 3.12 standard library. `reference/go/**` и implementation-revealing project material запрещены до freeze checkpoint.

Текущий co-development context уже участвовал в Go reference. Поэтому он может строить protocol, packet и neutral infrastructure, но не должен выдавать новую реализацию, написанную по памяти, за независимое evidence.

---

# 4. Дизайн NEX-1 v0.1

## 4.1 Terms

```text
Term ::= Var(index)
       | Lam(body)
       | App(function, argument)
       | Let(value, body)
       | Nat(value)
       | Prim(id)
```

## 4.2 Types

```text
T ::= a | 1 | N | T -> T | T * T | T + T
S ::= forall a1 ... an. T
```

Static semantics используют rank-1 HM-style inference с instantiation, generalization, unification и occurs check [3,4].

## 4.3 Core primitives

```text
0  fix
1  succ
2  pred
3  ifz
4  pair
5  fst
6  snd
7  inl
8  inr
9  case
10 unit
```

## 4.4 Wire

```text
00   U(k)   Var(k)
01   T      Lam(T)
10   T T    App(T,T)
110  T T    Let(T,T)
1110 U(n)   Nat(n)
1111 U(p)   Prim(p)
```

`U(n)` = Elias gamma от `n + 1`.

## 4.5 Dynamic semantics

Нормативная стратегия — weak CBN. Arguments и `Let` values delayed, reduction under `Lam` не производится до применения, primitive forcing selective, `fix` задаёт общую рекурсию.

---

# 5. Stage 0 — исследовательская и архитектурная база

Stage 0 ввёл canonical documentation, Russian mirrors, architecture/workflow/testing docs, ADR governance, repository-as-memory и primary-source registry.

**Вывод:** до оптимизации минимального языка необходим механизм, предотвращающий silent semantic drift и retrospective rationale rewriting.

---

# 6. Stage 1 — canonical wire foundation

Stage 1 реализовал arbitrary-precision `U(n)`, six-constructor term model, encode/decode, exact/prefix APIs, malformed errors и resource limits, отделённые от wire invalidity.

Wire corpus содержит 17 integer vectors, 12 term vectors и 15 invalid exact-input vectors.

```text
Var(0)                    001
Nat(0)                    11101
Prim(0)                   11111
Lam(Var(0))               01001
Lam(App(Prim(1),Var(0)))  01101111010001
```

**Вывод:** RQ1 поддерживается executable conformance, но formal proof и independent decoder пока отсутствуют.

---

# 7. Stage 2 — static validation и principal types

Реализованы closed de Bruijn scope, type representation, substitutions, unification + occurs check, primitive schemes, instantiation, generalization и Algorithm-W-style inference.

Ordinary type annotations erased из v0.1 wire. ADR-0007 фиксирует это как design choice, а не доказанный global optimum.

**Вывод:** RQ2 функционально поддерживается reference implementation, total comparison explicit/certified alternatives остаётся открыт.

---

# 8. Stage 3 — dynamic semantics и evaluator

Stage 3 реализовал weak CBN и проверял саму non-strictness:

```text
(lambda x. 7) divergingTerm
ifz 0 42 divergingTerm
fst (pair 1 divergingTerm)
```

должны давать `7`, `42`, `1`, не вычисляя irrelevant computation. Curried primitives, `fix`, WHNF и resource refusal покрыты language-neutral vectors.

**Вывод:** RQ3 поддерживается на normative-semantics уровне; sharing вынесен в empirical experiment.

---

# 9. Stage 4 — эмпирическая проверка и benchmarking

Stage 4 завершён PR #6, squash merge `ebffde6c8669f65dfcba98d31d261d59b48d4dd0`. Финальный PR head прошёл CI `35377200520`, post-merge `main` — `35377892126`.

## 9.1 Frozen corpus

```text
programs   17
wire bits  1371
AST nodes  345
```

## 9.2 Wire attribution

| Constructor | Bits | Share |
|---|---:|---:|
| `Prim` | 460 | 33,6% |
| `Var` | 286 | 20,9% |
| `App` | 264 | 19,3% |
| `Nat` | 244 | 17,8% |
| `Lam` | 84 | 6,1% |
| `Let` | 33 | 2,4% |

Ранняя гипотеза о доминировании `App` не подтверждена v0.3; largest measured category — `Prim`.

## 9.3 `Let`

Для 5-bit payload `Let` стоит +4 bits при 2 uses, +2 при 3, tie при 4, и экономит 8 при 8. Для tested 14-bit payload два uses уже экономят 5 bits.

**Решение:** сохранить `Let`.

## 9.4 Direct naturals

```text
Nat(255)          21 bits
succ-chain(255) 2300 bits
```

**Решение:** сохранить direct `Nat`; global numeric-code optimality не заявляется.

## 9.5 Root-type experiment

```text
erased term bits  1371
root type bits      134
hybrid total       1505
overhead           +9,77%
```

Это только `Delta P`; bootstrap saving не доказан.

**Решение:** сохранить erased HM в v0.1 до реального checker/bootstrap comparison.

## 9.6 Baselines

Pure-lambda subset:

```text
NEX  37 bits
BLC  30 bits
Jot via fixed SK translation  288 bits
```

Universal NEX-over-BLC claim запрещён.

Full v0.3:

```text
NEX canonical wire  1371 bits
tiny postfix stack  1529 bits
```

Tiny stack reuse NEX numeric/primitive assumptions, поэтому сравнение structural, а не total-bootstrap.

## 9.7 CBN vs call-by-need

Все 17 программ имеют одинаковый observable WHNF.

```text
CBN transitions             226151
call-by-need transitions      2484
reduction                    98,90%
memo hits                       237
programs improved              6/17
```

Например `factorial-4`: 209315 -> 895. Это host/reference evidence, не часть `C`.

**Решение:** weak CBN нормативен, call-by-need разрешён при observable equivalence.

## 9.8 Total information

```text
P exact                         1371 bits
spec Markdown proxy           23440 UTF-8 bytes
selected Go reference Core    43013 UTF-8 bytes
B                              unknown
C                              not numerically computable
```

**Вывод Stage 4:** локальные design decisions получили evidence, но global minimality и numerical total cost не подтверждены.

---

# 10. Stage 5 — независимое восстановление и receiver-neutral bootstrap

Stage 5 начат. Текущая граница evidence включает только Stage 5.0 и Stage 5.1; сама independent implementation намеренно не начата в co-development context.

## 10.1 Stage 5.0 — independence protocol

ADR-0013 фиксирует packet относительно commit:

```text
4f9c50aed13cdbdf72c9ce6510521477d49c05a5
```

Первый independent implementation target:

```text
Python 3.12+
standard library only
```

Python выбран из-за существенного отличия host model от Go и наличия arbitrary-precision integers без third-party dependency. Его source size не является `B`.

Packet allowlist включает canonical spec, wire/static/eval conformance и только ADR, необходимые для Core validity/resource semantics. До freeze checkpoint запрещены `reference/go/**`, Stage 4 experiment material, benchmark corpora, status/dissertation/history documents и ADR-0008, описывающий Go evaluator architecture.

Текущий co-development context уже знает Go reference, поэтому новая реализация здесь была бы портом, но не сильным independent evidence. Требуется fresh isolated context или другой implementer с доступом только к packet и allowlisted theory.

## 10.2 Reproducible packet

`stage5/conformance-packet-v0.1/manifest.json` хранит exact Git blob hashes frozen source files. `stage5/build_packet.py` проверяет их, валидирует schema IDs, materializes только allowlisted files и создаёт SHA-256 manifest.

Dedicated GitHub Actions run `35379868436` — success. Опубликован standalone artifact:

```text
name: nex1-independent-conformance-packet-v0.1
artifact id: 10560808823
archive size: 28199 bytes
artifact digest: sha256:fca1fddff742674c4e0b832ea53022d712f292d1361dfbe9b1b62c022ead15c3
```

Размер архива — engineering artifact size, не `S` и не `B`.

## 10.3 Stage 5.1 completeness audit

Audit не обнаружил известного отсутствующего Core semantic rule, блокирующего первый independent pass, но выявил два presentation-layer omission.

### F1 — principal type observation format

Principal schemes семантически определены с точностью до alpha-renaming, но static conformance хранит текст `T0`, `T1`, ... . Теперь packet задаёт canonical comparison rendering: quantified variables переименовываются по first occurrence, compound monotypes fully parenthesized.

**Классификация:** conformance observation-format omission, не Core typing ambiguity.

### F2 — JSON fixture mapping

Conformance использовал JSON `kind/value/a/b`, но JSON не является NEX wire syntax и mapping не был явно зафиксирован как fixture contract.

**Классификация:** test-fixture representation omission, не Core wire ambiguity.

F1/F2 оформлены в `stage5/conformance-packet-v0.1/OBSERVATIONS.md` без изменения NEX-1 v0.1 semantics.

### F3 — deliberately unspecified details

Fresh type-variable allocation, substitution-map layout, evaluator object representation и environment/substitution machinery остаются implementation-specific. Packet сравнивает normalized principal schemes и observable WHNF, а не host internals.

### F4 — error precedence

Не вводится искусственный global precedence rule для гипотетического input с несколькими independent static defects. Если independent/generated testing покажет необходимость такого portable rule, Stage 5.6 добавит минимальный explicit case.

## 10.4 Интерпретация

Даже до второй реализации Stage 5 уже показал пользу independent reconstruction: он вынудил разделить **language semantics**, **test presentation conventions** и **reference implementation architecture**. Именно такие hidden dependencies трудно обнаружить, тестируя только одну реализацию против её же assumptions.

## 10.5 Следующий checkpoint

Stage 5.2–5.4 должны выполняться в fresh isolated context по frozen packet. До открытия `reference/go` должен быть frozen pre-comparison implementation commit. После этого каждое discrepancy классифицируется как specification ambiguity/omission, Go bug, independent implementation bug, conformance gap или deliberately unspecified behavior.

Bootstrap-часть Stage 5 затем определит explicit receiver assumption sets и будет записывать измерения условно как `B | A`.

---

# 11. Обсуждение и ответы на RQ

## 11.1 RQ1

**Поддерживается reference implementation; independent confirmation pending.** Wire grammar и vectors зрелые, но Stage 5 ещё должен доказать независимое восстановление.

## 11.2 RQ2

**Функционально поддерживается, globally unresolved.** HM inference работает; root-type experiment дал +9,77% `P`, но bootstrap saving неизвестен.

## 11.3 RQ3

**Сильно поддерживается на tested corpus.** Weak CBN прост, call-by-need сохранил observables и сильно уменьшил repeated work на части recursive workloads.

## 11.4 RQ4

**Corpus-specific:** `Prim` — largest measured v0.3 contributor; `Let` и direct `Nat` оправданы против tested alternatives.

## 11.5 RQ5

**Смешанный результат:** BLC меньше на common pure-lambda subset; NEX меньше selected tiny postfix baseline на full v0.3. Total-cost winner неизвестен.

## 11.6 RQ6

**Нет.** `P` известен, receiver-neutral `S`/`B` отсутствуют.

## 11.7 RQ7

**Пока не отвечен.** Stage 5.0–5.1 создали credible protocol и выявили presentation gaps, но isolated second implementation ещё не frozen.

## 11.8 RQ8

**Пока не отвечен.** Принят принцип `B | A`, но Stage 5.7–5.8 ещё не выполнены.

---

# 12. Ограничения и угрозы валидности

1. **Малый corpus:** 17 программ не представляют всё software distribution.
2. **Hand-construction bias:** часть terms/translations разработана вручную.
3. **Одна complete implementation:** Go пока единственная полная реализация.
4. **Cognitive contamination:** текущий context знает Go implementation и не может сам служить единственным источником independent evidence.
5. **Runtime counters host-specific:** transitions/depth не portable computation units.
6. **Explicit-type experiment incomplete:** root type не заменяет alternative checker/bootstrap.
7. **External baselines limited:** BLC comparison узкий; tiny stack reuse NEX conventions; Jot зависит от одной translation.
8. **Receiver-neutral `S`/`B` unknown:** главный gap исходной цели.
9. **Нет machine-checked proof:** fuzz/conformance/CI — empirical evidence.
10. **Packet completeness provisional:** окончательный аудит выполнит сам independent implementer; необходимость «посмотреть Go» до freeze будет evidence packet/spec gap.

---

# 13. Научный вклад на текущем этапе

1. Concrete architecture-neutral typed Core с canonical binary representation.
2. Executable separation wire/scope/type validity и resource refusal.
3. Language-neutral conformance для wire/static/dynamic semantics.
4. Evidence-gated process с frozen benchmarks.
5. Exact constructor-level wire attribution.
6. Measured break-even `Let` и evidence за direct `Nat` против repeated `succ`.
7. Quantified root-type transmission experiment.
8. Controlled BLC/Jot/stack comparisons.
9. Observational CBN/call-by-need experiment.
10. Total-information accounting, запрещающий подменять `B` host source size.
11. Living dissertation process.
12. Frozen independent-conformance protocol с контролем leakage implementation knowledge.
13. Reproducible standalone packet artifact с content hashes и dedicated CI.
14. Early specification-audit findings, отделяющие semantics от presentation conventions.

---

# 14. Дальнейшие исследования

## 14.1 Isolated independent implementation

Реализовать wire/static/normative dynamic semantics на Python 3.12 только по frozen packet и allowed theory; freeze commit до Go comparison.

## 14.2 Differential conformance

После independence freeze сравнить portable outputs с Go и классифицировать каждое расхождение, а не принудительно подгонять одну сторону.

## 14.3 Receiver-assumption model

Определить explicit assumption sets для channel/framing, binary ordering, math concepts, integer coding, term structure и execution. Bootstrap cost должен записываться как `B | A`.

## 14.4 First measurable bootstrap artifact

Исследовать concrete transmitted artifact: tiny abstract machine, layered decoder-validator-evaluator description или другую explicitly decodable форму. Circular interpreter assumptions нельзя скрывать.

## 14.5 Primitive-reference encoding

`Prim` остаётся largest measured wire category, но compactness redesign отложен до independent reconstruction.

## 14.6 Full typing alternatives

Meaningful erased-vs-explicit comparison требует alternative verifier/checker и bootstrap accounting.

## 14.7 Broader corpora и formal verification

Нужны common-source corpora и возможная proof-assistant formalization decoder/substitution/unification/evaluator properties после дальнейшей стабилизации.

---

# 15. Заключение

Исследование началось с вопроса: если языки программирования создаются для людей и известных машин, какое вычислительное представление использовать, когда нельзя предполагать ни то, ни другое?

Результаты показывают, что ответ нельзя свести к самому короткому syntax. NEX-1 v0.1 имеет compact canonical binary form, reconstructible principal typing в reference implementation и явно non-strict semantics. Stage 4 показал ценность измерений: direct naturals сильно оправданы против tested successor construction, `Let` имеет реальный break-even, BLC компактнее на measured pure-lambda subset, call-by-need способен устранять огромный repeated runtime work без изменения program bits, а `Prim`, не `App`, оказался крупнейшим measured wire contributor. Одновременно total `C` остаётся unknown из-за отсутствия receiver-neutral `S`/`B`.

Stage 5 меняет формулировку с «проходит ли наша реализация наши tests?» на «может ли реализация, которая не видела нашу реализацию, восстановить ту же систему?». Уже первый protocol checkpoint показал ценность этого сдвига, выявив assumptions представления, которые были безвредны внутри одной codebase, но недостаточно явны для внешнего implementer.

Следующее решающее evidence должно прийти из двух источников: isolated second implementation и measurable bootstrap при explicit receiver assumptions. Только после этого имеет смысл рассматривать NEX-1 v0.2 compactness redesign.

---

# Словарь терминов

**ABI (Application Binary Interface)** — соглашения бинарного взаимодействия компонентов с платформой.

**Alpha-equivalence** — эквивалентность lambda-термов, различающихся только именами bound variables.

**Architecture-neutral** — не зависящий от конкретной ISA, word size, ABI, OS или host runtime.

**AST (Abstract Syntax Tree)** — структурное представление программы.

**Binary Lambda Calculus (BLC)** — compact binary representation untyped lambda terms Джона Тромпа [2].

**Bootstrap (`B`)** — receiver-neutral информация, необходимая для реализации механизма обработки NEX; пока unknown.

**Call-by-name (CBN)** — non-strict strategy, где argument не вычисляется заранее и может вычисляться повторно [9].

**Call-by-need** — lazy evaluation с sharing/memoization [10,11].

**Cognitive independence** — условие эксперимента, при котором implementer/context до freeze не использовал excluded reference implementation как implementation guidance.

**Conformance packet** — frozen, versioned набор specification, normative decisions, vectors и observation conventions для independent implementation.

**Conformance vector** — language-neutral input/expected-output artifact.

**de Bruijn index** — numeric reference на binding depth вместо имени [1].

**Erased typing** — ordinary term wire не несёт type annotations; типы восстанавливаются inference.

**Hindley–Milner (HM)** — rank-1 polymorphic inference discipline [3,4].

**Occurs check** — проверка, запрещающая унифицировать variable с типом, содержащим её же.

**Principal type scheme** — наиболее общий HM type scheme [4].

**Primitive (`Prim`)** — фиксированная Core operation с numeric ID.

**Receiver-neutral** — не зависящий от непереданных terrestrial implementation conventions.

**Resource refusal** — отказ реализации из-за finite limits, отличный от malformed/static invalid/normal result.

**Specification cost (`S`)** — информация, необходимая для передачи правил вычислительной системы.

**Thunk** — delayed computation, концептуально term + environment или эквивалентная отложенная форма.

**Total information cost (`C`)** — `C = S + B + P`.

**Transmitted-program cost (`P`)** — exact canonical program bits для workload.

**Weak-head normal form (WHNF)** — вычисление только до раскрытия внешней computational form.

**Wire format** — canonical transmitted bit representation NEX terms.

---

# Библиография

Stable source identifiers соответствуют `docs/SOURCES.md`.

1. **de Bruijn, N. G.** (1972). *Lambda calculus notation with nameless dummies, a tool for automatic formula manipulation, with application to the Church-Rosser theorem.* DOI: https://doi.org/10.1016/1385-7258(72)90034-0. `[SRC-0001]`
2. **Tromp, J.** *Binary Lambda Calculus.* https://tromp.github.io/cl/Binary_lambda_calculus.html. `[SRC-0002]`
3. **Milner, R.** (1978). *A Theory of Type Polymorphism in Programming.* DOI: https://doi.org/10.1016/0022-0000(78)90014-4. `[SRC-0003]`
4. **Damas, L.; Milner, R.** (1982). *Principal Type-Schemes for Functional Programs.* DOI: https://doi.org/10.1145/582153.582176. `[SRC-0004]`
5. **Plotkin, G. D.** (1977). *LCF Considered as a Programming Language.* DOI: https://doi.org/10.1016/0304-3975(77)90044-5. `[SRC-0005]`
6. **Elias, P.** (1975). *Universal codeword sets and representations of the integers.* DOI: https://doi.org/10.1109/TIT.1975.1055349. `[SRC-0006]`
7. **Wells, J. B.** (1999). *Typability and type checking in System F are equivalent and undecidable.* DOI: https://doi.org/10.1016/S0168-0072(98)00047-5. `[SRC-0007]`
8. **Schönfinkel, M.** (1924). *Über die Bausteine der mathematischen Logik.* `[SRC-0009]`
9. **Plotkin, G. D.** (1975). *Call-by-name, call-by-value and the lambda-calculus.* DOI: https://doi.org/10.1016/0304-3975(75)90017-1. `[SRC-0011]`
10. **Launchbury, J.** (1993). *A Natural Semantics for Lazy Evaluation.* DOI: https://doi.org/10.1145/158511.158618. `[SRC-0012]`
11. **Sestoft, P.** (1997). *Deriving a lazy abstract machine.* DOI: https://doi.org/10.1017/S0956796897002712. `[SRC-0013]`
12. **Barker, C.** (2001). *Iota and Jot: the simplest languages?* https://web.archive.org/web/20201112014512/http://www.nyu.edu/projects/barker/Iota/. `[SRC-0014]`
13. **W3C WebAssembly Working Group.** *WebAssembly Core Specification.* https://www.w3.org/TR/wasm-core/. `[SRC-0008]`
14. **The Go Project.** *The Go Programming Language Specification; math/big; testing/fuzzing documentation.* https://go.dev/ref/spec. `[SRC-0010]`

---

# Приложение A. Воспроизводимость и артефакты

## A.1 Нормативные / архитектурные

- `docs/NEX-1-v0.1.md`
- `docs/NEX-1-v0.1.ru.md`
- `docs/ARCHITECTURE.md`
- `docs/adr/`
- `docs/SOURCES.md`

## A.2 Conformance

- `conformance/wire-v0.1.json`
- `conformance/static-v0.1.json`
- `conformance/eval-v0.1.json`

## A.3 Stage 4

- `benchmarks/corpus-v0.1.json`
- `benchmarks/corpus-v0.2.json`
- `benchmarks/corpus-v0.3.json`
- `reference/go/cmd/nexbench`
- `reference/go/cmd/nexexperiment`
- `reference/go/cmd/nextypeexperiment`
- `reference/go/cmd/nexbaseline`
- `reference/go/cmd/nexstrategy`
- `reference/go/cmd/nexaccount`
- `reference/go/cmd/nexreport`

## A.4 Stage 5 packet

- `docs/adr/0013-stage5-independence-protocol.md`
- `stage5/conformance-packet-v0.1/manifest.json`
- `stage5/conformance-packet-v0.1/OBSERVATIONS.md`
- `stage5/conformance-packet-v0.1/AUDIT.md`
- `stage5/build_packet.py`
- `.github/workflows/stage5-independence.yml`

Dedicated verification:

```text
GitHub Actions run 35379868436 — success
artifact 10560808823
sha256:fca1fddff742674c4e0b832ea53022d712f292d1361dfbe9b1b62c022ead15c3
```

## A.5 Stage completion evidence

- Stage 1 merge: `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`.
- Stage 2 merge: `cefe889d90a275897de31aa23c4b9742a388ec8f`.
- Stage 3 merge: `166cdc03282ea500263fdca7185f006f9b17a702`.
- Stage 4 merge: `ebffde6c8669f65dfcba98d31d261d59b48d4dd0`.
- Stage 4 post-merge CI: `35377892126` — success.

---

# Приложение B. Evidence-gated decisions

| Вопрос | Текущее решение | Evidence status |
|---|---|---|
| Сохранять direct `Nat`? | Да | Strong corpus experiment; не global optimality |
| Сохранять `Let`? | Да | Measured break-even |
| Сохранять erased HM? | Да в v0.1 | Working inference + root-type `Delta P`; bootstrap comparison missing |
| CBN нормативен? | Да | Specification/conformance |
| Call-by-need? | Allowed optimization | 17/17 agreement; reference-runtime savings |
| `Prim` future priority? | Да, после independence | Largest measured v0.3 category |
| NEX меньше BLC? | Global claim отсутствует | BLC 30 vs NEX 37 на shared lambda subset |
| Total `C` известен? | Нет | Receiver-neutral `S`/`B` unresolved |
| NEX independently reconstructable? | Ещё не установлено | Protocol/packet ready; isolated implementation pending |
| Может текущий context дать independent implementation evidence? | Нет | Prior Go exposure = cognitive contamination |

---

# Правило дальнейшего ведения

Согласно ADR-0012 любое будущее изменение, создающее materially significant measurement, research decision, baseline/source, independent conformance result, formal proof/counterexample, stage-level conclusion, revised `S/B/P/C` evidence или falsification/qualification предыдущей hypothesis, должно обновлять английскую рукопись и этот русский mirror в том же PR, если только PR явно не объясняет отсутствие research-text changes.
