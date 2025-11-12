from abc import ABC, abstractmethod
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QPen, QBrush, QPolygon
from PyQt6.QtCore import QRect, Qt, QPoint
from src.domain.entities import PieceType, Team, Piece


class PieceRenderingStrategy(ABC):
    @abstractmethod
    def render(self, painter: QPainter, rect: QRect, piece: Piece) -> None:
        pass


class SVGPieceRenderer(PieceRenderingStrategy):
    def __init__(self, piece_size: int = 60):
        self.piece_size = piece_size

    def render(self, painter: QPainter, rect: QRect, piece: Piece) -> None:
        color = QColor("white") if piece.team == Team.WHITE else QColor("black")
        outline_color = QColor("black") if piece.team == Team.WHITE else QColor("white")

        self._draw_piece_symbol(painter, rect, piece.piece_type, color, outline_color)

    def _draw_piece_symbol(
        self,
        painter: QPainter,
        rect: QRect,
        piece_type: PieceType,
        color: QColor,
        outline_color: QColor,
    ) -> None:
        painter.save()
        painter.translate(rect.center())
        painter.scale(rect.width() / self.piece_size, rect.height() / self.piece_size)

        outline_pen = QPen(outline_color, 2)
        painter.setPen(outline_pen)
        painter.setBrush(QBrush(color))

        match piece_type:
            case PieceType.PAWN:
                self._draw_pawn(painter)
            case PieceType.ROOK:
                self._draw_rook(painter)
            case PieceType.KNIGHT:
                self._draw_knight(painter)
            case PieceType.BISHOP:
                self._draw_bishop(painter)
            case PieceType.QUEEN:
                self._draw_queen(painter)
            case PieceType.KING:
                self._draw_king(painter)

        painter.restore()

    def _draw_pawn(self, painter: QPainter) -> None:
        painter.drawEllipse(-8, 0, 16, 20)
        painter.drawRect(-12, 18, 24, 8)

    def _draw_rook(self, painter: QPainter) -> None:
        painter.drawRect(-10, 0, 20, 24)
        painter.drawRect(-15, -4, 8, 4)
        painter.drawRect(7, -4, 8, 4)
        painter.drawRect(-2, -4, 4, 4)

    def _draw_knight(self, painter: QPainter) -> None:
        points = [
            (-10, 24),
            (-10, 8),
            (-5, 0),
            (0, -6),
            (8, -4),
            (12, 8),
            (8, 24),
            (-10, 24),
        ]
        polygon_points = QPolygon([QPoint(x, y) for x, y in points])
        painter.drawPolygon(polygon_points)

    def _draw_bishop(self, painter: QPainter) -> None:
        painter.drawEllipse(-6, -8, 12, 12)
        painter.drawEllipse(-8, 2, 16, 12)
        painter.drawRect(-12, 14, 24, 10)

    def _draw_queen(self, painter: QPainter) -> None:
        for i in range(5):
            x = -10 + i * 5
            painter.drawEllipse(x - 2, -8, 4, 4)
        points = [
            (-12, 0),
            (-5, 0),
            (-3, 8),
            (0, 2),
            (3, 8),
            (5, 0),
            (12, 0),
            (8, 24),
            (-8, 24),
        ]
        polygon_points = QPolygon([QPoint(x, y) for x, y in points])
        painter.drawPolygon(polygon_points)

    def _draw_king(self, painter: QPainter) -> None:
        painter.drawRect(-10, 0, 20, 20)
        painter.drawRect(-6, -6, 2, 10)
        painter.drawRect(4, -6, 2, 10)
        painter.drawRect(-1, -8, 2, 12)
        painter.drawEllipse(-3, -12, 6, 6)
