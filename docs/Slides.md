# Presentation Slides (Outline)

Time: 4.5 minutes + 1 minute Q&A

## 1. CLI UI design
- Commands overview (new/name/show/move/undo/save/load/record/replay)
- Output legend (pieces/terrain)
- Error handling examples

## 2. Overall design
- Architecture: MVC rationale (model separation)
- Main components: Board, Rules, GameState, CLI
- Diagrams: include from Design.md (Mermaid)

## 3. Example turn
- `move b3 b4` path through `GameState` -> `Rules` -> apply -> status

## 4. One key lesson learned
- Example: Writing verifiable requirements improves testability; or designing APIs around pure functions makes unit tests easier.

Note: Export this Markdown to PDF (e.g., VS Code Markdown PDF extension or print to PDF).
