import unittest
from model.game import GameState
from model.board import Board, DEN_POS
from model.types import Player, Animal, Piece
from model.rules import is_legal_move


def setup_minimal(gs: GameState):
    gs.board.pieces.clear()


def place(gs: GameState, animal: Animal, owner: Player, x: int, y: int):
    p = Piece(animal, owner, x, y)
    gs.board.place_piece(p, x, y)
    return p


class TestRules(unittest.TestCase):
    def test_cannot_enter_own_den(self):
        gs = GameState()
        setup_minimal(gs)
        # Put a dog next to own den and try to enter
        dx, dy = (3, 8)
        place(gs, Animal.DOG, Player.P1, 3, 7)
        ok, msg = gs.legal_move((3, 7), (dx, dy))
        self.assertFalse(ok)

    def test_rat_water_and_capture_elephant(self):
        gs = GameState()
        setup_minimal(gs)
        # Rat can enter water, but cannot capture elephant from water
        # Place rat in river (1,3) and elephant adjacent on land at (1,2)
        place(gs, Animal.RAT, Player.P1, 1, 3)
        place(gs, Animal.ELEPHANT, Player.P2, 1, 2)
        ok, msg = gs.legal_move((1, 3), (1, 2))
        self.assertFalse(ok)  # cannot from water
        # Now put rat on land at (1,1) and elephant at (1,2) to test rat>elephant
        setup_minimal(gs)
        place(gs, Animal.RAT, Player.P1, 1, 1)
        place(gs, Animal.ELEPHANT, Player.P2, 1, 2)
        ok, msg = gs.legal_move((1, 1), (1, 2))
        self.assertTrue(ok)

    def test_lion_jump_blocked_by_rat(self):
        gs = GameState()
        setup_minimal(gs)
        # Place lion at (0,2) and attempt jump to (0,6) across river rows 3..5
        place(gs, Animal.LION, Player.P1, 0, 2)
        # Place blocking rat in river at (0,3) (not a river square; rivers are columns 1,2,4,5) -> adjust to (1,3)
        gs.board.remove_piece(0, 2)  # reset
        place(gs, Animal.LION, Player.P1, 1, 2)  # column 1 above river
        place(gs, Animal.RAT, Player.P1, 1, 3)   # in river
        # Try jump from (1,2) to (1,6)
        ok, msg = gs.legal_move((1, 2), (1, 6))
        self.assertFalse(ok)

    def test_trap_capture_any(self):
        gs = GameState()
        setup_minimal(gs)
        # Put weak cat to capture strong elephant in own traps
        # P1 traps at (2,8),(4,8),(3,7)
        place(gs, Animal.ELEPHANT, Player.P2, 3, 7)  # enemy in our trap
        place(gs, Animal.CAT, Player.P1, 3, 6)
        ok, msg = gs.legal_move((3, 6), (3, 7))
        self.assertTrue(ok)

    def test_undo_limit(self):
        gs = GameState()
        setup_minimal(gs)
        # Place two rats to shuffle
        place(gs, Animal.RAT, Player.P1, 0, 6)
        place(gs, Animal.RAT, Player.P2, 0, 2)
        # Make 3 moves and undo each time by same player (simulate alternating)
        for i in range(3):
            ok, _ = gs.move((0, 6), (0, 5))
            self.assertTrue(ok)
            ok, _ = gs.undo()
            self.assertTrue(ok)
        # Fourth undo should fail for P1
        ok, msg = gs.undo()
        self.assertFalse(ok)


if __name__ == '__main__':
    unittest.main()
