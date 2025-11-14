from __future__ import annotations

from dataclasses import dataclass

BOARD_WIDTH = 7
BOARD_HEIGHT = 9
COLUMN_NAMES = "abcdefg"


def in_bounds(row: int, col: int) -> bool:
    return 0 <= row < BOARD_HEIGHT and 0 <= col < BOARD_WIDTH


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def delta(self, other: "Position") -> tuple[int, int]:
        return other.row - self.row, other.col - self.col

    def is_adjacent(self, other: "Position") -> bool:
        dy, dx = self.delta(other)
        return abs(dy) + abs(dx) == 1

    def to_notation(self) -> str:
        return f"{COLUMN_NAMES[self.col]}{self.row + 1}"

    @staticmethod
    def from_notation(token: str) -> "Position":
        token = token.strip().lower()
        if len(token) < 2 or token[0] not in COLUMN_NAMES:
            raise ValueError(f"Invalid coordinate: {token}")
        try:
            col = COLUMN_NAMES.index(token[0])
            row = int(token[1:]) - 1
        except ValueError as exc:  # pragma: no cover - ValueError already described
            raise ValueError(f"Invalid coordinate: {token}") from exc
        if not in_bounds(row, col):
            raise ValueError(f"Coordinate out of range: {token}")
        return Position(row=row, col=col)
