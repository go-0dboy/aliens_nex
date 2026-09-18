#!/usr/bin/env sh
set -eu

unformatted=$(gofmt -l nex/*.go bench/*.go experiment/*.go cmd/nexbench/*.go cmd/nexexperiment/*.go cmd/nextypeexperiment/*.go cmd/nexbaseline/*.go cmd/nexstrategy/*.go cmd/nexaccount/*.go cmd/nexreport/*.go)
if [ -n "$unformatted" ]; then
  echo "gofmt required for:" >&2
  echo "$unformatted" >&2
  exit 1
fi

go vet ./...
go test ./...

go run ./cmd/nexbench -corpus ../../benchmarks/corpus-v0.1.json -pretty=false >/tmp/nex-benchmark-v0.1.json
go run ./cmd/nexbench -corpus ../../benchmarks/corpus-v0.3.json -pretty=false >/tmp/nex-benchmark-v0.3.json
go run ./cmd/nexexperiment -pretty=false | tee /tmp/nex-internal-experiments-v0.1.json
go run ./cmd/nextypeexperiment -corpus ../../benchmarks/corpus-v0.3.json -pretty=false | tee /tmp/nex-type-experiment-v0.1.json
go run ./cmd/nexbaseline -corpus ../../benchmarks/corpus-v0.3.json -pretty=false | tee /tmp/nex-baseline-comparison-v0.1.json
go run ./cmd/nexstrategy -corpus ../../benchmarks/corpus-v0.3.json -pretty=false | tee /tmp/nex-evaluation-strategy-v0.1.json
go run ./cmd/nexaccount -corpus ../../benchmarks/corpus-v0.3.json -repo-root ../.. -pretty=false | tee /tmp/nex-accounting-v0.1.json
go run ./cmd/nexreport -corpus ../../benchmarks/corpus-v0.3.json -repo-root ../.. -pretty=false | tee /tmp/nex-stage4-report-v0.1.json

go test -run '^$' -fuzz=FuzzSubstitutionComposition -fuzztime=1s ./nex
go test -run '^$' -fuzz=FuzzUnifyProducesEqualAppliedTypes -fuzztime=1s ./nex
go test -run '^$' -fuzz=FuzzInferenceSuccessfulSchemeIsClosedAndStable -fuzztime=1s ./nex
go test -run '^$' -fuzz=FuzzEvaluationDeterministicObservation -fuzztime=1s ./nex
