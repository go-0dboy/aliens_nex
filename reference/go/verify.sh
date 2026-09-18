#!/usr/bin/env sh
set -eu

unformatted=$(gofmt -l nex/*.go cmd/nexbench/*.go)
if [ -n "$unformatted" ]; then
  echo "gofmt required for:" >&2
  echo "$unformatted" >&2
  exit 1
fi

go vet ./...
go test ./...

go run ./cmd/nexbench -corpus ../../benchmarks/corpus-v0.1.json -pretty=false >/tmp/nex-benchmark-v0.1.json
go run ./cmd/nexbench -corpus ../../benchmarks/corpus-v0.3.json -pretty=false >/tmp/nex-benchmark-v0.3.json

go test -run '^$' -fuzz=FuzzSubstitutionComposition -fuzztime=1s ./nex
go test -run '^$' -fuzz=FuzzUnifyProducesEqualAppliedTypes -fuzztime=1s ./nex
go test -run '^$' -fuzz=FuzzInferenceSuccessfulSchemeIsClosedAndStable -fuzztime=1s ./nex
go test -run '^$' -fuzz=FuzzEvaluationDeterministicObservation -fuzztime=1s ./nex
