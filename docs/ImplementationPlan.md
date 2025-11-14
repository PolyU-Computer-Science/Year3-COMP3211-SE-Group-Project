# Jungle Game Implementation Plan

## Technology & Project Structure
- **Language**: Python 3.11 (standard library only for the runtime).  Unit tests use the stock `unittest` module; coverage measurements rely on the optional `coverage` tool.
- **Project layout** (``src`` layout for clean imports and testing):
  - `src/model`: Pure game logic (board, pieces, rules engine, serialization helpers, record keeping).  This satisfies the requirement that all model code reside in a dedicated `model` package.
  - `src/cli`: Command-line interface components (command parsing, interactive shell, board rendering, replay visualizer).
  - `src/main.py`: Entry point that wires CLI to the model.
  - `tests`: Automated unit tests that exercise the model layer only.
  - `docs`: Manuals, SRS/design notes, coverage reports, and requirement-tracking tables.

## Core Functional Goals (mapping to user stories)
| User Story | Implementation Detail |
|------------|-----------------------|
| US1 / US2  | `new` and `quit` commands handled by the CLI controller. |
| US3        | `new --p1 <name> --p2 <name>` arguments or on-demand `players` command to rename; default randomized pronounceable names when omitted. |
| US4        | Interactive REPL loop with contextual help and inline validation errors.
| US5        | `show` command renders the board, captured pieces, remaining undo credits, and next player.
| US6        | Model keeps an immutable snapshot stack (max three per player) to support `undo` while enforcing the "<= 3 moves" constraint.
| US7 / US8  | `export-record` writes a `.record` JSON file capturing players + ordered move list; `replay-record` loads the file and animates the game on the console.
| US9 / US10 | `save-game` / `load-game` serialize/restore the complete game state (board, captured pieces, active player, undo credits) to/from `.jungle` JSON files.

## Architectural Overview (textual)
- **Pattern**: MVC variant tailored for CLI.
  - `model.board.Board` owns square topology, special tiles (dens/traps/rivers), and validates primitive moves.
  - `model.game_state.GameState` maintains players, turn order, history stack, and high-level commands such as `apply_move`, `undo`, `is_finished`.
  - `model.move.Move` and `model.record.MoveRecordEntry` are lightweight dataclasses shared between layers.
  - `cli.shell.JungleShell` acts as controller + view: it parses tokens, invokes `GameService`, and renders textual output via `cli.renderers`.
  - `cli.persistence` orchestrates JSON serialization by delegating to `model.serialization` (keeps persistence logic testable in isolation).

## Key Rules Engine Considerations
- Board coordinates use zero-based `(row, column)` internally, while the CLI exposes human-friendly ``<file><rank>`` notation (`a1` = top-left).  Helper utilities convert between the two.
- Movement validation includes:
  - Basic orthogonal movement (no diagonals, no entering own den).
  - Rat-specific swimming rules and capture prohibitions between land/water contexts.
  - Lion/Tiger river jumps that fail if a rat occupies an intervening water square.
  - Traps reducing defender rank to zero for capture comparisons.
  - Elephant vs. Rat special-case logic.
- Victory detection triggers when a player reaches the opponent den or eliminates all enemy pieces; both conditions flag `GameState.winner`.

## Persistence Formats
- **`.jungle` files**: JSON containing board layout, players, turn, undo counters, and move history for resuming a match.
- **`.record` files**: JSON containing immutable record (players, timestamp, winner, ordered move list with capture metadata).  These files are append-only and power the replay command; they do not influence undo/save functionality.

## Testing Strategy
- Unit tests target the `model` package only.  Focus areas: legal/illegal moves (rat in water, lion/tiger jumps, trap behavior), win detection, undo limit enforcement, serialization round-trips.
- Coverage measurement: `python -m coverage run -m unittest` + `python -m coverage html` with reports stored under `docs/coverage/` (generated, therefore ignored by git).

## Documentation Deliverables
- `docs/manuals/DeveloperManual.md` – build/run/IDE instructions per assignment brief.
- `docs/manuals/UserManual.md` – CLI commands, examples, error conditions.
- `docs/RequirementsCoverage.md` – table that cross-references SRS requirements & user stories with the implemented artifacts.
- `docs/ImplementationPlan.md` (this file) – living architecture roadmap.

This plan provides the baseline for the upcoming implementation tasks.  Adjustments will be recorded in commit messages and the requirements coverage table as the project evolves.
