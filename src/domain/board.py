from typing import Dict, Set
from src.domain.entities import Piece, Position, PieceType, Team


class Board:
    BOARD_SIZE = 8
    STANDARD_START_ROW_WHITE = 7
    STANDARD_START_ROW_BLACK = 0

    def __init__(self):
        self._pieces: Dict[Position, Piece] = {}

    def add_piece(self, piece: Piece) -> None:
        self._pieces[piece.position] = piece

    def remove_piece(self, position: Position) -> None:
        self._pieces.pop(position, None)

    def get_piece(self, position: Position) -> Piece | None:
        return self._pieces.get(position)

    def get_pieces_by_team(self, team: Team) -> list[Piece]:
        return [p for p in self._pieces.values() if p.team == team]

    def get_all_pieces(self) -> list[Piece]:
        return list(self._pieces.values())

    def clear(self) -> None:
        self._pieces.clear()

    @staticmethod
    def starting_positions() -> Dict[Position, tuple[PieceType, Team]]:
        positions = {}

        back_row_order = [
            PieceType.ROOK,
            PieceType.KNIGHT,
            PieceType.BISHOP,
            PieceType.QUEEN,
            PieceType.KING,
            PieceType.BISHOP,
            PieceType.KNIGHT,
            PieceType.ROOK,
        ]

        for col, piece_type in enumerate(back_row_order):
            positions[Position(Board.STANDARD_START_ROW_WHITE, col)] = (
                piece_type,
                Team.WHITE,
            )
            positions[Position(Board.STANDARD_START_ROW_BLACK, col)] = (
                piece_type,
                Team.BLACK,
            )

        for col in range(Board.BOARD_SIZE):
            positions[Position(Board.STANDARD_START_ROW_WHITE - 1, col)] = (
                PieceType.PAWN,
                Team.WHITE,
            )
            positions[Position(Board.STANDARD_START_ROW_BLACK + 1, col)] = (
                PieceType.PAWN,
                Team.BLACK,
            )

        return positions
