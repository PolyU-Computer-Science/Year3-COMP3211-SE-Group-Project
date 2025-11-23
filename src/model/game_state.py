from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .board import Board, BLUE_DEN, RED_DEN, InvalidMoveError
from .enums import PieceType, PlayerSide
from .move import Move
from .piece import Piece
from .position import Position


UNDO_LIMIT = 3


@dataclass
class HistorySnapshot:
    board: Board
    current_player: PlayerSide
    winner: Optional[PlayerSide]
    move_log_size: int


@dataclass
class GameState:
    board: Board = field(default_factory=Board.initial)
    player_names: Dict[PlayerSide, str] = field(
        default_factory=lambda: {PlayerSide.BLUE: "Blue", PlayerSide.RED: "Red"})
    current_player: PlayerSide = PlayerSide.BLUE
    winner: Optional[PlayerSide] = None
    undo_remaining: Dict[PlayerSide, int] = field(
        default_factory=lambda: {PlayerSide.BLUE: UNDO_LIMIT, PlayerSide.RED: UNDO_LIMIT})
    _history: List[HistorySnapshot] = field(default_factory=list)
    _move_log: List[Move] = field(default_factory=list)

    @staticmethod
    def new(player_blue: Optional[str] = None, player_red: Optional[str] = None) -> "GameState":
        state = GameState()
        if player_blue:
            state.player_names[PlayerSide.BLUE] = player_blue
        if player_red:
            state.player_names[PlayerSide.RED] = player_red
        return state

    def rename_player(self, side: PlayerSide, name: str) -> None:
        if not name.strip():
            raise ValueError("Player name may not be empty.")
        self.player_names[side] = name.strip()

    def available_moves(self) -> int:
        return len(self._move_log)

    def last_moves(self, count: int = 5) -> List[Move]:
        return self._move_log[-count:]

    def move(self, src: Position, dst: Position) -> Move:
        if self.winner:
            raise InvalidMoveError("The game has already finished.")

        snapshot = self._create_snapshot()
        moved_piece, captured = self.board.move(self.current_player, src, dst)
        self._history.append(snapshot)
        move_record = Move.from_pieces(
            player=self.player_names[self.current_player],
            moving_piece=moved_piece,
            source=src,
            target=dst,
            captured=captured,
        )
        self._move_log.append(move_record)

        victor = self._determine_victory(moved_piece, captured)
        if victor:
            self.winner = victor

        self.current_player = self.current_player.opponent()
        return move_record

    def _determine_victory(self, moved_piece: Piece, captured: Optional[Piece]) -> Optional[PlayerSide]:
        if moved_piece.owner is PlayerSide.BLUE and moved_piece.position == RED_DEN:
            return PlayerSide.BLUE
        if moved_piece.owner is PlayerSide.RED and moved_piece.position == BLUE_DEN:
            return PlayerSide.RED

        if captured and not any(p.owner is captured.owner for p in self.board.iter_pieces()):
            return moved_piece.owner
        return None

    def undo(self, requester: PlayerSide) -> None:
        if not self._history:
            raise InvalidMoveError("No moves to undo.")
        if self.undo_remaining[requester] <= 0:
            raise InvalidMoveError(
                "Undo limit reached (max three per player).")

        snapshot = self._history.pop()
        self.board = snapshot.board
        self.current_player = snapshot.current_player
        self.winner = snapshot.winner
        while len(self._move_log) > snapshot.move_log_size:
            self._move_log.pop()
        self.undo_remaining[requester] -= 1

    def _create_snapshot(self) -> HistorySnapshot:
        return HistorySnapshot(
            board=self.board.copy(),
            current_player=self.current_player,
            winner=self.winner,
            move_log_size=len(self._move_log),
        )

    def to_dict(self) -> dict:
        return {
            "players": {side.value: name for side, name in self.player_names.items()},
            "current_player": self.current_player.value,
            "winner": self.winner.value if self.winner else None,
            "undo_remaining": {side.value: count for side, count in self.undo_remaining.items()},
            "pieces": [
                {
                    "type": piece.piece_type.value,
                    "owner": piece.owner.value,
                    "row": piece.position.row,
                    "col": piece.position.col,
                }
                for piece in self.board.iter_pieces()
            ],
            "moves": [move.__dict__ for move in self._move_log],
        }

    @staticmethod
    def from_dict(payload: dict) -> "GameState":
        board = Board()
        for entry in payload["pieces"]:
            piece = Piece(
                piece_type=PieceType(entry["type"]),
                owner=PlayerSide(entry["owner"]),
                position=Position(row=entry["row"], col=entry["col"]),
            )
            board._place_piece(piece)
        state = GameState(board=board)
        state.player_names = {PlayerSide(
            side): name for side, name in payload["players"].items()}
        state.current_player = PlayerSide(payload["current_player"])
        state.winner = PlayerSide(
            payload["winner"]) if payload.get("winner") else None
        state.undo_remaining = {PlayerSide(
            side): count for side, count in payload["undo_remaining"].items()}
        state._move_log = [Move(**entry) for entry in payload.get("moves", [])]
        return state

    @property
    def move_log(self) -> List[Move]:
        return list(self._move_log)
