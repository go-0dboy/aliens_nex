from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from .term import App, Lam, Let, Nat, Prim, Term, Var
from .typesys import UnknownPrimitiveError, infer_principal


class EvaluationError(RuntimeError):
    pass


class EvaluationResourceLimitError(EvaluationError):
    pass


class RuntimeShapeError(EvaluationError):
    """Internal guard: well-typed terms should never reach these mismatches."""


@dataclass(frozen=True, slots=True)
class EvaluationLimits:
    max_steps: int | None = 100_000
    max_depth: int | None = 700

    def __post_init__(self) -> None:
        for name in ("max_steps", "max_depth"):
            value = getattr(self, name)
            if value is not None and value < 0:
                raise ValueError(f"{name} must be non-negative or None")

    @staticmethod
    def active(value: int | None) -> bool:
        return value not in (None, 0)


@dataclass(frozen=True, slots=True)
class TermThunk:
    term: Term
    env: "RuntimeEnv"

    def force(self, evaluator: "_Evaluator", depth: int) -> "Value":
        return evaluator.eval_term(self.term, self.env, depth)


@dataclass(frozen=True, slots=True)
class FixThunk:
    function: "Thunk"

    def force(self, evaluator: "_Evaluator", depth: int) -> "Value":
        return evaluator.eval_fix(self.function, depth)


Thunk: TypeAlias = TermThunk | FixThunk
RuntimeEnv: TypeAlias = list[Thunk]


@dataclass(frozen=True, slots=True)
class VClosure:
    body: Term
    env: RuntimeEnv


@dataclass(frozen=True, slots=True)
class VNat:
    value: int


@dataclass(frozen=True, slots=True)
class VUnit:
    pass


@dataclass(frozen=True, slots=True)
class VPair:
    left: Thunk
    right: Thunk


@dataclass(frozen=True, slots=True)
class VInl:
    payload: Thunk


@dataclass(frozen=True, slots=True)
class VInr:
    payload: Thunk


@dataclass(frozen=True, slots=True)
class VPrim:
    primitive_id: int
    arguments: tuple[Thunk, ...]


Value: TypeAlias = VClosure | VNat | VUnit | VPair | VInl | VInr | VPrim

ARITIES = {
    0: 1,  # fix
    1: 1,  # succ
    2: 1,  # pred
    3: 3,  # ifz
    4: 2,  # pair
    5: 1,  # fst
    6: 1,  # snd
    7: 1,  # inl
    8: 1,  # inr
    9: 3,  # case
    10: 0, # unit
}


class _Evaluator:
    __slots__ = ("limits", "steps")

    def __init__(self, limits: EvaluationLimits) -> None:
        self.limits = limits
        self.steps = 0

    def tick(self, depth: int) -> None:
        self.steps += 1
        if EvaluationLimits.active(self.limits.max_steps) and self.steps > self.limits.max_steps:  # type: ignore[operator]
            raise EvaluationResourceLimitError("evaluation step limit exceeded")
        if EvaluationLimits.active(self.limits.max_depth) and depth > self.limits.max_depth:  # type: ignore[operator]
            raise EvaluationResourceLimitError("evaluation depth limit exceeded")

    def force(self, thunk: Thunk, depth: int) -> Value:
        self.tick(depth)
        return thunk.force(self, depth + 1)

    def eval_term(self, term: Term, env: RuntimeEnv, depth: int) -> Value:
        self.tick(depth)
        match term:
            case Var(index):
                try:
                    thunk = env[index]
                except IndexError:
                    raise RuntimeShapeError(f"runtime Var({index}) out of scope") from None
                return self.force(thunk, depth + 1)

            case Lam(body):
                # Weak semantics: do not reduce under Lam.
                return VClosure(body, env)

            case App(function, argument):
                function_value = self.eval_term(function, env, depth + 1)
                argument_thunk = TermThunk(argument, env)
                return self.apply_value(function_value, argument_thunk, depth + 1)

            case Let(value, body):
                # Non-recursive and non-strict: value captures the outer env.
                delayed_value = TermThunk(value, env)
                return self.eval_term(body, [delayed_value, *env], depth + 1)

            case Nat(value):
                return VNat(value)

            case Prim(primitive_id):
                try:
                    arity = ARITIES[primitive_id]
                except KeyError:
                    raise UnknownPrimitiveError(f"unknown Core primitive id {primitive_id}") from None
                if arity == 0:
                    return VUnit()
                return VPrim(primitive_id, ())

            case _:
                raise TypeError(f"unsupported term object: {type(term).__name__}")

    def apply_value(self, function: Value, argument: Thunk, depth: int) -> Value:
        self.tick(depth)
        match function:
            case VClosure(body, closure_env):
                return self.eval_term(body, [argument, *closure_env], depth + 1)
            case VPrim(primitive_id, arguments):
                args = (*arguments, argument)
                arity = ARITIES[primitive_id]
                if len(args) < arity:
                    return VPrim(primitive_id, args)
                if len(args) == arity:
                    return self.run_primitive(primitive_id, args, depth + 1)
                raise RuntimeShapeError("primitive over-application invariant violated")
            case _:
                raise RuntimeShapeError(f"attempted to apply non-function WHNF {type(function).__name__}")

    def require_nat(self, thunk: Thunk, depth: int) -> VNat:
        value = self.force(thunk, depth + 1)
        if not isinstance(value, VNat):
            raise RuntimeShapeError("typed natural argument did not evaluate to Nat WHNF")
        return value

    def eval_fix(self, function: Thunk, depth: int) -> Value:
        self.tick(depth)
        function_value = self.force(function, depth + 1)
        recursive_argument = FixThunk(function)
        return self.apply_value(function_value, recursive_argument, depth + 1)

    def run_primitive(self, primitive_id: int, args: tuple[Thunk, ...], depth: int) -> Value:
        self.tick(depth)

        if primitive_id == 0:  # fix
            return self.eval_fix(args[0], depth + 1)

        if primitive_id == 1:  # succ
            n = self.require_nat(args[0], depth + 1)
            return VNat(n.value + 1)

        if primitive_id == 2:  # pred
            n = self.require_nat(args[0], depth + 1)
            return VNat(0 if n.value == 0 else n.value - 1)

        if primitive_id == 3:  # ifz
            n = self.require_nat(args[0], depth + 1)
            selected = args[1] if n.value == 0 else args[2]
            return self.force(selected, depth + 1)

        if primitive_id == 4:  # pair
            return VPair(args[0], args[1])

        if primitive_id == 5:  # fst
            pair = self.force(args[0], depth + 1)
            if not isinstance(pair, VPair):
                raise RuntimeShapeError("fst argument did not evaluate to Pair WHNF")
            return self.force(pair.left, depth + 1)

        if primitive_id == 6:  # snd
            pair = self.force(args[0], depth + 1)
            if not isinstance(pair, VPair):
                raise RuntimeShapeError("snd argument did not evaluate to Pair WHNF")
            return self.force(pair.right, depth + 1)

        if primitive_id == 7:  # inl
            return VInl(args[0])

        if primitive_id == 8:  # inr
            return VInr(args[0])

        if primitive_id == 9:  # case
            scrutinee = self.force(args[0], depth + 1)
            if isinstance(scrutinee, VInl):
                selected_function = self.force(args[1], depth + 1)
                return self.apply_value(selected_function, scrutinee.payload, depth + 1)
            if isinstance(scrutinee, VInr):
                selected_function = self.force(args[2], depth + 1)
                return self.apply_value(selected_function, scrutinee.payload, depth + 1)
            raise RuntimeShapeError("case scrutinee did not evaluate to sum WHNF")

        if primitive_id == 10:
            return VUnit()

        raise UnknownPrimitiveError(f"unknown Core primitive id {primitive_id}")


def evaluate(term: Term, limits: EvaluationLimits = EvaluationLimits()) -> Value:
    # A conforming evaluator accepts only closed, well-typed Core terms.
    infer_principal(term)
    evaluator = _Evaluator(limits)
    try:
        return evaluator.eval_term(term, [], 1)
    except RecursionError:
        # Host recursion exhaustion is an implementation resource refusal, never
        # a semantic proof of divergence or an invalidity classification.
        raise EvaluationResourceLimitError("host recursion resource exhausted") from None


def observe(value: Value) -> dict[str, str]:
    # Observation is intentionally shallow: delayed pair/sum components are not forced.
    if isinstance(value, (VClosure, VPrim)):
        return {"kind": "Function"}
    if isinstance(value, VNat):
        return {"kind": "Nat", "value": str(value.value)}
    if isinstance(value, VUnit):
        return {"kind": "Unit"}
    if isinstance(value, VPair):
        return {"kind": "Pair"}
    if isinstance(value, VInl):
        return {"kind": "Inl"}
    if isinstance(value, VInr):
        return {"kind": "Inr"}
    raise TypeError(type(value).__name__)


def evaluate_observed(term: Term, limits: EvaluationLimits = EvaluationLimits()) -> dict[str, str]:
    return observe(evaluate(term, limits))
