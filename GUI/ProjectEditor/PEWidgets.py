from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QLineEdit


class PELabel(QLabel):

    def __init__(self, text:str=None):
        super().__init__(text)
        self.setFont(QFont("Consolas", 16))


class PELineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Consolas", 16))
