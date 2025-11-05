from __future__ import annotations
import json
from typing import Dict, Any
from .types import Player, Animal, Piece
from .board import Board
from .game import GameState


def save_game(gs: GameState, path: str) -> None:
    data: Dict[str, Any] = {
        "current_player": gs.current_player.value,
        "pieces": [
            {
                "owner": p.owner.value,
                "animal": p.animal.value,
                "x": p.x,
                "y": p.y,
            }
            for p in gs.board.all_pieces()
        ],
        "undo_used": {str(k.value): v for k, v in gs.undo_used.items()},
        "players_name": {str(k.value): v for k, v in gs.players_name.items()},
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_game(path: str) -> GameState:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    gs = GameState()
    gs.current_player = Player(data["current_player"])
    gs.undo_used = {Player(int(k)): v for k, v in data["undo_used"].items()}
    gs.players_name = {Player(int(k)): v for k,
                       v in data["players_name"].items()}
    # Rebuild pieces
    gs.board.pieces.clear()
    for item in data["pieces"]:
        owner = Player(item["owner"])
        animal = Animal(item["animal"])
        p = Piece(animal, owner, item["x"], item["y"])
        gs.board.place_piece(p, p.x, p.y)
    return gs
