# Requirements Coverage Report

This table maps Appendix C user stories and SRS features to implementation artifacts.

| ID  | Description | Implementation | Status |
|-----|-------------|----------------|--------|
| US1 | Start new game | `cli/main.py:new`, `GameState.reset()` | Implemented |
| US2 | End ongoing game | `quit|exit` | Implemented |
| US3 | Name players | `cli/main.py:name` | Implemented |
| US4 | Play via CLI | REPL in `cli/main.py` | Implemented |
| US5 | Show game status | `show`, `GameState.status_lines()` | Implemented |
| US6 | Undo up to 3 moves | `GameState.undo()` with per-player counters | Implemented |
| US7 | Record to .record | `Recorder.start/record_move/stop` | Implemented |
| US8 | Replay from .record | `replay` command using `Recorder.parse_record` | Implemented |
| US9 | Save to .jungle | `save_game()` | Implemented |
| US10| Load from .jungle | `load_game()` | Implemented |

SRS Functional (F1..F10): implemented as above.

Non-functional:
- Model in isolated `model/` package — Yes
- No 3rd-party libraries in implementation — Yes
- Unit tests and coverage — Yes (`tests/`, `run_tests_with_coverage.py`)
