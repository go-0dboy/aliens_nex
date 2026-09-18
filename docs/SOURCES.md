# Research sources registry

This file is the durable registry of external technical sources materially used by NEX. It is intentionally narrower than a general bibliography: each entry states what the project uses from the source and what the source does **not** establish for NEX.

## Source policy

1. Prefer primary papers, standards, original-author books, official records, and author-maintained technical material.
2. Use secondary sources for orientation only when a stronger source is unavailable.
3. Source IDs `SRC-xxxx` are stable and never reused.
4. New external theory, prior art, methodology, or comparison that materially changes a project claim is added here in the same research change.
5. Project measurements are not external sources; they belong in reproducible artifacts.
6. A citation is not a transfer of proof: the project must state exactly which claim is borrowed and which NEX-specific theorem/measurement remains open.

---

# Representation, typing, and semantics

## SRC-0001 — de Bruijn indices

**N. G. de Bruijn (1972), _Lambda calculus notation with nameless dummies, a tool for automatic formula manipulation, with application to the Church-Rosser theorem_.**

- DOI: https://doi.org/10.1016/1385-7258(72)90034-0
- Used for: nameless references to enclosing binders.
- NEX impact: `Var(index)` uses zero-based de Bruijn indices.
- Limitation: zero-based numbering, NEX wire syntax, primitives, and types are NEX choices.

## SRC-0002 — Binary Lambda Calculus

**John Tromp, _Binary Lambda Calculus_.**

- Author reference: https://tromp.github.io/cl/Binary_lambda_calculus.html
- Used for: exact BLC encoding, compact binary lambda representation, pure-lambda baseline, possible `A2(U)` basis.
- NEX impact: Stage 4 compares identical pure-lambda terms; Stage 5 considers BLC as a bootstrap-machine candidate.
- Limitation: BLC is untyped and does not supply NEX's HM system, data primitives, or complete bootstrap.

## SRC-0003 — Hindley–Milner / Algorithm W

**Robin Milner (1978), _A Theory of Type Polymorphism in Programming_.**

- DOI: https://doi.org/10.1016/0022-0000(78)90014-4
- Used for: let-polymorphism, Algorithm-W-style inference, syntactic/semantic type discipline.
- NEX impact: v0.1 uses rank-1 HM-style inference.
- Limitation: Milner's proof is for his formal system; it is not automatically a proof of NEX-specific primitive/evaluation soundness.

## SRC-0004 — Principal type schemes

**Luis Damas and Robin Milner (1982), _Principal Type-Schemes for Functional Programs_.**

- DOI: https://doi.org/10.1145/582153.582176
- Used for: principal type schemes and rank-1 let-polymorphism.
- NEX impact: supports recovering types instead of transmitting ordinary term annotations.
- Limitation: future effects/richer polymorphism may invalidate the same inference/generalization discipline.

## SRC-0005 — PCF/LCF-style typed recursion

**Gordon D. Plotkin (1977), _LCF Considered as a Programming Language_.**

- DOI: https://doi.org/10.1016/0304-3975(77)90044-5
- Used for: small typed functional calculus with naturals, operational semantics, and fixed-point recursion.
- NEX impact: motivates `Nat` and typed `fix`.
- Limitation: NEX is not PCF; higher-order definability claims for PCF are not silently transferred.

## SRC-0006 — Universal integer coding

**Peter Elias (1975), _Universal codeword sets and representations of the integers_.**

- DOI: https://doi.org/10.1109/TIT.1975.1055349
- Used for: the universal prefix-code family and Elias gamma coding.
- NEX impact: `U(n)` is gamma coding of `n+1`.
- Limitation: gamma is not claimed optimal for every NEX integer distribution.

## SRC-0007 — System F inference boundary

**J. B. Wells (1999), _Typability and type checking in System F are equivalent and undecidable_.**

- DOI: https://doi.org/10.1016/S0168-0072(98)00047-5
- Used for: a theoretical boundary against unrestricted implicit System F.
- NEX impact: supports the conservative v0.1 choice of rank-1 HM.
- Limitation: decidable richer restricted systems remain future candidates.

## SRC-0008 — WebAssembly Core / embedding separation

**W3C WebAssembly Working Group, _WebAssembly Core Specification_.**

- URL: https://www.w3.org/TR/wasm-core/
- Last reviewed: 2026-09-19.
- Used for: modern precedent separating portable core semantics from host embedding.
- Limitation: NEX does not copy Wasm's stack machine, memory, modules, or numeric model.

## SRC-0009 — Combinatory logic / SK basis

**Moses Schönfinkel (1924), _Über die Bausteine der mathematischen Logik_; H. B. Curry and later combinatory-logic literature.**

- Used for: compact combinator bases and binder-elimination alternatives.
- NEX impact: SK/SKI remains a serious comparison family.
- Limitation: basis size alone does not establish smaller programs or smaller total `C | A`.

## SRC-0010 — Go implementation platform

**The Go Project, official language and standard-library documentation.**

- URL: https://go.dev/ref/spec
- Used for: first reference implementation host, arbitrary-precision library, unit/fuzz tooling.
- Limitation: Go semantics/runtime do not define NEX and Go source size is not receiver-neutral `B`.

## SRC-0011 — Call-by-name / call-by-value

**Gordon D. Plotkin (1975), _Call-by-name, call-by-value and the lambda-calculus_.**

- DOI: https://doi.org/10.1016/0304-3975(75)90017-1
- Used for: operational distinction between CBN and CBV.
- NEX impact: supports explicit weak CBN rather than accidental CBV.
- Limitation: NEX's data primitives and forcing rules are separate.

## SRC-0012 — Lazy evaluation with sharing

**John Launchbury (1993), _A Natural Semantics for Lazy Evaluation_.**

- DOI: https://doi.org/10.1145/158511.158618
- Used for: formal non-strict evaluation with sharing.
- Limitation: not the normative NEX machine or cost model.

## SRC-0013 — Lazy abstract machine

**Peter Sestoft (1997), _Deriving a lazy abstract machine_.**

- DOI: https://doi.org/10.1017/S0956796897002712
- Used for: implementation precedent for lazy environment/closure machinery.
- Limitation: NEX does not adopt Sestoft's state/instruction set as semantics.

## SRC-0014 — Iota/Jot exact encoding

**Chris Barker (2001), _Iota and Jot: the simplest languages?_**

- Archived author page: https://web.archive.org/web/20201112014512/http://www.nyu.edu/projects/barker/Iota/
- Used for: exact Jot rules used by the Stage 4 fixed translation.
- Limitation: NEX's measured lambda->SK->Jot result is not the shortest possible Jot program.

## SRC-0018 — Principal types in combinatory logic

**J. Roger Hindley (1969), _The Principal Type-Scheme of an Object in Combinatory Logic_. Transactions of the American Mathematical Society 146, 29–60.**

- AMS DOI: https://doi.org/10.1090/S0002-9947-1969-0253905-6
- Used for: the fact that combinatory logic admits substantive static type assignment and principal type schemes.
- NEX impact: corrects the earlier suggestion that SK/SKI is intrinsically unsuitable for the project's static-typing objective.
- Limitation: typed combinators are not thereby proved smaller than NEX in `S+B+P`.

## SRC-0023 — Call-by-need observational relationship

**John Maraist, Martin Odersky, Philip Wadler (1998), _The call-by-need lambda calculus_. Journal of Functional Programming 8(3), 275–317.**

- DOI: https://doi.org/10.1017/S0956796898003037
- Used for: a formal call-by-need calculus with the same observational equivalence relation as call-by-name in the studied calculus.
- NEX impact: strengthens motivation for sharing as implementation rather than new semantics.
- Limitation: NEX's exact `fix`, naturals, sums/products, and primitive forcing still require a NEX-specific equivalence proof.

## SRC-0025 — Polymorphic references

**Mads Tofte (1990), _Type Inference for Polymorphic References_. Information and Computation 89(1), 1–34.**

- DOI: https://doi.org/10.1016/0890-5401(90)90018-D
- Used for: the unsoundness boundary of unrestricted HM-style polymorphism with mutable reference creation/update.
- NEX impact: future mutable/effectful profiles must revisit pure-Core `Let` generalization.
- Limitation: current NEX-1 v0.1 has no mutable references.

## SRC-0026 — Syntactic type-soundness methodology

**Andrew K. Wright, Matthias Felleisen (1994), _A Syntactic Approach to Type Soundness_. Information and Computation 115(1), 38–94.**

- DOI: https://doi.org/10.1006/inco.1994.1093
- Used for: preservation/progress-style proof methodology.
- NEX impact: motivates a NEX-specific metatheory rather than borrowing Milner's theorem by analogy.
- Limitation: the paper does not itself prove NEX sound.

---

# Information accounting and research methodology

## SRC-0015 — Shannon communication-system boundary

**Claude E. Shannon (1948), _A Mathematical Theory of Communication_.**

- Publication: Bell System Technical Journal 27, 379–423 and 623–656.
- Reprint: https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf
- Used for: separation of the engineering communication system from message semantics.
- NEX impact: physical framing below `A0` is named as a boundary rather than treated as zero cost.
- Limitation: Shannon does not define the NEX receiver prior or make mathematics semantically universal.

## SRC-0016 — Algorithmic-description relativity

**A. N. Kolmogorov (1965), _Three approaches to the definition of the concept “quantity of information”_.**

- Official record: https://www.mathnet.ru/eng/ppi68
- Used for: description length relative to an effective description method.
- NEX impact: supports conditioning executable descriptions on a declared interpretation.
- Limitation: NEX does not claim Kolmogorov-optimal programs or a privileged unknown-receiver machine.

## SRC-0017 — Self-delimiting program-size information

**Gregory J. Chaitin (1975), _A Theory of Program Size Formally Identical to Information Theory_.**

- DOI: https://doi.org/10.1145/321892.321894
- Used for: self-delimiting program-size reasoning under a specified program interpretation.
- Limitation: NEX does not adopt Chaitin's chosen universal computer.

## SRC-0019 — Minimum Description Length precursor

**Jorma Rissanen (1978), _Modeling by shortest data description_. Automatica 14(5), 465–471.**

- DOI: https://doi.org/10.1016/0005-1098(78)90005-5
- Used for: methodological evidence that a shortest-description comparison includes the chosen model/description framework.
- NEX impact: `C=S+B+P` is treated as a concrete transmitted-bit ledger under a declared profile, not an unconditional information scalar.
- Limitation: NEX is not an MDL statistical model-selection method.

## SRC-0024 — Independent versions can share failures

**John C. Knight, Nancy G. Leveson (1986), _An Experimental Evaluation of the Assumption of Independence in Multiversion Programming_. IEEE Transactions on Software Engineering SE-12(1), 96–109.**

- DOI: https://doi.org/10.1109/TSE.1986.6312924
- Used for: empirical evidence that independently produced versions can have correlated failures when built from a common problem/specification.
- NEX impact: the Python/Go agreement is evidence of reconstructability and conformance, not proof that shared errors are impossible.
- Limitation: NEX is not an N-version voting safety system; the source constrains interpretation rather than supplying a direct quantitative model.

## SRC-0027 — Differential testing

**William M. McKeeman (1998), _Differential Testing for Software_. Digital Technical Journal 10(1), 100–107.**

- Bibliographic record: https://dblp.org/rec/journals/dtj/McKeeman98
- Used for: comparing implementations on common inputs where no simple independent oracle is available.
- NEX impact: supports the Stage 5 differential method.
- Limitation: agreement cannot detect an error common to every compared implementation.

---

# Interstellar / unknown-receiver communication prior work

## SRC-0020 — Lincos

**Hans Freudenthal (1960), _Lincos: Design of a Language for Cosmic Intercourse, Part 1_. North-Holland, 224 pp.**

- Bibliographic record: https://books.google.com/books?id=s7XPAAAAMAAJ
- Used for: direct prior art on constructing a formal language for communication with unknown extraterrestrial intelligence, beginning from mathematical/logical concepts.
- NEX impact: NEX does not claim novelty for the general idea of a formal interstellar language.
- Limitation: Lincos does not provide NEX's exact typed binary Core or its empirical/accounting methodology.

## SRC-0021 — CosmicOS

**Paul Fitzpatrick, _CosmicOS: a next-generation Contact message_.**

- Project page: https://cosmicos.github.io/about.html
- Source repository: https://github.com/paulfitz/cosmicos
- Author page: https://people.csail.mit.edu/paulfitz/cosmicos.shtml
- Last reviewed: 2026-09-19.
- Used for: prior work that bootstraps mathematics/logic and then shows how to run programs and simulations.
- NEX impact: NEX does not claim novelty for transmitting programs/simulations to an unknown extraterrestrial receiver.
- Limitation: CosmicOS has a different objective; NEX's exact total-bit accounting and static Core are separate work.

## SRC-0022 — Lingua Cosmica and constructive type theory

**Alexander Ollongren, Douglas A. Vakoch (2011), _Typing logic contents using Lingua Cosmica_. Acta Astronautica 68(3–4), 535–538.**

- DOI: https://doi.org/10.1016/j.actaastro.2010.08.017
- Used for: explicit prior use of constructive type theory to clarify logical contents of ETI messages.
- NEX impact: NEX does not claim novelty merely for using types in interstellar-message design.
- Limitation: the paper does not define NEX's HM inference, binary Core, evaluator, or cost ledger.

## SRC-0028 — Science-based alien language and minimal prior knowledge

**Carl L. DeVito, Richard T. Oehrle (1990), _A Language Based on the Fundamental Facts of Science_. Journal of the British Interplanetary Society 43(12), 561–568.**

- Official society record: https://bis-space.com/shop/product/a-language-based-on-the-fundamental-facts-of-science/
- PubMed record: https://pubmed.ncbi.nlm.nih.gov/11540499/
- Used for: direct prior work constructing a language for alien communication from shared science/mathematics and explicitly considering what minimal prior knowledge is required.
- NEX impact: significantly narrows any novelty claim around “formal language + minimal shared knowledge.” NEX's candidate contribution must lie in its exact typed binary/accounting/conformance methodology.
- Limitation: the source does not provide NEX's executable wire, HM Core, receiver-conditioned bit ledger, or blind independent implementation experiment.

## SRC-0029 — Exosemiotic challenge to universal mathematics/science assumptions

**Douglas A. Vakoch (1998), _Constructing messages to extraterrestrials: an exosemiotic perspective_. Acta Astronautica 42(10–12), 697–704.**

- DOI: https://doi.org/10.1016/S0094-5765(98)00029-0
- Used for: explicit analysis of the disagreement between treating mathematics/science as straightforward common ground and treating even those concepts as potentially species-specific.
- NEX impact: `A1` is a **conditional experimental prior**, not a claim that an actual extraterrestrial receiver necessarily shares human mathematical conceptualization.
- Limitation: NEX does not resolve the philosophical/semiotic universality question; it parameterizes assumptions instead.

## SRC-0030 — Astrolinguistics / modern Lincos development

**Alexander Ollongren (2013), _Astrolinguistics: Design of a Linguistic System for Interstellar Communication Based on Logic_. Springer.**

- DOI: https://doi.org/10.1007/978-1-4614-5468-7
- Used for: broader modern treatment of Lincos/Lingua Cosmica, applied logic, types/declarations, induction, and interpretation of interstellar messages.
- NEX impact: further establishes a substantial prior research tradition in logic-based interstellar languages.
- Limitation: it does not establish NEX's quantitative compactness or bootstrap-accounting results.

---

# Citation and maintenance rule

Project documents should cite stable source IDs, for example:

```text
The nameless binder representation follows the de Bruijn approach [SRC-0001].
```

The source ID does not replace project reasoning. Before merging research- or architecture-affecting work, ask whether a new theorem, prior-art system, research-method result, encoding, or comparison materially changed a claim. If yes, this registry and the relevant research synthesis must be updated together.
