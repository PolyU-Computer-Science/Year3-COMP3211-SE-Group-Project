# User Manual

This is a command-line Jungle (Dou Shou Qi) game for two players.

## Start
```powershell
python -m cli.main
```

## Commands
- `new` — start a new game
- `name <p1> <p2>` — set player names; or `name random` to auto-generate
- `show` — print board and status
- `move <from> <to>` — make a move, e.g. `move b3 b4`
- `undo` — undo the last move (each player can undo at most 3 times per game)
- `save <file.jungle>` — save current game state
- `load <file.jungle>` — load a saved game
- `record start <file.record>` — start recording all moves
- `record stop` — stop and write the record file
- `replay <file.record>` — replay a recorded game to the final state
- `help` — show help
- `quit|exit` — exit the program

## Coordinates
- Columns: a..g; Rows: 1..9. Example: `a1`, `g9`.

## Board legend in output
- Pieces: uppercase = P1, lowercase = P2
  - r/c/d/w/l/t/L/e = rat/cat/dog/wolf/leopard/tiger/lion/elephant
- Terrain:
  - `~` river
  - `D` P1 den, `d` P2 den
  - `^` P1 trap, `v` P2 trap
  - `.` land

## Invalid input
- The game prints a specific error message, examples:
  - "起始位置没有棋子"
  - "不是你的回合"
  - "不能进入该格子（河流/己方兽穴）"
  - "只能正交移动一格" / "狮/虎跳河受阻或目标不合法"
  - "无法吃掉该棋子（规则限制/等级不足）"

## Recording and replay
- `.record` is a human-readable text listing player names and moves.
- `replay` command reconstructs the final state by applying the sequence from an initial setup.

## Winning
- Enter the opponent's den OR capture all opponent pieces.
