from enum import Enum
from src.domain.entities import Team


class GameStatus(Enum):
    IN_PROGRESS = "in_progress"
    WHITE_IN_CHECK = "white_in_check"
    BLACK_IN_CHECK = "black_in_check"
    WHITE_WON = "white_won"
    BLACK_WON = "black_won"
    DRAW = "draw"


class GameState:
    def __init__(self, current_turn: Team = Team.WHITE):
        self._current_turn = current_turn
        self._status = GameStatus.IN_PROGRESS
        self._move_count = 0

    @property
    def current_turn(self) -> Team:
        return self._current_turn

    @property
    def status(self) -> GameStatus:
        return self._status

    @property
    def move_count(self) -> int:
        return self._move_count

    def next_turn(self) -> None:
        self._current_turn = Team.BLACK if self._current_turn == Team.WHITE else Team.WHITE
        self._move_count += 1

    def set_winner(self, winner: Team) -> None:
        self._status = GameStatus.WHITE_WON if winner == Team.WHITE else GameStatus.BLACK_WON

    def end_game(self, status: GameStatus) -> None:
        self._status = status

    def reset(self) -> None:
        self._current_turn = Team.WHITE
        self._status = GameStatus.IN_PROGRESS
        self._move_count = 0
