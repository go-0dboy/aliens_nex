package nex

import "testing"

func FuzzInferenceSuccessfulSchemeIsClosedAndStable(f *testing.F) {
	for _, seed := range [][]byte{
		{0},
		{1, 2, 3},
		{3, 1, 4, 1, 5, 9},
		{4, 0, 1, 10, 2, 7},
	} {
		f.Add(seed)
	}

	f.Fuzz(func(t *testing.T, data []byte) {
		if len(data) == 0 {
			return
		}
		pos := 0
		term := termFromFuzzBytes(data, &pos, 0)

		first, err := InferClosed(term)
		if err != nil {
			return
		}
		free, err := FreeSchemeVars(first)
		if err != nil {
			t.Fatal(err)
		}
		if len(free) != 0 {
			t.Fatalf("successful closed inference left free scheme variables: %#v", free)
		}
		firstText, err := CanonicalSchemeString(first)
		if err != nil {
			t.Fatal(err)
		}

		second, err := InferClosed(term)
		if err != nil {
			t.Fatalf("same term inferred successfully once and then failed: %v", err)
		}
		secondText, err := CanonicalSchemeString(second)
		if err != nil {
			t.Fatal(err)
		}
		if firstText != secondText {
			t.Fatalf("principal type is not deterministic: %q != %q", firstText, secondText)
		}
	})
}
