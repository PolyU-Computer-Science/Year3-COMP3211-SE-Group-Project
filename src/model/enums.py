from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PlayerSide(str, Enum):
    BLUE = "BLUE"
    RED = "RED"

    def opponent(self) -> "PlayerSide":
        return PlayerSide.RED if self is PlayerSide.BLUE else PlayerSide.BLUE


class SquareType(str, Enum):
    LAND = "LAND"
    RIVER = "RIVER"
    TRAP_BLUE = "TRAP_BLUE"
    TRAP_RED = "TRAP_RED"
    DEN_BLUE = "DEN_BLUE"
    DEN_RED = "DEN_RED"

    @property
    def is_trap(self) -> bool:
        return self in {SquareType.TRAP_BLUE, SquareType.TRAP_RED}

    @property
    def is_den(self) -> bool:
        return self in {SquareType.DEN_BLUE, SquareType.DEN_RED}


@dataclass(frozen=True)
class PieceDefinition:
    rank: int
    label: str
    short_name: str
    can_swim: bool = False
    can_jump: bool = False


class PieceType(str, Enum):
    ELEPHANT = "ELEPHANT"
    LION = "LION"
    TIGER = "TIGER"
    LEOPARD = "LEOPARD"
    WOLF = "WOLF"
    DOG = "DOG"
    CAT = "CAT"
    RAT = "RAT"

    @property
    def definition(self) -> PieceDefinition:
        return _PIECE_DEFINITIONS[self]


_PIECE_DEFINITIONS: dict[PieceType, PieceDefinition] = {
    PieceType.ELEPHANT: PieceDefinition(rank=8, label="Elephant", short_name="El"),
    PieceType.LION: PieceDefinition(rank=7, label="Lion", short_name="Li", can_jump=True),
    PieceType.TIGER: PieceDefinition(rank=6, label="Tiger", short_name="Ti", can_jump=True),
    PieceType.LEOPARD: PieceDefinition(rank=5, label="Leopard", short_name="Le"),
    PieceType.WOLF: PieceDefinition(rank=4, label="Wolf", short_name="Wo"),
    PieceType.DOG: PieceDefinition(rank=3, label="Dog", short_name="Do"),
    PieceType.CAT: PieceDefinition(rank=2, label="Cat", short_name="Ca"),
    PieceType.RAT: PieceDefinition(rank=1, label="Rat", short_name="Ra", can_swim=True),
}
