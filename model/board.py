from __future__ import annotations
from typing import Dict, List, Optional, Tuple
from .types import SquareType, Player, Animal, Piece

BOARD_WIDTH = 7
BOARD_HEIGHT = 9

# Coordinates: x in [0..6] left->right (a..g), y in [0..8] top->bottom (1..9)

RIVER_COLUMNS = {1, 2, 4, 5}
RIVER_ROWS = {3, 4, 5}

DEN_POS = {
    Player.P1: (3, 8),
    Player.P2: (3, 0),
}

TRAP_POS = {
    Player.P1: {(2, 8), (4, 8), (3, 7)},
    Player.P2: {(2, 0), (4, 0), (3, 1)},
}


class Board:
    def __init__(self) -> None:
        self.grid: List[List[SquareType]] = [
            [SquareType.LAND for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self._init_terrain()
        self.pieces: Dict[Tuple[int, int], Piece] = {}
        self._init_pieces()

    def _init_terrain(self) -> None:
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if x in RIVER_COLUMNS and y in RIVER_ROWS:
                    self.grid[y][x] = SquareType.RIVER
        # Dens
        dx1, dy1 = DEN_POS[Player.P1]
        dx2, dy2 = DEN_POS[Player.P2]
        self.grid[dy1][dx1] = SquareType.DEN_P1
        self.grid[dy2][dx2] = SquareType.DEN_P2
        # Traps
        for p in TRAP_POS[Player.P1]:
            self.grid[p[1]][p[0]] = SquareType.TRAP_P1
        for p in TRAP_POS[Player.P2]:
            self.grid[p[1]][p[0]] = SquareType.TRAP_P2

    def _place(self, a: Animal, owner: Player, x: int, y: int) -> None:
        self.pieces[(x, y)] = Piece(a, owner, x, y)

    def _init_pieces(self) -> None:
        # Initial setup based on common Jungle layout (Wikipedia)
        # Top (Player 2)
        self._place(Animal.LION, Player.P2, 0, 0)
        self._place(Animal.TIGER, Player.P2, 6, 0)
        self._place(Animal.DOG, Player.P2, 1, 1)
        self._place(Animal.CAT, Player.P2, 5, 1)
        self._place(Animal.RAT, Player.P2, 0, 2)
        self._place(Animal.LEOPARD, Player.P2, 2, 2)
        self._place(Animal.WOLF, Player.P2, 4, 2)
        self._place(Animal.ELEPHANT, Player.P2, 6, 2)
        # Bottom (Player 1)
        self._place(Animal.ELEPHANT, Player.P1, 0, 6)
        self._place(Animal.WOLF, Player.P1, 2, 6)
        self._place(Animal.LEOPARD, Player.P1, 4, 6)
        self._place(Animal.RAT, Player.P1, 6, 6)
        self._place(Animal.CAT, Player.P1, 1, 7)
        self._place(Animal.DOG, Player.P1, 5, 7)
        self._place(Animal.TIGER, Player.P1, 0, 8)
        self._place(Animal.LION, Player.P1, 6, 8)

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT

    def square_type(self, x: int, y: int) -> SquareType:
        return self.grid[y][x]

    def piece_at(self, x: int, y: int) -> Optional[Piece]:
        return self.pieces.get((x, y))

    def remove_piece(self, x: int, y: int) -> Optional[Piece]:
        return self.pieces.pop((x, y), None)

    def place_piece(self, piece: Piece, x: int, y: int) -> None:
        piece.set_pos((x, y))
        self.pieces[(x, y)] = piece

    def all_pieces(self) -> List[Piece]:
        return list(self.pieces.values())

    def owner_pieces(self, owner: Player) -> List[Piece]:
        return [p for p in self.pieces.values() if p.owner == owner]

    def is_enemy_trap(self, owner: Player, x: int, y: int) -> bool:
        st = self.square_type(x, y)
        return (owner == Player.P1 and st == SquareType.TRAP_P2) or (owner == Player.P2 and st == SquareType.TRAP_P1)

    def is_ally_trap(self, owner: Player, x: int, y: int) -> bool:
        st = self.square_type(x, y)
        return (owner == Player.P1 and st == SquareType.TRAP_P1) or (owner == Player.P2 and st == SquareType.TRAP_P2)

    def ally_den(self, owner: Player) -> Tuple[int, int]:
        return DEN_POS[owner]

    def enemy_den(self, owner: Player) -> Tuple[int, int]:
        return DEN_POS[owner.opponent()]
