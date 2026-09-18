from __future__ import annotations

from dataclasses import dataclass

from .term import App, Lam, Let, Nat, Prim, Term, Var


class WireError(ValueError):
    """Base class for wire syntax/shape errors."""


class TruncatedError(WireError):
    pass


class TrailingDataError(WireError):
    pass


class InvalidBitError(WireError):
    pass


class ResourceLimitError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class DecodeLimits:
    max_integer_bits: int | None = None
    max_depth: int | None = None
    max_nodes: int | None = None

    def __post_init__(self) -> None:
        for name in ("max_integer_bits", "max_depth", "max_nodes"):
            value = getattr(self, name)
            if value is not None and value < 0:
                raise ValueError(f"{name} must be non-negative or None")

    @staticmethod
    def _active(value: int | None) -> bool:
        # Packet ADR-0006 notes that zero in the reference API means unlimited.
        return value not in (None, 0)


UNLIMITED = DecodeLimits()


def _validate_bits(bits: str) -> None:
    if not isinstance(bits, str):
        raise TypeError("bit stream must be a string")
    bad = next((c for c in bits if c not in "01"), None)
    if bad is not None:
        raise InvalidBitError(f"invalid bit {bad!r}")


def encode_u(n: int) -> str:
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("U(n) is defined only for non-negative n")
    payload = bin(n + 1)[2:]
    return "0" * (len(payload) - 1) + payload


def decode_u(bits: str, offset: int = 0, limits: DecodeLimits = UNLIMITED) -> tuple[int, int]:
    _validate_bits(bits)
    if offset < 0 or offset > len(bits):
        raise ValueError("offset outside bit stream")
    start = offset
    zeros = 0
    while offset < len(bits) and bits[offset] == "0":
        zeros += 1
        integer_bits = zeros + 1
        if DecodeLimits._active(limits.max_integer_bits) and integer_bits > limits.max_integer_bits:  # type: ignore[operator]
            raise ResourceLimitError("integer bit-length limit exceeded")
        offset += 1
    if offset >= len(bits):
        raise TruncatedError("truncated U(n): missing leading 1")

    length = zeros + 1
    if DecodeLimits._active(limits.max_integer_bits) and length > limits.max_integer_bits:  # type: ignore[operator]
        raise ResourceLimitError("integer bit-length limit exceeded")
    end = offset + length
    if end > len(bits):
        raise TruncatedError("truncated U(n) payload")
    payload = bits[offset:end]
    # payload necessarily begins with 1 due to the loop above.
    m = int(payload, 2)
    return m - 1, end - start


def encode_term(term: Term) -> str:
    match term:
        case Var(index):
            return "00" + encode_u(index)
        case Lam(body):
            return "01" + encode_term(body)
        case App(function, argument):
            return "10" + encode_term(function) + encode_term(argument)
        case Let(value, body):
            return "110" + encode_term(value) + encode_term(body)
        case Nat(value):
            return "1110" + encode_u(value)
        case Prim(id):
            return "1111" + encode_u(id)
        case _:
            raise TypeError(f"unsupported term object: {type(term).__name__}")


@dataclass(slots=True)
class _DecodeState:
    bits: str
    limits: DecodeLimits
    nodes: int = 0

    def note_node(self, depth: int) -> None:
        self.nodes += 1
        if DecodeLimits._active(self.limits.max_nodes) and self.nodes > self.limits.max_nodes:  # type: ignore[operator]
            raise ResourceLimitError("node limit exceeded")
        if DecodeLimits._active(self.limits.max_depth) and depth > self.limits.max_depth:  # type: ignore[operator]
            raise ResourceLimitError("term depth limit exceeded")

    def need(self, offset: int, literal: str) -> int:
        end = offset + len(literal)
        if end > len(self.bits):
            raise TruncatedError("truncated term prefix")
        if self.bits[offset:end] != literal:
            raise AssertionError("internal prefix parser mismatch")
        return end

    def decode_term(self, offset: int, depth: int) -> tuple[Term, int]:
        self.note_node(depth)
        if offset >= len(self.bits):
            raise TruncatedError("truncated term")
        # Prefix-free dispatch. Check shorter discriminants first.
        if self.bits.startswith("00", offset):
            pos = self.need(offset, "00")
            value, used = decode_u(self.bits, pos, self.limits)
            return Var(value), pos + used
        if self.bits.startswith("01", offset):
            pos = self.need(offset, "01")
            body, pos = self.decode_term(pos, depth + 1)
            return Lam(body), pos
        if self.bits.startswith("10", offset):
            pos = self.need(offset, "10")
            function, pos = self.decode_term(pos, depth + 1)
            argument, pos = self.decode_term(pos, depth + 1)
            return App(function, argument), pos
        # Any stream beginning with 11 needs at least a third bit before Let/Nat/Prim is known.
        if not self.bits.startswith("11", offset):
            # With valid bits this can only happen when one prefix bit remains.
            raise TruncatedError("truncated term prefix")
        if offset + 3 > len(self.bits):
            raise TruncatedError("truncated term prefix")
        if self.bits.startswith("110", offset):
            pos = self.need(offset, "110")
            value, pos = self.decode_term(pos, depth + 1)
            body, pos = self.decode_term(pos, depth + 1)
            return Let(value, body), pos
        # Prefix 111 requires one more bit.
        if offset + 4 > len(self.bits):
            raise TruncatedError("truncated term prefix")
        if self.bits.startswith("1110", offset):
            pos = self.need(offset, "1110")
            value, used = decode_u(self.bits, pos, self.limits)
            return Nat(value), pos + used
        if self.bits.startswith("1111", offset):
            pos = self.need(offset, "1111")
            value, used = decode_u(self.bits, pos, self.limits)
            return Prim(value), pos + used
        raise AssertionError("unreachable prefix")


def decode_one(bits: str, limits: DecodeLimits = UNLIMITED) -> tuple[Term, int]:
    _validate_bits(bits)
    state = _DecodeState(bits, limits)
    try:
        term, end = state.decode_term(0, 1)
    except RecursionError:
        # Host stack exhaustion on a syntactically valid, deeply nested term is
        # an implementation resource refusal, not malformed wire data.
        raise ResourceLimitError("host recursion resource exhausted while decoding") from None
    return term, end


def decode_exact(bits: str, limits: DecodeLimits = UNLIMITED) -> Term:
    term, consumed = decode_one(bits, limits)
    if consumed != len(bits):
        raise TrailingDataError(f"{len(bits) - consumed} trailing bit(s)")
    return term
