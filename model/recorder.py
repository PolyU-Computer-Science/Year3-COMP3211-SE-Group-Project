from __future__ import annotations
from typing import List, Tuple, Optional
from .types import Move


class Recorder:
    def __init__(self) -> None:
        self.enabled = False
        self.path: Optional[str] = None
        self.lines: List[str] = []

    def start(self, path: str, p1: str, p2: str) -> None:
        self.enabled = True
        self.path = path
        self.lines = [f"P1:{p1}", f"P2:{p2}"]

    def record_move(self, mv: Move) -> None:
        if not self.enabled:
            return
        fx, fy = mv.from_pos
        tx, ty = mv.to_pos
        cap = mv.captured.animal.name if mv.captured else "-"
        self.lines.append(
            f"{mv.player.value}:{fx},{fy}->{tx},{ty}:{mv.moved_animal.name}:{cap}")

    def stop(self) -> Optional[str]:
        if not self.enabled or not self.path:
            return None
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines))
        self.enabled = False
        return self.path

    @staticmethod
    def parse_record(path: str) -> Tuple[str, str, List[Tuple[int, int, int, int]]]:
        with open(path, "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f.readlines() if ln.strip()]
        p1 = lines[0].split(":", 1)[1]
        p2 = lines[1].split(":", 1)[1]
        moves: List[Tuple[int, int, int, int]] = []
        for ln in lines[2:]:
            # format: player:fx,fy->tx,ty:animal:cap
            try:
                _, rest = ln.split(":", 1)
                pos, _, _ = rest.split(":")
                ff, tt = pos.split("->")
                fx, fy = map(int, ff.split(","))
                tx, ty = map(int, tt.split(","))
                moves.append((fx, fy, tx, ty))
            except Exception:
                continue
        return p1, p2, moves
