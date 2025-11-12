from src.domain.entities import Piece, PieceType, Team, Position


class PieceFactory:
    @staticmethod
    def create(piece_type: PieceType, team: Team, position: Position) -> Piece:
        return Piece(piece_type=piece_type, team=team, position=position)

    @staticmethod
    def create_from_starting_position(
        piece_type: PieceType, team: Team, row: int, col: int
    ) -> Piece:
        position = Position(row=row, col=col)
        return PieceFactory.create(piece_type, team, position)
