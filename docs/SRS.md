# Software Requirements Specification (SRS) — Jungle CLI Game

Version: 1.0 — 2025-11-05

## 1. Introduction
- Purpose: Provide a CLI Jungle game implementation for COMP3211 course project with separated model and unit tests.
- Scope: Two-player local CLI, no GUI/online features. Obeys Appendix B rules. Supports user stories US1–US10 from Appendix C.

## 2. Overall Description
- Product perspective: Standalone Python program; standard library only.
- Users: Two human players sharing one console.
- Constraints: No third-party libs in implementation; Windows primary platform.
- Assumptions: Players enter valid commands as documented; filenames are accessible.

## 3. System Features (Functional Requirements)
F1. Start new game (US1)
- FR-1.1: System initializes board to standard layout and sets current player to P1.

F2. End game (US2)
- FR-2.1: User can exit at any time with `quit|exit`.

F3. Player naming (US3)
- FR-3.1: Users can set names via `name <p1> <p2>` or `name random`.

F4. CLI gameplay (US4)
- FR-4.1: REPL accepts commands listed in User Manual.
- FR-4.2: Moves are validated against Jungle rules.

F5. Show game status (US5)
- FR-5.1: `show` prints all pieces and their positions, current player, and winner if any.

F6. Undo (US6)
- FR-6.1: Each player may undo at most 3 times per game.
- FR-6.2: Undo reverts last move (including restoring captured piece) and current player.

F7. Record game (US7)
- FR-7.1: `record start <file.record>` starts recording with player names.
- FR-7.2: Each move is appended; `record stop` writes the file.

F8. Replay record (US8)
- FR-8.1: `replay <file.record>` replays moves from initial state and shows final board.

F9. Save current game (US9)
- FR-9.1: `save <file.jungle>` writes current state as JSON (pieces, player turn, names, undo counters).

F10. Load game (US10)
- FR-10.1: `load <file.jungle>` restores from JSON and continues play.

## 4. Game Rules (Model Requirements)
- R1 Movement: Orthogonal one step; lion/tiger may jump straight over rivers to next land unless a rat is on any intervening river square.
- R2 Rivers: Only rats may enter river squares.
- R3 Dens: A piece may not enter its own den.
- R4 Captures: Higher rank captures lower/equal rank; rat may capture elephant; elephant may not capture rat.
- R5 Water/land rat captures: A rat in water may not capture a piece on land (incl. elephant) or vice versa; rats may fight only if both on land or both in water.
- R6 Traps: A piece may capture any enemy in one of the player's own trap squares regardless of rank.
- R7 Win: Enter opponent's den OR capture all opponent pieces.

## 5. Non-functional Requirements
- NFR-1: Reliability — All rules enforced; unit tests pass.
- NFR-2: Usability — Helpful error messages and `help` command.
- NFR-3: Portability — Python 3.11+ on Windows, no 3rd-party deps.
- NFR-4: Testability — Model isolated under `model/`, unit tests in `tests/`.
- NFR-5: Performance — Commands respond within 100 ms on typical hardware.

## 6. External Interface Requirements
- CLI text input/output via standard stdin/stdout.
- Filesystem read/write for `.jungle` (JSON) and `.record` (text).

## 7. Acceptance Criteria
- All US1–US10 demonstrably supported.
- Unit tests pass with line coverage report for `model/`.
- Developer and user manuals completed.

## 8. Appendices
- A: See `docs/Design.md` for architecture and diagrams.
- B: See `docs/Requirements-Coverage.md` for coverage mapping.
