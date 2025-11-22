# Jungle CLI – COMP3211 Group Project

Command-line implementation of the Jungle (Dou Shou Qi) board game adhering to the assignment brief for COMP3211 (Fall 2025).  The runtime uses only Python's standard library; development tooling (tests, coverage) relies on `unittest` and `coverage`.

## Project Layout

```
├── src/
│   ├── __init__.py
│   ├── main.py                 # entry point (python -m src.main)
│   ├── cli/                    # shell, renderers, CLI utilities
│   │   ├── __init__.py
│   │   ├── shell.py            # JungleShell REPL + commands
│   │   ├── renderers.py        # ASCII board + status rendering
│   │   └── utils.py            # parsing helpers, random names, file checks
│   └── model/                  # pure game logic & serialization helpers
│       ├── __init__.py
│       ├── enums.py            # PlayerSide, PieceType, SquareType definitions
│       ├── position.py         # board coordinates + a1-style notation
│       ├── piece.py            # Piece dataclass + printing helpers
│       ├── board.py            # rules for movement, capture, traps, rivers
│       ├── game_state.py       # GameState, undo stack, victory detection
│       ├── move.py             # Move record structure
│       └── serialization.py    # .jungle save & .record export/import
├── tests/                      # unittest-based model tests + coverage report
│   ├── test_model.py           # unit tests for model layer
│   └── COVERAGE.md             # latest model coverage snapshot
├── pyproject.toml              # project metadata + coverage config
├── .gitignore
└── README.md
```

## Requirements

- Python **3.11+** (tested on 3.12 via Conda)
- Optional: `coverage` package for coverage measurement (`python -m pip install coverage`)

## Quick Start

```bash
# Run the interactive CLI
python -m src.main

# Execute the unit tests
python -m unittest discover -s tests

# Reproduce coverage numbers
python -m coverage run -m unittest discover -s tests
python -m coverage report --include "src/model/*"
```

While playing, use `help` inside the REPL to see every available command.

## Key Features

- Full Jungle rule set (movement, rivers, traps, lion/tiger jumps, rat exceptions, den capture, elimination win condition)
- MVC-style separation with an isolated `model` package for easier testing
- Undo system enforcing **three** take-backs per player each game
- Game state persistence to `.jungle` files and record/replay support for `.record` files
- Printable board, piece lists, and recent move history directly in the CLI
- Developer/user manuals plus SRS, design document, and requirement traceability artifacts under `docs/`

## Contributing / Collaboration Notes

1. Stick to the `src` layout and keep game logic within `src/model`.
2. Before committing, run tests (`python -m unittest discover -s tests`).
3. Update `docs/RequirementsCoverage.md` whenever new requirements are implemented.
4. When editing documentation intended for DOC/PDF submission, convert Markdown into the requested format before uploading to Blackboard.

## Licence / Academic Integrity

This codebase is for the COMP3211 group project.  Follow PolyU's Honour Declaration guidelines.
