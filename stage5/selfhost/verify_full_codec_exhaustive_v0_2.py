#!/usr/bin/env python3
"""Bounded-exhaustive Stage 5.12 full codec v0.2 verification.

Uses the class frozen before v0.2 execution and never reads the v0.2 holdout.
Static identity/type verification is a separate cheap gate and is not repeated here.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PYTHON_IMPL = ROOT / "independent" / "python"
GO_IMPL = ROOT / "reference" / "go"
ARTIFACT = ROOT / "stage5" / "selfhost" / "full-codec-v0.2.json"
CONTRACT = ROOT / "stage5" / "selfhost" / "full-codec-contract-v0.2.json"

sys.path.insert(0, str(PYTHON_IMPL))
sys.setrecursionlimit(max(sys.getrecursionlimit(), 40_000))

from nex.wire import decode_exact, encode_term  # noqa: E402
from build_foundation import app  # noqa: E402
from build_full_codec import literal_finite_bits, literal_finite_tokens  # noqa: E402
from build_full_codec_v0_2 import source_terms_full_codec_v0_2  # noqa: E402
from validate_full_codec_contract import encode_ast, exhaustive_terms, tokens_of  # noqa: E402
from verify_full_codec_exhaustive import (  # noqa: E402
    eval_python,
    finite_payload,
    result_matches,
    stat_value,
)

GO_MAX_TRANSITIONS = 5_000_000
GO_MAX_DEPTH = 20_000


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12 bounded exhaustive full-codec v0.2 failed: {message}")


def main() -> None:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    frozen = contract.get("bounded_exhaustive_class", {})
    if artifact.get("version") != "0.2" or artifact.get("holdout_status") != "preregistered_unexecuted":
        fail("candidate identity/holdout status drifted")
    if frozen.get("maximum_ast_nodes") != 3 or frozen.get("expected_term_count") != 27:
        fail("bounded class contract drifted")
    if frozen.get("leaf_set") != ["Var(0)", "Nat(0)", "Prim(0)"]:
        fail("bounded leaf set drifted")

    terms = [term for nodes in range(1, 4) for term in exhaustive_terms(nodes)]
    if len(terms) != 27:
        fail(f"generated {len(terms)} terms, expected 27")

    controls = []
    cases = []
    for index, ast in enumerate(terms):
        cid = f"term-{index:02d}"
        bits = encode_ast(ast)
        tokens = list(tokens_of(ast))
        if encode_term(decode_exact(bits)) != bits:
            fail(f"{cid}: Direct Python re-encode mismatch")
        cases.append((cid, bits, tokens))
        controls.append({"id": cid, "bits": bits})

    go_control = subprocess.run(
        ["go", "run", "./cmd/nextermcontrol"], cwd=GO_IMPL,
        input=json.dumps(controls), text=True, capture_output=True, check=False,
    )
    if go_control.returncode != 0:
        fail(f"Direct Go term control failed: {go_control.stderr.strip()}")
    rows = json.loads(go_control.stdout)
    by_control = {row["id"]: row for row in rows}
    for cid, bits, tokens in cases:
        row = by_control.get(cid)
        if row is None or row.get("error") or row.get("reencoded") != bits:
            fail(f"{cid}: Direct Go control mismatch: {row}")
        if row.get("tokens") != [str(x) for x in tokens]:
            fail(f"{cid}: Direct Go token projection mismatch")

    sources = source_terms_full_codec_v0_2()
    decode = sources["decodeTerm"]
    encode = sources["encodeTerm"]
    wrappers = []
    for cid, bits, tokens in cases:
        bit_values = [int(ch) for ch in bits]
        decode_call = app(decode, literal_finite_bits(bits))
        encode_call = app(encode, literal_finite_tokens(tokens))
        wrappers.append((f"decode:{cid}", result_matches(decode_call, tokens, 0)))
        wrappers.append((f"encode:{cid}", result_matches(encode_call, bit_values, 2)))
        wrappers.append((f"law1:{cid}", result_matches(app(decode, finite_payload(encode_call)), tokens, 0)))
        wrappers.append((f"law2:{cid}", result_matches(app(encode, finite_payload(decode_call)), bit_values, 2)))

    go_requests = []
    python_results = {}
    py_refusals = []
    max_py_transitions = 0
    max_py_case = ""
    for wrapper_id, wrapper in wrappers:
        wrapper_bits, py = eval_python(wrapper, wrapper_id)
        python_results[wrapper_id] = py
        if py["status"] == "resource_refusal":
            py_refusals.append(f"{wrapper_id}: {py['detail']}")
        elif py["transitions"] > max_py_transitions:
            max_py_transitions = py["transitions"]
            max_py_case = wrapper_id
        go_requests.append({
            "id": f"eval:{wrapper_id}", "level": "eval", "bits": wrapper_bits,
            "max_transitions": GO_MAX_TRANSITIONS, "max_depth": GO_MAX_DEPTH,
        })

    go_run = subprocess.run(
        ["go", "run", "./cmd/nexselfhostprobe"], cwd=GO_IMPL,
        input=json.dumps(go_requests), text=True, capture_output=True, check=False,
    )
    if go_run.returncode != 0:
        fail(f"Go NEX probe failed: {go_run.stderr.strip()}")
    by_id = {row["id"]: row for row in json.loads(go_run.stdout)}

    go_need_refusals = []
    go_cbn_refusals = []
    matched = 0
    max_go_transitions = 0
    max_go_case = ""
    expected = {"kind": "Nat", "value": "1"}
    for wrapper_id, _ in wrappers:
        row = by_id.get(f"eval:{wrapper_id}")
        if row is None or row.get("static_error"):
            fail(f"{wrapper_id}: Go missing/static error: {row}")
        if row.get("need_error"):
            go_need_refusals.append(f"{wrapper_id}: {row['need_error']}")
        else:
            if row.get("need_result") != expected:
                fail(f"{wrapper_id}: Go need mismatch: {row.get('need_result')}")
            transitions = stat_value(row.get("need_stats") or {}, "transitions")
            if transitions > max_go_transitions:
                max_go_transitions = transitions
                max_go_case = wrapper_id
        if row.get("cbn_error"):
            go_cbn_refusals.append(f"{wrapper_id}: {row['cbn_error']}")
        elif row.get("cbn_result") != expected:
            fail(f"{wrapper_id}: Go CBN mismatch: {row.get('cbn_result')}")
        py = python_results[wrapper_id]
        if py["status"] == "value" and not row.get("need_error"):
            if py["result"] != row.get("need_result"):
                fail(f"{wrapper_id}: Python/Go need mismatch")
            matched += 1

    if py_refusals:
        fail("Python need refusals: " + " | ".join(py_refusals))
    if go_need_refusals:
        fail("Go need refusals: " + " | ".join(go_need_refusals))

    print("stage5.12 bounded exhaustive full codec v0.2: verified")
    print("complete frozen Term class: 27/27")
    print("Direct Python canonical round trips: 27/27")
    print("Direct Go canonical round trips/token projections: 27/27")
    print(f"NEX-on-Python/Go forced law observations: {matched}/{len(wrappers)}")
    print("Python call-by-need resource refusals: 0")
    print("Go call-by-need resource refusals: 0")
    print(f"Go CBN resource refusals: {len(go_cbn_refusals)}")
    print(f"largest Python need transition count: {max_py_transitions} at {max_py_case}")
    print(f"largest Go need transition count: {max_go_transitions} at {max_go_case}")
    print("v0.2 holdout: NOT READ / NOT EXECUTED")


if __name__ == "__main__":
    main()
