from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel


class Troop:
    def __init__(self, window, team):
        self.frame = None
        self.window = window
        self.image = None
        self.icon = None
        self.team = team

    def verifyMove(self, move):
        pass

    def draw(self):
        self.image = QPixmap(f"assets\\{self.team}\\{self.icon}")
        self.frame = QLabel(self.window)
        self.frame.setPixmap(self.image)
        self.frame.resize(self.image.width(),
                          self.image.height())
