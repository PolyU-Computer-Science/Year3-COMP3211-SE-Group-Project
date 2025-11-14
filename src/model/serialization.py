from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from .game_state import GameState
from .move import Move
from .enums import PlayerSide


@dataclass
class GameRecord:
    players: dict[PlayerSide, str]
    moves: List[Move]
    winner: Optional[str]
    created_at: str


class SerializationError(RuntimeError):
    pass


def save_game(state: GameState, destination: Path) -> None:
    payload = state.to_dict()
    payload["saved_at"] = datetime.now(timezone.utc).isoformat()
    destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_game(source: Path) -> GameState:
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SerializationError(f"File not found: {source}") from exc
    except json.JSONDecodeError as exc:  # pragma: no cover - handled uniformly
        raise SerializationError("Save file is not valid JSON.") from exc
    return GameState.from_dict(data)


def export_record(state: GameState, destination: Path) -> None:
    payload = {
        "players": {side.value: name for side, name in state.player_names.items()},
        "winner": state.winner.value if state.winner else None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "moves": [move.__dict__ for move in state.move_log],
    }
    destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_record(source: Path) -> GameRecord:
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SerializationError(f"File not found: {source}") from exc
    except json.JSONDecodeError as exc:
        raise SerializationError("Record file contains invalid JSON.") from exc

    moves = [Move(**entry) for entry in data.get("moves", [])]
    players = {PlayerSide(side): name for side,
               name in data.get("players", {}).items()}
    return GameRecord(players=players, moves=moves, winner=data.get("winner"), created_at=data.get("created_at", ""))
