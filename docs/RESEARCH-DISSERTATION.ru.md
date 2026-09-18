# NEX-1: минимальное архитектурно-независимое типизированное ядро для информационно-эффективной передачи вычислений

## Проектирование, формализация, исполняемая семантика, эмпирическая оценка, независимое восстановление и учёт предположений о получателе

**Тип документа:** живая исследовательская рукопись в диссертационном стиле  
**Основной язык:** английский  
**Каноническая версия:** `RESEARCH-DISSERTATION.md`  
**Граница учтённых данных:** Stages 0–4 завершены; Stage 5.0–5.6 завершены независимым восстановлением и differential conformance; Stage 5.7 — receiver-assumption model проверена первым clean-checkout PR checkpoint, 18.09.2026  
**Проект:** NEX / `aliens_nex`

> Эта рукопись является научным синтезом исследования, поддерживаемым непосредственно в репозитории. Она ещё не оформлена под требования конкретного университета, ВАК, национальной системы аттестации или библиографического стандарта. Нормативное определение языка остаётся в `docs/NEX-1-v0.1.md`, а архитектурные и исследовательско-методологические решения — в принятых ADR.

---

## Аннотация

В работе исследуется вопрос о том, может ли очень небольшое, архитектурно-независимое и статически типизированное вычислительное ядро уменьшить объём информации, необходимой для передачи исполняемого вычислительного знания между сторонами, которые не могут предполагать общий язык программирования, архитектуру процессора, ABI, операционную систему, текстовую нотацию или общую среду реализации. Целью оптимизации является не только размер программы, а полная информационная модель

```text
C = S + B + P
```

где `S` — информация, необходимая для описания вычислительной системы, `B` — bootstrap-информация на стороне получателя, необходимая для её реализации при явно заданных исходных предположениях, а `P` — передаваемый программный payload.

Экспериментальная система NEX-1 v0.1 использует шесть канонических конструкторов термов (`Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`), нулевые индексы де Брёйна, rank-1 Hindley–Milner let-полиморфизм, натуральные числа произвольной точности, небольшой фиксированный набор примитивов, явную общую рекурсию через `fix`, самоделимитирующееся бинарное представление и weak call-by-name семантику. Теоретической основой служат безымянное представление де Брёйна [1; SRC-0001], Binary Lambda Calculus как компактный сравнительный baseline [2; SRC-0002], вывод типов Hindley–Milner и principal type schemes [3,4; SRC-0003, SRC-0004], типизированная рекурсия в традиции PCF/LCF [5; SRC-0005], универсальные коды Элиаса [6; SRC-0006] и работы по call-by-name и ленивому вычислению с sharing [9–11; SRC-0011–SRC-0013].

Stages 1–3 формируют исполняемые wire-, static- и dynamic-semantics. Stage 4 фиксирует benchmark corpora и правила измерений до оптимизаций. На принятом корпусе v0.3 из 17 программ канонические NEX-программы занимают 1371 бит при 345 AST-узлах. Ссылки на примитивы являются крупнейшим измеренным источником wire-cost: 460 бит, или 33,6%. Прямое `Nat(255)` занимает 21 бит против 2300 бит у проверенной цепочки повторных `succ`. `Let` имеет измеримую точку безубыточности и не является безусловно выгодным. Экспериментальная передача только principal root type добавляет 134 бита, или 9,77% `P`, не доказывая сокращение bootstrap. На одинаковом pure-lambda подмножестве Binary Lambda Calculus компактнее NEX: 30 против 37 бит, поэтому глобальное превосходство NEX по размеру программ не заявляется. Экспериментальный call-by-need evaluator сохранил наблюдаемые результаты всех 17 программ, снизив число transitions Go-reference evaluator с 226151 до 2484 в сумме; это результат об эффективности реализации, а не об информационной стоимости передачи.

Stage 5 проверяет, определяется ли поведение NEX спецификацией и language-neutral conformance artifacts независимо от исходной Go-реализации. До создания второй реализации был заморожен versioned conformance packet. Отдельная модель/контекст, получившая этот packet, но не `reference/go`, независимо восстановила wire codec, проверку closed scope, rank-1 HM inference и weak call-by-name evaluator на Python 3.12+ только со стандартной библиотекой. До сравнения с Go реализация прошла 17/17 integer wire vectors, 12/12 term wire vectors, 15/15 invalid wire vectors, 15/15 scope vectors, 19/19 type vectors, 21/21 evaluation vectors и 23/23 собственных теста. Затем полученная реализация была зафиксирована SHA-256 архива, и лишь после этой границы был открыт Go reference. Последующий детерминированный post-freeze differential-эксперимент сравнил 942 архитектурно-независимых наблюдения и получил 942 совпадения, 0 semantic mismatch и 0 finite-resource asymmetry. Это сильное эмпирическое свидетельство независимой восстанавливаемости на проверенной семантической поверхности, но не формальное доказательство полноты спецификации.

Stage 5.7 исследует более глубокую проблему учёта: длина исполняемого bootstrap в битах бессмысленна без явного указания того, что получатель уже знает. ADR-0014 поэтому делает claims о specification/bootstrap условными относительно явного receiver prior `A`. Первая versioned-модель задаёт `A0` — точный конечный упорядоченный бинарный кадр; `A1` — `A0` плюс явно перечисленный дискретно-математический метаязык; `A2(U)` — `A1` плюс одна точно заданная универсальная бинарная абстрактная машина `U` и её self-delimiting program/data convention; а `A_host(H)` используется как земной инженерный контроль и запрещён для receiver-neutral claims. Поэтому проект использует `B | A`, `S | A`, `C | A`, а не безусловный scalar `B`. Вводится также правило отсутствия двойного счёта: если один передаваемый артефакт неразделимо выполняет одновременно роль specification и executable bootstrap, его биты учитываются один раз как `SB | A`, а не отдельно как `S` и `B`.

Модель Stage 5.7 представлена machine-readable registry и прошла dedicated clean-checkout validator на PR #9 вместе с прежними independence/differential regression gates. Validator подтверждает 4 effective assumption atoms для `A0`, 7 для `A1`, 9 для `A2(U)` и 8 для non-neutral control `A_host(H)`. Эта проверка подтверждает внутренние structural invariants registry, но не даёт численной стоимости bootstrap или prior information.

Stage 5.7 не выбирает конкретную universal machine `U`, не назначает bit-price receiver priors и не ранжирует профили с более сильными и более слабыми assumptions только по числу передаваемых битов. Главная следующая задача — Stage 5.8: заморозить хотя бы один конкретный bootstrap artifact под одним объявленным профилем и измерить реальный transmitted ledger без циклического исчезновения необходимого интерпретатора. До этого полная `C | A` остаётся численно не определённой, а проект не утверждает глобальную минимальность NEX или общее превосходство над альтернативными исчислениями.

**Ключевые слова:** минимальный язык программирования, архитектурно-независимые вычисления, Binary Lambda Calculus, индексы де Брёйна, Hindley–Milner, бинарное кодирование, bootstrap, условная информационная стоимость, receiver assumptions, call-by-name, call-by-need, независимая реализация, differential conformance, воспроизводимое исследование.

---

# 1. Введение

## 1.1 Мотивация

Большинство исполняемого программного обеспечения предполагает значительный общий контекст: кодировки символов, синтаксис, модель процессора, разрядность, объектные форматы, сервисы ОС, компиляторы, виртуальные машины и соглашения о представлении данных. Для обычной разработки это полезно. В задаче, где отправитель и получатель не могут считать общей земную вычислительную платформу, эти предположения становятся скрытой стоимостью.

Поэтому вопрос исследования состоит не просто в сжатии программы. Требуется понять, как передавать вычислительное знание, если нельзя считать известными земной язык программирования, CPU, ABI, ОС, текстовую кодировку или runtime.

Однобитная программа бесполезна, если её смысл зависит от огромного непереданного интерпретатора. И наоборот, чрезмерно маленький универсальный интерпретатор может сделать все последующие программы слишком дорогими. Поэтому NEX рассматривает совместную стоимость:

```text
C = S + B + P
```

Неизвестная величина не принимается равной нулю. Исходный код на host-языке не считается bootstrap для неизвестного получателя. Stage 5.7 дополнительно делает явным receiver prior: измеренный bootstrap всегда условен относительно объявленного набора предположений.

## 1.2 Научная проблема

Необходимо определить, может ли компактное типизированное функциональное ядро обеспечить выгодный компромисс полной информационной стоимости для передачи вычислений общего назначения без общей вычислительной платформы, может ли это ядро быть независимо восстановлено из конечного specification/conformance package и при каких явно объявленных receiver priors позднее можно измерить конкретный bootstrap.

Проблема включает:

1. компактность представления;
2. детерминированное декодирование и валидацию;
3. восстановление типов;
4. вычислительную выразительность;
5. non-strict семантику;
6. стоимость bootstrap;
7. независимую воспроизводимость;
8. зависимость executable description от receiver prior;
9. эмпирическую фальсифицируемость сравнительных утверждений.

## 1.3 Объект и предмет

**Объект:** архитектурно-независимое представление, проверка и выполнение вычислений общего назначения при крайне ограниченной передаче информации.

**Предмет:** компромиссы между стоимостью specification, bootstrap получателя, размером программ, выводом типов, стратегией вычисления, independent conformance и явно условленными receiver priors минимального типизированного lambda-core.

## 1.4 Цель

Создать и эмпирически проверить минимальное исполняемое ядро, бинарная форма и семантика которого достаточно явны для независимого восстановления, и выработать воспроизводимую методику оценки его полной информационной стоимости относительно альтернатив при одинаково сформулированных receiver assumptions.

## 1.5 Задачи

1. Определить архитектурно-независимый Core.
2. Определить канонический самоделимитирующийся wire-format.
3. Создать исполняемую encode/decode conformance.
4. Определить closed-scope и principal-type semantics.
5. Определить weak non-strict dynamic semantics.
6. Отделить валидность языка от конечных implementation resource limits.
7. Зафиксировать benchmark corpora до оптимизаций.
8. Измерить точную wire-cost конструкций и контролируемых альтернатив.
9. Сравнивать внешние baselines только при явных предположениях.
10. Разделить точный `P`, proxies и неизвестный bootstrap.
11. Проверить независимое восстановление без доступа к первой реализации.
12. Явно определить receiver assumptions до численной оценки bootstrap.
13. Исключить двойной счёт там, где specification и executable bootstrap используют одни и те же передаваемые биты.
14. Сохранять положительные, отрицательные и нерешённые результаты в живой исследовательской рукописи.

## 1.6 Исследовательские вопросы

**RQ1.** Можно ли задать детерминированное архитектурно-независимое самоделимитирующееся бинарное представление NEX с исполняемой conformance-проверкой?

**RQ2.** Можно ли восстанавливать principal rank-1 types без обычных term-level type annotations?

**RQ3.** Может ли простая weak call-by-name semantics сосуществовать с существенно более эффективными реализациями, сохраняющими portable observations?

**RQ4.** Какие конструкции доминируют в `P`, и оправданы ли `Let` и direct `Nat`?

**RQ5.** Как NEX сравнивается с выбранными альтернативными кодировками при контролируемых условиях?

**RQ6.** Можно ли уже численно вычислить `C = S + B + P`?

**RQ7.** Может ли implementation, созданная без доступа к `reference/go`, восстановить то же portable wire/static/dynamic behavior по frozen specification/conformance packet?

**RQ8.** При каких явно заданных receiver assumptions `A` можно представить и измерить bootstrap artifact как `B | A` или, если specification и bootstrap неразделимы, как `SB | A`?

## 1.7 Рабочие гипотезы

**H1.** Nameless binding и compact prefix encoding могут дать небольшой однозначный wire.

**H2.** Rank-1 HM inference позволяет исключить обычные type annotations из `P`, но итоговая выгода зависит от bootstrap.

**H3.** `Let` и direct naturals могут уменьшать `P`, несмотря на увеличение определения языка.

**H4.** Weak CBN может оставаться normative, а sharing/memoization — быть observationally equivalent implementation optimization для проверенных pure Core programs.

**H5.** Нельзя заранее считать NEX компактнее сильно сжатых untyped lambda encodings на pure lambda terms.

**H6.** `P` сам по себе не доказывает total superiority.

**H7.** Достаточно явная normative specification + portable vectors позволяют cognitively isolated implementation восстановить NEX без guidance из reference source.

**H8.** Осмысленная численная стоимость bootstrap требует явного receiver prior, а не скрытого host language/VM.

**H9.** Точный total-information accounting требует transmitted-bit ledger, в котором бит, одновременно выполняющий роль specification и executable bootstrap, учитывается один раз, а не независимо в `S` и `B`.

---

# 2. Теоретическая база и связанные работы

## 2.1 Безымянные переменные

Работа де Брёйна показывает возможность числового представления связанных переменных без имён [1]. NEX фиксирует zero-based вариант; alpha-renaming не передаётся.

## 2.2 Binary Lambda Calculus

BLC Тромпа демонстрирует компактное прямое бинарное кодирование lambda terms [2]. Для NEX это precedent и falsifying baseline, но не источник exact NEX grammar.

## 2.3 Hindley–Milner

Milner и Damas–Milner дают теоретическую основу rank-1 let-polymorphism и principal schemes [3,4]. Результат Wells используется как граница против безусловного перехода к unrestricted implicit System F [7].

## 2.4 Рекурсия и натуральные числа

PCF/LCF Plotkin служит precedent для небольшого типизированного языка с naturals и fixed-point recursion [5]. Точный NEX primitive set является отдельным design decision.

## 2.5 Universal integer codes

Elias ввёл семейства universal codes [6]. NEX использует gamma-code от `n+1` как `U(n)`.

## 2.6 Evaluation strategy

Plotkin формализовал различие call-by-name/call-by-value [9]; Launchbury и Sestoft дают основу lazy sharing [10,11]. NEX сохраняет CBN нормативным и рассматривает call-by-need как implementation optimization.

## 2.7 Combinatory alternatives

Классическая combinatory logic и Iota/Jot Barker дают comparative background [8,12]. Stage 4 использует только явно описанную deterministic translation и не заявляет shortest Jot.

## 2.8 Portable core и embedding

WebAssembly Core — современный пример разделения portable computation и embedding assumptions [13]. NEX заимствует принцип границы, а не instruction set или runtime model.

## 2.9 Граница канала и относительность исполняемого описания

Модель Shannon явно разделяет инженерную структуру source/transmitter/channel/receiver/destination и семантическую интерпретацию сообщения [15; SRC-0015]. Из этого NEX не делает вывода, что бинарный кадр является универсально естественным или бесплатным. Разделение используется только для явного определения начала текущего digital-semantic experiment: physical acquisition, synchronization, modulation discovery и error correction находятся ниже границы `A0`, а не получают цену ноль.

Алгоритмический подход Kolmogorov определяет длину описания относительно эффективного способа описания, а не как один implementation-free scalar [16; SRC-0016]. Program-size formulation Chaitin аналогично использует заданную self-delimiting интерпретацию программ [17; SRC-0017]. Для NEX это методологическое основание: численная длина executable bootstrap требует зафиксированной интерпретации. Эти работы не выбирают привилегированную universal machine для неизвестного получателя и не доказывают оптимальность будущего NEX bootstrap.

---

# 3. Методология

## 3.1 Evidence-gated workflow

```text
Problem
 -> Contract
 -> Invariant
 -> Executable example / failing test
 -> Implementation
 -> Verification
 -> Diff review
 -> Status checkpoint
 -> Research synthesis checkpoint
```

Долговременная память проекта — репозиторий, а не история чатов.

## 3.2 Классы утверждений

Различаются:

1. external established results;
2. NEX design decisions;
3. reproducible NEX measurements;
4. выводы из текущих evidence;
5. открытые hypotheses/unknowns.

Повторение гипотезы не делает её фактом.

## 3.3 Воспроизводимость

Evidence сохраняются через conformance JSON, unit/property/fuzz tests, frozen corpora, deterministic CLIs, Git hashes, clean-checkout CI, versioned reports и machine-readable receiver-assumption profiles с validator.

## 3.4 Frozen corpus

Корпус, на котором опубликован comparative conclusion, не переписывается. Поэтому v0.2 с `factorial-5`, превышающим default CBN transition budget, сохранён как неудобный, но важный ресурсный checkpoint.

## 3.5 Independence protocol

Вторая реализация не становится independent только из-за другого host language. Stage 5 замораживает packet, исключает `reference/go`, а затем freeze-ит independent implementation по content hash до начала direct comparison.

## 3.6 Differential conformance

После freeze сравниваются только portable observations:

```text
wire bits
normalized principal type / portable static error
observable WHNF / portable evaluation error
```

Host internals исключены.

## 3.7 Условный total-information accounting

Историческая модель:

```text
C = S + B + P
```

Stage 5.7 делает receiver prior явным. Assumption profile `A` — это prior knowledge/capability, разделяемые до измеряемой передачи. То, что `A` не передаётся внутри измеряемого сообщения, не означает, что ему приписана нулевая информационная стоимость.

Первая лестница профилей:

```text
A0        exact finite ordered binary frame
A1        A0 + явно заданный discrete mathematical metalanguage
A2(U)     A1 + точная universal binary abstract machine U
              + exact self-delimiting program/data convention
A_host(H) A1 + конкретный terrestrial host H; только engineering control
```

Поэтому exact claims используют:

```text
B | A
S | A
C | A
```

Если specification и executable bootstrap являются раздельными transmitted segments:

```text
C | A = (S | A) + (B | A,S) + P
```

Если один artifact неразделимо выполняет обе роли:

```text
C | A = (SB | A) + P
```

Каждый передаваемый бит учитывается ровно один раз. Stage 5.7 не назначает численную цену assumption atoms, поэтому меньший transmitted bootstrap при более сильном prior не считается автоматически лучшим cross-profile total solution.

Текущая интерпретация:

- `P` — exact canonical program bits для заданного corpus после установления wire contract;
- `S | A` — отдельный transmitted specification segment под объявленным prior, пока не измеренный receiver-neutral artifact;
- `B | A,S` — executable realization segment, когда отдельная specification уже передана;
- `SB | A` — joint segment при невозможности защитимо разделить specification/execution roles;
- `R` — host/reference implementation proxy, который нельзя подменять receiver-neutral bootstrap.

---

# 4. NEX-1 v0.1

## 4.1 Terms

```text
Term ::= Var(index)
       | Lam(body)
       | App(function, argument)
       | Let(value, body)
       | Nat(value)
       | Prim(id)
```

Используются zero-based de Bruijn indices.

## 4.2 Types

```text
T ::= a | 1 | N | T -> T | T * T | T + T
S ::= forall a1 ... an. T
```

Static system — rank-1 HM inference с unification, occurs check, instantiation и let-generalization.

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

`U(n)` — Elias gamma code от `n+1`.

```text
00   U(k)   Var(k)
01   T      Lam(T)
10   T T    App(T,T)
110  T T    Let(T,T)
1110 U(n)   Nat(n)
1111 U(p)   Prim(p)
```

## 4.5 Dynamic semantics

Normative semantics — weak call-by-name. Arguments и `Let` values задерживаются, под lambda редукция до application не выполняется, primitive forcing selective, общая рекурсия явна через `fix`.

---

# 5. Stages 0–3: формальная и исполняемая основа

## 5.1 Stage 0

Зафиксированы canonical specification, ADR, source registry, testing/workflow rules, English canonical/Russian mirror и repository-as-memory.

## 5.2 Stage 1 — wire

Реализованы arbitrary-precision `U(n)`, term encode/decode, exact/prefix decoding, malformed-input classes и отдельные resource limits.

Conformance: 17 integer, 12 term и 15 invalid exact-input vectors.

```text
Var(0)                    001
Nat(0)                    11101
Prim(0)                   11111
Lam(Var(0))               01001
Lam(App(Prim(1),Var(0)))  01101111010001
```

**Вывод:** RQ1 поддержан эмпирически для v0.1 wire grammar.

## 5.3 Stage 2 — static semantics

Реализованы closed scope, Type/TypeScheme, FTV, substitutions, unification, occurs check, primitive schemes, instantiation, let-generalization и Algorithm-W-style inference.

**Вывод:** RQ2 функционально поддержан, но total-cost optimality erased typing не доказана.

## 5.4 Stage 3 — dynamic semantics

Определён weak CBN evaluator и observable WHNF conformance. Проверена lazy selective forcing; resource refusal отделён от invalidity и divergence proof.

**Вывод:** получена стабильная динамическая семантика, пригодная как цель независимой реализации.

---

# 6. Stage 4: эмпирическая проверка

## 6.1 Corpus v0.3

| Метрика | Значение |
|---|---:|
| Программ | 17 |
| AST nodes | 345 |
| Wire bits | 1371 |

| Конструктор | Биты | Доля |
|---|---:|---:|
| `Prim` | 460 | 33,6% |
| `Var` | 286 | 20,9% |
| `App` | 264 | 19,3% |
| `Nat` | 244 | 17,8% |
| `Lam` | 84 | 6,1% |
| `Let` | 33 | 2,4% |

Гипотеза о доминировании `App` не подтверждена на данном corpus; крупнейшим измеренным источником оказался `Prim`.

## 6.2 `Let`

Для 5-битного payload `Let` проигрывает при двух/трёх использованиях, даёт ничью при четырёх и экономит 8 бит при восьми. Для проверенного 14-битного payload два использования уже дают экономию 5 бит.

**Решение:** `Let` сохраняется.

## 6.3 Direct `Nat`

```text
Nat(255)          21 бит
succ-chain(255) 2300 бит
```

**Решение:** direct naturals сохраняются; global optimality конкретного numeric code не заявляется.

## 6.4 Root-type envelope

```text
erased terms      1371 бит
root type           134 бита
hybrid             1505 бит
overhead           +9,77%
```

Это измеряет только `Delta P`, а не уменьшение `B`.

## 6.5 Baselines

На одинаковом pure-lambda subset:

```text
NEX  37 бит
BLC  30 бит
```

Поэтому общее превосходство NEX над BLC не заявляется.

Tiny postfix baseline на полном corpus: 1529 бит против 1371 у NEX, но baseline наследует integer/primitive assumptions NEX и не является независимым total-bootstrap сравнением.

## 6.6 CBN vs call-by-need

```text
CBN transitions          226151
call-by-need transitions   2484
reduction                 98,90%
```

Все 17 observable results совпали. Выигрыш сосредоточен в тяжёлых recursive/reused workloads и не является прямой частью `C`.

## 6.7 Accounting

`P=1371` бит известно точно. Markdown specification и Go source — только proxies. `R != B`; `C` пока численно не вычисляется.

---

# 7. Stage 5: независимое восстановление и receiver priors

## 7.1 Зачем нужна вторая реализация

Specification и первая implementation могли разделять одно и то же неявное допущение. Поэтому внутренне зелёные тесты недостаточны. Более сильная проверка — дать спецификацию другому implementer, не раскрывая reference source.

ADR-0013 делает когнитивную независимость условием эксперимента, а не неформальным обещанием.

## 7.2 Frozen conformance packet

Packet зафиксирован относительно commit:

```text
4f9c50aed13cdbdf72c9ce6510521477d49c05a5
```

Первый independent target: Python 3.12+ standard-library-only. Packet содержит canonical specification, conformance vectors, выбранные normative ADR, source hashes и packet-local observation rules, но не раскрывает Go evaluator architecture.

Audit выявил два presentation omissions:

- canonical scheme text `T0`, `T1`, ...;
- явное определение JSON fixture AST.

Они оформлены как observation conventions и не меняют язык.

## 7.3 Independent checkpoint

Отдельная модель/контекст получила только frozen packet и инструкции эксперимента. Полученный архив:

```text
nex1-independent-python-v0.1.zip
SHA-256 = 783e4186f9a8c024f00a732deae33b547c81ed4d7639c610a1e8bc5997eb3fbe
```

ZIP comment / внешний checkpoint marker:

```text
a594b73b711998df04b45eec296086d5577fba2f
```

До открытия Go были получены:

| Проверка | Результат |
|---|---:|
| Integer wire | 17 / 17 |
| Term wire | 12 / 12 |
| Invalid wire | 15 / 15 |
| Scope | 15 / 15 |
| Types | 19 / 19 |
| Evaluation | 21 / 21 |
| Independent tests | 23 / 23 |

Дополнительно проведены 20000 generated wire round trips, проверки больших arbitrary-precision integer, typing/laziness и resource separation без обнаруженного дефекта.

Внутренняя архитектура не обязана совпадать с Go. Например, independent evaluator использует dedicated `FixThunk`, а не точное представление рекурсии Go reference.

## 7.4 Защита freeze

Для каждого импортированного author-written файла записаны byte length и SHA-256. CI сначала проверяет эти hashes, затем материализует canonical packet и запускает неизменённый verifier. Это не позволяет после сравнения незаметно «исправить» independent implementation и выдать исправление за blind reconstruction.

## 7.5 Post-freeze differential conformance

Только после фиксации archive SHA был открыт Go reference.

Детерминированный набор `seed=20260918`:

| Группа | Случаи |
|---|---:|
| Frozen corpus v0.3 | 17 |
| Generated valid | 325 |
| Generated static single-defect | 100 |
| Generated wire | 500 |
| **Всего** | **942** |

Сравнивались:

```text
canonical wire bits
normalized principal type / static error class
observable WHNF / evaluation error class
```

Результат:

```text
portable matches       942
semantic mismatches      0
resource asymmetries     0
success                true
```

Final PR #8 CI:

```text
reference-go        35385704921  success
stage5-independence 35385705027  success
stage5-differential 35385705162  success
```

PR #8 squash-merged как `f500a5c5485b4cd5f6b5d9bd6bc76980f2f06cdb`. Post-merge `main` также прошёл runs `35386452647`, `35386452451`, `35386452447`.

## 7.6 Интерпретация

H7 поддержана, а RQ7 получает наиболее сильный текущий ответ:

> На замороженном conformance suite, принятом benchmark corpus и детерминированных generated differential cases реализация, созданная без перевода `reference/go`, восстановила то же portable wire/static/observable dynamic behavior.

Ограничение важно: конечный набор тестов не доказывает, что prose specification однозначно определяет каждый возможный term или malformed input. Это strong empirical conformance evidence, но не formal proof semantic equivalence.

## 7.7 Неоднозначности

Independent implementation отдельно зафиксировала вопрос diagnostic precedence для терма с несколькими независимыми static defects. Python выбирает scope-first. После freeze выяснилось, что Go делает то же, но совпадение не превращается автоматически в normative rule.

Текущий differential result не выявил Go semantic bug, independent Python semantic bug, contradictory conformance vector или новую Core ambiguity, требующую несовместимого изменения v0.1. Поэтому global multi-error precedence остаётся implementation-specific.

## 7.8 Вывод независимого восстановления

RQ7 сильно поддержан в пределах текущей evidence horizon. NEX-1 v0.1 теперь опирается не только на co-developed specification + Go, но и на hash-frozen second reconstruction с zero-mismatch post-freeze differential checkpoint.

Главный нерешённый вопрос смещается к bootstrap: что должен знать получатель до начала передачи NEX и сколько информации требуется для восстановления системы при таких assumptions.

## 7.9 Модель receiver assumptions

ADR-0014 превращает этот вопрос в versioned experimental contract вместо неформальной формулы вроде «получатель знает математику».

Канонический machine-readable registry: `stage5/receiver-assumptions/assumptions-v0.1.json`.

Первая лестница assumptions:

```text
A0  digital transport prior
    - два различимых binary symbols
    - конечный first-to-last порядок
    - точные start/end/length кадра
    - отсутствие residual bit error внутри модели

A1  A0 + discrete mathematical metalanguage
    - non-negative integers и базовые arithmetic/order concepts
    - finite sequences, length, concatenation, positional indexing
    - deterministic finite/recursive rule descriptions

A2(U)  A1 + fixed universal-machine prior
       - exact binary operational semantics одной named U
       - exact self-delimiting program/data convention для U

A_host(H)  A1 + concrete terrestrial host H
           - только engineering control
           - не receiver-neutral
```

Иерархия не утверждает, что эти priors универсальны, бесплатны или одинаково правдоподобны для неизвестной цивилизации. Она задаёт, на какой именно prior опирается конкретный experiment.

Physical layer ниже `A0` намеренно исключён из текущего NEX experiment. Signal discovery, modulation, synchronization, error correction и discovery frame boundary не измерены. Это scope boundary, а не zero-cost claim.

Universal machine в `A2(U)` остаётся параметром. Stage 5.7 намеренно не выбирает её. Любое будущее число требует exact versioned `U`, иначе executable description length недоопределена.

Ключевой методологический результат: cross-profile bit totals нельзя напрямую ранжировать. Например, 100-bit bootstrap при `A2(U)` нельзя автоматически объявить лучше 500-bit bootstrap при `A1`, потому что первый использует более сильный receiver-side computational prior. Stage 5.7 пока не назначает priors bit-equivalent cost или probability.

Второй результат — no-double-counting ledger. Если compact artifact одновременно определяет NEX и исполняет его, одни и те же bits нельзя отдельно отнести к `S` и к `B`; неразделимый segment учитывается как `SB | A`.

Первый clean-checkout checkpoint PR #9 подтвердил модель и сохранил весь предыдущий independent-conformance evidence:

```text
stage5-receiver-assumptions  35387833962  success
stage5-independence          35387833785  success
stage5-differential          35387833852  success
```

Dedicated validator сообщает 4, 7, 9 и 8 effective assumption atoms соответственно для `A0`, `A1`, `A2(U)` и `A_host(H)`. Это structural verification registry, а не измерение information content priors.

Таким образом, RQ8 получает частичный ответ: profiles и допустимая accounting notation определены и clean-checkout verified, но executable bootstrap по ним ещё не измерен.

---

# 8. Ответы на исследовательские вопросы

## RQ1

**Поддержан эмпирически.** Wire имеет language-neutral vectors, property/fuzz evidence и согласие двух независимо разработанных реализаций.

## RQ2

**Функционально поддержан; global total-cost optimality не доказана.** Обе реализации восстанавливают проверенные principal schemes без ordinary annotations.

## RQ3

**Поддержан на проверенных программах.** Weak CBN независимо реконструирован; call-by-need показывает значительный implementation-level выигрыш на части workloads.

## RQ4

**Получен corpus-specific ответ.** `Prim` доминирует в v0.3; direct `Nat` и `Let` оправданы против проверенных альтернатив.

## RQ5

**Результат смешанный.** BLC выигрывает на pure-lambda subset; NEX выигрывает у выбранного structural postfix baseline на v0.3; total-cost winner не определён.

## RQ6

**Пока нет.** `P` известен. Stage 5.7 определяет, как `S`, `B` или joint `SB` должны зависеть от receiver profile, но measured receiver-neutral bootstrap ещё отсутствует.

## RQ7

**Сильно поддержан текущими данными.** Frozen independent Python проходит packet и совпадает с Go во всех 942 post-freeze differential cases без resource asymmetry.

## RQ8

**Методологически отвечен частично; численный ответ открыт.** Stage 5.7 задаёт и clean-checkout проверяет `A0`, `A1`, parameterized `A2(U)`, non-neutral `A_host(H)`, а также `B | A`, `S | A`, `SB | A`. Stage 5.8 должен зафиксировать хотя бы один concrete artifact и, для `A2`, одну exact `U` до принятия численного результата.

---

# 9. Ограничения и угрозы валидности

## 9.1 Репрезентативность corpus

17 программ не представляют всё пространство возможного ПО. Constructor shares остаются corpus-specific.

## 9.2 Translation bias

Некоторые baseline programs проектировались внутри NEX research и не являются independently shortest translations.

## 9.3 Конечность независимой проверки

Second implementation существенно усиливает evidence, но не доказывает полноту specification. Неисследованный corner case может оставаться неоднозначным.

## 9.4 Когнитивная независимость процедурна

Blind packet boundary и independence declaration фиксируются, но технически невозможно доказать, что модель никогда ранее не видела сходного материала. Поэтому independence claim методологический, а не абсолютный.

## 9.5 Покрытие differential generator

942 cases охватывают accepted corpus, valid templates, основные static error classes и arbitrary well-shaped wire terms, но не бесконечное пространство термов.

## 9.6 Runtime counters implementation-specific

Transitions/depth из Stage 4 относятся к конкретным Go evaluators.

## 9.7 Explicit typing experiment неполон

Измерен только root type envelope, а не полноценный альтернативный checker/bootstrap.

## 9.8 Receiver-assumption profiles — модели исследования, а не факты об инопланетной цивилизации

`A0`, `A1`, `A2(U)` — явные experimental conditions. Они не утверждают, что extraterrestrial, future machine или иной конкретный receiver действительно разделяет такой prior. Модель делает assumptions видимыми, но не решает epistemic problem вероятности или bit-equivalent стоимости priors.

## 9.9 Physical-layer cost остаётся вне текущей границы

`A0` начинается с уже восстановленного finite ordered binary frame. Не измерены signal acquisition, modulation discovery, timing, synchronization, framing discovery, noise correction и physical units. Эти omitted costs не объявляются нулевыми.

## 9.10 Reference-machine sensitivity пока не измерена

`A2(U)` параметризован, поскольку executable bit length зависит от machine и input convention. Пока Stage 5.8 не заморозит и не сравнит concrete candidates, чувствительность `B | A2(U)` к выбору `U` неизвестна.

## 9.11 Receiver-neutral `S`, `B`, joint `SB` численно не определены

Stage 5.7 задаёт дисциплинированную conditional model, но не measured bootstrap artifact. Это крупнейший пробел относительно исходной total-information цели.

## 9.12 Нет machine-checked proof

Conformance, fuzzing, frozen checkpoints, differential testing и receiver-prior validator остаются empirical/structural methods и не заменяют formal proof correctness/equivalence/optimality.

---

# 10. Научные результаты и вклад

1. Конкретный architecture-neutral typed Core с canonical binary representation.
2. Исполняемое разделение wire validity, scope validity, type validity и resource refusal.
3. Language-neutral conformance corpora.
4. Frozen benchmark methodology.
5. Exact constructor-level wire attribution.
6. Empirical break-even для `Let` и сильный результат direct `Nat` против repeated `succ`.
7. Quantified root-type transmission experiment.
8. Контролируемые BLC/Jot/stack comparisons.
9. CBN/call-by-need experiment с сохранением наблюдаемого результата.
10. Total-information accounting discipline, не подменяющая `B` host source size.
11. Versioned independence protocol и frozen conformance packet.
12. Second implementation, созданная без перевода reference source.
13. Hash-frozen pre-comparison checkpoint.
14. 942-case post-freeze differential result: 942 matches, 0 semantic mismatch, 0 resource asymmetry.
15. Machine-readable и clean-checkout-validated receiver-assumption ladder `A0 ⊂ A1 ⊂ A2(U)` и non-neutral host control `A_host(H)`.
16. Conditional notation `B | A`, `S | A`, `C | A`, не позволяющая undeclared receiver priors исчезать из claims.
17. No-double-counting transmitted-bit ledger с joint `SB | A` для неразделимого specification/bootstrap artifact.
18. Living dissertation process, сохраняющий положительные, отрицательные и нерешённые результаты.

---

# 11. Следующее исследование: measurable bootstrap

## 11.1 Сначала фиксируется assumption profile

Stage 5.7 устранил неоднозначность выражения «receiver-neutral bootstrap»: будущий measurement обязан назвать profile.

Полезно разделить два независимых трека:

```text
Track A: попытка более receiver-neutral artifact при A1
Track B: instantiate A2(U) одной exact tiny universal machine U
         и измерить executable bootstrap при более сильном prior
```

Треки отвечают на разные вопросы. Меньший численный Track B нельзя объявить global winner только потому, что часть вычислительной структуры вынесена в stronger prior.

## 11.2 Concrete bootstrap candidates

Возможны:

- tiny mathematical abstract machine;
- minimal calculus/combinator bootstrap;
- layered decoder → validator → evaluator artifact;
- compact executable notation с явно учитываемой decoding base.

Ни один вариант заранее не объявляется правильным.

## 11.3 Exact ledger requirements

Каждый Stage 5.8 report должен назвать:

1. exact receiver profile/version;
2. все transmitted setup segments;
3. exact bit length каждого segment;
4. роль каждого segment;
5. можно ли защитимо разделить `S` и `B` или требуется `SB`;
6. все interpreters/machines, необходимые для candidate;
7. `P`, на который setup amortized.

При возможности:

```text
B_decode
B_static
B_eval
S
```

иначе:

```text
SB | A
```

Negative result допустим: если при `A1` нельзя построить defensible executable artifact, это предпочтительнее, чем задним числом перенести скрытый interpreter в prior.

## 11.4 Дальнейшая верификация

Возможны sensitivity analysis по нескольким exact `U`, third independent implementation, proof assistant для отдельных свойств, более широкий normalized corpus, полноценное erased-vs-explicit bootstrap comparison и total-cost comparisons альтернатив при одном receiver profile.

---

# 12. Заключение

Исследование началось с идеи о том, что существующие языки проектируются для людей и известных машин, тогда как экстремально удалённый или неизвестный получатель может не разделять ни то, ни другое. Постепенно эта идея была превращена в фальсифицируемую экспериментальную систему.

NEX-1 v0.1 имеет canonical wire, principal rank-1 type reconstruction, weak call-by-name semantics, исполняемую conformance, reproducible benchmarks, отрицательные внешние сравнения и явные границы accounting. Stage 4 показал, что интуиции о «минимальном языке» недостаточны: `App` не является главным measured wire contributor на принятом corpus, direct naturals могут экономить порядки бит, `Let` имеет условную точку безубыточности, BLC может быть компактнее на pure lambda terms, а call-by-need способен резко уменьшать receiver work без изменения проверенного observable result.

Stage 5 добавил independent reconstruction evidence. Frozen packet был выдан отдельному implementation context до доступа к Go. Полученная реализация прошла все packet vectors и была зафиксирована content hash. Лишь после этого был открыт Go reference. Последующий 942-case differential дал 942 portable matches, 0 semantic mismatch и 0 resource asymmetry. Это не доказывает global correctness/minimality/optimality NEX, но существенно усиливает утверждение о независимой восстанавливаемости specification/conformance package на проверенной семантической поверхности.

Stage 5.7 сделал явным то, что сокращённая формула `C = S + B + P` оставляла скрытым: bootstrap size зависит от того, что получатель знает заранее. Теперь различаются минимальная digital transport boundary `A0`, explicit mathematical metalanguage prior `A1`, parameterized universal-machine prior `A2(U)` и terrestrial host controls. Physical layer ниже `A0` находится вне текущей модели, а не бесплатен; stronger prior не превращается автоматически в cost-free winner; overlapping specification/bootstrap bits учитываются один раз через joint `SB | A`. Первый clean-checkout checkpoint PR #9 подтвердил registry и одновременно сохранил зелёными прежние independence/differential gates.

Главный оставшийся вопрос теперь конкретен: можно ли заморозить и точно посчитать конечный bootstrap artifact при одном из этих profiles без circular accounting? До результата Stage 5.8 проект не будет заявлять численную `C | A` или глобальное превосходство. Сохранение этой неопределённости является частью научного метода, позволяющего будущим claims стать воспроизводимыми и фальсифицируемыми.

---

# Словарь терминов

**ABI (Application Binary Interface)** — соглашения бинарного взаимодействия программ и платформы.

**Alpha-equivalence** — эквивалентность lambda terms, отличающихся только именами связанных переменных.

**Architecture-neutral** — не зависящий от конкретного CPU ISA, word size, ABI, ОС или host runtime.

**AST (Abstract Syntax Tree)** — структурное представление программного терма.

**`A0`** — Stage 5.7 digital-transport prior: один точный конечный упорядоченный бинарный кадр без residual bit error внутри модели; physical acquisition находится ниже model boundary.

**`A1`** — `A0` плюс явно перечисленный discrete mathematical metalanguage, но без fixed universal computer и NEX-specific semantics.

**`A2(U)`** — `A1` плюс одна exact versioned universal binary abstract machine `U` и её exact self-delimiting program/data convention.

**`A_host(H)`** — engineering-control profile с concrete terrestrial host `H`; явно не подходит для receiver-neutral bootstrap claim.

**Assumption atom** — одно явно сформулированное receiver-side prior knowledge/capability в machine-readable registry Stage 5.7.

**Binder** — конструкция, вводящая связанную переменную; в NEX v0.1 это `Lam` и body-часть `Let`.

**Binary Lambda Calculus (BLC)** — компактное бинарное представление нетипизированных lambda terms Тромпа [2].

**Bootstrap (`B`)** — информация, необходимая получателю для реализации достаточной вычислительной основы NEX; exact Stage 5 claims записывают её условно как `B | A`.

**Call-by-name (CBN)** — non-strict стратегия с delayed arguments и возможным повторным вычислением [9].

**Call-by-need** — lazy evaluation с sharing/memoization [10,11].

**Canonical representation** — уникальное проектное представление для wire/conformance.

**Conditional bootstrap cost (`B | A`)** — transmitted bootstrap length при explicit receiver-assumption profile `A`; не unconditional machine-free scalar.

**Conformance packet** — frozen allowlisted набор specification, ADR, vectors и observation rules для независимого implementer.

**Conformance vector** — language-neutral вход/ожидаемый результат.

**de Bruijn index** — числовая ссылка на binder position [1].

**Differential conformance** — сравнение двух implementations на одинаковых входах только по portable observations.

**Erased typing** — ordinary term wire не несёт type annotations; тип восстанавливается inference.

**Hindley–Milner (HM)** — rank-1 polymorphic inference discipline [3,4].

**Independent checkpoint** — неизменяемое hash-identified состояние второй реализации, зафиксированное до reference comparison.

**Joint specification/bootstrap segment (`SB | A`)** — передаваемые bits, которые неразделимо выполняют обе роли и поэтому считаются один раз.

**Occurs check** — проверка unification, запрещающая бесконечный self-containing type.

**Portable observation** — архитектурно-независимый результат: canonical bits, normalized type scheme, observable WHNF и т.п.

**Principal type scheme** — наиболее общая HM type scheme [4].

**Primitive (`Prim`)** — фиксированная Core operation с numeric ID.

**Receiver-assumption profile (`A`)** — versioned набор prior knowledge/capability получателя, относительно которого условно измеряется bootstrap/specification.

**Receiver-neutral** — не опирающийся на незаявленные земные implementation conventions; это не означает prior-free.

**Resource asymmetry** — ситуация, когда одна implementation упирается в finite resource guard, а другая выдаёт результат; это не автоматически semantic disagreement.

**Resource refusal** — отказ из-за конечного implementation limit, отличный от malformed input, static invalidity или доказанной divergence.

**Specification cost (`S`)** — информация для передачи computational rules; в exact Stage 5 accounting отдельный specification segment записывается как `S | A`.

**Thunk** — delayed computation.

**Total information cost (`C`)** — историческая цель `C = S + B + P`; exact Stage 5 measurements условны относительно receiver profile.

**Transmitted-program cost (`P`)** — точное число canonical program bits для заданного набора программ после установления wire contract.

**Unification** — решение равенств типов через substitutions.

**Weak-head normal form (WHNF)** — вычисление до выявления внешнего constructor/function/value.

**Wire format** — canonical bit representation NEX terms.

---

# Библиография

Стабильные идентификаторы источников соответствуют `docs/SOURCES.md`. Предпочтение отдаётся первичным и официальным источникам; выводы NEX не приписываются литературе.

1. **de Bruijn, N. G.** (1972). *Lambda calculus notation with nameless dummies, a tool for automatic formula manipulation, with application to the Church-Rosser theorem.* Indagationes Mathematicae (Proceedings), 75(5), 381–392. DOI: https://doi.org/10.1016/1385-7258(72)90034-0. `[SRC-0001]`
2. **Tromp, J.** *Binary Lambda Calculus.* https://tromp.github.io/cl/Binary_lambda_calculus.html. `[SRC-0002]`
3. **Milner, R.** (1978). *A Theory of Type Polymorphism in Programming.* JCSS, 17(3), 348–375. DOI: https://doi.org/10.1016/0022-0000(78)90014-4. `[SRC-0003]`
4. **Damas, L.; Milner, R.** (1982). *Principal Type-Schemes for Functional Programs.* POPL. DOI: https://doi.org/10.1145/582153.582176. `[SRC-0004]`
5. **Plotkin, G. D.** (1977). *LCF Considered as a Programming Language.* Theoretical Computer Science, 5(3), 223–255. DOI: https://doi.org/10.1016/0304-3975(77)90044-5. `[SRC-0005]`
6. **Elias, P.** (1975). *Universal codeword sets and representations of the integers.* IEEE Transactions on Information Theory, 21(2), 194–203. DOI: https://doi.org/10.1109/TIT.1975.1055349. `[SRC-0006]`
7. **Wells, J. B.** (1999). *Typability and type checking in System F are equivalent and undecidable.* Annals of Pure and Applied Logic, 98(1–3), 111–156. DOI: https://doi.org/10.1016/S0168-0072(98)00047-5. `[SRC-0007]`
8. **Schönfinkel, M.** (1924). *Über die Bausteine der mathematischen Logik.* Mathematische Annalen, 92, 305–316. `[SRC-0009]`
9. **Plotkin, G. D.** (1975). *Call-by-name, call-by-value and the lambda-calculus.* Theoretical Computer Science, 1(2), 125–159. DOI: https://doi.org/10.1016/0304-3975(75)90017-1. `[SRC-0011]`
10. **Launchbury, J.** (1993). *A Natural Semantics for Lazy Evaluation.* POPL. DOI: https://doi.org/10.1145/158511.158618. `[SRC-0012]`
11. **Sestoft, P.** (1997). *Deriving a lazy abstract machine.* Journal of Functional Programming, 7(3), 231–264. DOI: https://doi.org/10.1017/S0956796897002712. `[SRC-0013]`
12. **Barker, C.** (2001). *Iota and Jot: the simplest languages?* Archived author-maintained technical reference. `[SRC-0014]`
13. **W3C WebAssembly Working Group.** *WebAssembly Core Specification.* https://www.w3.org/TR/wasm-core/. `[SRC-0008]`
14. **The Go Project.** *The Go Programming Language Specification; math/big; testing/fuzzing documentation.* https://go.dev/ref/spec. `[SRC-0010]`
15. **Shannon, C. E.** (1948). *A Mathematical Theory of Communication.* Bell System Technical Journal, 27, 379–423 и 623–656. `[SRC-0015]`
16. **Kolmogorov, A. N.** (1965). *Three approaches to the definition of the concept “quantity of information”.* Problemy Peredachi Informatsii, 1(1), 3–11. `[SRC-0016]`
17. **Chaitin, G. J.** (1975). *A Theory of Program Size Formally Identical to Information Theory.* Journal of the ACM, 22(3), 329–340. DOI: https://doi.org/10.1145/321892.321894. `[SRC-0017]`

---

# Приложение A. Воспроизводимые артефакты

## A.1 Нормативные и исследовательские документы

- `docs/NEX-1-v0.1.md` — canonical Core specification.
- `docs/NEX-1-v0.1.ru.md` — Russian mirror.
- `docs/ARCHITECTURE.md` — architecture boundaries.
- `docs/adr/` — решения, включая ADR-0014 по receiver-assumption accounting.
- `docs/SOURCES.md` — source registry.

## A.2 Conformance

- `conformance/wire-v0.1.json`.
- `conformance/static-v0.1.json`.
- `conformance/eval-v0.1.json`.

## A.3 Benchmarks

- `benchmarks/corpus-v0.1.json`.
- `benchmarks/corpus-v0.2.json` — сохранённый resource checkpoint.
- `benchmarks/corpus-v0.3.json` — accepted Stage 4 corpus.

## A.4 Independent reconstruction

- `stage5/conformance-packet-v0.1/` — packet definition/audit.
- `stage5/build_packet.py` — reproducible packet builder.
- `independent/python/` — frozen first independent reconstruction.
- `stage5/independent-checkpoints/python-v0.1.json` — file/hash checkpoint.
- `stage5/verify_independent_checkpoint.py` — frozen-file verifier.
- `stage5/differential/run.py` — post-freeze differential runner.
- `reference/go/cmd/nexdiffprobe` — Go portable-observation adapter.

## A.5 Receiver-assumption model

- `docs/adr/0014-condition-bootstrap-cost-on-receiver-assumptions.md` — accounting decision.
- `stage5/receiver-assumptions/assumptions-v0.1.json` — canonical profile/atom registry.
- `stage5/receiver-assumptions/README.md` — interpretation/limitations.
- `stage5/validate_receiver_assumptions.py` — structural/invariant validator.
- `.github/workflows/stage5-receiver-assumptions.yml` — dedicated clean-checkout gate.

## A.6 Merge и CI evidence

- Stage 1 merge: `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`.
- Stage 2 merge: `cefe889d90a275897de31aa23c4b9742a388ec8f`.
- Stage 3 merge: `166cdc03282ea500263fdca7185f006f9b17a702`.
- Stage 4 merge: `ebffde6c8669f65dfcba98d31d261d59b48d4dd0`.
- Stage 5 protocol/packet merge: `04f4f84cce50a15638802babbe934b70e495911c`.
- Stage 5 independent/differential merge: `f500a5c5485b4cd5f6b5d9bd6bc76980f2f06cdb`.
- Final PR #8 CI: `35385704921`, `35385705027`, `35385705162` — success.
- Post-merge PR #8 CI: `35386452647`, `35386452451`, `35386452447` — success.
- Differential report: 942/942 portable matches, 0 mismatches, 0 resource asymmetries.
- Stage 5.7 first receiver-assumption PR checkpoint: `35387833962`, `35387833785`, `35387833852` — success.

---

# Приложение B. Evidence-Gated Decision Summary

| Вопрос | Текущее решение | Evidence status |
|---|---|---|
| Сохранять direct `Nat`? | Да, в v0.1 | Сильный corpus experiment против repeated `succ`; не global numeric-code optimality |
| Сохранять `Let`? | Да, в v0.1 | Measured break-even; зависит от payload/reuse |
| Сохранять erased HM? | Да, в v0.1; redesign отложен | Две реализации infer одинаковые tested schemes; bootstrap comparison ещё нет |
| CBN normative? | Да | Specification + two-implementation conformance |
| Call-by-need допустим? | Да, как optimization при observable equivalence | Stage 4 17/17 agreement |
| Оптимизировать `App` первым? | Нет current evidence | `Prim` больше на v0.3 |
| NEX меньше BLC? | Global claim отсутствует | BLC 30 vs NEX 37 бит на identical pure-lambda subset |
| NEX independently reconstructable? | Сильно поддержано на tested surface | Frozen independent implementation + 942/942 differential |
| Имеет ли смысл unconditional `B`? | Такой claim не принимается | Stage 5.7 требует explicit `B | A` |
| Можно напрямую ранжировать bootstrap при разных priors? | Нет | Prior strength в v0.1 assumption model не имеет numerical price |
| Можно дважды считать shared specification/bootstrap bits? | Нет | ADR-0014; joint `SB | A` при inseparable artifact |
| NEX глобально минимален? | Утверждение не делается | Данных недостаточно |
| `C` известно? | Нет | Receiver-conditioned `S/B/SB` artifact ещё не measured |

---

# Правило поддержки

Согласно ADR-0012, рукопись является частью исследовательского процесса. Новое воспроизводимое измерение, значимое архитектурное решение, внешний baseline, independent conformance result, proof/counterexample, stage-level conclusion, изменение модели `S/B/P/C` или опровержение/существенное уточнение гипотезы должны обновлять английскую рукопись и её русское зеркало в том же PR, если в PR явно не зафиксировано обоснование отсутствия такого обновления.
