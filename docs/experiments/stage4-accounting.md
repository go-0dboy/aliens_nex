# Stage 4.7 — Total-information accounting model

Status: experimental accounting model; does not provide a complete value for total transmission cost.

## Objective

Keep the project goal

```text
C = S + B + P
```

measurable without substituting convenient host-language quantities for unknown transmission costs.

The terms are deliberately separated:

```text
P  transmitted program payload
S  transmitted specification / semantic contract
B  bootstrap required to reconstruct/check/execute the representation
R  host reference implementation proxy (diagnostic only; not a term in C)
```

## P — exact program payload

For a fixed corpus and encoding, `P` is exact.

For NEX-1 v0.1 this is the sum of canonical wire bit lengths emitted by the normative encoder. Stage 4 uses frozen corpus versions so `P` cannot be silently changed after seeing a comparison result.

## S — specification proxy, not yet an accepted transmission cost

No architecture-neutral transmission encoding for the NEX specification itself has been defined.

Stage 4 therefore records a transparent proxy only:

```text
UTF-8 byte count of docs/NEX-1-v0.1.md
raw UTF-8 bits = bytes * 8
```

This is useful for tracking/documenting magnitude, but it is **not** accepted as `S` in the objective function. Markdown, English prose, UTF-8, URLs, formatting, and terrestrial notation are not assumptions the intended receiver may share.

## R — reference implementation proxy

Stage 4 also records the UTF-8 byte size of an explicit manifest of Go reference source files implementing the Core wire/static/runtime path.

The manifest intentionally excludes tests, benchmark tooling, and Stage 4 instrumentation. It includes the reference implementation of:

```text
Term representation
wire codec
scope validation
type representation
substitution/polymorphism/unification
primitive table
type inference
runtime representation
reference evaluator
```

This quantity is named `R`, not `B`.

Go syntax, `math/big`, Go's compiler/runtime, standard library, garbage collector, and host ABI are not part of a receiver-neutral bootstrap. Therefore:

```text
R != B
```

and no conversion factor from `R` to `B` is assumed.

## B — unknown until there is a bootstrap artifact

`B` remains unknown in Stage 4 because the project does not yet have an architecture-neutral, transmissible bootstrap artifact from which a receiver can reconstruct the required decoder/validator/evaluator machinery.

Consequently:

```text
total C is not numerically computable yet
```

This is a result, not a missing-data value to be filled with the Go source size.

## Comparing two designs

For designs A and B over a chosen program population:

```text
Delta C = Delta S + Delta B + Delta P
```

For repeated programs where an average per-program payload delta is meaningful:

```text
Delta C(N) = Delta S + Delta B + N * Delta P_avg
```

A break-even population can be computed only when enough of `Delta S`, `Delta B`, and `Delta P_avg` are known. If bootstrap delta is unknown, Stage 4 must leave the total comparison unresolved or state a symbolic threshold.

Examples from earlier Stage 4 experiments:

- the root-type hybrid adds `+134` program bits for one v0.3 corpus batch; it is beneficial in total cost only if a real reduction in `S+B` eventually outweighs accumulated payload overhead;
- BLC saves 7 payload bits over NEX on the three-program pure-lambda subset, but the relative `S+B` costs are not measured;
- call-by-need changes no program bits at all; its large runtime transition reduction cannot be inserted into `C`, and sharing machinery may change bootstrap cost.

## Machine-readable accounting report

`reference/go/cmd/nexaccount` emits:

- exact corpus `P`;
- raw UTF-8 specification-size proxy;
- explicit Go reference-source proxy `R`;
- `B.known = false` with a reason;
- `total_C_computable = false`.

The report is intentionally designed so an unknown bootstrap cannot accidentally be represented as zero.

## Reproduction

From `reference/go/`:

```sh
go run ./cmd/nexaccount \
  -corpus ../../benchmarks/corpus-v0.3.json \
  -repo-root ../.. \
  -pretty=false
```

The same command is part of `verify.sh`; accepted values require clean-checkout CI.
