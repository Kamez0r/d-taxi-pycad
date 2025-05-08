from PyQt6.QtGui import QColor

from Project.Drawable.Block.Block import Block


class BlockPhysical(Block):

    def __init__(self):
        super().__init__()
        self.penColor = QColor(0, 0, 255)