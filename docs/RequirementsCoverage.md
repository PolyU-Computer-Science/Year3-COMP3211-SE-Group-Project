# Requirements Coverage Report

_Last updated: 2025-11-14_

## 1. User Story Coverage
| User Story | Implementation Reference | Test Reference | Status |
|------------|-------------------------|----------------|--------|
| US1 – Start a new game | `JungleShell._cmd_new`, `GameState.new` | `tests/test_model.py::GameStateTest` (state initialization) | ✅ Implemented |
| US2 – End ongoing game | `JungleShell._cmd_quit` | Manual (CLI prompt exit) | ✅ Implemented |
| US3 – Name players (manual or random) | `JungleShell._cmd_new`, `_cmd_players`, `cli.utils.random_name` | Manual (rename command) | ✅ Implemented |
| US4 – Play via CLI | `cli.shell.JungleShell` (REPL) | Manual | ✅ Implemented |
| US5 – View status | `JungleShell._cmd_status`, `cli.renderers.render_board/status` | Manual smoke tests | ✅ Implemented |
| US6 – Undo up to 3 moves | `GameState.undo`, `UNDO_LIMIT`, `JungleShell._cmd_undo` | `tests/test_model.py::test_undo_limit_enforced` | ✅ Implemented |
| US7 – Record to `.record` | `model.serialization.export_record`, `JungleShell._cmd_export_record` | Manual (file inspection) | ✅ Implemented |
| US8 – Replay `.record` | `JungleShell._cmd_replay_record`, `GameState` replay loop | Manual walkthrough | ✅ Implemented |
| US9 – Save `.jungle` | `model.serialization.save_game`, CLI `save-game` | `tests/test_model.py::test_save_and_load_roundtrip` | ✅ Implemented |
| US10 – Load `.jungle` | `model.serialization.load_game`, CLI `load-game` | `tests/test_model.py::test_save_and_load_roundtrip` | ✅ Implemented |

## 2. Functional Requirement Coverage
| FR ID | Brief | Implementation | Verification | Status |
|-------|-------|----------------|-------------|--------|
| FR-1 | Start new game | `GameState.new`, `JungleShell._cmd_new` | Manual | ✅ |
| FR-2 | Quit gracefully | `JungleShell._cmd_quit` | Manual | ✅ |
| FR-3 | CLI interaction | `cli.shell`, `cli.renderers`, `cli.utils` | Manual | ✅ |
| FR-4 | Board/status display | `render_board`, `render_status`, `status` command | Manual | ✅ |
| FR-5 | Jungle rules | `model.board`, `model.enums`, `model.position` | `tests/test_model.py::BoardRulesTest` suite | ✅ |
| FR-6 | Undo limit | `GameState.undo`, `UNDO_LIMIT`, `_cmd_undo` | `tests/test_model.py::test_undo_limit_enforced` | ✅ |
| FR-7 | Save/Load | `model.serialization.save_game/load_game`, CLI wrappers | `tests/test_model.py::test_save_and_load_roundtrip` | ✅ |
| FR-8 | Export record | `model.serialization.export_record` + CLI | Manual | ✅ |
| FR-9 | Replay record | `JungleShell._cmd_replay_record`, `GameState` playback | Manual | ✅ |
| FR-10 | Error handling | Exception catching in CLI dispatch | Manual (negative tests) | ✅ |

## 3. Non-Functional Requirement Coverage
| NFR ID | Description | Evidence |
|--------|-------------|----------|
| NFR-1 (Usability) | Commands documented in User Manual + in-shell `help`. | `docs/manuals/UserManual.md`, `JungleShell._cmd_help`. |
| NFR-2 (Reliability) | Automated tests + `tests/COVERAGE.md` (81% model coverage). | Test & coverage reports. |
| NFR-3 (Performance) | Pure-Python logic with O(1) board lookups; no heavy loops beyond 9×7 grid. | Code review. |
| NFR-4 (Maintainability) | Strict `model` vs `cli` separation, immutable pieces, documented plan. | `docs/DesignDocument.md`, `docs/ImplementationPlan.md`. |
| NFR-5 (Portability) | Python stdlib only; instructions for Windows/macOS/Linux. | `README.md`, Developer Manual. |
| NFR-6 (Integrity) | Honour declaration template, validation of file extensions in `cli.utils.ensure_extension`. | `docs/HonourDeclaration.md`, `cli/utils.py`. |

## 4. Outstanding Items / Future Work
- Optional: expand automated tests for serialization edge cases and CLI-level integration (currently covered manually).
- Prepare PDF/DOC exports of Markdown documents plus the gameplay video & slides for final submission.
