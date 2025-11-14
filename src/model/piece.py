from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .enums import PieceType, PlayerSide
from .position import Position


@dataclass(frozen=True)
class Piece:
    piece_type: PieceType
    owner: PlayerSide
    position: Position

    def with_position(self, position: Position) -> "Piece":
        return Piece(piece_type=self.piece_type, owner=self.owner, position=position)

    @property
    def notation(self) -> str:
        base = self.piece_type.definition.short_name
        return base.upper() if self.owner is PlayerSide.BLUE else base.lower()


CapturedPiece = tuple[Piece, Position]


def describe_capture(piece: Optional[Piece]) -> str:
    if not piece:
        return ""
    return f"{piece.owner.name} {piece.piece_type.name}"
