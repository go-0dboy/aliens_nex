#!/usr/bin/env python3
"""Experimental Python call-by-need control for post-Stage-5 self-hosting work.

This module intentionally lives outside independent/python so the frozen Stage 5
independence checkpoint remains byte-for-byte historical evidence. It reuses only
the frozen Python AST/type checker as inputs and implements its own memoizing
runtime control for corroborating post-Stage-5 resource measurements.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from nex.term import App, Lam, Let, Nat, Prim, Term, Var
from nex.typesys import UnknownPrimitiveError, infer_principal


class NeedEvaluationError(RuntimeError):
    pass


class NeedResourceLimitError(NeedEvaluationError):
    pass


class NeedRuntimeShapeError(NeedEvaluationError):
    pass


@dataclass(frozen=True, slots=True)
class NeedLimits:
    max_transitions: int = 5_000_000
    max_depth: int = 2_000


@dataclass(slots=True)
class NeedStats:
    transitions: int = 0
    max_depth: int = 0
    thunk_forces: int = 0
    thunk_evaluations: int = 0
    memo_hits: int = 0


@dataclass(slots=True)
class NeedThunk:
    term: Term
    env: "NeedEnv"
    ready: bool = False
    value: "NeedValue | None" = None


NeedEnv: TypeAlias = list[NeedThunk]


@dataclass(frozen=True, slots=True)
class NeedClosure:
    body: Term
    env: NeedEnv


@dataclass(frozen=True, slots=True)
class NeedNat:
    value: int


@dataclass(frozen=True, slots=True)
class NeedUnit:
    pass


@dataclass(frozen=True, slots=True)
class NeedPair:
    left: NeedThunk
    right: NeedThunk


@dataclass(frozen=True, slots=True)
class NeedInl:
    payload: NeedThunk


@dataclass(frozen=True, slots=True)
class NeedInr:
    payload: NeedThunk


@dataclass(frozen=True, slots=True)
class NeedPrim:
    primitive_id: int
    arguments: tuple[NeedThunk, ...]


NeedValue: TypeAlias = (
    NeedClosure | NeedNat | NeedUnit | NeedPair | NeedInl | NeedInr | NeedPrim
)

ARITIES = {
    0: 1,
    1: 1,
    2: 1,
    3: 3,
    4: 2,
    5: 1,
    6: 1,
    7: 1,
    8: 1,
    9: 3,
    10: 0,
}


class _NeedEvaluator:
    __slots__ = ("limits", "stats")

    def __init__(self, limits: NeedLimits) -> None:
        self.limits = limits
        self.stats = NeedStats()

    @staticmethod
    def clone_env(env: NeedEnv) -> NeedEnv:
        return list(env)

    def step(self, depth: int) -> None:
        self.stats.transitions += 1
        if depth > self.stats.max_depth:
            self.stats.max_depth = depth
        if self.stats.transitions > self.limits.max_transitions:
            raise NeedResourceLimitError(
                f"transition limit exceeded: {self.stats.transitions} > "
                f"{self.limits.max_transitions}"
            )
        if depth > self.limits.max_depth:
            raise NeedResourceLimitError(
                f"depth limit exceeded: {depth} > {self.limits.max_depth}"
            )

    def force(self, thunk: NeedThunk, depth: int) -> NeedValue:
        self.step(depth)
        self.stats.thunk_forces += 1
        if thunk.ready:
            self.stats.memo_hits += 1
            assert thunk.value is not None
            return thunk.value
        self.stats.thunk_evaluations += 1
        value = self.eval_term(thunk.term, thunk.env, depth + 1)
        thunk.value = value
        thunk.ready = True
        return value

    def eval_term(self, term: Term, env: NeedEnv, depth: int) -> NeedValue:
        self.step(depth)
        match term:
            case Var(index):
                try:
                    thunk = env[index]
                except IndexError:
                    raise NeedRuntimeShapeError(f"runtime Var({index}) out of scope") from None
                return self.force(thunk, depth + 1)
            case Lam(body):
                return NeedClosure(body, self.clone_env(env))
            case App(function, argument):
                fn = self.eval_term(function, env, depth + 1)
                arg = NeedThunk(argument, self.clone_env(env))
                return self.apply_value(fn, arg, depth + 1)
            case Let(value, body):
                binding = NeedThunk(value, self.clone_env(env))
                return self.eval_term(body, [binding, *env], depth + 1)
            case Nat(value):
                return NeedNat(value)
            case Prim(primitive_id):
                try:
                    arity = ARITIES[primitive_id]
                except KeyError:
                    raise UnknownPrimitiveError(
                        f"unknown Core primitive id {primitive_id}"
                    ) from None
                if arity == 0:
                    return NeedUnit()
                return NeedPrim(primitive_id, ())
            case _:
                raise TypeError(type(term).__name__)

    def apply_value(self, fn: NeedValue, arg: NeedThunk, depth: int) -> NeedValue:
        self.step(depth)
        match fn:
            case NeedClosure(body, closure_env):
                return self.eval_term(body, [arg, *closure_env], depth + 1)
            case NeedPrim(primitive_id, arguments):
                args = (*arguments, arg)
                arity = ARITIES[primitive_id]
                if len(args) < arity:
                    return NeedPrim(primitive_id, args)
                if len(args) == arity:
                    return self.run_primitive(primitive_id, args, depth + 1)
                raise NeedRuntimeShapeError("primitive over-application invariant violated")
            case _:
                raise NeedRuntimeShapeError(
                    f"attempted to apply non-function WHNF {type(fn).__name__}"
                )

    def require_nat(self, thunk: NeedThunk, depth: int) -> NeedNat:
        value = self.force(thunk, depth + 1)
        if not isinstance(value, NeedNat):
            raise NeedRuntimeShapeError("typed natural argument did not evaluate to Nat")
        return value

    def run_primitive(
        self,
        primitive_id: int,
        args: tuple[NeedThunk, ...],
        depth: int,
    ) -> NeedValue:
        self.step(depth)
        if primitive_id == 0:
            fn = self.force(args[0], depth + 1)
            recursive_term = App(Prim(0), args[0].term)
            recursive = NeedThunk(recursive_term, self.clone_env(args[0].env))
            return self.apply_value(fn, recursive, depth + 1)
        if primitive_id == 1:
            n = self.require_nat(args[0], depth + 1)
            return NeedNat(n.value + 1)
        if primitive_id == 2:
            n = self.require_nat(args[0], depth + 1)
            return NeedNat(0 if n.value == 0 else n.value - 1)
        if primitive_id == 3:
            n = self.require_nat(args[0], depth + 1)
            selected = args[1] if n.value == 0 else args[2]
            return self.force(selected, depth + 1)
        if primitive_id == 4:
            return NeedPair(args[0], args[1])
        if primitive_id == 5:
            pair = self.force(args[0], depth + 1)
            if not isinstance(pair, NeedPair):
                raise NeedRuntimeShapeError("fst argument did not evaluate to Pair")
            return self.force(pair.left, depth + 1)
        if primitive_id == 6:
            pair = self.force(args[0], depth + 1)
            if not isinstance(pair, NeedPair):
                raise NeedRuntimeShapeError("snd argument did not evaluate to Pair")
            return self.force(pair.right, depth + 1)
        if primitive_id == 7:
            return NeedInl(args[0])
        if primitive_id == 8:
            return NeedInr(args[0])
        if primitive_id == 9:
            scrutinee = self.force(args[0], depth + 1)
            if isinstance(scrutinee, NeedInl):
                selected = self.force(args[1], depth + 1)
                return self.apply_value(selected, scrutinee.payload, depth + 1)
            if isinstance(scrutinee, NeedInr):
                selected = self.force(args[2], depth + 1)
                return self.apply_value(selected, scrutinee.payload, depth + 1)
            raise NeedRuntimeShapeError("case scrutinee did not evaluate to a sum")
        if primitive_id == 10:
            return NeedUnit()
        raise UnknownPrimitiveError(f"unknown Core primitive id {primitive_id}")


def observe_need(value: NeedValue) -> dict[str, str]:
    if isinstance(value, (NeedClosure, NeedPrim)):
        return {"kind": "Function"}
    if isinstance(value, NeedNat):
        return {"kind": "Nat", "value": str(value.value)}
    if isinstance(value, NeedUnit):
        return {"kind": "Unit"}
    if isinstance(value, NeedPair):
        return {"kind": "Pair"}
    if isinstance(value, NeedInl):
        return {"kind": "Inl"}
    if isinstance(value, NeedInr):
        return {"kind": "Inr"}
    raise TypeError(type(value).__name__)


def evaluate_need_observed(
    term: Term,
    limits: NeedLimits = NeedLimits(),
) -> tuple[dict[str, str], NeedStats]:
    infer_principal(term)
    evaluator = _NeedEvaluator(limits)
    try:
        value = evaluator.eval_term(term, [], 1)
    except RecursionError:
        raise NeedResourceLimitError("host recursion resource exhausted") from None
    return observe_need(value), evaluator.stats
