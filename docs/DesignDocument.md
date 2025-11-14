# Design Document

## 1. Architectural Overview
- **Pattern**: Model–View–Controller (MVC) tailored for a CLI.
  - **Model** (`src/model`): Encapsulates the complete Jungle rule set, board topology, serialization helpers, undo stack, and move history.
  - **Controller/View** (`src/cli`): A command parser (`JungleShell`) that interprets user input, calls the model, and renders textual output (`renderers`).
- **Rationale**: Clean separation keeps the model deterministic and unit-testable, while the CLI can evolve independently (e.g., substituting a GUI in the future).
- **Component Instantiation**:
  - `GameState` is the façade for the rules engine. It maintains the `Board`, players, undo credits, and move log.
  - `Board` enforces low-level movement restrictions (rivers, traps, special pieces) and owns the mutable piece map.
  - `serialization` module converts `GameState` instances to/from JSON for both saves and match records.
  - `JungleShell` orchestrates commands, relying on helper modules (`renderers`, `utils`) for parsing and presentation.

## 2. Component Responsibilities
| Component | Responsibilities | Key Interfaces |
|-----------|------------------|----------------|
| `model.enums` | Declares `PlayerSide`, `SquareType`, and `PieceType` metadata (rank, abilities). | Referenced across the entire model layer. |
| `model.position` | Coordinate helpers, notation parsing (`a1` ↔ `(row, col)`). | `Board`, `GameState`, CLI. |
| `model.piece` | Immutable `Piece` objects + textual notation helpers. | Stored in `Board`'s occupancy map. |
| `model.board` | Validates and executes moves, handles captures, traps, rivers, lion/tiger jumps. | Called by `GameState.move`. |
| `model.game_state` | High-level state machine: turn alternation, undo stack, win detection, serialization. | Invoked directly by the CLI. |
| `model.serialization` | JSON persistence for `.jungle` (full state) and `.record` (move log). | `save-game`, `load-game`, `export-record`, `replay-record`. |
| `cli.utils` | Random player names, coordinate parsing, file extension validation. | Used by `JungleShell`. |
| `cli.renderers` | ASCII board/status rendering. | `show`, `status`, `replay-record`. |
| `cli.shell` | Command REPL, routing, user feedback, replay animation. | Entry point `main.py`. |

## 3. Data Structures
- **Board representation**: `Dict[(row, col), Piece]` for O(1) lookup/removal.  Special tiles (rivers, traps, dens) precomputed as coordinate sets.
- **Move history**: `List[Move]` within `GameState` keeps chronological data for export + `history` command.
- **Undo stack**: `List[HistorySnapshot]` storing deep copies of the board plus metadata (`current_player`, `winner`, `move_log_size`).  Copies are taken only after successful moves to avoid polluting the stack.
- **Persistence payload**: JSON object with `players`, `current_player`, `winner`, `undo_remaining`, `pieces[]`, `moves[]`, `saved_at` (for saves) or `created_at` (for records).

## 4. Turn Flow (Sequence)
```
Player -> CLI (`move a3 a4`)
CLI -> GameState.move(src, dst)
GameState -> Board.move(current_player, src, dst)
Board -> (rule checks: ownership, adjacency/jump, rivers, traps, capture legality)
Board -> GameState (returns moved_piece, captured_piece)
GameState -> (append snapshot, record move, check victory, swap current_player)
GameState -> CLI (Move dataclass)
CLI -> Renderer (print summary + board/status)
```
Errors (invalid moves/files) propagate as exceptions that the CLI catches and converts into user-friendly text.

## 5. Example Use Case – Player Turn
1. CLI reads `move c3 c4`.
2. Positions parsed to `(row, col)` objects.
3. `GameState.move` verifies the game isn’t finished, clones the snapshot, and delegates to `Board.move`.
4. `Board` enforces Jungle rules:
   - Ensures the piece belongs to the active player.
   - Validates river/trap/den constraints and special jumps.
   - Optionally computes capture legality (rank comparison, rat/elephant exceptions).
5. On success, `GameState` logs the move (for history + record), checks victory (den entry or elimination), toggles the current player, and returns a `Move` summary to the CLI.
6. CLI prints an acknowledgement, updates the board display, and prompts the next player.

## 6. Diagram Placeholders
- **Architecture Diagram**: MVC layers (`CLI` ↔ `GameState` ↔ `Board`/`Serialization`).
- **Component Diagram**: Entities described in sections 2–3.
- **Sequence Diagram**: Turn flow described above can be converted into a UML sequence diagram for submission by mirroring the textual steps.

## 7. Rationale & Trade-offs
- **Immutable pieces** reduce accidental state sharing when copying boards for undo.
- **Snapshot-based undo** is simpler than replaying inverse operations and aligns with the "≤3 undo" constraint (bounded stack).
- **JSON persistence** keeps saves human-readable and debuggable without additional libraries.
- **CLI-first design** avoids GUI overhead and matches the assignment’s prohibition on extra features.

This document should be paired with `docs/ImplementationPlan.md` and `docs/RequirementsCoverage.md` during submission.
