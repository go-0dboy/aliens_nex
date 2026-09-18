# Research sources registry

This file is the durable registry of external technical sources used by the NEX project. It is not a general bibliography: a source belongs here when it materially affects a specification rule, ADR, algorithm, comparison, research-method decision, or claim.

## Source policy

1. Prefer primary papers, standards, official specifications, books from the original author, and author-maintained technical material.
2. Secondary sources may be used for orientation, but important claims should be traced to a primary or official source where practical.
3. Every source has a stable `SRC-xxxx` ID; IDs are never reused.
4. A source entry states both what NEX uses from the source and what NEX must not infer from it.
5. Experimental project results are not external sources; they belong in tests, benchmark artifacts, and experiment reports.
6. Living web sources include a review date when project conclusions depend on their current form.

---

## Foundational representation, typing, and semantics

### SRC-0001 — de Bruijn indices

**N. G. de Bruijn (1972), _Lambda calculus notation with nameless dummies, a tool for automatic formula manipulation, with application to the Church-Rosser theorem_.**

- Type: primary research paper.
- DOI: https://doi.org/10.1016/1385-7258(72)90034-0
- Used by NEX for: nameless references to enclosing binders.
- NEX impact: `Var(index)` uses zero-based de Bruijn indices.
- Limitation: the paper does not define NEX's zero-based convention, wire code, types, or primitives.

### SRC-0002 — Binary Lambda Calculus

**John Tromp, _Binary Lambda Calculus_.**

- Type: author-maintained technical/research reference.
- URL: https://tromp.github.io/cl/Binary_lambda_calculus.html
- Used by NEX for: compact self-delimiting binary lambda syntax, direct pure-lambda baseline, and a candidate universal binary basis.
- NEX impact: Stage 4 compares identical pure-lambda terms directly; Stage 5 considers BLC as a possible `A2(U)` basis.
- Limitation: BLC is untyped and does not define NEX's data, HM typing, primitive set, or total bootstrap.

### SRC-0003 — Hindley–Milner / Algorithm W

**Robin Milner (1978), _A Theory of Type Polymorphism in Programming_.**

- Type: primary research paper.
- DOI: https://doi.org/10.1016/0022-0000(78)90014-4
- Used by NEX for: HM-style polymorphism, Algorithm-W-style inference, and the distinction between inference implementation and type soundness.
- NEX impact: v0.1 uses rank-1 let-polymorphism with unification, instantiation, generalization, and occurs check.
- Limitation: Milner proves results for his formal language; those proofs do not automatically establish type soundness for NEX-specific primitives and operational semantics.

### SRC-0004 — Principal type schemes

**Luis Damas and Robin Milner (1982), _Principal Type-Schemes for Functional Programs_.**

- Type: primary research paper.
- DOI: https://doi.org/10.1145/582153.582176
- Used by NEX for: principal type schemes for HM-style let-polymorphism.
- NEX impact: supports erasing ordinary term-level type annotations in the current pure Core while reconstructing principal types.
- Limitation: it does not prove that future NEX extensions with effects or richer polymorphism preserve this property.

### SRC-0005 — PCF/LCF-style typed recursion

**Gordon D. Plotkin (1977), _LCF Considered as a Programming Language_.**

- Type: primary research paper.
- DOI: https://doi.org/10.1016/0304-3975(77)90044-5
- Used by NEX for: a small typed functional calculus with naturals, operational semantics, and fixed-point/general recursive behavior.
- NEX impact: motivates `Nat`, natural-number primitives, and typed `fix`.
- Limitation: NEX is not PCF; products/sums, HM let-polymorphism, wire format, and primitive forcing are project-specific. Higher-order definability results for PCF must not be silently generalized to all computable functionals.

### SRC-0006 — Universal integer codes

**Peter Elias (1975), _Universal codeword sets and representations of the integers_.**

- Type: primary research paper.
- DOI: https://doi.org/10.1109/TIT.1975.1055349
- Used by NEX for: universal prefix coding of integers and the basis for Elias gamma coding.
- NEX impact: `U(n)` is gamma coding of `n+1`.
- Limitation: gamma coding is not claimed optimal for every empirical integer distribution.

### SRC-0007 — System F inference boundary

**J. B. Wells (1999), _Typability and type checking in System F are equivalent and undecidable_.**

- Type: primary research paper.
- DOI: https://doi.org/10.1016/S0168-0072(98)00047-5
- Used by NEX for: a boundary against unrestricted implicit System F inference.
- NEX impact: supports choosing rank-1 HM for v0.1.
- Limitation: richer restricted systems may remain decidable and are not ruled out by this result.

### SRC-0011 — Call-by-name / call-by-value distinction

**Gordon D. Plotkin (1975), _Call-by-name, call-by-value and the lambda-calculus_.**

- Type: primary research paper.
- DOI: https://doi.org/10.1016/0304-3975(75)90017-1
- Used by NEX for: operational distinction between call-by-name and call-by-value.
- NEX impact: supports weak call-by-name as the reference strategy instead of silently using call-by-value.
- Limitation: Plotkin's calculus does not define NEX's primitives, `Let`, sums/products, or wire format.

### SRC-0012 — Lazy evaluation with sharing

**John Launchbury (1993), _A Natural Semantics for Lazy Evaluation_.**

- Type: primary research paper.
- DOI: https://doi.org/10.1145/158511.158618
- Used by NEX for: formal semantics of non-strict evaluation with sharing.
- NEX impact: theoretical precedent for memoizing implementations.
- Limitation: Launchbury's semantics is not the normative NEX machine or cost model.

### SRC-0013 — Lazy abstract machine

**Peter Sestoft (1997), _Deriving a lazy abstract machine_.**

- Type: primary research paper.
- DOI: https://doi.org/10.1017/S0956796897002712
- Used by NEX for: implementation precedent for environment/closure machines and sharing.
- NEX impact: informs, but does not prescribe, evaluator architecture.
- Limitation: NEX does not adopt Sestoft's state, stack, or instruction set as semantics.

### SRC-0018 — Principal types in combinatory logic

**J. Roger Hindley (1969), _The Principal Type-Scheme of an Object in Combinatory Logic_. Transactions of the American Mathematical Society 146, 29–60.**

- Type: primary research paper.
- DOI/stable record: https://doi.org/10.2307/1995158
- Used by NEX for: the fact that combinatory logic admits meaningful type assignment and principal type-scheme results.
- NEX impact: corrects an earlier ADR-0002 rationale that could be read as suggesting SK/SKI is intrinsically unsuitable for static typing.
- Limitation: typed combinatory logic does not by itself establish a smaller total `S+B+P` than the current NEX design.

### SRC-0023 — Call-by-need observational relationship

**John Maraist, Martin Odersky, Philip Wadler (1998), _The call-by-need lambda calculus_. Journal of Functional Programming 8(3), 275–317.**

- Type: primary research paper.
- DOI: https://doi.org/10.1017/S0956796898003037
- Used by NEX for: a call-by-need calculus that has the same observational equivalence relation as call-by-name for the studied lambda calculus.
- NEX impact: strengthens the theoretical motivation for treating sharing as an implementation strategy rather than redefining v0.1 semantics.
- Limitation: NEX-specific `fix`, naturals, sums/products, and forcing rules still require their own equivalence argument or proof.

### SRC-0025 — Polymorphic references boundary

**Mads Tofte (1990), _Type Inference for Polymorphic References_. Information and Computation 89(1), 1–34.**

- Type: primary research paper.
- DOI: https://doi.org/10.1016/0890-5401(90)90018-D
- Used by NEX for: evidence that unrestricted HM-style polymorphic generalization is not sound when terms can create and update mutable references.
- NEX impact: future mutable-memory/effect profiles must revisit v0.1's pure `Let` generalization rules instead of inheriting them unchanged.
- Limitation: this is a future-extension warning; pure NEX-1 v0.1 has no mutable references.

### SRC-0026 — Syntactic type soundness methodology

**Andrew K. Wright, Matthias Felleisen (1994), _A Syntactic Approach to Type Soundness_. Information and Computation 115(1), 38–94.**

- Type: primary research paper.
- DOI: https://doi.org/10.1006/inco.1994.1093
- Used by NEX for: preservation/progress-style metatheory methodology for HM-style programming languages and richer effects.
- NEX impact: supports a future formal NEX type-safety proof rather than treating Milner's theorem as automatically covering NEX-specific primitives.
- Limitation: it does not itself prove NEX sound.

---

## Comparative and implementation sources

### SRC-0008 — WebAssembly Core / embedding separation

**W3C WebAssembly Working Group, _WebAssembly Core Specification_.**

- Type: official living standard.
- URL: https://www.w3.org/TR/wasm-core/
- Last reviewed by NEX: 2026-09-19.
- Used by NEX for: precedent for a portable computational core specified separately from embeddings.
- Limitation: NEX does not copy WebAssembly's stack machine, module system, memory, or numeric model.

### SRC-0009 — Combinatory logic / SK basis

**Moses Schönfinkel (1924), _Über die Bausteine der mathematischen Logik_; H. B. Curry and later combinatory-logic literature.**

- Type: comparison background.
- Used by NEX for: comparison with small combinator bases such as `S` and `K`.
- NEX impact: SK/SKI remains a valid compact-basis competitor and typed variants are explicitly acknowledged through SRC-0018.
- Limitation: no global wire/bootstrap comparison is implied by the existence of a small basis.

### SRC-0014 — Iota/Jot exact encoding

**Chris Barker (2001), _Iota and Jot: the simplest languages?_**

- Type: archived primary author-maintained technical reference.
- Archived URL: https://web.archive.org/web/20201112014512/http://www.nyu.edu/projects/barker/Iota/
- Used by NEX for: exact Jot rules `K -> 11100`, `S -> 11111000`, and `AB -> 1[A][B]`.
- NEX impact: Stage 4 measures one deterministic NEX-lambda -> SK -> Jot translation.
- Limitation: the resulting length is not the shortest Jot program for the same function.

### SRC-0010 — Go reference implementation platform

**The Go Project, official language and standard-library documentation.**

- Type: official living specification/documentation.
- URL: https://go.dev/ref/spec
- Last reviewed by NEX: 2026-09-18.
- Used by NEX for: first reference implementation host, `math/big`, testing, and fuzzing.
- Limitation: Go runtime/platform semantics do not define NEX and Go source size is not receiver-neutral bootstrap cost.

---

## Information accounting and research methodology

### SRC-0015 — Shannon communication-system boundary

**Claude E. Shannon (1948), _A Mathematical Theory of Communication_.**

- Type: primary research paper.
- Original publication: Bell System Technical Journal 27, 379–423 and 623–656.
- Reprint: https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf
- Used by NEX for: separating the engineering communication system from semantic interpretation.
- NEX impact: motivates naming the digital framing boundary as `A0` rather than treating the physical layer as zero cost.
- Limitation: Shannon does not define a universal receiver prior or NEX's `A` taxonomy.

### SRC-0016 — Algorithmic description relativity

**A. N. Kolmogorov (1965), _Three approaches to the definition of the concept “quantity of information”_.**

- Type: primary research paper.
- Official record: https://www.mathnet.ru/eng/ppi68
- Used by NEX for: description length relative to an effective description method.
- NEX impact: supports conditioning executable description claims on an explicit computational prior.
- Limitation: NEX does not claim Kolmogorov-optimal encodings or a privileged alien machine.

### SRC-0017 — Self-delimiting program-size information

**Gregory J. Chaitin (1975), _A Theory of Program Size Formally Identical to Information Theory_.**

- Type: primary research paper.
- DOI: https://doi.org/10.1145/321892.321894
- Used by NEX for: self-delimiting program-size reasoning under a fixed program interpretation.
- NEX impact: reinforces that a bootstrap bit length requires an exact interpretation and input convention.
- Limitation: NEX does not adopt Chaitin's particular universal computer.

### SRC-0019 — Minimum Description Length precursor

**Jorma Rissanen (1978), _Modeling by shortest data description_. Automatica 14(5), 465–471.**

- Type: primary research paper.
- DOI: https://doi.org/10.1016/0005-1098(78)90005-5
- Used by NEX for: the methodological principle that description length depends on the model/description framework and that model cost cannot be ignored when comparing descriptions.
- NEX impact: motivates treating `C=S+B+P` as a transmitted-bit ledger under an explicit profile/encoding rather than an unconditional machine-free scalar.
- Limitation: NEX is not an MDL statistical model-selection system; the analogy is methodological.

### SRC-0024 — Independence is not independent failure

**John C. Knight, Nancy G. Leveson (1986), _An Experimental Evaluation of the Assumption of Independence in Multiversion Programming_. IEEE Transactions on Software Engineering SE-12(1), 96–109.**

- Type: primary empirical software-engineering paper.
- DOI: https://doi.org/10.1109/TSE.1986.6312924
- Used by NEX for: evidence that independently developed implementations can still exhibit correlated failures when based on the same specification.
- NEX impact: Stage 5's second implementation is evidence of reconstructability and differential conformance, not proof that both implementations are semantically correct.
- Limitation: NEX's experiment is different from safety-critical N-version voting; the source informs interpretation of independence, not a direct quantitative model.

### SRC-0027 — Differential testing

**William M. McKeeman (1998), _Differential Testing for Software_. Digital Technical Journal 10(1), 100–107.**

- Type: primary software-testing paper.
- Stable bibliographic record: https://dblp.org/rec/journals/dtj/McKeeman98
- Used by NEX for: the testing method of comparing implementations on common inputs when a simple independent oracle is unavailable.
- NEX impact: supports the Stage 5 cross-implementation harness while reinforcing that agreement is evidence, not a proof oracle.
- Limitation: differential testing cannot detect errors shared by every compared implementation.

---

## Interstellar / unknown-receiver communication prior work

### SRC-0020 — Lincos

**Hans Freudenthal (1960), _Lincos: Design of a Language for Cosmic Intercourse, Part 1_. North-Holland, 224 pp.**

- Type: primary book by the language designer.
- Bibliographic record: https://books.google.com/books?id=s7XPAAAAMAAJ
- Used by NEX for: direct prior art on constructing a formal language intended for communication with an unknown extraterrestrial intelligence, beginning from mathematical/logical concepts.
- NEX impact: NEX must not claim novelty merely for the idea of a formal language for interstellar communication.
- Limitation: Lincos does not provide NEX's compact typed binary Core, executable conformance discipline, or `S/B/P` accounting methodology.

### SRC-0021 — CosmicOS

**Paul Fitzpatrick, _CosmicOS: a next-generation Contact message_.**

- Type: author-maintained research/engineering project.
- Project page: https://cosmicos.github.io/about.html
- Source repository: https://github.com/paulfitz/cosmicos
- Last reviewed by NEX: 2026-09-19.
- Used by NEX for: prior work in which an interstellar message bootstraps mathematics and logic and then introduces executable programs and simulations; the project explicitly describes its core as a programming language.
- NEX impact: narrows NEX novelty to quantitative typed/binary/bootstrap methodology, not the general idea of transmitting programs to an unknown intelligence.
- Limitation: CosmicOS optimizes communicability and semantic teaching rather than NEX's exact total-bit accounting objective.

### SRC-0022 — Lingua Cosmica and constructive type theory

**Alexander Ollongren, Douglas A. Vakoch (2011), _Typing logic contents using Lingua Cosmica_. Acta Astronautica 68(3–4), 535–538.**

- Type: peer-reviewed research paper.
- DOI: https://doi.org/10.1016/j.actaastro.2010.08.017
- Used by NEX for: prior work applying constructive type theory to clarify logical content in messages intended for extraterrestrial intelligence.
- NEX impact: demonstrates that types in interstellar-message design are not unique to NEX; NEX's contribution must be stated more narrowly.
- Limitation: this paper does not define NEX's HM inference, binary representation, evaluator, or bootstrap ledger.

---

## How to cite sources inside project documents

Documents may reference stable IDs, for example:

```text
The nameless variable representation follows the de Bruijn approach [SRC-0001].
```

A source ID does not replace project reasoning. External literature establishes theory, prior art, or methodological cautions; NEX documents must still state what is adopted, modified, measured, rejected, or left open.

## Maintenance checklist

Before merging research- or architecture-affecting work, ask:

```text
Did the change rely on a new external theorem, algorithm, encoding,
prior-art system, research-method result, or measured baseline?
    |
    +-- no  -> no registry change required
    |
    +-- yes -> add or update the verified SRC entry in the same PR.
```

Update an entry when a living source materially changes, a stronger primary source becomes available, or NEX begins relying on a materially different claim from that source.
