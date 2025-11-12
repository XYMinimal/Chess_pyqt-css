from src.domain.board import Board
from src.domain.entities import Position, Piece, Team
from src.domain.game_state import GameState, GameStatus
from src.application.usecases import (
    InitializeGameUseCase,
    RenderBoardUseCase,
    GetValidMovesUseCase,
    ExecuteMoveUseCase,
)


class ChessController:
    def __init__(self, board: Board, game_state: GameState):
        self._board = board
        self._game_state = game_state
        self._initialize_game_use_case = InitializeGameUseCase(board, game_state)
        self._render_board_use_case = RenderBoardUseCase(board)
        self._get_valid_moves_use_case = GetValidMovesUseCase(board)
        self._execute_move_use_case = ExecuteMoveUseCase(board, game_state)

    def initialize_game(self) -> None:
        self._initialize_game_use_case.execute()

    def get_pieces_for_rendering(self):
        return self._render_board_use_case.get_pieces_to_render()

    def get_piece_renderer(self):
        return self._render_board_use_case.get_renderer()

    def get_piece_at(self, position: Position) -> Piece | None:
        piece = self._board.get_piece(position)
        return piece

    def get_valid_moves(self, piece: Piece) -> list[Position]:
        return self._get_valid_moves_use_case.execute(piece)

    def move_piece(self, piece: Piece, target: Position) -> tuple[Piece | None, GameStatus]:
        return self._execute_move_use_case.execute(piece, target)

    def get_current_turn(self) -> Team:
        return self._game_state.current_turn

    def get_game_status(self) -> GameStatus:
        return self._game_state.status

    def is_game_over(self) -> bool:
        return self._game_state.status != GameStatus.IN_PROGRESS

    def get_winner(self) -> Team | None:
        if self._game_state.status == GameStatus.WHITE_WON:
            return Team.WHITE
        elif self._game_state.status == GameStatus.BLACK_WON:
            return Team.BLACK
        return None

    def reset_game(self) -> None:
        self.initialize_game()
