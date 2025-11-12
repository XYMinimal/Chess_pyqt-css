from src.domain.board import Board
from src.infrastructure.factories import PieceFactory
from src.domain.entities import PieceType, Team, Position
from src.application.services import BoardSetupService, BoardQueryService


class TestBoardSetupService:
    def test_initialize_standard_game(self):
        board = Board()
        setup_service = BoardSetupService(board)
        setup_service.initialize_standard_game()

        all_pieces = board.get_all_pieces()
        assert len(all_pieces) == 32

        white_pieces = board.get_pieces_by_team(Team.WHITE)
        black_pieces = board.get_pieces_by_team(Team.BLACK)

        assert len(white_pieces) == 16
        assert len(black_pieces) == 16

    def test_initialize_clears_previous_state(self):
        board = Board()
        setup_service = BoardSetupService(board)

        setup_service.initialize_standard_game()
        assert len(board.get_all_pieces()) == 32

        setup_service.initialize_standard_game()
        assert len(board.get_all_pieces()) == 32


class TestBoardQueryService:
    def setup_method(self):
        self.board = Board()
        self.setup_service = BoardSetupService(self.board)
        self.query_service = BoardQueryService(self.board)
        self.setup_service.initialize_standard_game()

    def test_get_piece_at_white_pawn_starting_position(self):
        pos = Position(6, 0)
        piece = self.query_service.get_piece_at(pos)
        assert piece is not None
        assert piece.piece_type == PieceType.PAWN
        assert piece.team == Team.WHITE

    def test_get_piece_at_empty_square(self):
        pos = Position(4, 4)
        piece = self.query_service.get_piece_at(pos)
        assert piece is None

    def test_is_square_occupied(self):
        occupied = Position(7, 4)
        empty = Position(4, 4)

        assert self.query_service.is_square_occupied(occupied)
        assert not self.query_service.is_square_occupied(empty)

    def test_get_all_pieces_returns_32_at_start(self):
        pieces = self.query_service.get_all_pieces()
        assert len(pieces) == 32
