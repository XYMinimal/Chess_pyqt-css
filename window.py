import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from PyQt6.QtGui import QPixmap
from troop_list import *


class Root(QWidget):
    def __init__(self, parent=None):
        super(Root, self).__init__(parent)
        self.resize(950, 950)
        self.boardI = QPixmap(r"assets\board.png")
        self.board = QLabel(self)
        self.board.setPixmap(self.boardI)
        self.board.resize(self.boardI.width(),
                          self.boardI.height())
        pawn1 = Pawn(self, "orange")
        pawn1.draw()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Root()
    ex.show()
    sys.exit(app.exec())
