from enum import Enum
from dataclasses import dataclass
from typing import Optional


class PieceType(Enum):
    PAWN = "pawn"
    ROOK = "rook"
    KNIGHT = "knight"
    BISHOP = "bishop"
    QUEEN = "queen"
    KING = "king"


class Team(Enum):
    WHITE = "white"
    BLACK = "black"


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __post_init__(self):
        if not (0 <= self.row < 8 and 0 <= self.col < 8):
            raise ValueError(f"Position ({self.row}, {self.col}) out of board bounds")

    @property
    def algebraic(self) -> str:
        return f"{chr(97 + self.col)}{8 - self.row}"


@dataclass
class Piece:
    piece_type: PieceType
    team: Team
    position: Position

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return (
            self.piece_type == other.piece_type
            and self.team == other.team
            and self.position == other.position
        )
