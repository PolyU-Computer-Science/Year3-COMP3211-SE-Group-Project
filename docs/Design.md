# Design Document

## Architecture
- Pattern: Model-View-Controller (MVC)
  - Model: `model/*` — board, rules, game state, save/load, recorder
  - View/Controller: `cli/main.py` — REPL parses commands, prints status
- Rationale: MVC isolates pure game logic (testable) from UI.

## Main Components

### Model classes
- `types.py`
  - `Player` (enum): P1, P2
  - `Animal` (enum): RAT..ELEPHANT with ranks 1..8
  - `SquareType` (enum): LAND, RIVER, TRAP_P1, TRAP_P2, DEN_P1, DEN_P2
  - `Piece` (dataclass): animal, owner, x, y
  - `Move` (dataclass): player, from_pos, to_pos, moved_animal, captured
- `board.py`
  - Constants for size and terrain; initial piece placement
  - APIs: `piece_at`, `place_piece`, `remove_piece`, `square_type`, `owner_pieces`
- `rules.py`
  - `is_legal_move(board, piece, to_x, to_y) -> (bool, reason)`
  - `can_capture(attacker, defender, board, from_pos, to_pos) -> bool`
  - Implements movement, river, den, trap, lion/tiger jump, rat/elephant exceptions.
- `game.py`
  - `GameState`: board, player turn, history, undo limit, winner check
  - Methods: `legal_move`, `move`, `undo`, `status_lines`, `reset`
- `save_load.py`
  - Save/Load `.jungle` JSON files (pieces, turn, names, counters)
- `recorder.py`
  - Start/stop `.record` and record move list; parse for replay.

### CLI
- `cli/main.py`
  - REPL commands; coordinate parsing; prints status board.

## Diagrams

### Architecture (Mermaid)
```mermaid
flowchart LR
  UI[CLI REPL] -->|commands| GameState
  GameState --> Board
  GameState --> Rules
  GameState --> Recorder
  GameState --> SaveLoad
```

### Class relationships (Mermaid)
```mermaid
classDiagram
  class GameState {
    - Board board
    - Player current_player
    - Move[] history
    + move(from,to)
    + undo()
    + status_lines()
  }
  class Board {
    + piece_at(x,y) Piece
    + place_piece(p,x,y)
    + remove_piece(x,y) Piece
  }
  class Rules {
    + is_legal_move(board,piece,to_x,to_y) bool
    + can_capture(attacker,defender,board,from,to) bool
  }
  class Piece { Animal animal; Player owner; int x; int y }
  class Move { Player player; tuple from; tuple to; Animal moved; Piece captured }

  GameState --> Board
  GameState --> Rules
  Board --> Piece
  GameState --> Move
```

### Turn flow (Sequence)
```mermaid
sequenceDiagram
  participant U as User
  participant C as CLI
  participant G as GameState
  participant R as Rules

  U->>C: move b3 b4
  C->>G: legal_move((1,2),(1,3))
  G->>R: is_legal_move(board,piece,1,3)
  R-->>G: ok/err
  alt ok
    G->>G: apply move, push history, switch player
    G-->>C: success
    C-->>U: print board
  else err
    G-->>C: error reason
    C-->>U: show error
  end
```

## Exception handling
- Invalid commands => print usage and continue
- Illegal moves => print rule reason and keep turn
- File IO errors => show message and continue

## Justification
- Modularity and testability: rules isolated in `rules.py`, board state in `board.py`.
- Extendibility: additional commands or alternative UIs can reuse the `model`.
