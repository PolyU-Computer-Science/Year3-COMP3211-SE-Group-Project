import sys
import random
from typing import Tuple
from model.game import GameState
from model.save_load import save_game, load_game
from model.recorder import Recorder
from model.board import BOARD_WIDTH, BOARD_HEIGHT
from model.types import Player


HELP = """
命令：
  new                          开始新局
  name <p1> <p2>              设置玩家名称；或使用：name random
  show                         显示棋盘与状态
  move <from> <to>            落子移动，如：move b3 b4 或 move a7 a6
  undo                         悔棋（每人最多3次）
  save <file.jungle>           保存当前对局
  load <file.jungle>           载入对局
  record start <file.record>   开始记录
  record stop                  停止记录并写入文件
  replay <file.record>         回放记录（从初始局面）
  help                         显示帮助
  quit/exit                    退出
坐标：列 a..g，行 1..9，例如 a1, g9。
"""


def parse_coord(s: str) -> Tuple[int, int]:
    s = s.strip().lower()
    if len(s) < 2:
        raise ValueError("坐标格式错误")
    col = ord(s[0]) - ord('a')
    row = int(s[1:]) - 1
    if not (0 <= col < BOARD_WIDTH and 0 <= row < BOARD_HEIGHT):
        raise ValueError("坐标越界")
    return (col, row)


def cmdloop() -> None:
    gs = GameState()
    rec = Recorder()

    print("Jungle (Dou Shou Qi) CLI —— 输入 help 查看命令。")
    print("使用 python -m cli.main 启动。")

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        parts = line.split()
        cmd = parts[0].lower()

        if cmd in ("quit", "exit"):
            break
        elif cmd == "help":
            print(HELP)
        elif cmd == "new":
            gs.reset()
            print("新局已开始。")
        elif cmd == "name":
            if len(parts) == 2 and parts[1].lower() == "random":
                p1 = "P1_" + \
                    ''.join(random.choice("ABCDEFGHJKLMNPQRSTUVWXYZ23456789")
                            for _ in range(4))
                p2 = "P2_" + \
                    ''.join(random.choice("ABCDEFGHJKLMNPQRSTUVWXYZ23456789")
                            for _ in range(4))
                gs.set_player_names(p1, p2)
            elif len(parts) >= 3:
                gs.set_player_names(parts[1], parts[2])
            else:
                print("用法：name <p1> <p2> 或 name random")
                continue
            print(
                f"玩家：P1={gs.players_name[Player.P1]}  P2={gs.players_name[Player.P2]}")
        elif cmd == "show":
            for ln in gs.status_lines():
                print(ln)
        elif cmd == "move":
            if len(parts) < 3:
                print("用法：move <from> <to>")
                continue
            try:
                f = parse_coord(parts[1])
                t = parse_coord(parts[2])
            except Exception as e:
                print(f"错误：{e}")
                continue
            ok, msg = gs.move(f, t)
            if not ok:
                print("非法：", msg)
            else:
                # show and record
                from model.types import Move as _MV  # local import for type name
                mv = gs.history[-1]
                rec.record_move(mv)
                for ln in gs.status_lines():
                    print(ln)
                if gs.winner() is not None:
                    print("游戏结束。")
        elif cmd == "undo":
            ok, msg = gs.undo()
            if not ok:
                print("失败：", msg)
            else:
                for ln in gs.status_lines():
                    print(ln)
        elif cmd == "save":
            if len(parts) < 2 or not parts[1].endswith(".jungle"):
                print("用法：save <file.jungle>")
                continue
            try:
                save_game(gs, parts[1])
                print(f"已保存 {parts[1]}")
            except Exception as e:
                print(f"保存失败：{e}")
        elif cmd == "load":
            if len(parts) < 2 or not parts[1].endswith(".jungle"):
                print("用法：load <file.jungle>")
                continue
            try:
                gs = load_game(parts[1])
                print(f"已载入 {parts[1]}")
                for ln in gs.status_lines():
                    print(ln)
            except Exception as e:
                print(f"载入失败：{e}")
        elif cmd == "record":
            if len(parts) >= 2 and parts[1] == "start":
                if len(parts) < 3 or not parts[2].endswith(".record"):
                    print("用法：record start <file.record>")
                    continue
                rec.start(parts[2], gs.players_name[Player.P1],
                          gs.players_name[Player.P2])
                print(f"已开始记录到 {parts[2]}")
            elif len(parts) >= 2 and parts[1] == "stop":
                out = rec.stop()
                print(f"已写入 {out}" if out else "未开始记录")
            else:
                print("用法：record start/stop ...")
        elif cmd == "replay":
            if len(parts) < 2 or not parts[1].endswith(".record"):
                print("用法：replay <file.record>")
                continue
            try:
                p1, p2, moves = Recorder.parse_record(parts[1])
                gs = GameState()
                gs.set_player_names(p1, p2)
                print(f"回放：P1={p1} P2={p2}")
                for (fx, fy, tx, ty) in moves:
                    ok, msg = gs.move((fx, fy), (tx, ty))
                    if not ok:
                        print(f"回放停止于非法步：{(fx, fy)}->{(tx, ty)}：{msg}")
                        break
                for ln in gs.status_lines():
                    print(ln)
            except Exception as e:
                print(f"回放失败：{e}")
        else:
            print("未知命令。输入 help 查看帮助。")


if __name__ == "__main__":
    cmdloop()
