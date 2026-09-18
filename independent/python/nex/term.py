from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias


@dataclass(frozen=True, slots=True)
class Var:
    index: int

    def __post_init__(self) -> None:
        if self.index < 0:
            raise ValueError("de Bruijn index must be non-negative")


@dataclass(frozen=True, slots=True)
class Lam:
    body: "Term"


@dataclass(frozen=True, slots=True)
class App:
    function: "Term"
    argument: "Term"


@dataclass(frozen=True, slots=True)
class Let:
    value: "Term"
    body: "Term"


@dataclass(frozen=True, slots=True)
class Nat:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("natural value must be non-negative")


@dataclass(frozen=True, slots=True)
class Prim:
    id: int

    def __post_init__(self) -> None:
        if self.id < 0:
            raise ValueError("primitive id must be non-negative")


Term: TypeAlias = Var | Lam | App | Let | Nat | Prim
