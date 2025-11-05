from __future__ import annotations
from typing import Optional, Tuple
from .types import Player, Animal, Piece
from .board import Board, BOARD_WIDTH, BOARD_HEIGHT, RIVER_COLUMNS, RIVER_ROWS


ORTHO_DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def _is_river(x: int, y: int) -> bool:
    return x in RIVER_COLUMNS and y in RIVER_ROWS


def _is_land(x: int, y: int) -> bool:
    return not _is_river(x, y)


def _lion_tiger_jump_target(board: Board, x: int, y: int, dx: int, dy: int) -> Optional[Tuple[int, int]]:
    # Must jump strictly across river in straight line to next non-water square
    cx, cy = x + dx, y + dy
    if not board.in_bounds(cx, cy):
        return None
    if _is_river(cx, cy):
        # Check for rats blocking in river along path
        while board.in_bounds(cx, cy) and _is_river(cx, cy):
            pc = board.piece_at(cx, cy)
            if pc and pc.animal == Animal.RAT:
                return None  # blocked by any rat
            cx += dx
            cy += dy
        # Now at first non-river square (if in bounds)
        if board.in_bounds(cx, cy) and _is_land(cx, cy):
            return (cx, cy)
    return None


def _can_enter_square(piece: Piece, to_x: int, to_y: int, board: Board) -> bool:
    st = board.square_type(to_x, to_y)
    if piece.owner == Player.P1 and st == board.square_type(*board.ally_den(Player.P1)):
        # Can't enter own den (P1)
        return False
    if piece.owner == Player.P2 and st == board.square_type(*board.ally_den(Player.P2)):
        # Can't enter own den (P2)
        return False
    # Only rat can enter river
    if _is_river(to_x, to_y):
        return piece.animal == Animal.RAT
    return True


def can_capture(attacker: Piece, defender: Piece, board: Board, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
    fx, fy = from_pos
    tx, ty = to_pos
    # Cannot capture own piece
    if attacker.owner == defender.owner:
        return False
    # Rat/land/water constraints
    attacker_in_water = _is_river(fx, fy)
    defender_in_water = _is_river(tx, ty)
    if attacker.animal == Animal.RAT and defender.animal == Animal.ELEPHANT and attacker_in_water:
        return False  # Rat cannot capture elephant from water
    if attacker.animal == Animal.RAT and defender.animal == Animal.RAT:
        # Rat vs rat only if both are in same medium (both land or both water)
        if attacker_in_water != defender_in_water:
            return False
    if attacker.animal != Animal.RAT:
        # Non-rats cannot capture rats in water (since they cannot enter water square anyway)
        if defender_in_water:
            return False
    # Trap rule: a piece may capture any enemy in its own traps regardless of rank
    # If defender is standing in attacker's side traps
    if board.is_ally_trap(attacker.owner, tx, ty):
        return True
    # Elephant cannot capture rat at all
    if attacker.animal == Animal.ELEPHANT and defender.animal == Animal.RAT:
        return False
    # Normal rank rule + special rat>elephant
    if attacker.animal == Animal.RAT and defender.animal == Animal.ELEPHANT:
        return True
    # Otherwise compare ranks, but if attacker is in enemy trap, its rank is reduced to 0 (i.e., can be captured by any),
    # but when attacking from inside a trap, its rank remains its own for capture eligibility (common rule interpretations vary).
    # We'll implement standard: trap reduces piece power only for being captured; attacking still uses base rank.
    return attacker.rank >= defender.rank


def is_legal_move(board: Board, piece: Piece, to_x: int, to_y: int) -> Tuple[bool, str]:
    from_x, from_y = piece.x, piece.y
    if not board.in_bounds(to_x, to_y):
        return False, "目标位置越界"
    if not _can_enter_square(piece, to_x, to_y, board):
        return False, "不能进入该格子（河流/己方兽穴）"

    dx = to_x - from_x
    dy = to_y - from_y
    md = abs(dx) + abs(dy)

    if piece.animal in (Animal.LION, Animal.TIGER):
        # Allow jump across river in straight line
        if (dx, dy) in ORTHO_DIRS and md == 1:
            pass  # normal step
        elif dx == 0 or dy == 0:
            sdx = 0 if dx == 0 else (1 if dx > 0 else -1)
            sdy = 0 if dy == 0 else (1 if dy > 0 else -1)
            tgt = _lion_tiger_jump_target(board, from_x, from_y, sdx, sdy)
            if tgt is None or tgt != (to_x, to_y):
                return False, "狮/虎跳河受阻或目标不合法"
        else:
            return False, "只能正交移动"
    else:
        if md != 1 or (dx, dy) not in ORTHO_DIRS:
            return False, "只能正交移动一格"

    # Occupancy & capture
    defender = board.piece_at(to_x, to_y)
    if defender is None:
        return True, ""
    else:
        if defender.owner == piece.owner:
            return False, "不能进入己方棋子所在格"
        if can_capture(piece, defender, board, (from_x, from_y), (to_x, to_y)):
            return True, ""
        return False, "无法吃掉该棋子（规则限制/等级不足）"
