from src.domain.board import Board
from src.domain.entities import Piece, Team, Position, PieceType


class BoardSetupService:
    def __init__(self, board: Board):
        self._board = board

    def initialize_standard_game(self) -> None:
        self._board.clear()
        starting_positions = Board.starting_positions()

        for position, (piece_type, team) in starting_positions.items():
            piece = __import__('src.infrastructure.factories', fromlist=['PieceFactory']).PieceFactory.create(piece_type, team, position)
            self._board.add_piece(piece)

    def get_all_pieces(self) -> list[Piece]:
        return self._board.get_all_pieces()

    def get_pieces_by_team(self, team: Team) -> list[Piece]:
        return self._board.get_pieces_by_team(team)


class BoardQueryService:
    def __init__(self, board: Board):
        self._board = board

    def get_piece_at(self, position: Position) -> Piece | None:
        return self._board.get_piece(position)

    def get_all_pieces(self) -> list[Piece]:
        return self._board.get_all_pieces()

    def is_square_occupied(self, position: Position) -> bool:
        return self._board.get_piece(position) is not None

    def get_pieces_attacking_position(self, position: Position) -> list[Piece]:
        all_pieces = self._board.get_all_pieces()
        return [p for p in all_pieces if self._can_piece_attack(p, position)]

    @staticmethod
    def _can_piece_attack(piece: Piece, target: Position) -> bool:
        return True


class MoveValidator:
    def __init__(self, board: Board):
        self._board = board
        self._query_service = BoardQueryService(board)

    def get_valid_moves(self, piece: Piece) -> list[Position]:
        match piece.piece_type:
            case PieceType.PAWN:
                return self._get_pawn_moves(piece)
            case PieceType.ROOK:
                return self._get_rook_moves(piece)
            case PieceType.KNIGHT:
                return self._get_knight_moves(piece)
            case PieceType.BISHOP:
                return self._get_bishop_moves(piece)
            case PieceType.QUEEN:
                return self._get_queen_moves(piece)
            case PieceType.KING:
                return self._get_king_moves(piece)

    def is_valid_move(self, piece: Piece, target: Position) -> bool:
        return target in self.get_valid_moves(piece)

    def _get_pawn_moves(self, piece: Piece) -> list[Position]:
        moves = []
        direction = 1 if piece.team == Team.BLACK else -1
        
        forward_one_row = piece.position.row + direction
        if 0 <= forward_one_row < 8:
            forward_one = Position(forward_one_row, piece.position.col)
            if not self._query_service.is_square_occupied(forward_one):
                moves.append(forward_one)
        
        starting_row = 1 if piece.team == Team.BLACK else 6
        if piece.position.row == starting_row:
            forward_two_row = piece.position.row + 2 * direction
            if 0 <= forward_two_row < 8:
                forward_two = Position(forward_two_row, piece.position.col)
                forward_one = Position(forward_one_row, piece.position.col)
                if not self._query_service.is_square_occupied(forward_one) and not self._query_service.is_square_occupied(forward_two):
                    moves.append(forward_two)
        
        for col_offset in [-1, 1]:
            capture_col = piece.position.col + col_offset
            capture_row = forward_one_row
            if 0 <= capture_col < 8 and 0 <= capture_row < 8:
                capture_pos = Position(capture_row, capture_col)
                target_piece = self._query_service.get_piece_at(capture_pos)
                if target_piece and target_piece.team != piece.team:
                    moves.append(capture_pos)
        
        return moves

    def _get_rook_moves(self, piece: Piece) -> list[Position]:
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        moves.extend(self._get_sliding_moves(piece, directions))
        return moves

    def _get_bishop_moves(self, piece: Piece) -> list[Position]:
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        moves.extend(self._get_sliding_moves(piece, directions))
        return moves

    def _get_queen_moves(self, piece: Piece) -> list[Position]:
        moves = []
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        moves.extend(self._get_sliding_moves(piece, directions))
        return moves

    def _get_knight_moves(self, piece: Piece) -> list[Position]:
        moves = []
        offsets = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for row_offset, col_offset in offsets:
            target_row = piece.position.row + row_offset
            target_col = piece.position.col + col_offset
            if 0 <= target_row < 8 and 0 <= target_col < 8:
                target = Position(target_row, target_col)
                target_piece = self._query_service.get_piece_at(target)
                if not target_piece or target_piece.team != piece.team:
                    moves.append(target)
        return moves

    def _get_king_moves(self, piece: Piece) -> list[Position]:
        moves = []
        offsets = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for row_offset, col_offset in offsets:
            target_row = piece.position.row + row_offset
            target_col = piece.position.col + col_offset
            if 0 <= target_row < 8 and 0 <= target_col < 8:
                target = Position(target_row, target_col)
                target_piece = self._query_service.get_piece_at(target)
                if not target_piece or target_piece.team != piece.team:
                    moves.append(target)
        return moves

    def _get_sliding_moves(self, piece: Piece, directions: list[tuple]) -> list[Position]:
        moves = []
        for row_dir, col_dir in directions:
            for distance in range(1, 8):
                row = piece.position.row + row_dir * distance
                col = piece.position.col + col_dir * distance
                
                if not (0 <= row < 8 and 0 <= col < 8):
                    break
                
                target = Position(row, col)
                target_piece = self._query_service.get_piece_at(target)
                if not target_piece:
                    moves.append(target)
                else:
                    if target_piece.team != piece.team:
                        moves.append(target)
                    break
        return moves

    @staticmethod
    def _is_valid_position(position: Position) -> bool:
        try:
            Position(position.row, position.col)
            return True
        except ValueError:
            return False


class MoveExecutor:
    def __init__(self, board: Board):
        self._board = board

    def execute_move(self, piece: Piece, target: Position) -> Piece:
        self._board.remove_piece(piece.position)
        moved_piece = Piece(piece.piece_type, piece.team, target)
        self._board.add_piece(moved_piece)
        return moved_piece


class PawnPromotionService:
    @staticmethod
    def should_promote(piece: Piece) -> bool:
        if piece.piece_type != PieceType.PAWN:
            return False
        
        promotion_row = 0 if piece.team == Team.WHITE else 7
        return piece.position.row == promotion_row

    @staticmethod
    def promote(piece: Piece, target_type: PieceType = PieceType.QUEEN) -> Piece:
        return Piece(target_type, piece.team, piece.position)


class KingCheckService:
    def __init__(self, board: Board):
        self._board = board
        self._query_service = BoardQueryService(board)
        self._validator = MoveValidator(board)

    def did_capture_king(self, capturing_piece: Piece, target_position: Position) -> bool:
        target_piece = self._query_service.get_piece_at(target_position)
        return target_piece is not None and target_piece.piece_type == PieceType.KING

    def is_king_alive(self, team: Team) -> bool:
        pieces = self._board.get_pieces_by_team(team)
        return any(p.piece_type == PieceType.KING for p in pieces)

    def get_kings_by_team(self, team: Team) -> Piece | None:
        pieces = self._board.get_pieces_by_team(team)
        for piece in pieces:
            if piece.piece_type == PieceType.KING:
                return piece
        return None

