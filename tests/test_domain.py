import pytest
from src.domain.entities import Piece, PieceType, Team, Position
from src.domain.board import Board
from src.infrastructure.factories import PieceFactory


class TestPosition:
    def test_position_creation_valid(self):
        pos = Position(0, 0)
        assert pos.row == 0
        assert pos.col == 0

    def test_position_algebraic_notation(self):
        pos = Position(0, 0)
        assert pos.algebraic == "a8"

        pos = Position(7, 7)
        assert pos.algebraic == "h1"

    def test_position_out_of_bounds_raises_error(self):
        with pytest.raises(ValueError):
            Position(8, 0)

        with pytest.raises(ValueError):
            Position(0, -1)

    def test_position_equality(self):
        pos1 = Position(3, 3)
        pos2 = Position(3, 3)
        assert pos1 == pos2

    def test_position_immutable(self):
        pos = Position(4, 4)
        with pytest.raises(AttributeError):
            pos.row = 5


class TestPiece:
    def test_piece_creation(self):
        pos = Position(0, 0)
        piece = Piece(PieceType.KING, Team.WHITE, pos)
        assert piece.piece_type == PieceType.KING
        assert piece.team == Team.WHITE
        assert piece.position == pos

    def test_piece_equality(self):
        pos = Position(0, 0)
        piece1 = Piece(PieceType.PAWN, Team.BLACK, pos)
        piece2 = Piece(PieceType.PAWN, Team.BLACK, pos)
        assert piece1 == piece2

    def test_piece_inequality_different_type(self):
        pos = Position(0, 0)
        piece1 = Piece(PieceType.PAWN, Team.BLACK, pos)
        piece2 = Piece(PieceType.ROOK, Team.BLACK, pos)
        assert piece1 != piece2


class TestBoard:
    def test_board_creation(self):
        board = Board()
        assert len(board.get_all_pieces()) == 0

    def test_add_piece_to_board(self):
        board = Board()
        pos = Position(0, 0)
        piece = Piece(PieceType.KING, Team.WHITE, pos)
        board.add_piece(piece)
        assert board.get_piece(pos) == piece

    def test_get_piece_returns_none_for_empty_square(self):
        board = Board()
        pos = Position(0, 0)
        assert board.get_piece(pos) is None

    def test_remove_piece_from_board(self):
        board = Board()
        pos = Position(0, 0)
        piece = Piece(PieceType.KING, Team.WHITE, pos)
        board.add_piece(piece)
        board.remove_piece(pos)
        assert board.get_piece(pos) is None

    def test_get_pieces_by_team(self):
        board = Board()
        board.add_piece(Piece(PieceType.PAWN, Team.WHITE, Position(0, 0)))
        board.add_piece(Piece(PieceType.PAWN, Team.WHITE, Position(0, 1)))
        board.add_piece(Piece(PieceType.PAWN, Team.BLACK, Position(1, 0)))

        white_pieces = board.get_pieces_by_team(Team.WHITE)
        black_pieces = board.get_pieces_by_team(Team.BLACK)

        assert len(white_pieces) == 2
        assert len(black_pieces) == 1

    def test_clear_board(self):
        board = Board()
        board.add_piece(Piece(PieceType.KING, Team.WHITE, Position(0, 0)))
        board.clear()
        assert len(board.get_all_pieces()) == 0

    def test_starting_positions(self):
        positions = Board.starting_positions()
        assert len(positions) == 32

        white_count = sum(1 for _, team in positions.values() if team == Team.WHITE)
        black_count = sum(1 for _, team in positions.values() if team == Team.BLACK)

        assert white_count == 16
        assert black_count == 16
