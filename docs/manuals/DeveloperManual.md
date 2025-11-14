# Developer Manual

## Target Platform
- **OS**: Windows 11 (primary), tested with Conda Python 3.12.  The project is OS-agnostic as long as Python 3.11+ is available.
- **IDE**: Visual Studio Code with the Python extension (recommended) or any editor that understands the `src` layout.
- **Runtime dependencies**: Python standard library only.
- **Dev/Test tools**: `coverage` (install via `python -m pip install coverage`).

## Project Setup
1. Clone/download the repository to your workspace.
2. Create/activate a Python 3.11+ environment (`conda create -n jungle python=3.11`, `python -m venv .venv`, etc.).
3. Install optional dev tools:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install coverage
   ```
4. Verify the tests: `python -m unittest discover -s tests`.

## Running / Debugging the Game
```bash
python -m src.main
```
- The program launches an interactive REPL (`jungle>` prompt).
- Use `help` inside the shell for the full command list (new, move, undo, save-game, load-game, export-record, replay-record, etc.).
- To debug, set breakpoints in VS Code and configure a `launch.json` entry that runs the module `src.main`.

## Code Structure
- `src/model`: pure game logic (board, pieces, rules, serialization). Keep all stateful logic here to preserve testability.
- `src/cli`: user interaction (REPL, command parser, board renderer). Avoid placing rules here.
- `tests`: `unittest` suites that exercise the model only. Add new cases when extending the rules.
- `docs`: architecture and process artifacts required by the assignment (SRS, design doc, manuals, requirement coverage, honour declaration template).

## Common Tasks
| Task | Command |
|------|---------|
| Run unit tests | `python -m unittest discover -s tests` |
| Run coverage (model focus) | `python -m coverage run -m unittest discover -s tests` then `python -m coverage report --include "src/model/*"` |
| Lint / format (optional) | Use `ruff`, `black`, or `flake8` if desired (not bundled). |
| Create distributable ZIP | `git archive -o jungle-project.zip HEAD` or use your OS zipper once docs/videos are ready. |

## Saving & Loading
- Saves (`save-game <name>.jungle`) contain the entire `GameState` JSON payload.
- Records (`export-record <name>.record`) list players + chronological moves and power the `replay-record` command.
- All persistence is JSON-based to keep the debugging story simple.

## Troubleshooting
- **Unknown module `model`**: Always run as `python -m src.main` (module-aware) or configure `PYTHONPATH` to include the repository root.
- **Undo not allowed**: Each player has exactly three undo credits; the CLI accepts `undo blue` / `undo red` to specify the requesting side explicitly.
- **Coverage includes CLI**: Limit the report scope via `--include "src/model/*"` as shown above.

## Contribution Workflow
1. Create a feature branch.
2. Update/extend model tests for new behavior.
3. Implement the feature under `src/model` (logic) or `src/cli` (presentation) as appropriate.
4. Run tests + coverage; update `tests/COVERAGE.md` if the numbers materially change.
5. Update `docs/RequirementsCoverage.md` to reflect new/updated requirements.
6. Raise a PR for peer review (attach test logs + coverage snippet).

Happy hacking and remember to log GenAI usage in the Honour Declaration before submission.
