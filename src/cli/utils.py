from __future__ import annotations

import random
import shlex
from pathlib import Path
from typing import List

from ..model.position import Position

_RANDOM_SYLLABLES = ["ka", "lo", "mi", "ta", "re",
                     "su", "na", "ri", "da", "po", "li", "fu"]


def random_name(seed: int | None = None) -> str:
    rng = random.Random(seed) if seed is not None else random
    return "".join(rng.choice(_RANDOM_SYLLABLES) for _ in range(3)).capitalize()


def parse_command(text: str) -> List[str]:
    return shlex.split(text)


def ensure_extension(path: str, extension: str) -> Path:
    if not path.lower().endswith(extension):
        raise ValueError(f"File must end with '{extension}'.")
    return Path(path)


def parse_position(token: str) -> Position:
    return Position.from_notation(token)
