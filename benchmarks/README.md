# Benchmark corpora

Stage 4 benchmark corpora are immutable once frozen for comparison. New findings create a new version rather than rewriting prior inputs.

## Corpus lineage

- `corpus-v0.1.json` — frozen foundation corpus, 10 direct NEX programs.
- `corpus-v0.2.json` — preserved extended candidate. It demonstrated that `factorial-5` exceeds the default non-memoizing reference evaluator budget of 1,000,000 transitions. It is retained as evidence and is not the accepted comparison corpus for Stage 4.3.
- `corpus-v0.3.json` — accepted extended corpus for Stage 4.3. It inherits v0.1 unchanged and uses bounded representative recursive workloads (`factorial-4`, `fibonacci-5`) together with polymorphic-let, sum/case, recognizer, multiplication, and repeated-expensive-let cases.

The v0.2 resource refusal is not a Core semantic failure and does not imply divergence. It is a reference-implementation measurement under the default Stage 3 resource budget.

Comparative reports must identify the exact corpus version used.