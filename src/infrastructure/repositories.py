from src.domain.board import Board
from src.domain.entities import Piece, Team


class PieceRepository:
    def __init__(self, board: Board):
        self._board = board

    def save(self, piece: Piece) -> None:
        self._board.add_piece(piece)

    def find_by_position(self, position):
        return self._board.get_piece(position)

    def find_all_by_team(self, team: Team) -> list[Piece]:
        return self._board.get_pieces_by_team(team)

    def find_all(self) -> list[Piece]:
        return self._board.get_all_pieces()

    def delete(self, position) -> None:
        self._board.remove_piece(position)


class BoardRepository:
    def __init__(self):
        self._board = Board()

    def get_board(self) -> Board:
        return self._board

    def get_piece_at(self, position):
        return self._board.get_piece(position)

    def add_piece(self, piece: Piece) -> None:
        self._board.add_piece(piece)

    def clear_board(self) -> None:
        self._board.clear()
