from __future__ import annotations

from typing import Iterable, List

from ..model.board import Board
from ..model.enums import PlayerSide, SquareType
from ..model.position import COLUMN_NAMES, Position, BOARD_HEIGHT, BOARD_WIDTH


SQUARE_SYMBOLS = {
    SquareType.RIVER: "~~",
    SquareType.DEN_BLUE: "DB",
    SquareType.DEN_RED: "DR",
    SquareType.TRAP_BLUE: "tb",
    SquareType.TRAP_RED: "tr",
    SquareType.LAND: "..",
}


def render_board(board: Board) -> str:
    lines: List[str] = []
    for row in range(BOARD_HEIGHT):
        row_cells: List[str] = []
        for col in range(BOARD_WIDTH):
            position = Position(row=row, col=col)
            piece = board.piece_at(position)
            if piece:
                row_cells.append(piece.notation.rjust(2))
            else:
                row_cells.append(SQUARE_SYMBOLS[board.square_type(position)])
        lines.append(f"{row + 1} | {' '.join(row_cells)}")
    footer = "    " + "  ".join(col.upper() for col in COLUMN_NAMES)
    return "\n".join(lines + [footer])


def render_status(board: Board) -> str:
    blue_remaining = _remaining(board, PlayerSide.BLUE)
    red_remaining = _remaining(board, PlayerSide.RED)
    return (
        "Remaining pieces:\n"
        f"  BLUE ({len(blue_remaining)}): {', '.join(blue_remaining)}\n"
        f"  RED  ({len(red_remaining)}): {', '.join(red_remaining)}"
    )


def _remaining(board: Board, side: PlayerSide) -> List[str]:
    return [p.piece_type.name for p in board.iter_pieces() if p.owner is side]
