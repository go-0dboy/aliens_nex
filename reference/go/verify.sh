#!/usr/bin/env sh
set -eu

unformatted=$(gofmt -l nex/*.go)
if [ -n "$unformatted" ]; then
  echo "gofmt required for:" >&2
  echo "$unformatted" >&2
  exit 1
fi

go vet ./...
go test ./...

go test -run '^$' -fuzz=FuzzSubstitutionComposition -fuzztime=1s ./nex
go test -run '^$' -fuzz=FuzzUnifyProducesEqualAppliedTypes -fuzztime=1s ./nex
go test -run '^$' -fuzz=FuzzInferenceSuccessfulSchemeIsClosedAndStable -fuzztime=1s ./nex
