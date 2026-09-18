# Ambiguities and omissions

## AMB-001 — error precedence for terms with multiple independent defects

- **Minimal example:** `App(Prim(11), Var(0))` at top level. It simultaneously contains an unknown Core primitive and an out-of-scope variable.
- **Relevant specification:** NEX-1 v0.1 §14 lists validity conditions but does not define a total ordering for reporting multiple failures. Packet `AUDIT.md` finding F5 explicitly classifies such precedence outside supplied cases as unspecified.
- **Interpretation A:** perform a complete scope-validation pass first, so this example reports `out_of_scope`.
- **Interpretation B:** traverse directly through type inference/primitive validation, in which case another defect could be encountered first.
- **Temporary decision:** this implementation validates closed scope before type inference and therefore reports `out_of_scope` for the example.
- **Reason:** the specification says a conforming receiver must type-check a decoded closed term before execution, and a separate pre-pass keeps scope errors distinct from type errors. This is an implementation ordering, not a claimed portable precedence rule.
- **Affected area:** static validation/error observation only; successful typing semantics are unaffected.
- **Conformance vector:** no vector fixes a global precedence rule. The packet explicitly says not to invent one.

## Packet-local omissions already resolved by the packet

These did not require an independent semantic choice:

1. Principal scheme text normalization is not fully fixed by the core prose, but `OBSERVATIONS.md` defines alpha-normalized `T0`, `T1`, ... rendering for conformance.
2. JSON fixture representation is not Core syntax, but `OBSERVATIONS.md` defines the exact mapping used by packet vectors.

## No additional semantic ambiguity found

No implementation step required consulting any source outside the packet to decide NEX-specific wire, scope, typing, primitive, or weak-call-by-name behavior.
