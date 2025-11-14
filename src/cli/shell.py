from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable, Dict, List, Optional

from ..model.board import InvalidMoveError
from ..model.enums import PlayerSide
from ..model.game_state import GameState
from ..model.serialization import SerializationError, export_record, load_game, load_record, save_game
from ..model.position import Position

from .renderers import render_board, render_status
from .utils import ensure_extension, parse_command, parse_position, random_name


class JungleShell:
    PROMPT = "jungle> "

    def __init__(self) -> None:
        self.state = GameState.new(random_name(), random_name())
        self._commands: Dict[str, Callable[[List[str]], None]] = {
            "help": self._cmd_help,
            "?": self._cmd_help,
            "new": self._cmd_new,
            "show": self._cmd_show,
            "status": self._cmd_status,
            "move": self._cmd_move,
            "undo": self._cmd_undo,
            "save-game": self._cmd_save,
            "load-game": self._cmd_load,
            "export-record": self._cmd_export_record,
            "replay-record": self._cmd_replay_record,
            "players": self._cmd_players,
            "history": self._cmd_history,
            "quit": self._cmd_quit,
            "exit": self._cmd_quit,
        }

    def cmdloop(self) -> None:
        print("Welcome to Jungle! Type 'help' to see available commands.")
        while True:
            try:
                raw = input(self.PROMPT)
            except EOFError:
                print()
                return
            command_line = raw.strip()
            if not command_line:
                continue
            self._dispatch(command_line)

    def _dispatch(self, command_line: str) -> None:
        try:
            parts = parse_command(command_line)
        except ValueError as exc:
            print(f"Invalid input: {exc}")
            return
        if not parts:
            return
        cmd = parts[0].lower()
        handler = self._commands.get(cmd)
        if not handler:
            print(
                f"Unknown command '{cmd}'. Type 'help' for a list of commands.")
            return
        try:
            handler(parts[1:])
        except InvalidMoveError as exc:
            print(f"Move rejected: {exc}")
        except SerializationError as exc:
            print(f"File error: {exc}")
        except ValueError as exc:
            print(f"Error: {exc}")

    # Command implementations -------------------------------------------------

    def _cmd_help(self, _: List[str]) -> None:
        print(
            "Available commands:\n"
            "  help                      Show this message\n"
            "  new [blue] [red]          Start a new game (optional player names)\n"
            "  players <side> <name>     Rename BLUE or RED player\n"
            "  show                      Display the board\n"
            "  status                    Show board plus remaining pieces & turn info\n"
            "  move <from> <to>          Move a piece using notation (e.g., move a3 a4)\n"
            "  history [n]               Show the last n moves (default 5)\n"
            "  undo [side]               Undo the last move (optional player: blue/red)\n"
            "  save-game <file.jungle>   Persist the current game\n"
            "  load-game <file.jungle>   Load a saved game\n"
            "  export-record <file.record> Save the finished game's move record\n"
            "  replay-record <file.record> Replay a recorded game\n"
            "  quit                      Exit the program"
        )

    def _cmd_new(self, args: List[str]) -> None:
        blue = args[0] if args else random_name()
        red = args[1] if len(args) > 1 else random_name()
        self.state = GameState.new(blue, red)
        print("New game created.")
        self._cmd_status([])

    def _cmd_players(self, args: List[str]) -> None:
        if len(args) < 2:
            raise ValueError("Usage: players <blue|red> <name>")
        side = self._parse_side(args[0])
        name = " ".join(args[1:])
        self.state.rename_player(side, name)
        print(f"Player {side.name} is now '{name}'.")

    def _cmd_show(self, _: List[str]) -> None:
        print(render_board(self.state.board))

    def _cmd_status(self, _: List[str]) -> None:
        print(render_board(self.state.board))
        print(
            f"Turn: {self.state.player_names[self.state.current_player]} ({self.state.current_player.name})\n"
            f"Undo credits - BLUE: {self.state.undo_remaining[PlayerSide.BLUE]}, "
            f"RED: {self.state.undo_remaining[PlayerSide.RED]}"
        )
        if self.state.winner:
            print(
                f"Winner: {self.state.player_names[self.state.winner]} ({self.state.winner.name})")
        print(render_status(self.state.board))

    def _cmd_move(self, args: List[str]) -> None:
        if len(args) != 2:
            raise ValueError("Usage: move <from> <to>")
        src = parse_position(args[0])
        dst = parse_position(args[1])
        record = self.state.move(src, dst)
        print(
            f"Moved {record.piece} from {record.source} to {record.target}" +
            (f", capturing {record.capture}" if record.capture else "")
        )
        if self.state.winner:
            print(
                f"Game over! Winner: {self.state.player_names[self.state.winner]} ({self.state.winner.name})")

    def _cmd_history(self, args: List[str]) -> None:
        count = int(args[0]) if args else 5
        moves = self.state.move_log
        recent = self.state.last_moves(count)
        start_index = len(moves) - len(recent) + 1 if recent else 0
        for idx, move in enumerate(recent, start=max(1, start_index)):
            details = f"#{idx}: {move.player} moved {move.piece} {move.source}->{move.target}"
            if move.capture:
                details += f" capturing {move.capture}"
            print(details)

    def _cmd_undo(self, args: List[str]) -> None:
        side = self._parse_side(args[0]) if args else self.state.current_player
        self.state.undo(side)
        print(
            f"Last move undone. Undo credits left for {side.name}: {self.state.undo_remaining[side]}")
        self._cmd_status([])

    def _cmd_save(self, args: List[str]) -> None:
        if len(args) != 1:
            raise ValueError("Usage: save-game <file.jungle>")
        path = ensure_extension(args[0], ".jungle")
        save_game(self.state, path)
        print(f"Game saved to {path}.")

    def _cmd_load(self, args: List[str]) -> None:
        if len(args) != 1:
            raise ValueError("Usage: load-game <file.jungle>")
        path = ensure_extension(args[0], ".jungle")
        self.state = load_game(path)
        print(f"Loaded game from {path}.")
        self._cmd_status([])

    def _cmd_export_record(self, args: List[str]) -> None:
        if len(args) != 1:
            raise ValueError("Usage: export-record <file.record>")
        if not self.state.move_log:
            raise ValueError("No moves have been played yet.")
        path = ensure_extension(args[0], ".record")
        export_record(self.state, path)
        print(f"Record exported to {path}.")

    def _cmd_replay_record(self, args: List[str]) -> None:
        if len(args) != 1:
            raise ValueError("Usage: replay-record <file.record>")
        path = ensure_extension(args[0], ".record")
        record = load_record(path)
        print(
            f"Replaying record created on {record.created_at}\n"
            f"Players: {record.players.get(PlayerSide.BLUE, 'Blue')} vs {record.players.get(PlayerSide.RED, 'Red')}"
        )
        replay_state = GameState.new(
            record.players.get(PlayerSide.BLUE, "Blue"),
            record.players.get(PlayerSide.RED, "Red"),
        )
        for idx, move in enumerate(record.moves, start=1):
            try:
                replay_state.move(Position.from_notation(
                    move.source), Position.from_notation(move.target))
            except InvalidMoveError as exc:
                print(f"Replay aborted at move {idx}: {exc}")
                return
            print(f"Move {idx}: {move.player} -> {move.source}->{move.target}")
            print(render_board(replay_state.board))
        print("Replay finished.")

    def _cmd_quit(self, _: List[str]) -> None:
        print("Goodbye!")
        sys.exit(0)

    # Helpers -----------------------------------------------------------------

    def _parse_side(self, token: str) -> PlayerSide:
        token = token.strip().lower()
        if token in {"blue", "b"}:
            return PlayerSide.BLUE
        if token in {"red", "r"}:
            return PlayerSide.RED
        raise ValueError("Player side must be 'blue' or 'red'.")


def run_shell() -> None:
    JungleShell().cmdloop()
