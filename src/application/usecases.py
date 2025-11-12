from src.domain.board import Board
from src.domain.entities import Position, Piece, PieceType, Team
from src.domain.game_state import GameState, GameStatus
from src.application.services import (
    BoardSetupService,
    BoardQueryService,
    MoveValidator,
    MoveExecutor,
    PawnPromotionService,
    KingCheckService,
)
from src.application.rendering import SVGPieceRenderer


class InitializeGameUseCase:
    def __init__(self, board: Board, game_state: GameState):
        self._setup_service = BoardSetupService(board)
        self._game_state = game_state

    def execute(self) -> None:
        self._setup_service.initialize_standard_game()
        self._game_state.reset()


class GetBoardStateUseCase:
    def __init__(self, board: Board):
        self._query_service = BoardQueryService(board)

    def execute(self):
        return self._query_service.get_all_pieces()


class RenderBoardUseCase:
    def __init__(self, board: Board):
        self._query_service = BoardQueryService(board)
        self._piece_renderer = SVGPieceRenderer()

    def get_renderer(self) -> SVGPieceRenderer:
        return self._piece_renderer

    def get_pieces_to_render(self):
        return self._query_service.get_all_pieces()


class GetValidMovesUseCase:
    def __init__(self, board: Board):
        self._validator = MoveValidator(board)

    def execute(self, piece: Piece) -> list[Position]:
        return self._validator.get_valid_moves(piece)


class ExecuteMoveUseCase:
    def __init__(self, board: Board, game_state: GameState):
        self._board = board
        self._validator = MoveValidator(board)
        self._executor = MoveExecutor(board)
        self._query_service = BoardQueryService(board)
        self._promotion_service = PawnPromotionService()
        self._king_check_service = KingCheckService(board)
        self._game_state = game_state

    def execute(self, piece: Piece, target: Position) -> tuple[Piece | None, GameStatus]:
        if piece.team != self._game_state.current_turn:
            return None, self._game_state.status
        
        if not self._validator.is_valid_move(piece, target):
            return None, self._game_state.status
        
        if self._king_check_service.did_capture_king(piece, target):
            moved_piece = self._executor.execute_move(piece, target)
            self._game_state.set_winner(piece.team)
            return moved_piece, self._game_state.status
        
        moved_piece = self._executor.execute_move(piece, target)
        
        if self._promotion_service.should_promote(moved_piece):
            promoted_piece = self._promotion_service.promote(moved_piece, PieceType.QUEEN)
            self._board.remove_piece(moved_piece.position)
            self._board.add_piece(promoted_piece)
            moved_piece = promoted_piece
        
        self._game_state.next_turn()
        return moved_piece, self._game_state.status
