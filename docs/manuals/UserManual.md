# Jungle CLI – User Manual

## 1. Introduction
This manual explains how to play the Jungle (Dou Shou Qi) command-line game delivered for COMP3211.  The interface is an interactive shell that guides both players through the full ruleset, including undo, save/load, and replay features.

## 2. Starting the Program
```bash
python -m src.main
```
You will see the prompt:
```
jungle>
```
Type `help` at any time to redisplay the command list.

## 3. Coordinate System
- Columns use the letters **a–g** (left to right).
- Rows use numbers **1–9** (top to bottom).
- Example: `a1` is the top-left square; `g9` is the bottom-right square.

## 4. Core Commands
| Command | Description |
|---------|-------------|
| `new [blue] [red]` | Starts a new game. Provide optional player names; otherwise random pronounceable names are generated. |
| `players <blue|red> <name>` | Renames a player at any time. |
| `show` | Prints only the current board. |
| `status` | Prints the board, remaining pieces for each side, undo credits, and (if applicable) the winner. |
| `move <from> <to>` | Moves one of your pieces. Coordinates must be valid and moves must follow Jungle rules. |
| `history [n]` | Shows the last `n` moves (default 5). |
| `undo [blue|red]` | Takes back the most recent move. Each side has **3** undo credits per game. Specify the side if you are undoing the other player's move; otherwise the current side to move is assumed. |
| `save-game <file.jungle>` | Saves the current game state (JSON) for later resumption. |
| `load-game <file.jungle>` | Loads a previously saved `.jungle` file. |
| `export-record <file.record>` | Exports the finished (or in-progress) move list for archival/replay. |
| `replay-record <file.record>` | Replays a recorded match, printing the board after each move. |
| `quit` | Exits the program safely.

## 5. Gameplay Notes
- Only the **rat** may enter river squares.
- Rats cannot capture elephants or other rats directly from water to land, nor can land rats attack water rats.
- Lions and tigers can jump across rivers horizontally or vertically, but the path must be clear of rats and must land on the first land square.
- A piece in the opponent's trap has **zero rank** and can be captured by any enemy piece.
- You **cannot** enter your own den; entering the enemy den immediately wins the game.
- Eliminating all opposing pieces is an alternative win condition.

## 6. Saving, Loading, Recording
- `.jungle` save files are complete snapshots (players, board, undo counts). Use `save-game` and `load-game` to continue a match later.
- `.record` files contain only metadata and the chronological list of moves. Use `export-record` to archive a finished match and `replay-record` to visualize it move by move.

## 7. Error Handling
- Invalid commands or malformed coordinates produce descriptive error messages but **do not** terminate the session.
- Illegal moves (rule violations) leave the board unchanged and explain what went wrong (e.g., "Only rats may enter the river.").
- File errors (`load-game`, `replay-record`) report missing files or JSON format issues.

## 8. Example Session
```
jungle> new Alice Bob
jungle> status          # inspect the starting layout
jungle> move a3 a4      # Alice (Blue) moves the rat forward
jungle> move g7 g6      # Bob replies
jungle> undo blue       # Alice retracts her previous move (1 credit consumed)
jungle> save-game demo.jungle
jungle> export-record demo.record
jungle> quit
```

## 9. Additional Tips
- Use `history` to double-check previous actions before undoing.
- The board renderer displays rivers as `~~`, dens as `DB/DR`, and traps as `tb/tr`.
- Keep `.jungle` and `.record` files in a dedicated folder (e.g., `saves/`) to simplify submission packaging.

Enjoy your command-line Jungle matches!
