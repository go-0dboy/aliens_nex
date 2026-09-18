# Research sources registry

This file is the durable registry of external technical sources used by the NEX project.

It is not a general bibliography. A source belongs here when it materially influences a specification rule, ADR, algorithm, benchmark baseline, compatibility decision, or research claim.

## Source policy

1. Prefer primary papers, standards, official specifications, and author-maintained technical material.
2. Secondary sources may be used for orientation, but important technical claims should be traced to a primary or official source where practical.
3. Every source receives a stable ID: `SRC-0001`, `SRC-0002`, ... IDs are never reused.
4. When a new external idea, theorem, algorithm, encoding, standard, or comparative baseline materially affects project work, the same change MUST add or update its entry here.
5. The entry MUST state what NEX relies on from the source. A citation alone is insufficient.
6. The entry SHOULD also state what NEX does **not** infer from the source when over-reading it would be easy.
7. Living standards or mutable web specifications MUST include an access/review date and SHOULD be rechecked when a decision depends on their current contents.
8. Reusing a source already registered does not require a duplicate entry; refer to its stable source ID.
9. Experimental project results are not external sources. They belong in reproducible benchmark/test artifacts and may reference this registry for external baselines.

---

## Current foundational sources

### SRC-0001 — de Bruijn indices

**N. G. de Bruijn (1972), _Lambda calculus notation with nameless dummies, a tool for automatic formula manipulation, with application to the Church-Rosser theorem_.**

- Type: primary research paper
- DOI: https://doi.org/10.1016/1385-7258(72)90034-0
- Used by NEX for: the principle of replacing bound-variable names with numeric references to enclosing binders; conceptual basis for the canonical nameless representation.
- Current project impact: NEX-1 v0.1 uses zero-based de Bruijn indices in `Var(index)`.
- Important limitation: the paper does not define the NEX wire format, zero-based convention, type system, or primitive set; those are NEX design decisions.

### SRC-0002 — Binary Lambda Calculus

**John Tromp, _Binary Lambda Calculus_.**

- Type: author-maintained technical reference / research implementation material
- URL: https://tromp.github.io/cl/Binary_lambda_calculus.html
- Used by NEX for: evidence that lambda terms with de Bruijn-style variables can be encoded directly as compact self-delimiting binary syntax; comparative baseline for description size.
- Current project impact: motivates a binary prefix term representation and the Stage 4 direct pure-lambda comparison against BLC.
- Important limitation: BLC is untyped and its exact constructor/variable encoding is not the NEX wire format. NEX's static typing and `Let`/`Nat`/`Prim` design are separate choices. Stage 4 compares identical pure lambda terms directly and does not silently Church-encode NEX built-ins.

### SRC-0003 — Hindley–Milner / Algorithm W

**Robin Milner (1978), _A Theory of Type Polymorphism in Programming_.**

- Type: primary research paper
- DOI: https://doi.org/10.1016/0022-0000(78)90014-4
- Used by NEX for: compile-time polymorphic type discipline and Algorithm W-style type inference.
- Current project impact: NEX-1 v0.1 adopts HM-style rank-1 let-polymorphism and plans an Algorithm-W-style reference inference implementation.
- Important limitation: NEX is not ML; its term grammar, primitives, wire representation, and evaluation strategy are project-specific.

### SRC-0004 — Principal type schemes

**Luis Damas and Robin Milner (1982), _Principal Type-Schemes for Functional Programs_.**

- Type: primary research paper
- DOI: https://doi.org/10.1145/582153.582176
- Used by NEX for: the principal-type-scheme basis of Hindley–Milner-style let-polymorphism.
- Current project impact: supports the design goal that most term-level type annotations need not be transmitted because a principal type scheme can be inferred for the supported fragment.
- Important limitation: this does not prove that every future NEX extension will preserve principal types or decidable inference.

### SRC-0005 — PCF-style typed general recursion

**Gordon D. Plotkin (1977), _LCF Considered as a Programming Language_.**

- Type: primary research paper
- DOI: https://doi.org/10.1016/0304-3975(77)90044-5
- Used by NEX for: the model of a small typed functional language with operational semantics, natural-number computation, and fixed-point/general recursive behavior.
- Current project impact: motivates the `N`/`Nat` computational basis and typed `fix` primitive used to retain general-purpose computational expressiveness.
- Important limitation: NEX is not a reproduction of PCF/LCF; its product/sum primitives, binary representation, HM let-polymorphism, and exact semantics are separate design choices.

### SRC-0006 — Universal/self-delimiting integer codes

**Peter Elias (1975), _Universal codeword sets and representations of the integers_.**

- Type: primary research paper
- DOI: https://doi.org/10.1109/TIT.1975.1055349
- Official record: https://ieeexplore.ieee.org/document/1055349/
- Used by NEX for: the family of universal prefix codes for integers and the basis for Elias gamma coding.
- Current project impact: NEX-1 v0.1 defines `U(n)` as Elias gamma coding of `n + 1` so that non-negative integers receive a self-delimiting representation.
- Important limitation: the choice to encode `n + 1`, and its placement inside NEX term encoding, are NEX-specific.

### SRC-0007 — System F inference boundary

**J. B. Wells (1999), _Typability and type checking in System F are equivalent and undecidable_.**

- Type: primary research paper
- DOI: https://doi.org/10.1016/S0168-0072(98)00047-5
- Used by NEX for: the theoretical boundary showing that Curry-style System F typability/type checking is undecidable in general.
- Current project impact: supports the v0.1 decision to prefer rank-1 HM-style inference rather than unrestricted implicit System F polymorphism.
- Important limitation: this result does not imply that all richer-than-HM type systems are unsuitable; specific restricted systems may remain decidable and could be evaluated in future ADRs.

### SRC-0008 — WebAssembly Core / embedding separation

**W3C WebAssembly Working Group, _WebAssembly Core Specification_.**

- Type: official living standard
- Current publication: https://www.w3.org/TR/wasm-core/
- Specification index: https://webassembly.org/specs/
- Last reviewed by NEX: 2026-09-18
- Used by NEX for: a modern comparison point showing a portable computational core specified independently from concrete embedding/environment interfaces, with explicit binary representation and validation.
- Current project impact: supports the architectural distinction between NEX Core semantics and optional machine/environment profiles.
- Important limitation: NEX does not copy the WebAssembly instruction set, stack machine, numeric model, module system, or memory model. WebAssembly is a comparison and architectural precedent, not the NEX execution model.

---

## Comparative / candidate sources

These sources are relevant to alternatives already discussed or benchmarked, but they are not normative foundations of NEX-1 v0.1.

### SRC-0009 — Combinatory logic / SK basis

**Combinatory logic literature; historical basis in Schönfinkel and Curry.**

- Type: comparison background
- Reference overview: https://encyclopediaofmath.org/wiki/Combinatory_logic
- Historical work identified there: M. Schönfinkel, _Über die Bausteine der mathematischen Logik_, Mathematische Annalen 92 (1924), 305–316.
- Used by NEX for: comparison with very small combinator bases such as `S` and `K`.
- Current project impact: ADR-0002 records pure SKI-style Core as rejected for v0.1 while retaining it as a benchmark candidate. Stage 4 uses a fixed SK bracket-abstraction translation only as an intermediate step for the Jot baseline.
- Important limitation: this general source does not define the exact binary Jot encoding. Stage 4's exact Jot program mapping is grounded separately in SRC-0014.

### SRC-0014 — Chris Barker Iota/Jot exact encoding

**Chris Barker, _Iota and Jot: the simplest languages?_ (2001; author page preserved by the Internet Archive).**

- Type: archived primary author-maintained technical reference
- Archived URL: https://web.archive.org/web/20201112014512/http://www.nyu.edu/projects/barker/Iota/
- Last reviewed by NEX: 2026-09-18
- Used by NEX for: the exact Jot semantics and the author's mapping from combinatory logic to Jot: `K -> 11100`, `S -> 11111000`, and application `AB -> 1[A][B]`.
- Current project impact: Stage 4.5 uses those exact bit rules after a separately documented deterministic NEX-pure-lambda -> SK bracket abstraction. The resulting number is a reproducible translation cost.
- Important limitation: the Stage 4 bracket-abstraction algorithm is a NEX experiment choice, not a claim that Barker prescribed that exact lambda-to-SK translator. The measured Jot length is not claimed to be the shortest Jot program for the same function; for example Barker's Jot semantics gives the empty program the identity meaning.

---

## Receiver-assumption / information-accounting sources

### SRC-0015 — Shannon communication-system boundary

**Claude E. Shannon (1948), _A Mathematical Theory of Communication_.**

- Type: primary research paper
- Original publication: _Bell System Technical Journal_, Vol. 27, pp. 379–423 and 623–656, July/October 1948.
- Reprint checked by NEX: https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf
- Last reviewed by NEX: 2026-09-18
- Used by NEX for: the explicit decomposition of a communication system into source/transmitter/channel/receiver/destination and the methodological separation between engineering transmission and semantic interpretation.
- Current project impact: supports Stage 5.7's decision to name the digital channel/framing substrate as an explicit assumption boundary (`A0`) rather than silently mixing raw physical signalling with NEX semantics.
- Important limitation: Shannon does not define the NEX receiver prior, does not justify that binary framing is universally natural, and does not assign zero cost to establishing a channel. The `A0/A1/A2(U)` taxonomy is a NEX research model.

### SRC-0016 — Kolmogorov algorithmic description relativity

**A. N. Kolmogorov (1965), _Three approaches to the definition of the concept “quantity of information”_.**

- Type: primary research paper
- Official record: https://www.mathnet.ru/eng/ppi68
- Publication: _Problemy Peredachi Informatsii_, 1(1), 3–11, 1965.
- Last reviewed by NEX: 2026-09-18
- Used by NEX for: the algorithmic approach to information in which description length is defined through an effective description method rather than as a machine-free absolute scalar.
- Current project impact: supports treating the computational prior/reference machine as part of the condition for a bootstrap measurement rather than pretending an executable bit length is unconditional.
- Important limitation: NEX does not claim its concrete bootstrap artifacts are Kolmogorov-optimal, nor does this source identify a privileged universal machine for an unknown receiver.

### SRC-0017 — Chaitin self-delimiting program-size information

**Gregory J. Chaitin (1975), _A Theory of Program Size Formally Identical to Information Theory_.**

- Type: primary research paper
- DOI: https://doi.org/10.1145/321892.321894
- IBM Research record: https://research.ibm.com/publications/a-theory-of-program-size-formally-identical-to-information-theory
- Last reviewed by NEX: 2026-09-18
- Used by NEX for: the program-size formulation based on self-delimiting programs and the methodological importance of fixing the program interpretation before assigning bit lengths.
- Current project impact: supports requiring an exact program/data and self-delimiting input convention when Stage 5.8 instantiates `A2(U)`.
- Important limitation: NEX does not adopt Chaitin's particular universal computer as its bootstrap machine, and a self-delimiting bootstrap candidate remains conditional on the selected `U`.

---

## Implementation platform sources

### SRC-0010 — Go reference implementation platform

**The Go Project, official language and standard-library documentation.**

- Type: official living language specification and standard-library documentation
- Language specification: https://go.dev/ref/spec
- Arbitrary-precision integers: https://go.dev/src/math/big/doc.go
- Testing/fuzzing package: https://pkg.go.dev/testing
- Current release reviewed by NEX: Go 1.27, released 2026-08-19
- Last reviewed by NEX: 2026-09-18
- Used by NEX for: selecting Go as the first reference-implementation host; relying on static host typing, standard-library arbitrary-precision `big.Int`, and built-in unit/fuzz testing without third-party codec dependencies.
- Current project impact: ADR-0005 chooses Go for `reference/go/`; the module intentionally declares Go 1.23 compatibility while using only stable facilities documented by current upstream Go.
- Important limitation: Go's runtime, garbage collector, integer implementation, package model, or execution semantics do not define NEX. Go is only a reference implementation vehicle.

---

## Dynamic-semantics sources

### SRC-0011 — Call-by-name / call-by-value operational distinction

**Gordon D. Plotkin (1975), _Call-by-name, call-by-value and the lambda-calculus_.**

- Type: primary research paper
- DOI: https://doi.org/10.1016/0304-3975(75)90017-1
- Publisher record: https://www.sciencedirect.com/science/article/pii/0304397575900171
- Used by NEX for: foundational operational distinction between call-by-name and call-by-value and the fact that evaluation strategy can change observable termination/equality behavior.
- Current project impact: supports keeping the Stage 3 reference evaluator aligned with the already accepted weak call-by-name NEX-1 v0.1 semantics rather than silently switching to call-by-value.
- Important limitation: Plotkin's calculi do not define NEX's `Let`, primitive table, product/sum forcing rules, wire format, or exact runtime representation; those remain NEX decisions.

### SRC-0012 — Natural semantics for lazy evaluation with sharing

**John Launchbury (1993), _A Natural Semantics for Lazy Evaluation_.**

- Type: primary research paper
- DOI: https://doi.org/10.1145/158511.158618
- ACM record: https://dl.acm.org/doi/10.1145/158511.158618
- Used by NEX for: a formal model of non-strict evaluation with sharing/heap-like bindings.
- Current project impact: provides theoretical grounding for a future call-by-need/memoizing implementation that may optimize the reference call-by-name evaluator while preserving observable Core results.
- Important limitation: Stage 3's first reference evaluator intentionally does **not** adopt Launchbury-style sharing as its normative model; NEX primitive forcing and conformance rules are project-specific.

### SRC-0013 — Lazy abstract machine / implementation precedent

**Peter Sestoft (1997), _Deriving a lazy abstract machine_.**

- Type: primary research paper
- DOI: https://doi.org/10.1017/S0956796897002712
- Publisher record: https://www.cambridge.org/core/journals/journal-of-functional-programming/article/deriving-a-lazy-abstract-machine/A1CF974BD4A92A2A9B47287F55B68DB6
- Used by NEX for: implementation precedent connecting environment/closure-style abstract machines, call-by-name ancestry, and a call-by-need machine with sharing, constructors, and base values.
- Current project impact: informs the Stage 3 choice to keep the first evaluator environment-based while deferring sharing/memoization to a later optimized implementation.
- Important limitation: NEX does not adopt Sestoft's machine state, stack format, instruction set, or cost model as normative semantics.

---

## How to cite sources inside project documents

When useful, project documents may refer to stable IDs, for example:

```text
The nameless variable representation follows the de Bruijn approach [SRC-0001].
```

For normative specifications and ADRs, a source ID does not replace the explanation of the project decision. External literature establishes prior theory or precedent; the ADR must still explain why NEX adopts, modifies, rejects, or defers it.

## Maintenance checklist for future work

Before merging a research- or architecture-affecting change, ask:

```text
Did we use a new external theorem, algorithm, encoding, standard, paper, or measured baseline?
    |
    +-- no  -> no registry change required
    |
    +-- yes -> is the exact source already in SOURCES.md?
                 |
                 +-- yes -> reference its SRC ID where useful
                 |
                 +-- no  -> add a verified source entry in the same PR
```

A source entry should be updated when:

- its URL/official publication location changes materially;
- a living standard has changed in a way relevant to NEX;
- NEX begins relying on an additional claim from the source;
- a formerly secondary citation is replaced with a better primary source;
- a benchmark begins using an exact external implementation/version as a baseline.
