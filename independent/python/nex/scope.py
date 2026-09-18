from __future__ import annotations

from .term import App, Lam, Let, Nat, Prim, Term, Var


class ScopeError(ValueError):
    pass


class OutOfScopeError(ScopeError):
    pass


def validate_closed(term: Term) -> None:
    _validate(term, 0)


def _validate(term: Term, depth: int) -> None:
    match term:
        case Var(index):
            if index >= depth:
                raise OutOfScopeError(f"Var({index}) is out of scope at binder depth {depth}")
        case Lam(body):
            _validate(body, depth + 1)
        case App(function, argument):
            _validate(function, depth)
            _validate(argument, depth)
        case Let(value, body):
            # Let is non-recursive: its binder is not visible in value.
            _validate(value, depth)
            _validate(body, depth + 1)
        case Nat() | Prim():
            return
        case _:
            raise TypeError(f"unsupported term object: {type(term).__name__}")
