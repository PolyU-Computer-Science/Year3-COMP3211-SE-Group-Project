# Model Package Test Coverage

The following metrics were produced on **2025-11-14** with:

```bash
python -m coverage run -m unittest discover -s tests
python -m coverage report --include "src/model/*"
```

| Module | Statements | Missed | Branches | Partial Branches | Coverage |
|--------|------------|--------|----------|------------------|----------|
| `model.board` | 140 | 19 | 70 | 19 | 82% |
| `model.enums` | 41 | 1 | 0 | 0 | 98% |
| `model.game_state` | 93 | 9 | 24 | 6 | 85% |
| `model.move` | 16 | 0 | 0 | 0 | 100% |
| `model.piece` | 21 | 5 | 2 | 0 | 70% |
| `model.position` | 29 | 11 | 4 | 0 | 55% |
| `model.serialization` | 40 | 13 | 0 | 0 | 68% |
| **Total (model package)** | 380 | 58 | 100 | 25 | **81%** |

> Tip: Generate an HTML report with `python -m coverage html` to inspect the remaining gaps (output lands in `htmlcov/`).
