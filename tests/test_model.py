import tempfile
import unittest
from pathlib import Path

from src.model.board import Board, InvalidMoveError
from src.model.enums import PieceType, PlayerSide
from src.model.game_state import GameState, UNDO_LIMIT
from src.model.piece import Piece
from src.model.position import Position
from src.model.serialization import load_game, save_game


class BoardRulesTest(unittest.TestCase):
    def test_initial_setup_has_all_pieces(self) -> None:
        board = Board.initial()
        pieces = list(board.iter_pieces())
        self.assertEqual(16, len(pieces))
        self.assertEqual(
            8, sum(1 for piece in pieces if piece.owner is PlayerSide.BLUE))
        self.assertEqual(
            8, sum(1 for piece in pieces if piece.owner is PlayerSide.RED))

    def test_non_rat_cannot_enter_water(self) -> None:
        board = Board()
        cat = Piece(PieceType.CAT, PlayerSide.BLUE, Position(3, 0))
        board._place_piece(cat)
        with self.assertRaises(InvalidMoveError):
            board.move(PlayerSide.BLUE, Position(3, 0), Position(3, 1))

    def test_rat_can_swim_and_capture_rules(self) -> None:
        water_board = Board()
        rat = Piece(PieceType.RAT, PlayerSide.BLUE, Position(3, 1))
        elephant = Piece(PieceType.ELEPHANT, PlayerSide.RED, Position(3, 2))
        water_board._place_piece(rat)
        water_board._place_piece(elephant)
        with self.assertRaises(InvalidMoveError):
            water_board.move(PlayerSide.BLUE, Position(3, 1), Position(3, 2))

        land_board = Board()
        land_rat = Piece(PieceType.RAT, PlayerSide.BLUE, Position(2, 3))
        elephant2 = Piece(PieceType.ELEPHANT, PlayerSide.RED, Position(2, 4))
        land_board._place_piece(land_rat)
        land_board._place_piece(elephant2)
        land_board.move(PlayerSide.BLUE, Position(2, 3), Position(2, 4))

    def test_lion_jump_blocked_by_rat(self) -> None:
        board = Board()
        lion = Piece(PieceType.LION, PlayerSide.BLUE, Position(2, 1))
        board._place_piece(lion)
        blocking_rat = Piece(PieceType.RAT, PlayerSide.RED, Position(4, 1))
        board._place_piece(blocking_rat)
        with self.assertRaises(InvalidMoveError):
            board.move(PlayerSide.BLUE, Position(2, 1), Position(6, 1))
        board.remove_piece(Position(4, 1))
        board.move(PlayerSide.BLUE, Position(2, 1), Position(6, 1))

    def test_trap_removes_rank(self) -> None:
        board = Board()
        cat = Piece(PieceType.CAT, PlayerSide.BLUE, Position(1, 2))
        elephant = Piece(PieceType.ELEPHANT, PlayerSide.RED,
                         Position(1, 3))  # Blue trap square
        board._place_piece(cat)
        board._place_piece(elephant)
        board.move(PlayerSide.BLUE, Position(1, 2), Position(1, 3))


class GameStateTest(unittest.TestCase):
    def test_victory_by_den_entry(self) -> None:
        board = Board()
        piece = Piece(PieceType.RAT, PlayerSide.BLUE, Position(7, 3))
        board._place_piece(piece)
        state = GameState(board=board)
        state.move(Position(7, 3), Position(8, 3))
        self.assertEqual(PlayerSide.BLUE, state.winner)

    def test_undo_limit_enforced(self) -> None:
        state = GameState.new("Blue", "Red")
        # perform enough moves to allow undo attempts
        state.move(Position(2, 0), Position(2, 1))
        state.move(Position(6, 6), Position(5, 6))
        state.move(Position(2, 1), Position(2, 0))
        state.move(Position(5, 6), Position(6, 6))
        for _ in range(UNDO_LIMIT):
            state.undo(PlayerSide.BLUE)
        with self.assertRaises(InvalidMoveError):
            state.undo(PlayerSide.BLUE)

    def test_save_and_load_roundtrip(self) -> None:
        state = GameState.new("Alpha", "Beta")
        state.move(Position(2, 0), Position(2, 1))
        state.move(Position(6, 6), Position(5, 6))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "game.jungle"
            save_game(state, path)
            loaded = load_game(path)
        self.assertEqual(state.player_names, loaded.player_names)
        self.assertEqual(state.current_player, loaded.current_player)
        self.assertEqual(len(state.move_log), len(loaded.move_log))


if __name__ == "__main__":
    unittest.main()
