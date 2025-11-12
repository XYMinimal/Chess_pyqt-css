import sys
from PyQt6.QtWidgets import QApplication

from src.domain.board import Board
from src.domain.game_state import GameState
from src.presentation.controller import ChessController
from src.presentation.ui import ChessApplication


def main():
    app = QApplication(sys.argv)
    window = ChessApplication()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
