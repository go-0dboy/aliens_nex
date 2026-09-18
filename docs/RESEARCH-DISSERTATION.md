# NEX-1: A Minimal Architecture-Neutral Typed Core for Information-Efficient Transmission of Computation

## Design, Formalization, Executable Semantics, and Empirical Evaluation

**Document type:** living dissertation-style research manuscript  
**Canonical language:** English  
**Russian mirror:** `RESEARCH-DISSERTATION.ru.md`  
**Evidence horizon:** Stages 0–4, 2026-09-18  
**Project:** NEX / `aliens_nex`

> This manuscript is a scholarly research synthesis maintained inside the project repository. It is not yet formatted for the submission rules of a particular university, national dissertation authority, or citation style. Its purpose is to preserve the research problem, literature basis, method, evidence, negative results, limitations, and conclusions as the project evolves. The normative language definition remains `docs/NEX-1-v0.1.md`; architecture decisions remain governed by Accepted ADRs.

---

## Abstract

This work investigates whether a very small, architecture-neutral, statically typed computational core can reduce the information required to transmit executable software between parties that cannot assume a shared programming language, processor architecture, ABI, operating system, textual notation, or implementation environment. The research object is the representation and reconstruction of general-purpose computation under severe communication constraints. The optimization target is not program payload alone, but a total information model

```text
C = S + B + P
```

where `S` denotes the information required to specify the computational system, `B` denotes the receiver-neutral bootstrap information required to realize it, and `P` denotes transmitted program payload.

The resulting experimental system, NEX-1 v0.1, uses six canonical term constructors (`Var`, `Lam`, `App`, `Let`, `Nat`, `Prim`), zero-based de Bruijn indices, rank-1 Hindley–Milner let-polymorphism, direct natural-number literals, products and sums through fixed primitives, explicit general recursion through `fix`, a self-delimiting prefix binary representation, and weak call-by-name semantics. The design draws on de Bruijn's nameless lambda notation [1], Binary Lambda Calculus as a compact binary-lambda comparison point [2], Hindley–Milner inference and principal type schemes [3,4], PCF/LCF-style typed recursion [5], Elias universal integer coding [6], and established distinctions between call-by-name and lazy sharing [9–11].

The research proceeds through executable stages. Stage 1 establishes canonical wire encoding and decoding with conformance vectors and resource-limit separation. Stage 2 establishes closed-scope validation, principal type inference, unification, occurs checking, and primitive type schemes. Stage 3 defines and implements weak call-by-name dynamic semantics, including laziness-sensitive behavior and fixed-point recursion. Stage 4 freezes benchmark corpora and measurement rules before optimization, then empirically evaluates the current design and controlled alternatives.

On the frozen 17-program corpus v0.3, canonical NEX programs occupy 1,371 bits over 345 AST nodes. Primitive references are the largest measured wire contributor at 460 bits (33.6%), followed by variables at 286 bits (20.9%), applications at 264 bits (19.3%), naturals at 244 bits (17.8%), lambdas at 84 bits (6.1%), and `Let` at 33 bits (2.4%). `Let` exhibits a measurable break-even point rather than being uniformly beneficial. Direct `Nat(n)` literals strongly outperform the tested repeated-`succ` construction; at `n = 255`, the canonical literal uses 21 bits versus 2,300 bits for the tested successor chain. An experimental envelope transmitting only the inferred principal root type adds 134 bits to the corpus, or 9.77% program-payload overhead, but this does not establish whether explicit typing would reduce bootstrap cost enough to compensate.

On the identical pure-lambda subset of three programs, Binary Lambda Calculus is smaller than NEX (30 versus 37 bits), demonstrating that NEX cannot claim universal program-size superiority. A project-defined tiny postfix stack encoding uses 1,529 bits over the full corpus versus 1,371 bits for NEX, but this structural comparison reuses NEX integer and primitive conventions and is not an independent total-bootstrap comparison. An experimental call-by-need implementation preserves the same observable weak-head results on all 17 accepted programs while reducing reference-evaluator transition counts from 226,151 to 2,484 in aggregate (98.90%), with most of the gain concentrated in recursive or repeatedly forced workloads. This is implementation evidence, not transmission-cost evidence.

The central negative result is equally important: total information cost `C` is not yet numerically known. Program cost `P` is exact for the selected corpus, but the current Markdown specification size is only a textual proxy for `S`, the Go implementation size is only a host/reference proxy `R`, and the actual receiver-neutral bootstrap `B` remains unknown. Consequently, this work does not claim that NEX is globally minimal, globally smaller than Binary Lambda Calculus, or optimal under the total-cost objective. The principal research contribution to date is an executable, falsifiable, and reproducible framework in which those stronger claims can eventually be tested rather than assumed.

**Keywords:** minimal programming language, architecture-neutral computation, binary lambda calculus, de Bruijn indices, Hindley–Milner, program encoding, bootstrap, information cost, call-by-name, call-by-need, conformance, reproducible benchmarking.

---

# 1. Introduction

## 1.1 Research motivation

Most programming-language and executable-format design assumes a large body of shared context: character encodings, textual syntax, processor models, word sizes, object formats, operating-system services, compiler conventions, or virtual-machine specifications. That assumption is usually reasonable for terrestrial software engineering. It becomes problematic in a communication scenario where the sender and receiver may share only an ordered bit channel and basic mathematical regularities.

The motivating thought experiment for NEX is therefore deliberately extreme: how can one transmit not merely data, but reusable computational knowledge, when no terrestrial language, CPU, ABI, operating system, or source notation may be assumed?

A naive answer is to minimize the program text alone. That objective is insufficient. A one-bit program is useless if it requires an enormous receiver-side specification and implementation whose semantics have not been communicated. Conversely, an extremely small interpreter may force every later program to become much larger. The project therefore treats the communication problem as a joint cost problem:

```text
C = S + B + P
```

This model is intentionally abstract. At the present stage, `P` is directly measurable for canonical NEX programs, while `S` and especially `B` are only partially characterized. The inability to assign a defensible scalar to all three terms is treated as an unresolved research result, not filled with an arbitrary zero or host-language source size.

## 1.2 Research problem

The research problem is to determine whether a compact typed functional core can provide a favorable total-information trade-off for transmitting general-purpose computation without assuming a shared implementation platform.

The problem has several coupled dimensions:

1. **Representational compactness.** Programs should admit a small, unambiguous, self-delimiting binary representation.
2. **Semantic reconstructability.** The receiver must be able to recover scope, types, and execution meaning from communicated rules rather than hidden host assumptions.
3. **Computational expressiveness.** The core must retain general-purpose recursion and compositional data construction.
4. **Verification burden.** A receiver should be able to reject malformed or ill-typed programs deterministically.
5. **Bootstrap burden.** Reducing transmitted program bits must not be evaluated independently of the cost of defining and realizing the language.
6. **Empirical falsifiability.** Claims of compactness should be measured against explicit alternatives and frozen workloads rather than asserted from aesthetic minimalism.

## 1.3 Object and subject of research

**Object of research:** architecture-neutral representation and execution of general-purpose computation under severe communication constraints.

**Subject of research:** the trade-offs among formal specification size, receiver bootstrap complexity, transmitted-program size, static verifiability, and evaluation strategy in a minimal typed lambda-based core.

## 1.4 Research goal

The goal is to construct and empirically evaluate a minimal executable core whose semantics and binary form are explicit enough to support independent reconstruction, while establishing a reproducible method for evaluating whether its total communication cost can eventually outperform alternative computational representations.

## 1.5 Research objectives

The work decomposes the goal into the following objectives:

1. define a minimal architecture-neutral Core and its invariants;
2. define a canonical self-delimiting wire representation;
3. implement executable encode/decode conformance;
4. define and implement static scope/type semantics;
5. define and implement dynamic semantics without hidden machine behavior;
6. create language-neutral conformance artifacts;
7. freeze benchmark corpora before optimization-driven comparisons;
8. measure constructor-level wire cost and internal design trade-offs;
9. compare selected external/structural baselines under explicit assumptions;
10. distinguish exact program cost from implementation and bootstrap proxies;
11. identify which design choices are supported, contradicted, or unresolved by current evidence;
12. preserve the results as a living research record that accumulates new evidence without erasing negative findings.

## 1.6 Research questions

The present manuscript organizes the investigation around the following research questions.

**RQ1.** Can a small typed lambda core be given a deterministic, architecture-neutral, self-delimiting binary representation with executable conformance tests?

**RQ2.** Can static validity and principal types be reconstructed without transmitting ordinary term-level type annotations?

**RQ3.** Can the dynamic semantics remain simple and non-strict while allowing materially more efficient receiver implementations that preserve observable results?

**RQ4.** Which current Core constructs dominate transmitted program cost, and do seemingly non-minimal constructs such as `Let` and direct `Nat` literals justify their presence empirically?

**RQ5.** How does NEX program payload compare with selected alternative encodings under controlled, explicitly limited comparisons?

**RQ6.** Can the total objective `C = S + B + P` already be evaluated numerically, and if not, what evidence is still missing?

## 1.7 Working hypotheses

The project began with hypotheses rather than conclusions.

**H1.** A nameless lambda representation with compact prefix encoding can provide a small unambiguous program wire format while retaining direct structural decoding.

**H2.** Hindley–Milner-style erased typing can reduce repeated program payload because many useful terms admit inferable principal type schemes [3,4], but its total benefit depends on the still-unknown bootstrap cost of inference.

**H3.** Adding a small number of semantic conveniences such as direct naturals and `Let` may reduce total program payload even though they enlarge the language definition.

**H4.** Weak call-by-name can serve as a simple normative semantics while call-by-need sharing can be an observationally equivalent implementation optimization on the tested pure fragment [9–11].

**H5.** NEX should not be assumed to dominate highly compressed untyped lambda encodings such as BLC on pure lambda terms; comparative performance must be measured [2].

**H6.** Program payload alone is insufficient to establish overall superiority; a defensible result ultimately requires receiver-neutral models of specification and bootstrap cost.

## 1.8 Claimed contribution at the current evidence horizon

The current contribution is not a proof of globally minimal computation. It is the construction of a coherent research artifact consisting of:

- a normative typed Core and binary wire format;
- a reference implementation with executable static and dynamic semantics;
- language-neutral conformance artifacts;
- explicit resource-limit separation from language validity;
- frozen benchmark corpora;
- reproducible internal and external comparison tools;
- a total-information accounting model that preserves unknowns rather than hiding them;
- an evidence-gated architectural process in which negative results can prevent premature redesign claims.

---

# 2. Theoretical and Related-Work Basis

## 2.1 Nameless binding and de Bruijn indices

Variable names are convenient for humans but costly and semantically redundant in a canonical transmission format. De Bruijn showed that bound variables can be represented without names by numerical references determined by binder structure [1; SRC-0001]. NEX adopts this principle but makes its own concrete choice of zero-based indices.

The practical consequence is that alpha-renaming does not affect canonical terms. A human source-level distinction such as `lambda x. x` versus `lambda y. y` disappears from the transmitted representation. This is directly aligned with the communication goal: variable spelling carries no computational information.

## 2.2 Binary Lambda Calculus

Tromp's Binary Lambda Calculus demonstrates that lambda terms using de Bruijn-style variables can be represented in a compact binary syntax [2; SRC-0002]. BLC is important to NEX in two different roles. First, it establishes that compact direct binary lambda representations are practical research objects rather than merely theoretical possibilities. Second, it provides an external compactness baseline that can falsify overly broad NEX claims.

NEX does not copy the BLC grammar. NEX introduces static typing, `Let`, direct natural literals, and fixed primitives; BLC remains untyped. This difference is precisely why the Stage 4 comparison is restricted to the identical pure-lambda subset rather than silently charging BLC for NEX-specific built-ins.

## 2.3 Hindley–Milner inference and principal type schemes

Milner's polymorphic type discipline provides decidable inference for a useful rank-1 let-polymorphic language [3; SRC-0003]. Damas and Milner established the principal-type-scheme property for the corresponding functional fragment [4; SRC-0004]. NEX uses these ideas to reconstruct types from terms rather than transmitting ordinary type annotations in the canonical v0.1 wire representation.

This choice is not treated as globally optimal. Wells' undecidability result for unrestricted System F typability/type checking [7; SRC-0007] is used as a boundary reminder: stronger implicit polymorphism cannot be assumed to retain the same decidable inference properties. NEX therefore deliberately remains at a restricted rank-1 HM-style point in v0.1.

## 2.4 Typed recursion and numeric computation

Plotkin's LCF/PCF work provides a precedent for a small typed functional computational language containing natural-number behavior and fixed-point recursion [5; SRC-0005]. NEX similarly retains explicit general recursion through a typed `fix` primitive. NEX's exact primitive set, product/sum support, wire representation, and HM `Let` are project-specific and should not be attributed to PCF.

## 2.5 Self-delimiting integer representation

Elias introduced universal codeword families for positive integers, including the gamma-code family [6; SRC-0006]. NEX defines `U(n)` as Elias gamma coding of `n + 1`, allowing non-negative integers, de Bruijn indices, and primitive IDs to use a self-delimiting representation. The offset by one and the placement of `U(n)` inside the term grammar are NEX-specific design choices.

## 2.6 Evaluation strategy

Plotkin's analysis of call-by-name and call-by-value establishes that evaluation strategy is semantically significant [9; SRC-0011]. NEX chooses weak call-by-name as its normative reference strategy. Launchbury's natural semantics for lazy evaluation formalizes sharing in non-strict computation [10; SRC-0012], while Sestoft derives implementation machinery for lazy evaluation and sharing [11; SRC-0013]. These sources motivate the experimental question tested in Stage 4: whether call-by-need can reduce receiver work while preserving the same NEX observable results.

The project does not adopt Launchbury's heap semantics or Sestoft's abstract machine as normative NEX semantics. They provide theoretical and implementation precedent for a possible optimized realization.

## 2.7 Combinatory alternatives and Jot

Small combinator bases such as `S` and `K` are historically important alternatives to named or nameless lambda syntax [8; SRC-0009]. Barker's Iota/Jot material provides an exact Jot mapping for `K`, `S`, and application used by the Stage 4 experiment [12; SRC-0014]. NEX does not claim that the deterministic lambda-to-SK translation used in the benchmark yields shortest Jot programs; the experiment measures one reproducible translation pipeline only.

## 2.8 Portable core versus host embedding

The WebAssembly Core specification is not a semantic basis for NEX, but it is a useful modern architectural precedent for separating a portable computational core from host/environment embedding [13; SRC-0008]. NEX adopts the separation principle while rejecting WebAssembly's concrete stack-machine instruction set, numeric model, module system, and memory model as NEX Core requirements.

---

# 3. Research Methodology

## 3.1 Artifact-centered experimental method

The project follows an iterative artifact-and-evidence method. A language-design claim is not considered established merely because it is plausible or elegant. Each meaningful subsystem is developed through the cycle:

```text
Problem
 -> Contract
 -> Invariant
 -> Failing test / executable example
 -> Implementation
 -> Verification
 -> Diff review
 -> Status checkpoint
```

This makes the implementation an experimental instrument as well as an engineering artifact. The repository, not chat history, is treated as durable research memory.

## 3.2 Evidence classes

NEX documentation explicitly separates five evidence classes:

1. **Established external result** — supported by primary literature or official specification.
2. **NEX design decision** — a project choice recorded in specification or Accepted ADR.
3. **Reproducible NEX measurement** — produced by repository artifacts and automated commands.
4. **Inference from current evidence** — a project interpretation that remains limited by the experiment.
5. **Open hypothesis / unknown** — not yet resolved by available evidence.

This distinction prevents repetition from converting a hypothesis into an apparent fact.

## 3.3 Reproducibility discipline

Where feasible, prose claims are backed by executable artifacts:

- wire golden/conformance vectors;
- malformed-input rejection cases;
- scope/type conformance vectors;
- evaluator conformance vectors;
- unit/property/fuzz tests;
- frozen benchmark corpora;
- deterministic experiment CLIs;
- clean-checkout GitHub Actions runs.

The final Stage 4 report is recomputed by `reference/go/cmd/nexreport`; it does not copy values from documentation.

## 3.4 Frozen-corpus rule

Benchmark-driven design is vulnerable to post hoc workload selection. ADR-0010 therefore requires corpus versions to become immutable once comparative results are published from them. New tasks require a new corpus version. The preserved `corpus-v0.2.json`, in which `factorial-5` exceeded the default CBN transition budget, is an example of retaining an inconvenient result rather than silently rewriting the workload.

## 3.5 Total-information accounting

The central accounting model is

```text
C = S + B + P
```

with the following current interpretation:

- `P`: exact canonical program-wire cost for a specified frozen corpus;
- `S`: receiver-neutral specification transmission cost, not yet represented by one accepted artifact;
- `B`: receiver-neutral bootstrap transmission cost, currently unknown;
- `R`: host/reference implementation size, reported only as a proxy and never substituted for `B`.

The current inability to calculate `C` is treated as a substantive result.

## 3.6 Scope of empirical claims

Measurements are corpus- and translation-specific unless otherwise demonstrated. For example, the finding that `Prim` is the largest wire contributor applies to corpus v0.3; it is not presented as a theorem about all NEX programs. Likewise, the BLC comparison applies only to the identical pure-lambda subset, and the Jot result applies only to the documented translation.

---

# 4. NEX-1 v0.1 Design

## 4.1 Canonical term language

NEX-1 v0.1 defines exactly six term constructors:

```text
Term ::= Var(index)
       | Lam(body)
       | App(function, argument)
       | Let(value, body)
       | Nat(value)
       | Prim(id)
```

The representation intentionally excludes source variable names and human formatting.

## 4.2 Type language

The Core type grammar is:

```text
T ::= a | 1 | N | T -> T | T * T | T + T
S ::= forall a1 ... an. T
```

Static semantics follow rank-1 HM-style inference, including fresh instantiation, let-generalization, unification, and an occurs check [3,4].

## 4.3 Primitive basis

Core v0.1 fixes eleven primitive IDs:

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

IDs 11–31 remain reserved Core space; profile-specific primitives begin at 32. The separation allows the universal core to remain independent of files, displays, networks, machine memory, and other environment-specific facilities.

## 4.4 Wire representation

Non-negative integers use `U(n)`, defined as Elias gamma coding of `n + 1` [6]. Terms use a prefix code:

```text
00   U(k)   Var(k)
01   T      Lam(T)
10   T T    App(T,T)
110  T T    Let(T,T)
1110 U(n)   Nat(n)
1111 U(p)   Prim(p)
```

This form is structurally decodable without textual tokenization.

## 4.5 Dynamic semantics

The normative reference semantics are weak call-by-name. Arguments and `Let` values are delayed; evaluation does not reduce under a lambda before application. Primitive forcing is selective: `ifz` forces the numeric condition but only the selected branch, `pair` can retain delayed components, and sum elimination selects only the matching branch. General recursion is explicit through `fix`.

---

# 5. Stage 0 — Research and Architectural Baseline

Stage 0 established the project as a research process rather than an unstructured language-design exercise. It introduced the canonical English specification, required Russian mirrors for primary documents, architecture/domain/workflow/testing documents, ADR governance, repository-as-memory rules, and a primary-source registry.

This stage produced no compactness result, but it established a methodological precondition for later claims: architectural reasoning, rejected alternatives, sources, and verification status must be durable and reviewable.

A dedicated source registry was then added. Its policy prioritizes primary papers, official standards, and author-maintained references and requires each source entry to state both what NEX relies on and what NEX does not infer from that source.

**Stage 0 conclusion.** Before optimizing a minimal language, the project needed a mechanism to prevent silent semantic drift and retrospective rewriting of rationale. The ADR/source/status system became part of the research method.

---

# 6. Stage 1 — Canonical Wire Foundation

## 6.1 Objective

Stage 1 tested RQ1 at the representation layer: can canonical NEX terms be converted to and from an exact bit stream with deterministic error behavior?

## 6.2 Implementation

The Go reference implementation introduced arbitrary-precision `U(n)` encode/decode, an in-memory six-constructor term representation, canonical term encode/decode, exact-versus-prefix decoding APIs, malformed-input errors, and resource limits distinct from malformed syntax.

This distinction is important. A mathematically valid NEX natural or deeply nested term may exceed implementation resources without becoming an invalid NEX encoding. The implementation therefore reports resource-limit refusal separately.

## 6.3 Conformance evidence

The completed Stage 1 conformance corpus contained:

- 17 integer vectors;
- 12 term vectors;
- 15 invalid exact-input vectors.

Representative normative encodings include:

```text
Var(0)                    001
Nat(0)                    11101
Prim(0)                   11111
Lam(Var(0))               01001
Lam(App(Prim(1),Var(0)))  01101111010001
```

The reference implementation passed formatting, static vetting, unit tests, conformance tests, and fuzz/property runs in clean CI.

## 6.4 Stage 1 conclusion

RQ1 is supported for the implemented v0.1 wire grammar: canonical NEX terms can be encoded and decoded deterministically with executable conformance evidence. This is not a formal proof of codec correctness, but it is stronger than a prose-only specification.

---

# 7. Stage 2 — Static Validation and Principal Type Inference

## 7.1 Scope validity

Wire validity does not imply program validity. For zero-based de Bruijn indices, a variable `Var(k)` is in scope only when `k` refers to an enclosing binder. `Lam` increases binder depth for its body. `Let(value, body)` validates the value in the current environment and the body in an environment extended by one binding.

A dedicated closed-scope validator separates binding errors from typing errors.

## 7.2 Type representation and substitutions

Stage 2 introduced internal type variables, unit, natural, function, product, and sum types together with quantified type schemes. It implemented free-type-variable calculation, substitutions, substitution composition, fresh instantiation, and environment-sensitive generalization.

A canonical type-variable renaming procedure normalizes implementation-internal IDs so independent implementations can compare principal schemes without depending on fresh-variable numbering.

## 7.3 Unification and occurs check

Algorithm-W-style inference requires unification. The implementation includes an occurs check so an equation such as

```text
T0 = T0 -> N
```

is rejected rather than constructing an infinite type. A canonical example is self-application `lambda x. x x`, which is not typable in the supported HM fragment.

## 7.4 Primitive schemes and inference

A single Core primitive table records ID, name, arity, and type scheme. `InferClosed` performs scope validation, primitive validation, and principal type inference across all six term constructors.

The conformance corpus includes positive principal-type cases and negative cases for out-of-scope variables, unknown primitives, type mismatch, and occurs-check failure.

## 7.5 Type-annotation decision

NEX-1 v0.1 does not transmit ordinary term-level type annotations. This is a design choice, not a completed optimality result. The theoretical motivation is that HM supports principal type inference [3,4], but the research question is total information cost, not type-theory elegance. ADR-0007 therefore keeps annotations erased in v0.1 while explicitly deferring a global comparison against explicit or certified typing.

## 7.6 Stage 2 conclusion

RQ2 is supported at the functional level: the reference implementation reconstructs principal type schemes for the supported closed Core without ordinary term annotations. However, the question of whether this minimizes `S + B + P` remains unresolved and is revisited empirically in Stage 4.

---

# 8. Stage 3 — Dynamic Semantics and Reference Evaluator

## 8.1 Evaluation model

Stage 3 defined an environment-based weak call-by-name evaluator using closures and delayed arguments. This avoids repeated syntactic substitution and aligns naturally with de Bruijn environments.

## 8.2 Laziness-sensitive behavior

The stage tested not only arithmetic results but non-strictness itself. Programs equivalent to

```text
(lambda x. 7) divergingTerm
ifz 0 42 divergingTerm
fst (pair 1 divergingTerm)
```

must return `7`, `42`, and `1` respectively without evaluating the unnecessary computation. These cases operationalize the distinction between non-strict semantics and an accidentally strict host implementation [9].

## 8.3 Curried primitives and fixed point

Primitives support partial application. `fix` provides general recursion. Divergence is possible by design, so evaluator fuel/depth limits are implementation controls rather than language-validity rules.

## 8.4 Conformance

`conformance/eval-v0.1.json` provides language-neutral evaluation examples, and fuzz/property tests check deterministic observable behavior for successful evaluations. English and Russian normative dynamic-semantics text were synchronized at stage completion.

## 8.5 Stage 3 conclusion

RQ3 is partially supported before optimization: a simple weak call-by-name semantics is executable and conformance-tested. Whether a sharing implementation can preserve results while reducing receiver work becomes an empirical Stage 4 question.

---

# 9. Stage 4 — Empirical Validation and Benchmarking

## 9.1 Measurement contract and corpora

Stage 4 intentionally froze measurement rules before optimization. Corpus v0.1 established ten foundation programs. Corpus v0.2 is preserved as a negative/resource checkpoint because `factorial-5` exceeded the default 1,000,000-transition non-memoizing CBN budget. Corpus v0.3 is the accepted 17-program extended corpus.

The v0.3 workloads include pure lambda terms, primitive arithmetic/control, pairs, sums, polymorphic `Let`, recursion, multiplication, factorial, Fibonacci, a small recognizer, and repeated expensive let binding.

## 9.2 Aggregate wire profile

The exact canonical aggregate is:

| Metric | Value |
|---|---:|
| Programs | 17 |
| Wire bits | 1,371 |
| AST nodes | 345 |

Constructor attribution is:

| Constructor | Bits | Share |
|---|---:|---:|
| `Prim` | 460 | 33.6% |
| `Var` | 286 | 20.9% |
| `App` | 264 | 19.3% |
| `Nat` | 244 | 17.8% |
| `Lam` | 84 | 6.1% |
| `Let` | 33 | 2.4% |

The early hypothesis that `App` would dominate transmitted bits is not supported by this corpus. Primitive references are the largest measured contributor. The correct interpretation is corpus-specific: future compactness experiments should prioritize primitive/profile encoding, but no universal constructor distribution is claimed.

## 9.3 `Let` versus duplication

A controlled experiment measured the wire break-even of sharing a closed payload through `Let` rather than duplicating it.

For a 5-bit payload:

| Repetitions | Effect of `Let` versus duplication |
|---:|---:|
| 2 | +4 bits |
| 3 | +2 bits |
| 4 | tie |
| 8 | −8 bits |

For the tested 14-bit payload, two repetitions already save 5 bits. The evidence therefore rejects both extreme claims that `Let` is always beneficial or always wasteful. It has a measurable break-even that depends on payload size and reuse count.

**Decision:** retain `Let` in v0.1.

## 9.4 Direct `Nat` versus repeated `succ`

Direct `Nat(n)` was compared with a simple computational construction based on repeated `succ` from zero. At `n = 0` the tested forms tie. For every tested `n` from 1 through 255, the direct literal is smaller. At the endpoint:

```text
Nat(255)          21 bits
succ-chain(255) 2300 bits
saved            2279 bits
```

This does not prove Elias-gamma `Nat` is globally optimal among numeric encodings. It does strongly reject the idea that the current Core should remove direct naturals in favor of the tested successor construction.

**Decision:** retain direct `Nat` in v0.1.

## 9.5 Erased HM versus transmitted principal root type

A non-normative hybrid envelope appended only the inferred closed principal top-level type scheme using an experimental compact type code. The canonical term itself remained unchanged.

Aggregate result:

```text
erased NEX terms       1371 bits
root type payload       134 bits
hybrid total           1505 bits
overhead               +9.77%
```

The relative overhead is highly workload-dependent. Small polymorphic functions pay heavily: identity +240%, constant +222.2%, composition +200%. Larger programs with final type `N` require only four experimental root-type bits, making the percentage much smaller (for example, factorial-4 about +1.67%).

This experiment measures only `Delta P`. A principal root type does not replace internal typing judgments, and no receiver-neutral explicit checker/bootstrap was implemented. Therefore the evidence does not settle the total-cost comparison between erased HM and an explicit/certified alternative.

**Decision:** retain erased HM in v0.1; defer global typing-format redesign until real bootstrap/checker evidence exists.

## 9.6 External and structural baselines

### 9.6.1 Binary Lambda Calculus

BLC was compared only on the identical pure-lambda subset (`identity`, `constant`, `composition`) to avoid silently replacing NEX built-ins with Church encodings.

| Program | NEX | BLC |
|---|---:|---:|
| identity | 5 | 4 |
| constant | 9 | 7 |
| composition | 23 | 19 |
| **Total** | **37** | **30** |

BLC is seven bits smaller on this restricted common subset. This falsifies any blanket claim that NEX's current lambda encoding is always more compact than BLC [2]. It does not establish BLC superiority for the full NEX computational basis because the compared languages expose different built-ins.

### 9.6.2 Jot through deterministic SK translation

The same pure-lambda subset produced 288 bits under the documented lambda-to-SK-to-Jot translation, compared with 37 NEX bits. The Jot mapping itself follows Barker's published encoding [12], but the bracket-abstraction path is a project experiment and not a shortest-program search. The result therefore characterizes the selected reproducible translation only.

### 9.6.3 Tiny postfix structural baseline

A project-defined three-bit postfix structural encoding was applied to all 17 programs while reusing NEX integer and primitive conventions:

```text
NEX canonical wire   1371 bits
tiny postfix stack   1529 bits
difference           +158 bits (+11.52%)
```

This supports the narrower claim that the selected NEX tree encoding is smaller than this selected postfix structural encoding on corpus v0.3. Because the baseline reuses NEX's numeric and primitive assumptions, it is not an independent `S+B+P` competitor.

## 9.7 Call-by-name versus call-by-need

A separate experimental call-by-need evaluator with sharing/memoization was implemented. Normative v0.1 semantics remained weak call-by-name. Every accepted v0.3 program was required to produce the same observable weak-head result under both evaluators.

All 17 programs agreed observationally.

Aggregate reference-only counters:

```text
CBN transitions             226151
call-by-need transitions      2484
saved                       223667
reduction                    98.90%
memo hits                       237
programs with fewer transitions 6/17
```

Representative workloads:

```text
countdown-5            127 -> 92
multiplication-3-4     446 -> 301
factorial-4         209315 -> 895
fibonacci-5           7424 -> 512
let-reuse-expensive    8710 -> 560
```

The aggregate is dominated by expensive recursive/reused computations. Most small programs show no transition reduction at all. Therefore the conclusion is not that call-by-need is universally faster by 98.90%; rather, sharing can eliminate catastrophic repeated work in important workload classes while preserving tested observables.

These transition counts are Go-reference metrics, not portable Core costs and not terms in `C`. Call-by-need may require additional bootstrap/runtime machinery.

**Decision:** keep weak call-by-name normative; permit call-by-need as an implementation optimization when observable equivalence is preserved.

## 9.8 Total-information accounting result

For corpus v0.3:

```text
P exact canonical program cost       1371 bits
canonical English spec Markdown     23440 UTF-8 bytes
raw Markdown text proxy            187520 bits
selected Go reference Core         43013 UTF-8 bytes
B receiver-neutral bootstrap       unknown
C total                             not numerically computable
```

The Markdown value is transparent but is not accepted as `S`: it assumes English, UTF-8, Markdown, and terrestrial textual conventions. The Go source value is `R`, not `B`: it assumes Go syntax, compiler/runtime behavior, machine memory, and many other shared conventions. Treating either proxy as receiver-neutral would answer the research question by assumption.

**Decision:** total-cost superiority remains unresolved; unknown `B` is never treated as zero.

## 9.9 Reproducible report and decision gate

`reference/go/cmd/nexreport` recomputes the principal Stage 4 measurements from the frozen corpus and experiment/reference functions. The completed decision gate is recorded in ADR-0011.

The final clean-checkout Stage 4 verification run on the completed branch was GitHub Actions run `35373798219`, which passed the reference verification pipeline including experiments and existing fuzz/property tests.

---

# 10. Discussion and Answers to the Research Questions

## 10.1 RQ1 — deterministic architecture-neutral wire representation

**Current answer: supported for NEX-1 v0.1.** The canonical term grammar, self-delimiting integer encoding, exact/prefix decoding distinction, error taxonomy, language-neutral vectors, and automated round-trip/fuzz evidence establish a functioning wire layer. A formal proof and a second independent decoder are still missing.

## 10.2 RQ2 — reconstructing types without ordinary annotations

**Current answer: functionally supported, globally unresolved.** The reference implementation infers principal schemes for the supported HM fragment without ordinary term annotations. Stage 4 shows that one hybrid root-type envelope adds 9.77% program payload on corpus v0.3, but no real alternative checker/bootstrap exists. Therefore erased HM remains a justified v0.1 choice, not a proven total-cost optimum.

## 10.3 RQ3 — simple semantics with efficient implementations

**Current answer: strongly supported on the tested corpus.** Weak CBN provides a simple normative semantics; a separate call-by-need implementation preserved all tested observables while drastically reducing repeated work on several recursive workloads. The result supports semantic/implementation separation, but does not quantify additional bootstrap cost.

## 10.4 RQ4 — which constructs dominate, and are `Let`/`Nat` justified?

**Current answer: `Prim` dominates this corpus; `Let` and direct `Nat` are empirically justified against the tested alternatives.** `Prim` contributes 33.6% of v0.3 wire bits. `Let` has a measurable break-even. Direct `Nat` strongly outperforms repeated successor construction. The data therefore rejects simplistic "fewer constructors is always smaller" reasoning.

## 10.5 RQ5 — comparison with alternatives

**Current answer: mixed, as expected for a research comparison.** BLC is smaller on the identical pure-lambda subset. NEX is smaller than the selected tiny postfix structural baseline on the full corpus. The Jot translation is much larger but is not a shortest-program result. No total-cost external winner can be declared because bootstrap/specification accounting is not yet comparable.

## 10.6 RQ6 — numerical total information cost

**Current answer: no.** `P` is exact for frozen NEX corpora, but receiver-neutral `S` and particularly `B` are not yet available. This is the highest-value unresolved problem after Stage 4.

---

# 11. Threats to Validity and Limitations

## 11.1 Corpus size and representativeness

Corpus v0.3 contains only 17 programs. It intentionally covers multiple language features, but it cannot represent all likely software distributions. Constructor percentages must therefore remain corpus-specific.

## 11.2 Hand construction and translation bias

Some terms and baseline translations are direct project constructions rather than products of independently optimized compilers. The project records translation classifications, but hand-designed terms may still favor one representation. Future work should compare canonical translations from common source semantics and independently optimized variants.

## 11.3 Single primary implementation

Go is currently the only full reference implementation. Shared misunderstandings between specification and implementation can survive all internal tests. A second implementation developed from the specification and conformance artifacts is required to strengthen conformance claims.

## 11.4 Runtime counters are implementation-specific

Transition counts and depth values describe the Go reference evaluators. They are useful comparative engineering evidence but are not architecture-neutral units of computation.

## 11.5 Explicit-type experiment is incomplete

The hybrid experiment transmits only the principal root type. It does not implement a full alternative typed wire format, proof object, or receiver checker. It therefore cannot establish the bootstrap savings side of the trade-off.

## 11.6 External baseline scope

The BLC comparison is deliberately narrow; the tiny stack baseline reuses NEX conventions; the Jot result depends on one deterministic bracket abstraction. These choices protect against hidden assumptions but limit the breadth of conclusions.

## 11.7 Unknown receiver-neutral specification and bootstrap

The largest validity gap relative to the motivating objective is that `S` and `B` do not yet have accepted receiver-neutral artifacts. Until they do, total-cost claims remain incomplete by construction.

## 11.8 No formal proof of full correctness

Fuzzing, conformance vectors, and clean CI are empirical evidence, not machine-checked proofs of decoder, type-inference, or evaluator correctness.

---

# 12. Research Contributions to Date

At the present evidence horizon, the work contributes:

1. a concrete architecture-neutral typed Core with a canonical binary representation;
2. an executable distinction between wire validity, scope validity, type validity, and evaluation resource refusal;
3. language-neutral conformance corpora for wire, static semantics, and dynamic semantics;
4. an evidence-gated process for language design in which benchmarks are frozen before optimization;
5. constructor-level exact wire attribution for a frozen corpus;
6. measured break-even evidence for `Let` and strong evidence for direct `Nat` against repeated `succ`;
7. a quantified first experiment on erased versus transmitted root type information;
8. controlled comparison with BLC, Jot translation, and a structural stack baseline;
9. an observational call-by-name/call-by-need experiment demonstrating large implementation-level savings on selected workloads;
10. a total-information accounting model that explicitly refuses to equate host source size with receiver-neutral bootstrap cost;
11. a living dissertation process that preserves positive, negative, and unresolved findings as the project continues.

---

# 13. Future Research

## 13.1 Independent conformance implementation

The next major evidentiary step should be a second implementation built from the public specification and conformance artifacts rather than by translating the Go code. Agreement would test whether the specification actually determines behavior independently.

## 13.2 Receiver-neutral bootstrap artifact

The most important unresolved variable is `B`. Future research should define what information a receiver must obtain to reconstruct enough computational machinery to decode, validate, type-check, and evaluate NEX without assuming Go, a conventional CPU, ASCII/UTF-8, files, or an operating system.

A bootstrap artifact must itself have a transmission representation before its size can enter `C` honestly.

## 13.3 Receiver-neutral specification cost

Similarly, the current Markdown file is not `S`. Research is needed into a self-describing mathematical/specification bootstrap: how primitives, bit parsing, binding, typing, and evaluation can be introduced from weaker shared assumptions.

## 13.4 Primitive-reference encoding

Since `Prim` is the largest measured constructor category on corpus v0.3, future compactness experiments should investigate primitive ID/profile encoding before redesigning `App` merely by intuition. Any incompatible wire change requires a new Core version and an ADR.

## 13.5 Full typing alternatives

A meaningful erased-versus-explicit comparison requires an actual alternative verifier/checker and an accounting model for its bootstrap, not only root-type transmission.

## 13.6 Broader corpora and source-language normalization

Future corpora should include larger structural programs and common-source translations so multiple target encodings can be compared from equivalent source semantics. Corpus expansion must preserve the freeze/version discipline.

## 13.7 Formal verification

Selected components, especially decoder prefix properties, substitution/unification invariants, and evaluator equivalence, are candidates for theorem-prover or proof-assistant formalization after the executable design stabilizes.

---

# 14. Conclusion

This research began from a deceptively simple idea: if existing programming languages are designed for human programmers and known machines, what computational representation should be used when the sender cannot assume either?

The work to date shows that the answer cannot be reduced to choosing the shortest syntax. NEX-1 v0.1 demonstrates that a small typed lambda-based Core can have a compact canonical binary form, infer principal types without ordinary annotations, and execute under explicitly non-strict semantics. More importantly, the staged implementation makes these claims executable and falsifiable.

The empirical results resist a simplistic success narrative. Direct naturals are strongly justified against the tested successor construction, and `Let` has a real size break-even. Yet Binary Lambda Calculus is smaller on the measured pure-lambda subset. Call-by-need can reduce repeated evaluation work by orders of magnitude on some programs, but that says nothing by itself about communication cost. Primitive references, not application nodes, are the largest measured wire contributor on the current corpus. And the central optimization target `C = S + B + P` remains unresolved because the receiver-neutral bootstrap has not yet been defined.

These are not defects to conceal; they are the principal value of the current research stage. The project has moved from an intuition about a "small language" to a reproducible experimental framework in which design hypotheses can be retained, contradicted, or refined by evidence. The next decisive question is no longer whether another AST constructor should be shaved by a bit. It is whether an independent receiver can reconstruct the system from a genuinely receiver-neutral specification and bootstrap, and what that bootstrap actually costs.

---

# Glossary

**ABI (Application Binary Interface)** — conventions governing binary interaction between compiled components and a platform.

**Alpha-equivalence** — equivalence of lambda terms that differ only in bound-variable names. Canonical de Bruijn representation removes those names from NEX wire terms.

**Architecture-neutral** — defined without dependence on a particular processor ISA, word size, ABI, operating system, or host-language runtime.

**AST (Abstract Syntax Tree)** — structural in-memory representation of a program term.

**Binder** — language construct that introduces a bound variable; in NEX v0.1, `Lam` and the body side of `Let` introduce binders.

**Binary Lambda Calculus (BLC)** — John Tromp's compact binary representation of untyped lambda terms, used here as a comparative baseline [2].

**Bootstrap (`B`)** — receiver-neutral information required to realize enough machinery to process NEX. It is currently unknown and must not be replaced by Go source size.

**Call-by-name (CBN)** — non-strict evaluation strategy in which an argument is not evaluated before substitution/use and may be recomputed when used repeatedly [9]. NEX v0.1 uses weak CBN as normative reference semantics.

**Call-by-need** — lazy evaluation with sharing/memoization, avoiding repeated evaluation of the same delayed computation [10,11]. Experimental in NEX, not normative.

**Canonical representation** — the unique project-defined structural/wire form used for conformance and measurement.

**Conformance vector** — language-neutral input/expected-output artifact used to test whether an implementation follows the specification.

**de Bruijn index** — numeric reference to a binding depth rather than a variable name [1]. NEX uses zero-based indices.

**Erased typing** — type information is not carried in ordinary term wire syntax and is reconstructed by inference.

**Hindley–Milner (HM)** — rank-1 polymorphic type-inference discipline used as the basis of NEX static semantics [3,4].

**Occurs check** — unification check preventing a type variable from being unified with a type containing itself.

**Principal type scheme** — most general type scheme from which other valid types can be instantiated for an HM term [4].

**Primitive (`Prim`)** — fixed Core operation identified by a numeric ID, such as `succ`, `ifz`, or `pair`.

**Receiver-neutral** — not relying on terrestrial implementation conventions that have not themselves been communicated.

**Resource refusal** — implementation failure due to configured finite limits, distinct from malformed syntax, type invalidity, or proven semantic divergence.

**Specification cost (`S`)** — information required to communicate the computational rules themselves. No accepted receiver-neutral scalar exists yet.

**Thunk** — delayed computation consisting conceptually of a term and its environment.

**Total information cost (`C`)** — research objective `C = S + B + P`.

**Transmitted-program cost (`P`)** — exact number of canonical program bits for a specified set of programs.

**Unification** — process of solving equality constraints between types by constructing substitutions.

**Weak-head normal form (WHNF)** — result evaluated only enough to reveal its outer constructor/function/value form rather than recursively normalizing all components.

**Wire format** — canonical transmitted bit representation of NEX terms.

---

# Bibliography

The stable project source identifiers correspond to `docs/SOURCES.md`. Primary/official sources are preferred; project-specific conclusions are not attributed to the literature.

1. **de Bruijn, N. G.** (1972). *Lambda calculus notation with nameless dummies, a tool for automatic formula manipulation, with application to the Church-Rosser theorem.* Indagationes Mathematicae (Proceedings), 75(5), 381–392. DOI: https://doi.org/10.1016/1385-7258(72)90034-0. `[SRC-0001]`
2. **Tromp, J.** *Binary Lambda Calculus.* Author-maintained technical reference. https://tromp.github.io/cl/Binary_lambda_calculus.html. `[SRC-0002]`
3. **Milner, R.** (1978). *A Theory of Type Polymorphism in Programming.* Journal of Computer and System Sciences, 17(3), 348–375. DOI: https://doi.org/10.1016/0022-0000(78)90014-4. `[SRC-0003]`
4. **Damas, L.; Milner, R.** (1982). *Principal Type-Schemes for Functional Programs.* Proceedings of POPL. DOI: https://doi.org/10.1145/582153.582176. `[SRC-0004]`
5. **Plotkin, G. D.** (1977). *LCF Considered as a Programming Language.* Theoretical Computer Science, 5(3), 223–255. DOI: https://doi.org/10.1016/0304-3975(77)90044-5. `[SRC-0005]`
6. **Elias, P.** (1975). *Universal codeword sets and representations of the integers.* IEEE Transactions on Information Theory, 21(2), 194–203. DOI: https://doi.org/10.1109/TIT.1975.1055349. `[SRC-0006]`
7. **Wells, J. B.** (1999). *Typability and type checking in System F are equivalent and undecidable.* Annals of Pure and Applied Logic, 98(1–3), 111–156. DOI: https://doi.org/10.1016/S0168-0072(98)00047-5. `[SRC-0007]`
8. **Schönfinkel, M.** (1924). *Über die Bausteine der mathematischen Logik.* Mathematische Annalen, 92, 305–316. Comparative combinatory-logic background; registry overview in `[SRC-0009]`.
9. **Plotkin, G. D.** (1975). *Call-by-name, call-by-value and the lambda-calculus.* Theoretical Computer Science, 1(2), 125–159. DOI: https://doi.org/10.1016/0304-3975(75)90017-1. `[SRC-0011]`
10. **Launchbury, J.** (1993). *A Natural Semantics for Lazy Evaluation.* Proceedings of POPL. DOI: https://doi.org/10.1145/158511.158618. `[SRC-0012]`
11. **Sestoft, P.** (1997). *Deriving a lazy abstract machine.* Journal of Functional Programming, 7(3), 231–264. DOI: https://doi.org/10.1017/S0956796897002712. `[SRC-0013]`
12. **Barker, C.** (2001). *Iota and Jot: the simplest languages?* Archived author-maintained technical reference: https://web.archive.org/web/20201112014512/http://www.nyu.edu/projects/barker/Iota/. `[SRC-0014]`
13. **W3C WebAssembly Working Group.** *WebAssembly Core Specification.* https://www.w3.org/TR/wasm-core/. `[SRC-0008]`
14. **The Go Project.** *The Go Programming Language Specification; math/big; testing/fuzzing documentation.* https://go.dev/ref/spec. `[SRC-0010]`

---

# Appendix A. Reproducibility and Project Artifacts

## A.1 Normative and architectural artifacts

- `docs/NEX-1-v0.1.md` — canonical Core specification.
- `docs/NEX-1-v0.1.ru.md` — Russian mirror.
- `docs/ARCHITECTURE.md` — architecture boundaries.
- `docs/adr/` — accepted/rejected/deferred decisions.
- `docs/SOURCES.md` — external research source registry.

## A.2 Conformance artifacts

- `conformance/wire-v0.1.json` — integer/term/error wire vectors.
- `conformance/static-v0.1.json` — scope and type conformance.
- `conformance/eval-v0.1.json` — dynamic semantics observations.

## A.3 Benchmark artifacts

- `benchmarks/corpus-v0.1.json` — frozen foundation corpus.
- `benchmarks/corpus-v0.2.json` — preserved resource-limit checkpoint.
- `benchmarks/corpus-v0.3.json` — accepted 17-program Stage 4 corpus.

## A.4 Reference and experiment tools

- `reference/go/nex/` — Go reference Core implementation.
- `reference/go/cmd/nexbench` — canonical benchmark measurement.
- `reference/go/cmd/nexexperiment` — internal `Let`/`Nat` experiments.
- `reference/go/cmd/nextypeexperiment` — hybrid root-type experiment.
- `reference/go/cmd/nexbaseline` — BLC/Jot/stack comparisons.
- `reference/go/cmd/nexstrategy` — CBN versus call-by-need experiment.
- `reference/go/cmd/nexaccount` — `S/B/P/R` accounting report.
- `reference/go/cmd/nexreport` — consolidated Stage 4 report.
- `reference/go/verify.sh` — clean verification entry point.

## A.5 Stage completion evidence

- Stage 1 merge: `e9bf6ff0bbc19fd36c27451572d7b617ebabc9f8`.
- Stage 2 merge: `cefe889d90a275897de31aa23c4b9742a388ec8f`.
- Stage 3 merge: `166cdc03282ea500263fdca7185f006f9b17a702`.
- Stage 4 final pre-merge clean-checkout CI: GitHub Actions run `35373798219` — success.

Stage 4 remains pending merge at this manuscript version; the dissertation must be updated when the stage is merged and when later stages produce material research evidence.

---

# Appendix B. Evidence-Gated Decision Summary

| Question | Current decision | Evidence status |
|---|---|---|
| Keep direct `Nat`? | Keep in v0.1 | Strong corpus experiment against repeated `succ`; not global numeric-code optimality |
| Keep `Let`? | Keep in v0.1 | Measured break-even; depends on payload/reuse |
| Keep erased HM? | Keep in v0.1, defer global redesign | Working inference + hybrid root-type `Delta P`; bootstrap comparison missing |
| Is CBN normative? | Yes | Existing semantics/conformance |
| Use call-by-need? | Allowed optimization when observably equivalent | 17/17 corpus agreement; major reference-runtime savings on 6 workloads |
| Optimize `App` first? | No evidence for priority | `Prim` is larger on v0.3 |
| Optimize `Prim`/profiles? | Priority for future experiments | Largest measured v0.3 wire category |
| Is NEX smaller than BLC? | No global claim | BLC wins 30 vs 37 bits on identical pure-lambda subset |
| Is NEX globally smallest? | No claim | Evidence insufficient |
| Is total `C` known? | No | Receiver-neutral `S` and especially `B` unresolved |

---

# Maintenance Rule

Per ADR-0012, this manuscript is part of the research process. A future change that creates a defensible new measurement, research-significant architectural decision, external baseline, independent conformance result, formal proof/counterexample, stage-level conclusion, revised `S/B/P/C` model, or falsification/qualification of a prior hypothesis must update this English manuscript and its Russian mirror in the same PR unless the PR explicitly documents why no research-text change is required.
