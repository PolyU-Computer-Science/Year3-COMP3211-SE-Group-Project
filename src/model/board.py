from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Optional, Tuple

from .enums import PieceType, PlayerSide, SquareType
from .piece import Piece
from .position import BOARD_HEIGHT, BOARD_WIDTH, Position, in_bounds


class InvalidMoveError(RuntimeError):
    """Raised when a move violates Jungle rules."""


PositionKey = Tuple[int, int]


def _pos_key(position: Position) -> PositionKey:
    return position.row, position.col


BLUE_TRAPS = {Position(0, 2), Position(0, 4), Position(1, 3)}
RED_TRAPS = {Position(8, 2), Position(8, 4), Position(7, 3)}
BLUE_DEN = Position(0, 3)
RED_DEN = Position(8, 3)
RIVER_COORDS = {
    (row, col)
    for row in (3, 4, 5)
    for col in (1, 2, 4, 5)
}


INITIAL_BLUE_POSITIONS: dict[PieceType, Position] = {
    PieceType.LION: Position(0, 0),
    PieceType.TIGER: Position(0, 6),
    PieceType.DOG: Position(1, 1),
    PieceType.CAT: Position(1, 5),
    PieceType.RAT: Position(2, 0),
    PieceType.LEOPARD: Position(2, 2),
    PieceType.WOLF: Position(2, 4),
    PieceType.ELEPHANT: Position(2, 6),
}


def _mirror_position(position: Position) -> Position:
    return Position(row=BOARD_HEIGHT - 1 - position.row, col=BOARD_WIDTH - 1 - position.col)


@dataclass
class Board:
    _pieces: Dict[PositionKey, Piece] = field(default_factory=dict)

    @staticmethod
    def initial() -> "Board":
        board = Board()
        for piece_type, pos in INITIAL_BLUE_POSITIONS.items():
            board._place_piece(Piece(piece_type=piece_type,
                               owner=PlayerSide.BLUE, position=pos))
            mirrored = _mirror_position(pos)
            board._place_piece(Piece(piece_type=piece_type,
                               owner=PlayerSide.RED, position=mirrored))
        return board

    def copy(self) -> "Board":
        clone = Board()
        for piece in self._pieces.values():
            clone._place_piece(
                Piece(piece_type=piece.piece_type, owner=piece.owner, position=piece.position))
        return clone

    def iter_pieces(self) -> Iterable[Piece]:
        return self._pieces.values()

    def piece_at(self, position: Position) -> Optional[Piece]:
        return self._pieces.get(_pos_key(position))

    def remove_piece(self, position: Position) -> Optional[Piece]:
        return self._pieces.pop(_pos_key(position), None)

    def _place_piece(self, piece: Piece) -> None:
        self._pieces[_pos_key(piece.position)] = piece

    def move(self, player: PlayerSide, source: Position, target: Position) -> Tuple[Piece, Optional[Piece]]:
        self._validate_basic_coordinates(source, target)
        piece = self.piece_at(source)
        if not piece:
            raise InvalidMoveError("No piece on the source square.")
        if piece.owner is not player:
            raise InvalidMoveError("You can only move your own pieces.")

        captured = self.piece_at(target)
        if captured and captured.owner is player:
            raise InvalidMoveError(
                "Target square already filled by your piece.")

        self._validate_movement(piece, source, target, captured)

        self.remove_piece(source)
        if captured:
            self.remove_piece(target)

        moved_piece = piece.with_position(target)
        self._place_piece(moved_piece)

        return moved_piece, captured

    def square_type(self, position: Position) -> SquareType:
        key = _pos_key(position)
        if key in RIVER_COORDS:
            return SquareType.RIVER
        if position == BLUE_DEN:
            return SquareType.DEN_BLUE
        if position == RED_DEN:
            return SquareType.DEN_RED
        if position in BLUE_TRAPS:
            return SquareType.TRAP_BLUE
        if position in RED_TRAPS:
            return SquareType.TRAP_RED
        return SquareType.LAND

    def _validate_basic_coordinates(self, source: Position, target: Position) -> None:
        if not in_bounds(source.row, source.col) or not in_bounds(target.row, target.col):
            raise InvalidMoveError("Move must remain inside the board.")
        if source == target:
            raise InvalidMoveError("Source and target squares differ.")

    def _validate_movement(self, piece: Piece, source: Position, target: Position, captured: Optional[Piece]) -> None:
        target_square = self.square_type(target)
        source_square = self.square_type(source)

        if target_square.is_den and ((target_square == SquareType.DEN_BLUE and piece.owner is PlayerSide.BLUE) or (target_square == SquareType.DEN_RED and piece.owner is PlayerSide.RED)):
            raise InvalidMoveError("You may not enter your own den.")

        if target_square == SquareType.RIVER and not piece.piece_type.definition.can_swim:
            raise InvalidMoveError("Only rats may enter the river.")

        dy, dx = source.delta(target)
        manhattan = abs(dy) + abs(dx)

        if manhattan == 1:
            self._validate_capture(piece, source_square,
                                   target_square, captured, source, target)
            return

        if piece.piece_type.definition.can_jump and (dy == 0 or dx == 0):
            self._validate_jump(piece, source, target, captured)
            return

        raise InvalidMoveError(
            "Illegal movement. Pieces move one square orthogonally, lions/tigers may jump rivers.")

    def _validate_jump(self, piece: Piece, source: Position, target: Position, captured: Optional[Piece]) -> None:
        direction_row = 0 if source.row == target.row else (
            1 if target.row > source.row else -1)
        direction_col = 0 if source.col == target.col else (
            1 if target.col > source.col else -1)

        if direction_row != 0 and direction_col != 0:
            raise InvalidMoveError("Jumping must be horizontal or vertical.")

        current = Position(source.row + direction_row,
                           source.col + direction_col)
        encountered_water = False
        while current != target:
            if not in_bounds(current.row, current.col):
                raise InvalidMoveError("Jump exceeds board boundaries.")
            if self.square_type(current) != SquareType.RIVER:
                raise InvalidMoveError(
                    "Lions and tigers may only jump over rivers.")
            encountered_water = True
            blocking_piece = self.piece_at(current)
            if blocking_piece:
                raise InvalidMoveError(
                    "Cannot jump because a rat blocks the river path.")
            current = Position(current.row + direction_row,
                               current.col + direction_col)

        if not encountered_water:
            raise InvalidMoveError(
                "Jump must cross at least one river square.")

        if self.square_type(target) == SquareType.RIVER:
            raise InvalidMoveError(
                "Jump lands on land immediately beyond the river.")

        self._validate_capture(piece, self.square_type(
            source), self.square_type(target), captured, source, target)

    def _validate_capture(
        self,
        piece: Piece,
        source_square: SquareType,
        target_square: SquareType,
        captured: Optional[Piece],
        source: Position,
        target: Position,
    ) -> None:
        if not captured:
            return

        if captured.owner is piece.owner:
            raise InvalidMoveError("Cannot capture your own piece.")

        if piece.piece_type is PieceType.RAT:
            self._validate_rat_capture(source_square, target_square, captured)
        elif captured.piece_type is PieceType.RAT and piece.piece_type is PieceType.ELEPHANT:
            raise InvalidMoveError("Elephants cannot capture rats.")

        attacker_rank = piece.piece_type.definition.rank
        defender_rank = captured.piece_type.definition.rank

        if target_square == SquareType.TRAP_BLUE and captured.owner is PlayerSide.RED:
            defender_rank = 0
        if target_square == SquareType.TRAP_RED and captured.owner is PlayerSide.BLUE:
            defender_rank = 0

        if attacker_rank < defender_rank and not (piece.piece_type is PieceType.RAT and captured.piece_type is PieceType.ELEPHANT):
            raise InvalidMoveError("Attacker rank too low to capture target.")

        if piece.piece_type is PieceType.RAT and captured.piece_type is PieceType.ELEPHANT:
            if source_square == SquareType.RIVER or target_square == SquareType.RIVER:
                raise InvalidMoveError(
                    "Rats cannot attack elephants from river squares.")

    def _validate_rat_capture(self, source_square: SquareType, target_square: SquareType, captured: Piece) -> None:
        if source_square == SquareType.RIVER and target_square != SquareType.RIVER and captured.piece_type in {PieceType.RAT, PieceType.ELEPHANT}:
            raise InvalidMoveError(
                "A rat cannot capture an elephant or rat on land directly from water.")
        if source_square != SquareType.RIVER and target_square == SquareType.RIVER and captured.piece_type is PieceType.RAT:
            raise InvalidMoveError(
                "A rat on land cannot attack a rat in the water.")
