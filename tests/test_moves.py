from src.domain.board import Board
from src.domain.entities import Piece, PieceType, Team, Position
from src.application.services import MoveValidator, MoveExecutor
from src.infrastructure.factories import PieceFactory


class TestMoveValidator:
    def setup_method(self):
        self.board = Board()
        self.validator = MoveValidator(self.board)

    def test_pawn_forward_one_move(self):
        board = Board()
        pawn = Piece(PieceType.PAWN, Team.WHITE, Position(6, 0))
        board.add_piece(pawn)
        
        validator = MoveValidator(board)
        valid_moves = validator.get_valid_moves(pawn)
        
        assert Position(5, 0) in valid_moves
        assert Position(4, 0) in valid_moves

    def test_pawn_cannot_move_forward_blocked(self):
        board = Board()
        pawn = Piece(PieceType.PAWN, Team.WHITE, Position(5, 0))
        blocking_piece = Piece(PieceType.PAWN, Team.BLACK, Position(4, 0))
        board.add_piece(pawn)
        board.add_piece(blocking_piece)
        
        validator = MoveValidator(board)
        valid_moves = validator.get_valid_moves(pawn)
        
        assert Position(4, 0) not in valid_moves

    def test_pawn_diagonal_capture(self):
        board = Board()
        white_pawn = Piece(PieceType.PAWN, Team.WHITE, Position(5, 0))
        black_pawn = Piece(PieceType.PAWN, Team.BLACK, Position(4, 1))
        board.add_piece(white_pawn)
        board.add_piece(black_pawn)
        
        validator = MoveValidator(board)
        valid_moves = validator.get_valid_moves(white_pawn)
        
        assert Position(4, 1) in valid_moves

    def test_knight_l_shaped_moves(self):
        board = Board()
        knight = Piece(PieceType.KNIGHT, Team.WHITE, Position(3, 3))
        board.add_piece(knight)
        
        validator = MoveValidator(board)
        valid_moves = validator.get_valid_moves(knight)
        
        expected_moves = [
            Position(5, 4), Position(5, 2),
            Position(1, 4), Position(1, 2),
            Position(4, 5), Position(4, 1),
            Position(2, 5), Position(2, 1),
        ]
        
        for move in expected_moves:
            assert move in valid_moves

    def test_rook_horizontal_and_vertical_moves(self):
        board = Board()
        rook = Piece(PieceType.ROOK, Team.WHITE, Position(3, 3))
        board.add_piece(rook)
        
        validator = MoveValidator(board)
        valid_moves = validator.get_valid_moves(rook)
        
        for col in range(8):
            if col != 3:
                assert Position(3, col) in valid_moves
        
        for row in range(8):
            if row != 3:
                assert Position(row, 3) in valid_moves

    def test_rook_blocked_by_own_piece(self):
        board = Board()
        rook = Piece(PieceType.ROOK, Team.WHITE, Position(3, 3))
        blocking_piece = Piece(PieceType.PAWN, Team.WHITE, Position(3, 5))
        board.add_piece(rook)
        board.add_piece(blocking_piece)
        
        validator = MoveValidator(board)
        valid_moves = validator.get_valid_moves(rook)
        
        assert Position(3, 5) not in valid_moves
        assert Position(3, 4) in valid_moves

    def test_bishop_diagonal_moves(self):
        board = Board()
        bishop = Piece(PieceType.BISHOP, Team.WHITE, Position(3, 3))
        board.add_piece(bishop)
        
        validator = MoveValidator(board)
        valid_moves = validator.get_valid_moves(bishop)
        
        for i in range(1, 4):
            assert Position(3 + i, 3 + i) in valid_moves
            assert Position(3 - i, 3 - i) in valid_moves
            assert Position(3 + i, 3 - i) in valid_moves
            assert Position(3 - i, 3 + i) in valid_moves

    def test_queen_combines_rook_and_bishop_moves(self):
        board = Board()
        queen = Piece(PieceType.QUEEN, Team.WHITE, Position(3, 3))
        board.add_piece(queen)
        
        validator = MoveValidator(board)
        valid_moves = validator.get_valid_moves(queen)
        
        assert Position(3, 5) in valid_moves
        assert Position(5, 3) in valid_moves
        assert Position(5, 5) in valid_moves
        assert Position(5, 1) in valid_moves

    def test_king_one_square_moves(self):
        board = Board()
        king = Piece(PieceType.KING, Team.WHITE, Position(3, 3))
        board.add_piece(king)
        
        validator = MoveValidator(board)
        valid_moves = validator.get_valid_moves(king)
        
        expected_moves = [
            Position(2, 2), Position(2, 3), Position(2, 4),
            Position(3, 2), Position(3, 4),
            Position(4, 2), Position(4, 3), Position(4, 4),
        ]
        
        for move in expected_moves:
            assert move in valid_moves


class TestMoveExecutor:
    def test_move_piece_updates_position(self):
        board = Board()
        pawn = Piece(PieceType.PAWN, Team.WHITE, Position(6, 0))
        board.add_piece(pawn)
        
        executor = MoveExecutor(board)
        target = Position(5, 0)
        moved_piece = executor.execute_move(pawn, target)
        
        assert moved_piece.position == target
        assert board.get_piece(Position(6, 0)) is None
        assert board.get_piece(target) == moved_piece

    def test_move_piece_captures_opponent(self):
        board = Board()
        white_piece = Piece(PieceType.PAWN, Team.WHITE, Position(5, 0))
        black_piece = Piece(PieceType.PAWN, Team.BLACK, Position(4, 0))
        board.add_piece(white_piece)
        board.add_piece(black_piece)
        
        executor = MoveExecutor(board)
        target = Position(4, 0)
        moved_piece = executor.execute_move(white_piece, target)
        
        assert board.get_piece(target) == moved_piece
        assert board.get_all_pieces() == [moved_piece]
