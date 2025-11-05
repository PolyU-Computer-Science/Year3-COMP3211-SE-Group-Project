from __future__ import annotations
from typing import List, Optional, Tuple
from .types import Player, Move, Piece
from .board import Board, DEN_POS
from .rules import is_legal_move


class GameState:
    def __init__(self) -> None:
        self.board = Board()
        self.current_player: Player = Player.P1
        self.history: List[Move] = []
        self.undo_used = {Player.P1: 0, Player.P2: 0}
        self.players_name = {Player.P1: "Player1", Player.P2: "Player2"}
        self._winner: Optional[Player] = None

    def set_player_names(self, p1: str, p2: str) -> None:
        self.players_name[Player.P1] = p1
        self.players_name[Player.P2] = p2

    def winner(self) -> Optional[Player]:
        return self._winner

    def _check_winner(self) -> Optional[Player]:
        # Enter enemy den
        for owner in (Player.P1, Player.P2):
            ex, ey = DEN_POS[owner]
            piece = self.board.piece_at(ex, ey)
            if piece and piece.owner != owner:
                self._winner = piece.owner
                return self._winner
        # Or capture all opponent pieces
        for owner in (Player.P1, Player.P2):
            if len(self.board.owner_pieces(owner)) == 0:
                self._winner = owner.opponent()
                return self._winner
        return None

    def legal_move(self, from_xy: Tuple[int, int], to_xy: Tuple[int, int]) -> Tuple[bool, str]:
        fx, fy = from_xy
        tx, ty = to_xy
        piece = self.board.piece_at(fx, fy)
        if piece is None:
            return False, "起始位置没有棋子"
        if piece.owner != self.current_player:
            return False, "不是你的回合"
        ok, reason = is_legal_move(self.board, piece, tx, ty)
        return ok, reason

    def move(self, from_xy: Tuple[int, int], to_xy: Tuple[int, int]) -> Tuple[bool, str]:
        ok, reason = self.legal_move(from_xy, to_xy)
        if not ok:
            return False, reason
        fx, fy = from_xy
        tx, ty = to_xy
        piece = self.board.remove_piece(fx, fy)
        assert piece is not None
        captured = self.board.remove_piece(tx, ty)
        self.board.place_piece(piece, tx, ty)
        mv = Move(self.current_player, from_xy, to_xy, piece.animal, captured)
        self.history.append(mv)
        self._check_winner()
        self.current_player = self.current_player.opponent()
        return True, ""

    def undo(self) -> Tuple[bool, str]:
        if len(self.history) == 0:
            return False, "无可撤销的步数"
        prev_player = self.current_player.opponent()
        if self.undo_used[prev_player] >= 3:
            return False, "每位玩家最多悔棋3次"
        mv = self.history.pop()
        # revert move
        piece = self.board.remove_piece(*mv.to_pos)
        assert piece is not None
        self.board.place_piece(piece, *mv.from_pos)
        if mv.captured is not None:
            self.board.place_piece(mv.captured, *mv.to_pos)
        self.undo_used[prev_player] += 1
        self._winner = None
        self.current_player = prev_player
        return True, ""

    def reset(self) -> None:
        self.__init__()

    def status_lines(self) -> List[str]:
        # Render simple ASCII board with pieces
        def piece_char(p: Piece) -> str:
            c = {
                1: 'r', 2: 'c', 3: 'd', 4: 'w', 5: 'l', 6: 't', 7: 'L', 8: 'e'
            }[p.animal.value]
            return c.upper() if p.owner == Player.P1 else c
        lines: List[str] = []
        header = "   a b c d e f g"
        lines.append(header)
        for y in range(9):
            row = [str(y + 1).rjust(2)]
            for x in range(7):
                p = self.board.piece_at(x, y)
                if p:
                    row.append(piece_char(p))
                else:
                    # water ~, den D/d, trap ^/v, land .
                    st = self.board.square_type(x, y)
                    ch = {
                        1: '~', 2: '^', 3: 'v', 4: 'D', 5: 'd'
                    }.get(st.value, '.')
                    row.append(ch)
            lines.append(" ".join(row))
        lines.append(
            f"回合: {self.players_name[self.current_player]} ({'P1' if self.current_player == Player.P1 else 'P2'})")
        if self._winner:
            lines.append(
                f"胜者: {self.players_name[self._winner]} ({'P1' if self._winner == Player.P1 else 'P2'})")
        return lines
