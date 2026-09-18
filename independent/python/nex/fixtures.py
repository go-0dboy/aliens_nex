from __future__ import annotations

from typing import Any

from .term import App, Lam, Let, Nat, Prim, Term, Var


class FixtureError(ValueError):
    pass


def term_from_json(obj: Any) -> Term:
    if not isinstance(obj, dict):
        raise FixtureError("term fixture must be an object")
    kind = obj.get("kind")
    try:
        if kind == "Var":
            return Var(_decimal_nat(obj["value"]))
        if kind == "Lam":
            return Lam(term_from_json(obj["a"]))
        if kind == "App":
            return App(term_from_json(obj["a"]), term_from_json(obj["b"]))
        if kind == "Let":
            return Let(term_from_json(obj["a"]), term_from_json(obj["b"]))
        if kind == "Nat":
            return Nat(_decimal_nat(obj["value"]))
        if kind == "Prim":
            return Prim(_decimal_nat(obj["value"]))
    except KeyError as exc:
        raise FixtureError(f"missing field for {kind!r}: {exc.args[0]}") from None
    raise FixtureError(f"unknown term fixture kind: {kind!r}")


def _decimal_nat(value: Any) -> int:
    if not isinstance(value, str) or not value or not value.isascii() or not value.isdecimal():
        raise FixtureError("numeric fixture fields must be decimal strings")
    result = int(value, 10)
    if result < 0:
        raise FixtureError("numeric fixture fields must be non-negative")
    return result
