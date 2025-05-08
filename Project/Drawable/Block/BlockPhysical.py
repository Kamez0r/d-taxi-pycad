from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QGraphicsItem

from Project.Drawable.Block.Block import Block


class BlockPhysical(Block):

    def __init__(self, serialized_data: dict):
        super().__init__(serialized_data)
        self.penColor = QColor(0, 0, 255)