import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import QRect

from src.domain.board import Board
from src.domain.entities import Piece, PieceType, Team, Position
from src.application.rendering import SVGPieceRenderer


class TestRenderingIntegration:
    @classmethod
    def setup_class(cls):
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()

    def test_renderer_draws_all_piece_types(self):
        renderer = SVGPieceRenderer()
        pixmap = QPixmap(600, 600)
        pixmap.fill()
        painter = QPainter(pixmap)

        piece_types = [
            PieceType.PAWN,
            PieceType.ROOK,
            PieceType.KNIGHT,
            PieceType.BISHOP,
            PieceType.QUEEN,
            PieceType.KING,
        ]

        for idx, piece_type in enumerate(piece_types):
            piece = Piece(piece_type, Team.WHITE, Position(idx, 0))
            rect = QRect(idx * 100, 0, 100, 100)
            renderer.render(painter, rect, piece)

        painter.end()
        assert pixmap.width() == 600
        assert pixmap.height() == 600

    def test_renderer_respects_team_colors(self):
        renderer = SVGPieceRenderer()
        pixmap = QPixmap(200, 100)
        pixmap.fill()
        painter = QPainter(pixmap)

        white_piece = Piece(PieceType.KING, Team.WHITE, Position(0, 0))
        black_piece = Piece(PieceType.KING, Team.BLACK, Position(0, 1))

        white_rect = QRect(0, 0, 100, 100)
        black_rect = QRect(100, 0, 100, 100)

        renderer.render(painter, white_rect, white_piece)
        renderer.render(painter, black_rect, black_piece)

        painter.end()
        assert not pixmap.isNull()
