from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeAlias

from .scope import validate_closed
from .term import App, Lam, Let, Nat, Prim, Term, Var


@dataclass(frozen=True, slots=True)
class TyVar:
    id: int


@dataclass(frozen=True, slots=True)
class TyUnit:
    pass


@dataclass(frozen=True, slots=True)
class TyNat:
    pass


@dataclass(frozen=True, slots=True)
class TyFun:
    argument: "Type"
    result: "Type"


@dataclass(frozen=True, slots=True)
class TyProd:
    left: "Type"
    right: "Type"


@dataclass(frozen=True, slots=True)
class TySum:
    left: "Type"
    right: "Type"


Type: TypeAlias = TyVar | TyUnit | TyNat | TyFun | TyProd | TySum
UNIT = TyUnit()
NAT = TyNat()


@dataclass(frozen=True, slots=True)
class Scheme:
    variables: tuple[int, ...]
    body: Type


Subst: TypeAlias = dict[int, Type]
Env: TypeAlias = list[Scheme]  # nearest binder first


class TypeInferenceError(ValueError):
    pass


class TypeMismatchError(TypeInferenceError):
    pass


class OccursCheckError(TypeInferenceError):
    pass


class UnknownPrimitiveError(TypeInferenceError):
    pass


def free_type_vars(ty: Type) -> set[int]:
    match ty:
        case TyVar(i):
            return {i}
        case TyUnit() | TyNat():
            return set()
        case TyFun(a, b) | TyProd(a, b) | TySum(a, b):
            return free_type_vars(a) | free_type_vars(b)
        case _:
            raise TypeError(type(ty).__name__)


def free_scheme_vars(scheme: Scheme) -> set[int]:
    return free_type_vars(scheme.body) - set(scheme.variables)


def free_env_vars(env: Iterable[Scheme]) -> set[int]:
    result: set[int] = set()
    for scheme in env:
        result |= free_scheme_vars(scheme)
    return result


def apply_subst(ty: Type, subst: Subst) -> Type:
    match ty:
        case TyVar(i):
            replacement = subst.get(i)
            if replacement is None or replacement == ty:
                return ty
            return apply_subst(replacement, subst)
        case TyUnit() | TyNat():
            return ty
        case TyFun(a, b):
            return TyFun(apply_subst(a, subst), apply_subst(b, subst))
        case TyProd(a, b):
            return TyProd(apply_subst(a, subst), apply_subst(b, subst))
        case TySum(a, b):
            return TySum(apply_subst(a, subst), apply_subst(b, subst))
        case _:
            raise TypeError(type(ty).__name__)


def apply_scheme(scheme: Scheme, subst: Subst) -> Scheme:
    if not subst:
        return scheme
    filtered = {k: v for k, v in subst.items() if k not in scheme.variables}
    return Scheme(scheme.variables, apply_subst(scheme.body, filtered))


def apply_env(env: Env, subst: Subst) -> Env:
    return [apply_scheme(s, subst) for s in env]


def compose(newer: Subst, older: Subst) -> Subst:
    """Return substitution equivalent to applying older, then newer."""
    out = {var: apply_subst(ty, newer) for var, ty in older.items()}
    for var, ty in newer.items():
        out[var] = ty
    return out


def _bind(var: int, ty: Type) -> Subst:
    if ty == TyVar(var):
        return {}
    if var in free_type_vars(ty):
        raise OccursCheckError(f"type variable {var} occurs in {ty!r}")
    return {var: ty}


def unify(left: Type, right: Type) -> Subst:
    if left == right:
        return {}
    match left, right:
        case TyVar(i), _:
            return _bind(i, right)
        case _, TyVar(i):
            return _bind(i, left)
        case TyFun(a1, b1), TyFun(a2, b2):
            s1 = unify(a1, a2)
            s2 = unify(apply_subst(b1, s1), apply_subst(b2, s1))
            return compose(s2, s1)
        case TyProd(a1, b1), TyProd(a2, b2):
            s1 = unify(a1, a2)
            s2 = unify(apply_subst(b1, s1), apply_subst(b2, s1))
            return compose(s2, s1)
        case TySum(a1, b1), TySum(a2, b2):
            s1 = unify(a1, a2)
            s2 = unify(apply_subst(b1, s1), apply_subst(b2, s1))
            return compose(s2, s1)
        case _:
            raise TypeMismatchError(f"cannot unify {left!r} with {right!r}")


class _InferState:
    __slots__ = ("next_id",)

    def __init__(self) -> None:
        self.next_id = 0

    def fresh(self) -> TyVar:
        result = TyVar(self.next_id)
        self.next_id += 1
        return result

    def instantiate(self, scheme: Scheme) -> Type:
        replacements: Subst = {var: self.fresh() for var in scheme.variables}
        return apply_subst(scheme.body, replacements)


def generalize(env: Env, ty: Type) -> Scheme:
    variables = tuple(sorted(free_type_vars(ty) - free_env_vars(env)))
    return Scheme(variables, ty)


def primitive_scheme(primitive_id: int) -> Scheme:
    # Primitive-scheme variables live in a private negative-ID namespace.
    # Inference-generated variables are non-negative, so instantiation can never
    # accidentally alias a scheme-local variable with an existing fresh variable.
    a, b, c = TyVar(-1), TyVar(-2), TyVar(-3)
    q1 = (-1,)
    q2 = (-1, -2)
    q3 = (-1, -2, -3)
    table: dict[int, Scheme] = {
        0: Scheme(q1, TyFun(TyFun(a, a), a)),
        1: Scheme((), TyFun(NAT, NAT)),
        2: Scheme((), TyFun(NAT, NAT)),
        3: Scheme(q1, TyFun(NAT, TyFun(a, TyFun(a, a)))),
        4: Scheme(q2, TyFun(a, TyFun(b, TyProd(a, b)))),
        5: Scheme(q2, TyFun(TyProd(a, b), a)),
        6: Scheme(q2, TyFun(TyProd(a, b), b)),
        7: Scheme(q2, TyFun(a, TySum(a, b))),
        8: Scheme(q2, TyFun(b, TySum(a, b))),
        9: Scheme(q3, TyFun(TySum(a, b), TyFun(TyFun(a, c), TyFun(TyFun(b, c), c)))),
        10: Scheme((), UNIT),
    }
    try:
        return table[primitive_id]
    except KeyError:
        raise UnknownPrimitiveError(f"unknown Core primitive id {primitive_id}") from None


def _infer(term: Term, env: Env, state: _InferState) -> tuple[Subst, Type]:
    match term:
        case Var(index):
            # Scope validation normally catches this first, but keep this total for callers.
            if index >= len(env):
                from .scope import OutOfScopeError
                raise OutOfScopeError(f"Var({index}) is out of typing environment")
            return {}, state.instantiate(env[index])

        case Nat():
            return {}, NAT

        case Prim(primitive_id):
            return {}, state.instantiate(primitive_scheme(primitive_id))

        case Lam(body):
            argument = state.fresh()
            s1, body_ty = _infer(body, [Scheme((), argument), *env], state)
            return s1, TyFun(apply_subst(argument, s1), body_ty)

        case App(function, argument):
            s1, function_ty = _infer(function, env, state)
            env1 = apply_env(env, s1)
            s2, argument_ty = _infer(argument, env1, state)
            result_ty = state.fresh()
            s3 = unify(apply_subst(function_ty, s2), TyFun(argument_ty, result_ty))
            total = compose(s3, compose(s2, s1))
            return total, apply_subst(result_ty, s3)

        case Let(value, body):
            s1, value_ty = _infer(value, env, state)
            env1 = apply_env(env, s1)
            normalized_value_ty = apply_subst(value_ty, s1)
            scheme = generalize(env1, normalized_value_ty)
            s2, body_ty = _infer(body, [scheme, *env1], state)
            return compose(s2, s1), body_ty

        case _:
            raise TypeError(f"unsupported term object: {type(term).__name__}")


def infer_principal(term: Term) -> Scheme:
    validate_closed(term)
    state = _InferState()
    subst, ty = _infer(term, [], state)
    final_ty = apply_subst(ty, subst)
    return generalize([], final_ty)


def render_scheme(scheme: Scheme) -> str:
    quantified = set(scheme.variables)
    names: dict[int, str] = {}

    def discover(ty: Type) -> None:
        match ty:
            case TyVar(i):
                if i in quantified and i not in names:
                    names[i] = f"T{len(names)}"
            case TyUnit() | TyNat():
                pass
            case TyFun(a, b) | TyProd(a, b) | TySum(a, b):
                discover(a)
                discover(b)
            case _:
                raise TypeError(type(ty).__name__)

    discover(scheme.body)

    def render(ty: Type) -> str:
        match ty:
            case TyVar(i):
                return names.get(i, f"T?{i}")
            case TyUnit():
                return "1"
            case TyNat():
                return "N"
            case TyFun(a, b):
                return f"({render(a)} -> {render(b)})"
            case TyProd(a, b):
                return f"({render(a)} * {render(b)})"
            case TySum(a, b):
                return f"({render(a)} + {render(b)})"
            case _:
                raise TypeError(type(ty).__name__)

    body = render(scheme.body)
    if names:
        ordered = " ".join(f"T{i}" for i in range(len(names)))
        return f"forall {ordered}. {body}"
    return body
