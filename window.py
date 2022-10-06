import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit


class Root(QWidget):
    def __init__(self, parent=None):
        super(Root, self).__init__(parent)
        self.resize(1920, 1080)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Root()
    ex.show()
    sys.exit(app.exec())
