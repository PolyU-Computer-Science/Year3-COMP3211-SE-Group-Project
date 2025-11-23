from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .piece import Piece
from .position import Position


@dataclass(frozen=True)
class Move:
    player: str
    piece: str
    source: str
    target: str
    capture: Optional[str] = None

    @staticmethod
    def from_pieces(player: str, moving_piece: Piece, source: Position, target: Position, captured: Optional[Piece]) -> "Move":
        capture_desc = f"{captured.owner.name} {captured.piece_type.name}" if captured else None
        return Move(
            player=player,
            piece=f"{moving_piece.owner.name} {moving_piece.piece_type.name}",
            source=source.to_notation(),
            target=target.to_notation(),
            capture=capture_desc,
        )
