#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import random
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PY_IMPL = ROOT / "independent/python"
sys.path.insert(0, str(PY_IMPL))

from nex.eval import EvaluationLimits, EvaluationResourceLimitError, evaluate_observed  # noqa: E402
from nex.fixtures import term_from_json  # noqa: E402
from nex.scope import OutOfScopeError  # noqa: E402
from nex.typesys import (  # noqa: E402
    OccursCheckError,
    TypeMismatchError,
    UnknownPrimitiveError,
    infer_principal,
    render_scheme,
)
from nex.wire import (  # noqa: E402
    InvalidBitError,
    ResourceLimitError,
    TrailingDataError,
    TruncatedError,
    decode_exact,
    encode_term,
)

EVAL_LIMITS = EvaluationLimits(max_steps=1_000_000, max_depth=10_000)


def V(i: int) -> dict[str, str]:
    return {"kind": "Var", "value": str(i)}


def N(i: int) -> dict[str, str]:
    return {"kind": "Nat", "value": str(i)}


def P(i: int) -> dict[str, str]:
    return {"kind": "Prim", "value": str(i)}


def L(body: dict[str, Any]) -> dict[str, Any]:
    return {"kind": "Lam", "a": body}


def A(fn: dict[str, Any], arg: dict[str, Any]) -> dict[str, Any]:
    return {"kind": "App", "a": fn, "b": arg}


def T(value: dict[str, Any], body: dict[str, Any]) -> dict[str, Any]:
    return {"kind": "Let", "a": value, "b": body}


def load_corpus(path: Path, seen: set[Path] | None = None) -> list[dict[str, Any]]:
    seen = set() if seen is None else seen
    path = path.resolve()
    if path in seen:
        raise RuntimeError(f"corpus inheritance cycle: {path}")
    seen.add(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    programs: list[dict[str, Any]] = []
    if data.get("extends"):
        programs.extend(load_corpus(path.parent / data["extends"], seen))
    programs.extend(data["programs"])
    return programs


def static_error(exc: BaseException) -> str:
    if isinstance(exc, OutOfScopeError):
        return "out_of_scope"
    if isinstance(exc, UnknownPrimitiveError):
        return "unknown_primitive"
    if isinstance(exc, TypeMismatchError):
        return "type_mismatch"
    if isinstance(exc, OccursCheckError):
        return "occurs_check"
    return "other"


def wire_error(exc: BaseException) -> str:
    if isinstance(exc, TruncatedError):
        return "truncated"
    if isinstance(exc, TrailingDataError):
        return "trailing"
    if isinstance(exc, InvalidBitError):
        return "invalid_bit"
    if isinstance(exc, ResourceLimitError):
        return "resource_limit"
    return "other"


def python_probe(case: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {"id": case["id"]}
    try:
        if "bits" in case:
            term = decode_exact(case["bits"])
        else:
            term = term_from_json(case["term"])
        out["wire_bits"] = encode_term(term)
    except BaseException as exc:
        out["wire_error"] = wire_error(exc)
        return out

    if case["level"] == "wire":
        return out
    try:
        out["type"] = render_scheme(infer_principal(term))
    except BaseException as exc:
        out["static_error"] = static_error(exc)
        return out

    if case["level"] == "static":
        return out
    try:
        out["result"] = evaluate_observed(term, EVAL_LIMITS)
    except EvaluationResourceLimitError:
        out["eval_error"] = "resource_limit"
    except BaseException as exc:
        out["eval_error"] = static_error(exc)
    return out


def random_wire_term(rng: random.Random, depth: int) -> dict[str, Any]:
    if depth <= 0:
        k = rng.randrange(3)
        if k == 0:
            return V(rng.randrange(0, 1 << 96))
        if k == 1:
            return N(rng.randrange(0, 1 << 192))
        return P(rng.randrange(0, 1 << 96))
    k = rng.randrange(6)
    if k == 0:
        return V(rng.randrange(0, 1 << 96))
    if k == 1:
        return L(random_wire_term(rng, depth - 1))
    if k == 2:
        return A(random_wire_term(rng, depth - 1), random_wire_term(rng, depth - 1))
    if k == 3:
        return T(random_wire_term(rng, depth - 1), random_wire_term(rng, depth - 1))
    if k == 4:
        return N(rng.randrange(0, 1 << 192))
    return P(rng.randrange(0, 1 << 96))


def build_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    corpus = load_corpus(ROOT / "benchmarks/corpus-v0.3.json")
    for program in corpus:
        cases.append(
            {
                "id": f"corpus:{program['id']}",
                "group": "corpus",
                "level": "full",
                "term": program["term"],
                "expected": program["expected"],
            }
        )

    rng = random.Random(20260918)
    for i in range(25):
        a = rng.randrange(0, 1 << 48)
        b = rng.randrange(0, 1 << 48)
        cond = rng.randrange(0, 3)
        templates = [
            N(a),
            P(10),
            L(V(0)),
            A(P(1), N(a)),
            A(P(2), N(a)),
            A(A(A(P(3), N(cond)), N(a)), N(b)),
            A(L(V(0)), N(a)),
            T(N(a), V(0)),
            A(P(5), A(A(P(4), N(a)), N(b))),
            A(P(6), A(A(P(4), N(a)), N(b))),
            A(A(A(P(9), A(P(7), N(a))), L(V(0))), L(N(b))),
            A(A(A(P(9), A(P(8), N(a))), L(N(b))), L(V(0))),
            A(P(4), N(a)),
        ]
        for j, term in enumerate(templates):
            cases.append(
                {
                    "id": f"generated-valid:{i}:{j}",
                    "group": "generated_valid",
                    "level": "full",
                    "term": term,
                }
            )

    for i in range(25):
        invalids = [
            ("out_of_scope", V(i)),
            ("unknown_primitive", P(11 + i)),
            ("type_mismatch", A(N(i), N(i + 1))),
            ("occurs_check", L(A(V(0), V(0)))),
        ]
        for expected_error, term in invalids:
            cases.append(
                {
                    "id": f"generated-static:{expected_error}:{i}",
                    "group": "generated_static",
                    "level": "static",
                    "term": term,
                    "expected_static_error": expected_error,
                }
            )

    for i in range(500):
        term_json = random_wire_term(rng, 5)
        term = term_from_json(term_json)
        bits = encode_term(term)
        cases.append(
            {
                "id": f"generated-wire:{i}",
                "group": "generated_wire",
                "level": "wire",
                "bits": bits,
            }
        )
    return cases


def go_probe(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    requests = [
        {k: case[k] for k in ("id", "level", "term", "bits") if k in case}
        for case in cases
    ]
    completed = subprocess.run(
        ["go", "run", "./cmd/nexdiffprobe"],
        cwd=ROOT / "reference/go",
        input=json.dumps(requests),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        print(completed.stderr, file=sys.stderr)
        raise RuntimeError(f"Go probe failed with exit code {completed.returncode}")
    return json.loads(completed.stdout)


def compare(cases: list[dict[str, Any]], go_results: list[dict[str, Any]]) -> dict[str, Any]:
    go_by_id = {r["id"]: r for r in go_results}
    counts: Counter[str] = Counter()
    mismatches: list[dict[str, Any]] = []
    resource_asymmetries: list[dict[str, Any]] = []

    for case in cases:
        counts[f"group_{case['group']}"] += 1
        py = python_probe(case)
        go = go_by_id.get(case["id"])
        if go is None:
            mismatches.append({"id": case["id"], "kind": "missing_go_response"})
            continue

        portable_fields = ["wire_bits", "wire_error"]
        if case["level"] in ("static", "full"):
            portable_fields += ["type", "static_error"]
        for field in portable_fields:
            if py.get(field, "") != go.get(field, ""):
                mismatches.append(
                    {
                        "id": case["id"],
                        "kind": f"{field}_mismatch",
                        "python": py.get(field),
                        "go": go.get(field),
                    }
                )
                break
        else:
            if case.get("expected_static_error"):
                expected = case["expected_static_error"]
                if py.get("static_error") != expected or go.get("static_error") != expected:
                    mismatches.append(
                        {
                            "id": case["id"],
                            "kind": "expected_static_error_mismatch",
                            "expected": expected,
                            "python": py,
                            "go": go,
                        }
                    )
                    continue

            if case["level"] == "full" and not py.get("static_error") and not go.get("static_error"):
                py_eval_error = py.get("eval_error", "")
                go_eval_error = go.get("eval_error", "")
                if py_eval_error != go_eval_error or py.get("result") != go.get("result"):
                    if "resource_limit" in (py_eval_error, go_eval_error):
                        resource_asymmetries.append(
                            {"id": case["id"], "python": py, "go": go}
                        )
                    else:
                        mismatches.append(
                            {
                                "id": case["id"],
                                "kind": "evaluation_mismatch",
                                "python": py,
                                "go": go,
                            }
                        )
                        continue

            if case.get("expected") is not None:
                expected = case["expected"]
                if py.get("result") is not None and py.get("result") != expected:
                    mismatches.append(
                        {
                            "id": case["id"],
                            "kind": "python_corpus_expected_mismatch",
                            "expected": expected,
                            "actual": py.get("result"),
                        }
                    )
                    continue
                if go.get("result") is not None and go.get("result") != expected:
                    mismatches.append(
                        {
                            "id": case["id"],
                            "kind": "go_corpus_expected_mismatch",
                            "expected": expected,
                            "actual": go.get("result"),
                        }
                    )
                    continue

            counts["portable_matches"] += 1

    return {
        "schema": "nex-stage5-differential-report-v0.1",
        "seed": 20260918,
        "cases_total": len(cases),
        "counts": dict(sorted(counts.items())),
        "mismatches": mismatches,
        "resource_asymmetries": resource_asymmetries,
        "success": not mismatches,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    cases = build_cases()
    report = compare(cases, go_probe(cases))
    text = json.dumps(report, indent=2, sort_keys=True)
    print(text)
    if args.report:
        args.report.write_text(text + "\n", encoding="utf-8")
    return 0 if report["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
