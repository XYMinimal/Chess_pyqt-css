from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel
import sys

from src.domain.board import Board
from src.domain.entities import Position, Team
from src.domain.game_state import GameState, GameStatus
from src.presentation.controller import ChessController


class ChessBoardWidget(QWidget):
    BOARD_SIZE = 8
    MIN_SQUARE_SIZE = 20
    MAX_SQUARE_SIZE = 150
    DEFAULT_SQUARE_SIZE = 60

    def __init__(self, controller: ChessController):
        super().__init__()
        self._controller = controller
        self._square_size = self.DEFAULT_SQUARE_SIZE
        self._selected_piece = None
        self._valid_moves = []
        
        self._update_widget_size()
        self.setWindowTitle("Chess")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _update_widget_size(self) -> None:
        board_dimension = self.BOARD_SIZE * self._square_size
        self.resize(board_dimension, board_dimension)

    def sizeHint(self) -> QSize:
        board_dimension = self.BOARD_SIZE * self._square_size
        return QSize(board_dimension, board_dimension)

    def resizeEvent(self, event):
        widget_size = min(event.size().width(), event.size().height())
        self._square_size = max(
            self.MIN_SQUARE_SIZE,
            min(self.MAX_SQUARE_SIZE, widget_size // self.BOARD_SIZE)
        )
        super().resizeEvent(event)
        self.update()

    def mousePressEvent(self, event):
        if self._controller.is_game_over():
            return
        
        col = event.position().x() // self._square_size
        row = event.position().y() // self._square_size
        
        if not (0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE):
            return
        
        position = Position(int(row), int(col))
        
        if self._selected_piece and position in self._valid_moves:
            self._execute_move(position)
            return
        
        piece = self._controller.get_piece_at(position)
        if piece and piece.team == self._controller.get_current_turn():
            self._select_piece(piece)
        else:
            self._deselect_piece()

    def _select_piece(self, piece) -> None:
        self._selected_piece = piece
        self._valid_moves = self._controller.get_valid_moves(piece)
        self.update()

    def _deselect_piece(self) -> None:
        self._selected_piece = None
        self._valid_moves = []
        self.update()

    def _execute_move(self, target: Position) -> None:
        moved_piece, game_status = self._controller.move_piece(self._selected_piece, target)
        if moved_piece:
            self._selected_piece = None
            self._valid_moves = []
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self._draw_board(painter)
        self._draw_valid_moves(painter)
        self._draw_pieces(painter)
        self._draw_selection_highlight(painter)

    def _draw_board(self, painter: QPainter) -> None:
        light_color = QColor(240, 217, 181)
        dark_color = QColor(181, 136, 99)

        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                rect = QRect(
                    col * self._square_size,
                    row * self._square_size,
                    self._square_size,
                    self._square_size,
                )
                is_light = (row + col) % 2 == 0
                color = light_color if is_light else dark_color
                painter.fillRect(rect, color)
                painter.drawRect(rect)

    def _draw_valid_moves(self, painter: QPainter) -> None:
        if not self._valid_moves:
            return
        
        highlight_color = QColor(76, 175, 80, 100)
        painter.fillRect(painter.viewport(), Qt.GlobalColor.transparent)
        
        for move_position in self._valid_moves:
            rect = QRect(
                move_position.col * self._square_size,
                move_position.row * self._square_size,
                self._square_size,
                self._square_size,
            )
            painter.fillRect(rect, highlight_color)

    def _draw_selection_highlight(self, painter: QPainter) -> None:
        if not self._selected_piece:
            return
        
        selection_color = QColor(255, 235, 59)
        rect = QRect(
            self._selected_piece.position.col * self._square_size,
            self._selected_piece.position.row * self._square_size,
            self._square_size,
            self._square_size,
        )
        painter.fillRect(rect, QColor(255, 235, 59, 100))
        painter.drawRect(rect)

    def _draw_pieces(self, painter: QPainter) -> None:
        pieces = self._controller.get_pieces_for_rendering()
        renderer = self._controller.get_piece_renderer()

        for piece in pieces:
            rect = QRect(
                piece.position.col * self._square_size,
                piece.position.row * self._square_size,
                self._square_size,
                self._square_size,
            )
            renderer.render(painter, rect, piece)


class ChessApplication(QWidget):
    def __init__(self):
        super().__init__()
        self._board = Board()
        self._game_state = GameState()
        self._controller = ChessController(self._board, self._game_state)
        self._controller.initialize_game()

        self._chess_widget = ChessBoardWidget(self._controller)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self._status_label = QLabel()
        self._update_status_label()
        
        layout.addWidget(self._status_label)
        layout.addWidget(self._chess_widget)
        
        board_height = self._chess_widget.height()
        self.resize(self._chess_widget.width(), board_height + 50)
        self.setWindowTitle("Chess Game")
        
        self._chess_widget.update()

    def _update_status_label(self) -> None:
        if self._controller.is_game_over():
            winner = self._controller.get_winner()
            winner_name = "White" if winner == Team.WHITE else "Black"
            self._status_label.setText(f"{winner_name} wins! Game Over")
            self._status_label.setStyleSheet("color: green; font-weight: bold; font-size: 14px;")
        else:
            current_turn = self._controller.get_current_turn()
            turn_name = "White" if current_turn == Team.WHITE else "Black"
            self._status_label.setText(f"Current Turn: {turn_name}")
            self._status_label.setStyleSheet("color: black; font-size: 12px;")

    def paintEvent(self, event):
        self._update_status_label()
        super().paintEvent(event)
