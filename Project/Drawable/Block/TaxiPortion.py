from typing import override

from PyQt6.QtCore import QRectF, QLineF
from PyQt6.QtWidgets import QGraphicsItem

from Project.Drawable.Block import BlockLogical
from Project.Drawable.Block.BlockPhysical import BlockPhysical


class TaxiPortion(BlockPhysical):

    width: float
    height: float
    penWidth: float

    def __init__(self, serialized_data: dict):
        super().__init__(serialized_data)
        self.load_from_serialized(serialized_data)

        self.header_text = "Taxiway Portion"
        self.title_text = "TWY [TAXIWAY_LABEL]"
        self.footer_text = "Portion Index: []\nUUID: []"

    def draw(self):
        pass

    def get_serialized(self):
        return {}

    def load_from_serialized(self, serialized: dict):
        pass

    def paint_graphics(self, painter, option, widget, bounds: QRectF):
        painter.drawLine(QLineF(
            bounds.x() + bounds.width() * 0.1,
            bounds.y() + bounds.height() * 0.5,
            bounds.x() + bounds.width() - bounds.width() * 0.1,
            bounds.y() + bounds.height() * 0.5
        ))