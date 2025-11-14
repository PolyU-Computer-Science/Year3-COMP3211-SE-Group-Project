# Software Requirements Specification (SRS)

## 1. Introduction
- **Purpose**: Define the functional and non-functional requirements for the COMP3211 Jungle (Dou Shou Qi) command-line game.
- **Scope**: Two-player, turn-based CLI game with save/load, record/replay, and undo functionality. Implementation is limited to the command line per the assignment brief.
- **Definitions/Abbreviations**:
  - **CLI** – Command-Line Interface
  - **Undo Credit** – Consumable allowance permitting a player to revert the most recent move (max three per player per game)
  - **Record File** – `.record` JSON file containing player metadata and chronological move list
  - **Save File** – `.jungle` JSON file containing the complete game snapshot

## 2. Overall Description
- **Product Perspective**: Standalone Python application following a lightweight MVC structure – `model` for game logic, `cli` for presentation.
- **User Classes**:
  - Primary players (two human users sharing the terminal)
  - Teaching staff (for grading, replay, and verification)
- **Operating Environment**: Windows/macOS/Linux terminal with Python 3.11+.
- **Design Constraints**: Standard library only at runtime; model code must reside in `model` package; no GUI or network play.
- **Assumptions**: Players alternate moves without time controls; file system is accessible for saves/records; users are familiar with Dou Shou Qi basics.

## 3. Functional Requirements
| ID | Description | Acceptance Criteria | Source |
|----|-------------|---------------------|--------|
| FR-1 | Start a new Jungle game with optional player names. | `new [blue] [red]` initializes board, resets undo credits. | US1, US3 |
| FR-2 | End the current session gracefully. | `quit` command terminates without corrupting data. | US2 |
| FR-3 | Provide a text-based interface for all interactions. | CLI prompt accepts commands per User Manual. | US4 |
| FR-4 | Display the full board state, next player, remaining pieces, and undo credits. | `status` command prints board + metadata. | US5 |
| FR-5 | Enforce Jungle movement and capture rules (rivers, traps, lions/tigers jumping, rat exceptions, dens, victory). | Illegal inputs rejected with clear messages; legal moves update board. | Appendix B |
| FR-6 | Track and limit undo actions to three per player per game. | `undo [side]` reverts latest move until credits exhausted; after 3 uses, command is disabled for that side. | US6 |
| FR-7 | Persist the full game snapshot to `.jungle` and reload it later. | `save-game`/`load-game` round-trip reproduces board, turn, undo counts, move log. | US9, US10 |
| FR-8 | Record matches (players + ordered move list) to `.record`. | `export-record` writes JSON describing the match. | US7 |
| FR-9 | Replay a `.record` file. | `replay-record` re-applies moves on a fresh board and prints intermediate boards. | US8 |
| FR-10 | Maintain user-friendly error handling. | Invalid commands/moves emit messages without crashing. | SRS |

## 4. External Interface Requirements
- **User Interface**: Text REPL with prompts, ASCII board rendering, and textual feedback. No GUI.
- **File Interfaces**: JSON-based `.jungle` and `.record` files (UTF-8). File extensions validated.
- **Hardware Interfaces**: Standard keyboard for input; display capable of showing ASCII board.

## 5. Non-Functional Requirements
| ID | Category | Description |
|----|----------|-------------|
| NFR-1 | Usability | Command syntax documented in the User Manual; `help` lists available commands. |
| NFR-2 | Reliability | Game logic covered by automated unit tests with ≥80% line coverage inside `src/model`. |
| NFR-3 | Performance | Command processing completes within 100 ms on a typical laptop (negligible CPU requirements). |
| NFR-4 | Maintainability | Strict separation between `model` (logic) and `cli` (presentation). All rules reside in `model`. |
| NFR-5 | Portability | Runs on any OS with Python 3.11+ without modification. |
| NFR-6 | Integrity | Honour declaration records all GenAI usage; save/record files validate extensions to reduce accidental misuse. |

## 6. System Constraints & Policies
- Undo credits are non-transferable and reset only when a new game starts.
- Files must use the prescribed extensions (`.jungle`, `.record`); other extensions trigger validation errors.
- The game rejects attempts to move before starting (`new`) or after a winner is declared.

## 7. Verification Plan (High-Level)
- Unit tests under `tests/` cover move validation, undo budgeting, persistence round-trips, and victory checks.
- Manual verification follows the User Manual scenarios (happy path, invalid input, save/load, replay).

## 8. Traceability
See `docs/RequirementsCoverage.md` for the mapping between FR/NFR IDs, user stories, and implementation/testing artifacts.
