# NEX-1: минимальное архитектурно-независимое типизированное ядро для информационно-эффективной передачи вычислений

## Проектирование, формализация, исполняемая семантика, эмпирическая оценка и независимое восстановление

**Тип документа:** живая исследовательская рукопись в диссертационном стиле  
**Основной язык:** английский  
**Каноническая версия:** `RESEARCH-DISSERTATION.md`  
**Граница учтённых данных:** Stage 0–4 завершены; Stage 5 доведён до независимого восстановления и differential conformance (checkpoint 5.0–5.6), 18.09.2026  
**Проект:** NEX / `aliens_nex`

> Эта рукопись является научным синтезом исследования, поддерживаемым непосредственно в репозитории. Она ещё не оформлена под требования конкретного университета, ВАК, национальной системы аттестации или библиографического стандарта. Нормативное определение языка остаётся в `docs/NEX-1-v0.1.md`, а архитектурные и исследовательско-методологические решения — в принятых ADR.

---

## Аннотация

В работе исследуется вопрос о том, может ли очень небольшое, архитектурно-независимое и статически типизированное вычислительное ядро уменьшить объём информации, необходимой для передачи исполняемого вычислительного знания между сторонами, которые не могут предполагать общий язык программирования, архитектуру процессора, ABI, операционную систему, текстовую нотацию или общую среду реализации. Целью оптимизации является не только размер программы, а полная информационная модель

```text
C = S + B + P
```

где `S` — информация, необходимая для описания вычислительной системы, `B` — информация bootstrap, необходимая получателю для её реализации при явно заданных исходных предположениях, а `P` — передаваемый программный payload.

Экспериментальная система NEX-1 v0.1 использует шесть канонических конструкторов термов (`Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`), нулевые индексы де Брёйна, rank-1 Hindley–Milner let-полиморфизм, натуральные числа произвольной точности, небольшой фиксированный набор примитивов, явную общую рекурсию через `fix`, самоделимитирующееся бинарное представление и weak call-by-name семантику. Теоретической основой служат безымянное представление де Брёйна [1; SRC-0001], Binary Lambda Calculus как компактный сравнительный baseline [2; SRC-0002], вывод типов Hindley–Milner и principal type schemes [3,4; SRC-0003, SRC-0004], типизированная рекурсия в традиции PCF/LCF [5; SRC-0005], универсальные коды Элиаса [6; SRC-0006] и работы по call-by-name и ленивому вычислению с sharing [9–11; SRC-0011–SRC-0013].

Stages 1–3 формируют исполняемые wire-, static- и dynamic-semantics. Stage 4 фиксирует benchmark corpora и правила измерений до оптимизаций. На принятом корпусе v0.3 из 17 программ канонические NEX-программы занимают 1371 бит при 345 AST-узлах. Ссылки на примитивы являются крупнейшим измеренным источником wire-cost: 460 бит, или 33,6%. Прямое `Nat(255)` занимает 21 бит против 2300 бит у проверенной цепочки повторных `succ`. `Let` имеет измеримую точку безубыточности и не является безусловно выгодным. Экспериментальная передача только principal root type добавляет 134 бита, или 9,77% `P`, не доказывая при этом сокращение bootstrap. На одинаковом pure-lambda подмножестве Binary Lambda Calculus компактнее NEX: 30 против 37 бит, поэтому глобальное превосходство NEX по размеру программ не заявляется. Экспериментальный call-by-need evaluator сохранил наблюдаемые результаты всех 17 программ, снизив число transitions Go-reference evaluator с 226151 до 2484 в сумме; это результат об эффективности реализации, а не об информационной стоимости передачи.

Stage 5 проверяет новый вопрос: определяется ли поведение NEX спецификацией и language-neutral conformance artifacts независимо от исходной Go-реализации. До создания второй реализации был заморожен versioned conformance packet. Отдельная модель/контекст, получившая этот packet, но не `reference/go`, независимо восстановила wire codec, проверку closed scope, rank-1 HM inference и weak call-by-name evaluator на Python 3.12+ только со стандартной библиотекой. До сравнения с Go реализация прошла 17/17 integer wire vectors, 12/12 term wire vectors, 15/15 invalid wire vectors, 15/15 scope vectors, 19/19 type vectors, 21/21 evaluation vectors и 23/23 собственных теста. Затем полученная реализация была зафиксирована SHA-256 архива, и лишь после этой границы был открыт Go reference.

В последующем post-freeze differential-эксперименте сравнивались только архитектурно-независимые наблюдения. Детерминированный набор содержит 942 случая: 17 программ frozen corpus v0.3, 325 сгенерированных корректных случаев, 100 сгенерированных случаев с одной статической ошибкой и 500 сгенерированных wire-термов. Все 942 portable observations совпали; не обнаружено ни semantic mismatch, ни resource asymmetry. Это сильное эмпирическое свидетельство того, что NEX-1 v0.1 может быть независимо восстановлен по замороженному specification/conformance packet без перевода исходной Go-реализации. Результат не является формальным доказательством полноты спецификации для всех возможных входов.

Главной нерешённой переменной остаётся receiver-neutral bootstrap. `P` точно измерим на выбранных корпусах, тогда как Markdown-спецификация является лишь текстовым proxy для `S`, а размеры Go/Python-кода являются host artifacts и не равны `B`. Поэтому следующий исследовательский шаг — явное описание receiver assumption sets и условной стоимости `B | A`. До появления такого артефакта численное значение полной `C` остаётся недоказуемым, а проект не утверждает глобальную минимальность NEX или общее превосходство над альтернативными исчислениями.

**Ключевые слова:** минимальный язык программирования, архитектурно-независимые вычисления, Binary Lambda Calculus, индексы де Брёйна, Hindley–Milner, бинарное кодирование, bootstrap, информационная стоимость, call-by-name, call-by-need, независимая реализация, differential conformance, воспроизводимое исследование.

---

# 1. Введение

## 1.1 Мотивация

Большинство исполняемого программного обеспечения предполагает значительный общий контекст: кодировки символов, синтаксис, модель процессора, разрядность, объектные форматы, сервисы ОС, компиляторы, виртуальные машины и соглашения о представлении данных. Для обычной разработки это полезно. В задаче, где отправитель и получатель могут разделять только надёжный упорядоченный канал и базовые математические закономерности, эти предположения становятся скрытой стоимостью.

Поэтому вопрос исследования состоит не просто в сжатии программы. Требуется понять, как передавать вычислительное знание, если нельзя считать известными земной язык программирования, CPU, ABI, ОС, текстовую кодировку или runtime.

Однобитная программа бесполезна, если её смысл зависит от огромного непереданного интерпретатора. И наоборот, чрезмерно маленький универсальный интерпретатор может сделать все последующие программы слишком дорогими. Поэтому NEX рассматривает совместную стоимость:

```text
C = S + B + P
```

Неизвестная величина не принимается равной нулю. Исходный код на host-языке не считается bootstrap для неизвестного получателя.

## 1.2 Научная проблема

Необходимо определить, может ли компактное типизированное функциональное ядро обеспечить выгодный компромисс полной информационной стоимости для передачи вычислений общего назначения без общей вычислительной платформы и может ли это ядро быть независимо восстановлено из конечного specification/conformance package.

Проблема включает:

1. компактность представления;
2. детерминированное декодирование и валидацию;
3. восстановление типов;
4. вычислительную выразительность;
5. non-strict семантику;
6. стоимость bootstrap;
7. независимую воспроизводимость;
8. эмпирическую фальсифицируемость сравнительных утверждений.

## 1.3 Объект и предмет

**Объект:** архитектурно-независимое представление, проверка и выполнение вычислений общего назначения при крайне ограниченной передаче информации.

**Предмет:** компромиссы между стоимостью спецификации, bootstrap получателя, размером программ, выводом типов, стратегией вычисления и независимой conformance-проверкой минимального типизированного lambda-core.

## 1.4 Цель

Создать и эмпирически проверить минимальное исполняемое ядро, бинарная форма и семантика которого достаточно явны для независимого восстановления, и выработать воспроизводимую методику оценки его полной информационной стоимости относительно альтернатив.

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
13. Сохранять положительные, отрицательные и нерешённые результаты в живой исследовательской рукописи.

## 1.6 Исследовательские вопросы

**RQ1.** Можно ли задать детерминированное архитектурно-независимое самоделимитирующееся бинарное представление NEX с исполняемой conformance-проверкой?

**RQ2.** Можно ли восстанавливать principal rank-1 types без обычных term-level type annotations?

**RQ3.** Может ли простая weak call-by-name semantics сосуществовать с существенно более эффективными реализациями, сохраняющими portable observations?

**RQ4.** Какие конструкции доминируют в `P`, и оправданы ли `Let` и direct `Nat`?

**RQ5.** Как NEX сравнивается с выбранными альтернативными кодировками при контролируемых условиях?

**RQ6.** Можно ли уже вычислить `C = S + B + P`?

**RQ7.** Может ли реализация без доступа к `reference/go` восстановить то же portable wire/static/dynamic behavior из замороженного packet?

**RQ8.** При каких явно заданных предположениях получателя `A` bootstrap может быть представлен и измерен как `B | A`?

## 1.7 Рабочие гипотезы

**H1.** Безымянные bindings и компактный prefix format дают небольшую однозначную wire-форму.

**H2.** Rank-1 HM уменьшает type payload, но итоговая выгода зависит от bootstrap inference.

**H3.** `Let` и direct naturals могут уменьшать `P`, несмотря на увеличение языка.

**H4.** Weak CBN может оставаться нормативным, а sharing — быть observationally equivalent оптимизацией на проверенном pure Core.

**H5.** NEX нельзя заранее считать компактнее BLC на pure lambda terms.

**H6.** `P` недостаточно для доказательства общего превосходства.

**H7.** Достаточно явный specification/conformance packet позволяет независимому реализатору восстановить поведение NEX без reference-source guidance.

**H8.** Численная стоимость bootstrap имеет смысл только при явных receiver assumptions.

---

# 2. Теоретическая база

## 2.1 Безымянные переменные

Де Брёйн показал, что связанные переменные могут быть представлены числовой позицией вместо имени [1]. NEX принимает этот принцип и фиксирует нулевые индексы. Alpha-renaming не влияет на передаваемый терм.

## 2.2 Binary Lambda Calculus

BLC Тромпа показывает практичность компактной прямой бинарной кодировки lambda terms [2]. Для NEX он служит как историческим ориентиром, так и baseline, способным опровергнуть чрезмерные утверждения о компактности.

## 2.3 Hindley–Milner

Работа Милнера и результат Дамаса–Милнера о principal type schemes лежат в основе rank-1 let-полиморфизма NEX [3,4]. Результат Уэллса о System F используется как граница: усиление неявного полиморфизма нельзя считать бесплатно сохраняющим decidable inference [7].

## 2.4 Рекурсия

Работа Плоткина по LCF/PCF даёт исторический прецедент малого типизированного функционального языка с натуральными операциями и fixed-point recursion [5]. Конкретный primitive basis NEX является проектным решением.

## 2.5 Универсальные коды

Коды Элиаса дают семейство самоделимитирующихся кодов целых [6]. NEX определяет `U(n)` как gamma code для `n+1`.

## 2.6 Стратегия вычисления

Плоткин формализует различия call-by-name/call-by-value [9]. Launchbury и Sestoft дают основания для lazy sharing [10,11]. NEX оставляет weak CBN нормативным и рассматривает call-by-need как реализационную оптимизацию при сохранении portable result.

## 2.7 Комбинаторные альтернативы

Классическая комбинаторная логика и материалы Barker по Iota/Jot используются как сравнительный фон [8,12]. Jot-эксперимент NEX не заявляет поиск кратчайшей программы.

## 2.8 Разделение Core и окружения

WebAssembly Core используется только как современный пример архитектурного разделения portable core и embedding [13], но не как семантическая основа NEX.

---

# 3. Методология

## 3.1 Evidence-gated цикл

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

Репозиторий является долговременной памятью исследования.

## 3.2 Классы утверждений

Различаются:

1. внешние установленные результаты;
2. проектные решения NEX;
3. воспроизводимые измерения;
4. интерпретации текущих данных;
5. гипотезы и неизвестные величины.

## 3.3 Воспроизводимость

Используются language-neutral conformance JSON, unit/property/fuzz tests, frozen corpora, deterministic experiment CLIs, Git/hash checkpoints, CI clean checkout и versioned reports.

## 3.4 Frozen corpus

После сравнительных выводов версия corpus не изменяется. Неудобные результаты сохраняются; например, v0.2 хранит факт превышения default CBN budget программой `factorial-5`.

## 3.5 Протокол независимости

Вторая реализация не считается независимой только потому, что написана на другом языке. Если implementer видел первую реализацию, он может неосознанно перенести скрытые предположения.

Поэтому Stage 5 замораживает packet до blind implementation, исключает `reference/go` и фиксирует полученную вторую реализацию content hash до разрешения прямого сравнения.

## 3.6 Differential conformance

После freeze сравниваются только portable observations:

```text
wire bits
normalized principal type / portable static error
observable WHNF / portable evaluation error
```

Object layout, fresh IDs, allocations, transition counts и internal runtime representation не являются conformance criteria.

## 3.7 Информационный учёт

```text
C = S + B + P
```

- `P` — точный размер canonical program bits для заданного corpus;
- `S` — receiver-neutral specification cost, пока не сведённый к принятому артефакту;
- `B` — receiver-neutral bootstrap, пока неизвестный;
- `R` — размер host/reference implementation, не равный `B`.

Будущая оценка bootstrap должна быть условной:

```text
B | A
```

---

# 4. NEX-1 v0.1

## 4.1 Термы

```text
Term ::= Var(index)
       | Lam(body)
       | App(function, argument)
       | Let(value, body)
       | Nat(value)
       | Prim(id)
```

## 4.2 Типы

```text
T ::= a | 1 | N | T -> T | T * T | T + T
S ::= forall a1 ... an. T
```

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

## 4.4 Wire format

```text
00   U(k)   Var(k)
01   T      Lam(T)
10   T T    App(T,T)
110  T T    Let(T,T)
1110 U(n)   Nat(n)
1111 U(p)   Prim(p)
```

## 4.5 Dynamic semantics

Нормативна weak call-by-name semantics: аргументы и `Let` values задерживаются, под `Lam` до применения reduction не выполняется, примитивы форсят только необходимые части, а общая рекурсия выражается через `fix`.

---

# 5. Stages 0–3: формальная и исполняемая основа

## 5.1 Stage 0

Созданы каноническая спецификация, русские зеркала, ADR, source registry, workflow/testing rules и repository-as-memory дисциплина.

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

**Решение:** direct naturals сохраняются; глобальная оптимальность конкретного numeric code не заявляется.

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

# 7. Stage 5: независимое восстановление

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

CI evidence:

```text
reference-go        35384938291  success
stage5-independence 35384938418  success
stage5-differential 35384938381  success
```

Artifact ID `10563821507`, digest:

```text
sha256:bda41629934f1c7b8f2554726002c3af5186d8cb19df649d8fab72129f8ba62a
```

## 7.6 Интерпретация

H7 поддержана, а RQ7 получает наиболее сильный текущий ответ:

> На замороженном conformance suite, принятом benchmark corpus и детерминированных generated differential cases реализация, созданная без перевода `reference/go`, восстановила то же portable wire/static/observable dynamic behavior.

Ограничение важно: конечный набор тестов не доказывает, что prose specification однозначно определяет каждый возможный term или malformed input. Это сильное empirical conformance evidence, но не формальное доказательство semantic equivalence.

## 7.7 Неоднозначности

Independent implementation отдельно зафиксировала вопрос diagnostic precedence для терма с несколькими независимыми static defects. Python выбирает scope-first. После freeze выяснилось, что Go делает то же, но совпадение не превращается автоматически в normative rule.

Текущий differential result не выявил:

- Go semantic bug;
- independent Python semantic bug;
- contradictory conformance vector;
- новую Core ambiguity, требующую несовместимого изменения v0.1.

Поэтому global multi-error precedence остаётся implementation-specific.

## 7.8 Вывод независимого восстановления

RQ7 сильно поддержан в пределах текущей evidence horizon. NEX-1 v0.1 теперь опирается не только на co-developed specification + Go, но и на hash-frozen second reconstruction с zero-mismatch post-freeze differential checkpoint.

Главный нерешённый вопрос смещается к bootstrap: что должен знать получатель до начала передачи NEX и сколько информации требуется для восстановления системы при таких assumptions.

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

**Нет.** `P` известен, receiver-neutral `S` и `B` нет.

## RQ7

**Сильно поддержан текущими данными.** Frozen independent Python проходит packet и совпадает с Go во всех 942 post-freeze differential cases без resource asymmetry.

## RQ8

**Открыт.** Необходимо определить assumption sets и measurable `B | A`.

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

## 9.8 `S` и `B` неизвестны

Это крупнейший пробел относительно исходной цели.

## 9.9 Нет machine-checked proof

Conformance, fuzzing, freeze и differential testing остаются эмпирическими методами.

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
15. Living dissertation process, сохраняющий положительные, отрицательные и нерешённые результаты.

---

# 11. Следующее исследование: receiver assumptions и bootstrap

## 11.1 Assumption sets

Нужно явно разделить:

```text
physical/channel assumptions
binary distinguishability/order
message framing / exact length
basic mathematics
integer/self-delimiting code concepts
tree/binding concepts
type/evaluation concepts
host-machine assumptions
```

Вместо одного «универсального инопланетного prior» можно определить versioned sets `A0`, `A1`, `A2`.

## 11.2 Conditional bootstrap

Любая стоимость должна записываться:

```text
B | A
```

Если bootstrap artifact требует interpreter `Y`, `Y` должен входить либо в `A`, либо в accounting.

## 11.3 Возможные bootstrap artifacts

- tiny mathematical abstract machine;
- minimal calculus/combinator bootstrap;
- layered decoder → validator → evaluator;
- compact executable notation с явно учитываемой decoding base.

Ни один вариант заранее не объявляется правильным.

Желательная декомпозиция:

```text
B_decode
B_static
B_eval
B_total_candidate
```

Отрицательный результат допустим: если receiver-neutral artifact пока нельзя обосновать, это лучше, чем подменить его размером Go/Python source.

## 11.4 Дальнейшая верификация

Возможны third independent implementation, proof assistant для отдельных свойств, более широкий normalized corpus, полноценное erased-vs-explicit bootstrap comparison и только после evidence-stage — исследование компактности `Prim` для будущей версии.

---

# 12. Заключение

Исследование началось с идеи о том, что существующие языки проектируются для людей и известных машин, тогда как экстремально удалённый или неизвестный получатель может не разделять ни то, ни другое. Постепенно эта идея была превращена в фальсифицируемую экспериментальную систему.

NEX-1 v0.1 имеет canonical wire, principal rank-1 type reconstruction, weak call-by-name semantics, исполняемую conformance, reproducible benchmarks, отрицательные внешние сравнения и явные границы accounting. Stage 4 показал, что интуиции о «минимальном языке» недостаточны: `App` не является главным measured wire contributor на принятом corpus, direct naturals могут экономить порядки бит, `Let` имеет условную точку безубыточности, BLC может быть компактнее на pure lambda terms, а call-by-need способен резко уменьшать receiver work без изменения проверенного observable result.

Stage 5 добавил другой вид доказательности. Specification и Go implementation развивались совместно, поэтому их внутреннее согласие не доказывало независимую определённость правил. Был создан frozen packet, выданный отдельному implementation context до доступа к Go. Полученная реализация прошла все packet vectors и была зафиксирована hash до сравнения. Лишь после этого был открыт Go reference. Последующий 942-case differential дал 942 portable matches, 0 semantic mismatch и 0 resource asymmetry.

Это не доказывает глобальную корректность, минимальность или оптимальность NEX. Но существенно усиливает утверждение о том, что текущий specification/conformance package независимо восстанавливаем на проверенной семантической поверхности. Главный нерешённый вопрос теперь снова совпадает с исходной мотивацией: что должен знать получатель заранее, что требуется передать для bootstrap NEX и какова цена этой информации при явных assumptions?

Пока не появится defensible `B | A`, проект не будет заявлять численное значение полной `C` или глобальное превосходство. Сохранение этой неопределённости является частью научного метода, а не недостатком результата.

---

# Словарь терминов

**ABI (Application Binary Interface)** — соглашения бинарного взаимодействия программ и платформы.

**Alpha-equivalence** — эквивалентность lambda terms, отличающихся только именами связанных переменных.

**Architecture-neutral** — не зависящий от конкретного CPU ISA, word size, ABI, ОС или host runtime.

**AST (Abstract Syntax Tree)** — структурное представление программного терма.

**Binder** — конструкция, вводящая связанную переменную; в NEX v0.1 это `Lam` и body-часть `Let`.

**Binary Lambda Calculus (BLC)** — компактное бинарное представление нетипизированных lambda terms Тромпа [2].

**Bootstrap (`B`)** — информация, необходимая получателю для реализации достаточной вычислительной основы NEX; не равна размеру Go/Python source.

**Call-by-name (CBN)** — non-strict стратегия с delayed arguments и возможным повторным вычислением [9].

**Call-by-need** — lazy evaluation с sharing/memoization [10,11].

**Canonical representation** — уникальное проектное представление для wire/conformance.

**Conformance packet** — frozen allowlisted набор specification, ADR, vectors и observation rules для независимого implementer.

**Conformance vector** — language-neutral вход/ожидаемый результат.

**de Bruijn index** — числовая ссылка на binder position [1].

**Differential conformance** — сравнение двух implementations на одинаковых входах только по portable observations.

**Erased typing** — ordinary term wire не несёт type annotations; тип восстанавливается inference.

**Hindley–Milner (HM)** — rank-1 polymorphic inference discipline [3,4].

**Independent checkpoint** — неизменяемое hash-identified состояние второй реализации, зафиксированное до reference comparison.

**Occurs check** — проверка unification, запрещающая бесконечный self-containing type.

**Portable observation** — архитектурно-независимый результат: canonical bits, normalized type scheme, observable WHNF и т.п.

**Principal type scheme** — наиболее общая HM type scheme [4].

**Primitive (`Prim`)** — фиксированная Core operation с numeric ID.

**Receiver-neutral** — не опирающийся на незаявленные земные implementation conventions.

**Resource asymmetry** — ситуация, когда одна implementation упирается в конечный resource guard, а другая выдаёт результат; это не автоматически semantic disagreement.

**Resource refusal** — отказ из-за конечного implementation limit, отличный от malformed input, static invalidity или доказанной divergence.

**Specification cost (`S`)** — информация для передачи самих вычислительных правил.

**Thunk** — delayed computation.

**Total information cost (`C`)** — `C = S + B + P`.

**Transmitted-program cost (`P`)** — точное число canonical program bits для заданного набора программ.

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
12. **Barker, C.** (2001). *Iota and Jot: the simplest languages?* `[SRC-0014]`
13. **W3C WebAssembly Working Group.** *WebAssembly Core Specification.* https://www.w3.org/TR/wasm-core/. `[SRC-0008]`
14. **The Go Project.** *The Go Programming Language Specification; math/big; testing/fuzzing documentation.* https://go.dev/ref/spec. `[SRC-0010]`

---

# Приложение A. Артефакты воспроизводимости

## A.1 Нормативные и исследовательские

- `docs/NEX-1-v0.1.md`.
- `docs/NEX-1-v0.1.ru.md`.
- `docs/ARCHITECTURE.md`.
- `docs/adr/`.
- `docs/SOURCES.md`.

## A.2 Conformance

- `conformance/wire-v0.1.json`.
- `conformance/static-v0.1.json`.
- `conformance/eval-v0.1.json`.

## A.3 Benchmarks

- `benchmarks/corpus-v0.1.json`.
- `benchmarks/corpus-v0.2.json`.
- `benchmarks/corpus-v0.3.json`.

## A.4 Independent reconstruction

- `stage5/conformance-packet-v0.1/`.
- `stage5/build_packet.py`.
- `independent/python/`.
- `stage5/independent-checkpoints/python-v0.1.json`.
- `stage5/verify_independent_checkpoint.py`.
- `stage5/differential/run.py`.
- `reference/go/cmd/nexdiffprobe`.

## A.5 Merge и CI evidence

- Stage 1 merge: `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`.
- Stage 2 merge: `cefe889d90a275897de31aa23c4b9742a388ec8f`.
- Stage 3 merge: `166cdc03282ea500263fdca7185f006f9b17a702`.
- Stage 4 merge: `ebffde6c8669f65dfcba98d31d261d59b48d4dd0`.
- Stage 5 protocol/packet merge: `04f4f84cce50a15638802babbe934b70e495911c`.
- Stage 5 post-merge packet CI: `35383798779` — success.
- Independent/differential CI: `35384938291`, `35384938418`, `35384938381` — success.
- Differential result: 942/942 portable matches, 0 mismatches, 0 resource asymmetries.

---

# Приложение B. Evidence-gated решения

| Вопрос | Текущее решение | Статус данных |
|---|---|---|
| Сохранять direct `Nat`? | Да, в v0.1 | Сильный corpus experiment против repeated `succ`; не global numeric-code optimality |
| Сохранять `Let`? | Да | Измеримый break-even |
| Сохранять erased HM? | Да, глобальный redesign отложен | Две реализации совпадают на проверенных principal schemes; bootstrap comparison отсутствует |
| CBN нормативен? | Да | Specification + two-implementation conformance |
| Call-by-need? | Допустим как observably equivalent optimization | Stage 4 runtime evidence |
| Сначала оптимизировать `App`? | Нет оснований | `Prim` больше на v0.3 |
| NEX меньше BLC? | Глобального утверждения нет | BLC 30 vs NEX 37 на common pure-lambda subset |
| NEX независимо восстанавливаем? | Сильно поддержано на проверенной поверхности | Frozen second implementation + 942/942 post-freeze agreement |
| NEX глобально минимален? | Утверждение не делается | Данных недостаточно |
| `C` известно? | Нет | Receiver-neutral `S` и `B | A` не определены |

---

# Правило поддержки

Согласно ADR-0012, рукопись является частью исследовательского процесса. Новое воспроизводимое измерение, значимое архитектурное решение, внешний baseline, independent conformance result, proof/counterexample, stage-level conclusion, изменение модели `S/B/P/C` или опровержение/существенное уточнение гипотезы должны обновлять английскую рукопись и её русское зеркало в том же PR, если в PR явно не зафиксировано обоснование отсутствия такого обновления.
