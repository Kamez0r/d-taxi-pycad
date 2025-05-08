from PyQt6.QtGui import QColor

from Project.Drawable.Block.Block import Block


class BlockLogical(Block):

    def __init__(self, serialized_data: dict):
        super().__init__(serialized_data)
        self.penColor = QColor(255, 0, 255)