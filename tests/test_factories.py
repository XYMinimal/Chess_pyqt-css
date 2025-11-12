from src.domain.board import Board
from src.infrastructure.factories import PieceFactory
from src.domain.entities import PieceType, Team, Position


class TestPieceFactory:
    def test_create_piece(self):
        pos = Position(0, 0)
        piece = PieceFactory.create(PieceType.KING, Team.WHITE, pos)

        assert piece.piece_type == PieceType.KING
        assert piece.team == Team.WHITE
        assert piece.position == pos

    def test_create_from_starting_position(self):
        piece = PieceFactory.create_from_starting_position(
            PieceType.QUEEN, Team.BLACK, 0, 3
        )

        assert piece.piece_type == PieceType.QUEEN
        assert piece.team == Team.BLACK
        assert piece.position.row == 0
        assert piece.position.col == 3
