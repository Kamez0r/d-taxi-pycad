from PyQt6.QtGui import QColor

from Project.Drawable.Block.Block import Block


class BlockLogical(Block):

    def __init__(self):
        super().__init__()
        self.penColor = QColor(255, 0, 255)