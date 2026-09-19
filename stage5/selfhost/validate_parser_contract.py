#!/usr/bin/env python3
"""Validate the preregistered Stage 5.12f stream-parser contract/workloads.

This is a host mathematical oracle only. It exists before any NEX parser
candidate and validates the frozen preregistration artifacts independently of
later candidate execution results, which are recorded separately.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "stage5" / "selfhost" / "parser-contract-v0.1.json"
DEVELOPMENT = ROOT / "stage5" / "selfhost" / "parser-development-v0.1.json"
HOLDOUT = ROOT / "stage5" / "selfhost" / "parser-holdout-v0.1.json"
PROTOCOL = ROOT / "stage5" / "selfhost" / "experiment-protocol-v0.1.json"

OK = 0
UNEXPECTED_EOF = 1
TRAILING_DATA = 2


def fail(message: str) -> None:
    raise SystemExit(f"stage5.12f parser contract invalid: {message}")


def symbol(bits: str, offset: int) -> int:
    if offset < 0:
        fail("negative cursor in workload")
    if offset >= len(bits):
        return 2
    ch = bits[offset]
    if ch == "0":
        return 0
    if ch == "1":
        return 1
    fail(f"non-bit character {ch!r} in workload")


def decode_u_at(bits: str, offset: int) -> tuple[int, int, int, int]:
    zeros = 0
    cursor = offset
    while True:
        current = symbol(bits, cursor)
        if current == 2:
            return (UNEXPECTED_EOF, 0, 0, cursor)
        cursor += 1
        if current == 1:
            break
        zeros += 1

    value_plus_one = 1
    for _ in range(zeros):
        current = symbol(bits, cursor)
        if current == 2:
            return (UNEXPECTED_EOF, 0, 0, cursor)
        value_plus_one = (value_plus_one << 1) | current
        cursor += 1
    return (OK, value_plus_one - 1, 0, cursor)


def read_head(bits: str, offset: int) -> tuple[int, int, int, int]:
    cursor = offset
    first = symbol(bits, cursor)
    if first == 2:
        return (UNEXPECTED_EOF, 0, 0, cursor)
    cursor += 1

    second = symbol(bits, cursor)
    if second == 2:
        return (UNEXPECTED_EOF, 0, 0, cursor)
    cursor += 1

    if first == 0:
        if second == 1:
            return (OK, 1, 0, cursor)  # Lam
        status, value, _, next_cursor = decode_u_at(bits, cursor)
        if status != OK:
            return (status, 0, 0, next_cursor)
        return (OK, 0, value, next_cursor)  # Var

    if second == 0:
        return (OK, 2, 0, cursor)  # App

    third = symbol(bits, cursor)
    if third == 2:
        return (UNEXPECTED_EOF, 0, 0, cursor)
    cursor += 1
    if third == 0:
        return (OK, 3, 0, cursor)  # Let

    fourth = symbol(bits, cursor)
    if fourth == 2:
        return (UNEXPECTED_EOF, 0, 0, cursor)
    cursor += 1
    kind = 4 if fourth == 0 else 5
    status, value, _, next_cursor = decode_u_at(bits, cursor)
    if status != OK:
        return (status, 0, 0, next_cursor)
    return (OK, kind, value, next_cursor)


def skip_term(bits: str, offset: int) -> tuple[int, int, int, int]:
    status, kind, _, cursor = read_head(bits, offset)
    if status != OK:
        return (status, 0, 0, cursor)

    arity = {0: 0, 1: 1, 2: 2, 3: 2, 4: 0, 5: 0}[kind]
    nodes = 1
    for _ in range(arity):
        child_status, child_nodes, _, child_cursor = skip_term(bits, cursor)
        if child_status != OK:
            return (child_status, 0, 0, child_cursor)
        nodes += child_nodes
        cursor = child_cursor
    return (OK, nodes, 0, cursor)


def exact_term(bits: str, offset: int) -> tuple[int, int, int, int]:
    status, nodes, _, cursor = skip_term(bits, offset)
    if status != OK:
        return (status, 0, 0, cursor)
    if symbol(bits, cursor) != 2:
        return (TRAILING_DATA, nodes, 0, cursor)
    return (OK, nodes, 0, cursor)


ORACLES = {
    "decodeUAt": decode_u_at,
    "readHead": read_head,
    "skipTerm": skip_term,
    "exactTerm": exact_term,
}


def validate_workload(path: Path, classification: str) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "nex-selfhost-stream-parser-workload":
        fail(f"{path.name}: unexpected schema")
    if data.get("version") != "0.1" or data.get("classification") != classification:
        fail(f"{path.name}: unexpected version/classification")
    if data.get("contract") != "stage5/selfhost/parser-contract-v0.1.json":
        fail(f"{path.name}: contract reference drifted")
    if data.get("result_fields") != ["status", "a", "b", "next_offset"]:
        fail(f"{path.name}: result field contract drifted")
    if classification == "holdout" and data.get("status") != "preregistered_unexecuted":
        fail("holdout registration status must remain preregistered_unexecuted")

    seen_ids: set[str] = set()
    for case in data.get("cases", []):
        case_id = case.get("id")
        if not case_id or case_id in seen_ids:
            fail(f"{path.name}: duplicate/missing case id {case_id!r}")
        seen_ids.add(case_id)
        operation = case.get("operation")
        oracle = ORACLES.get(operation)
        if oracle is None:
            fail(f"{case_id}: unknown operation {operation!r}")
        bits = case.get("bits")
        offset = case.get("offset")
        expected = case.get("expected")
        if not isinstance(bits, str) or any(ch not in "01" for ch in bits):
            fail(f"{case_id}: bits must contain only 0/1")
        if not isinstance(offset, int) or offset < 0:
            fail(f"{case_id}: invalid offset")
        actual = list(oracle(bits, offset))
        if actual != expected:
            fail(f"{case_id}: frozen expected {expected} != host oracle {actual}")
    return len(seen_ids)


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    if contract.get("schema") != "nex-selfhost-stream-parser-contract" or contract.get("version") != "0.1":
        fail("unexpected contract schema/version")
    if contract.get("status") != "preregistered_before_parser_implementation":
        fail("contract status was rewritten after preregistration")
    if contract.get("core_version") != "NEX-1 v0.1" or contract.get("stage") != "5.12f":
        fail("Core/stage target drifted")
    if contract.get("types") != {
        "BitStream": "N -> N",
        "Cursor": "N",
        "ParserResult": "N * (N * (N * N))",
    }:
        fail("fixed parser types drifted")
    if contract.get("status_codes") != {"Ok": 0, "UnexpectedEOF": 1, "TrailingData": 2}:
        fail("status codes drifted")
    if contract.get("constructor_kind_codes") != {
        "Var": 0, "Lam": 1, "App": 2, "Let": 3, "Nat": 4, "Prim": 5
    }:
        fail("constructor kind codes drifted")

    contract_budgets = contract.get("resource_budgets", {})
    global_budgets = protocol.get("resource_budgets", {})
    for name in ("python_call_by_need", "go_call_by_need", "go_normative_cbn"):
        for field in ("max_transitions", "max_depth"):
            if contract_budgets.get(name, {}).get(field) != global_budgets.get(name, {}).get(field):
                fail(f"parser budget {name}.{field} differs from frozen global protocol")

    dev_count = validate_workload(DEVELOPMENT, "development")
    holdout_count = validate_workload(HOLDOUT, "holdout")
    if dev_count != 27:
        fail(f"development case count {dev_count} != 27")
    if holdout_count != 12:
        fail(f"holdout case count {holdout_count} != 12")

    development = json.loads(DEVELOPMENT.read_text(encoding="utf-8"))
    head_kinds = {
        case["expected"][1]
        for case in development["cases"]
        if case["operation"] == "readHead" and case["expected"][0] == OK
    }
    if head_kinds != set(range(6)):
        fail(f"development readHead does not cover all constructor kinds: {sorted(head_kinds)}")

    print("stage5.12f parser contract: valid and preregistered")
    print(f"development cases: {dev_count}")
    print(f"holdout registration: {holdout_count} cases, host-oracle validated and frozen; execution result is recorded separately")
    print("constructor heads covered: Var Lam App Let Nat Prim")
    print("resource budgets: inherited unchanged from experiment-protocol-v0.1")


if __name__ == "__main__":
    main()
