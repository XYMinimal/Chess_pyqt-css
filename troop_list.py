from troop import Troop
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

class Pawn(Troop):
    def __init__(self, window, team):
        super(Pawn, self).__init__(window, team)
        self.icon = "pawn"
        pass


class Rook(Troop):
    def __init__(self, window, team):
        super(Rook, self).__init__(window, team)
        self.icon = "rook"
        pass


class Bishop(Troop):
    def __init__(self, window, team):
        super(Bishop, self).__init__(window, team)
        self.icon = "bishop"
        pass


class Knight(Troop):
    def __init__(self, window, team):
        super(Knight, self).__init__(window, team)
        self.icon = "knight"
        pass


class King(Troop):
    def __init__(self, window, team):
        super(King, self).__init__(window, team)
        self.icon = "king"
        pass


class Queen(Troop):
    def __init__(self, window, team):
        super(Queen, self).__init__(window, team)
        self.icon = "queen"
        pass


