import pytest
from src.domain.entities import Piece, PieceType, Team, Position
from src.domain.board import Board
from src.domain.game_state import GameState, GameStatus
from src.application.services import PawnPromotionService, KingCheckService
from src.application.usecases import ExecuteMoveUseCase


class TestGameState:
    def test_initial_turn_is_white(self):
        game_state = GameState()
        assert game_state.current_turn == Team.WHITE

    def test_next_turn_switches_teams(self):
        game_state = GameState()
        assert game_state.current_turn == Team.WHITE
        game_state.next_turn()
        assert game_state.current_turn == Team.BLACK
        game_state.next_turn()
        assert game_state.current_turn == Team.WHITE

    def test_move_count_increments(self):
        game_state = GameState()
        assert game_state.move_count == 0
        game_state.next_turn()
        assert game_state.move_count == 1

    def test_initial_status_is_in_progress(self):
        game_state = GameState()
        assert game_state.status == GameStatus.IN_PROGRESS

    def test_set_winner_white(self):
        game_state = GameState()
        game_state.set_winner(Team.WHITE)
        assert game_state.status == GameStatus.WHITE_WON

    def test_set_winner_black(self):
        game_state = GameState()
        game_state.set_winner(Team.BLACK)
        assert game_state.status == GameStatus.BLACK_WON

    def test_reset_clears_state(self):
        game_state = GameState()
        game_state.next_turn()
        game_state.set_winner(Team.WHITE)
        
        game_state.reset()
        
        assert game_state.current_turn == Team.WHITE
        assert game_state.status == GameStatus.IN_PROGRESS
        assert game_state.move_count == 0


class TestPawnPromotion:
    def test_white_pawn_promotes_at_row_0(self):
        pawn = Piece(PieceType.PAWN, Team.WHITE, Position(0, 0))
        
        assert PawnPromotionService.should_promote(pawn)

    def test_black_pawn_promotes_at_row_7(self):
        pawn = Piece(PieceType.PAWN, Team.BLACK, Position(7, 0))
        
        assert PawnPromotionService.should_promote(pawn)

    def test_pawn_does_not_promote_in_middle(self):
        pawn = Piece(PieceType.PAWN, Team.WHITE, Position(4, 0))
        
        assert not PawnPromotionService.should_promote(pawn)

    def test_non_pawn_does_not_promote(self):
        queen = Piece(PieceType.QUEEN, Team.WHITE, Position(0, 0))
        
        assert not PawnPromotionService.should_promote(queen)

    def test_promote_to_queen(self):
        pawn = Piece(PieceType.PAWN, Team.WHITE, Position(0, 3))
        promoted = PawnPromotionService.promote(pawn, PieceType.QUEEN)
        
        assert promoted.piece_type == PieceType.QUEEN
        assert promoted.team == Team.WHITE
        assert promoted.position == Position(0, 3)


class TestKingCheckService:
    def test_king_alive_with_king_on_board(self):
        board = Board()
        board.add_piece(Piece(PieceType.KING, Team.WHITE, Position(0, 4)))
        
        king_check = KingCheckService(board)
        assert king_check.is_king_alive(Team.WHITE)

    def test_king_not_alive_when_no_king(self):
        board = Board()
        board.add_piece(Piece(PieceType.PAWN, Team.WHITE, Position(0, 0)))
        
        king_check = KingCheckService(board)
        assert not king_check.is_king_alive(Team.WHITE)

    def test_get_king_by_team(self):
        board = Board()
        king = Piece(PieceType.KING, Team.WHITE, Position(0, 4))
        board.add_piece(king)
        
        king_check = KingCheckService(board)
        found_king = king_check.get_kings_by_team(Team.WHITE)
        
        assert found_king == king

    def test_get_king_returns_none_when_no_king(self):
        board = Board()
        board.add_piece(Piece(PieceType.PAWN, Team.WHITE, Position(0, 0)))
        
        king_check = KingCheckService(board)
        found_king = king_check.get_kings_by_team(Team.WHITE)
        
        assert found_king is None

    def test_did_capture_king(self):
        board = Board()
        white_pawn = Piece(PieceType.PAWN, Team.WHITE, Position(1, 1))
        black_king = Piece(PieceType.KING, Team.BLACK, Position(0, 0))
        board.add_piece(white_pawn)
        board.add_piece(black_king)
        
        king_check = KingCheckService(board)
        assert king_check.did_capture_king(white_pawn, Position(0, 0))


class TestExecuteMoveWithTurns:
    def test_white_can_move_on_white_turn(self):
        board = Board()
        game_state = GameState(Team.WHITE)
        
        white_pawn = Piece(PieceType.PAWN, Team.WHITE, Position(6, 0))
        board.add_piece(white_pawn)
        
        executor = ExecuteMoveUseCase(board, game_state)
        moved, status = executor.execute(white_pawn, Position(5, 0))
        
        assert moved is not None
        assert moved.position == Position(5, 0)

    def test_black_cannot_move_on_white_turn(self):
        board = Board()
        game_state = GameState(Team.WHITE)
        
        black_pawn = Piece(PieceType.PAWN, Team.BLACK, Position(1, 0))
        board.add_piece(black_pawn)
        
        executor = ExecuteMoveUseCase(board, game_state)
        moved, status = executor.execute(black_pawn, Position(2, 0))
        
        assert moved is None

    def test_game_advances_turn_after_valid_move(self):
        board = Board()
        game_state = GameState(Team.WHITE)
        
        white_pawn = Piece(PieceType.PAWN, Team.WHITE, Position(6, 0))
        board.add_piece(white_pawn)
        
        assert game_state.current_turn == Team.WHITE
        
        executor = ExecuteMoveUseCase(board, game_state)
        moved, status = executor.execute(white_pawn, Position(5, 0))
        
        assert moved is not None
        assert game_state.current_turn == Team.BLACK

    def test_pawn_promotes_on_final_row(self):
        board = Board()
        game_state = GameState(Team.WHITE)
        
        white_pawn = Piece(PieceType.PAWN, Team.WHITE, Position(1, 0))
        board.add_piece(white_pawn)
        
        executor = ExecuteMoveUseCase(board, game_state)
        moved, status = executor.execute(white_pawn, Position(0, 0))
        
        assert moved is not None
        assert moved.piece_type == PieceType.QUEEN
        assert moved.position == Position(0, 0)

    def test_game_ends_when_king_captured(self):
        board = Board()
        game_state = GameState(Team.WHITE)
        
        white_pawn = Piece(PieceType.PAWN, Team.WHITE, Position(1, 1))
        black_king = Piece(PieceType.KING, Team.BLACK, Position(0, 0))
        board.add_piece(white_pawn)
        board.add_piece(black_king)
        
        executor = ExecuteMoveUseCase(board, game_state)
        moved, status = executor.execute(white_pawn, Position(0, 0))
        
        assert moved is not None
        assert status == GameStatus.WHITE_WON
