from PyQt6.QtCore import QRectF, QLineF

from Project.Drawable.Block.BlockPhysical import BlockPhysical


class RunwayPortion(BlockPhysical):

    

    def __init__(self, serialized_data: dict):
        super().__init__()
        self.load_from_serialized(serialized_data)

        self.header_text = "Runway Portion"
        self.title_text = "RWY [LABEL]"
        self.footer_text = "Portion Index: []\nUUID: []"

    def get_serialized(self) -> dict:
        return {}

    def load_from_serialized(self, serialized_data: dict):
        pass

    def paint_graphics(self, painter, option, widget, bounds: QRectF):
        painter.drawLine(QLineF(
            bounds.x() + bounds.width() * 0.1,
            bounds.y() + bounds.height() * 0.3,
            bounds.x() + bounds.width() - bounds.width() * 0.1,
            bounds.y() + bounds.height() * 0.3
        ))

        painter.drawLine(QLineF(
            bounds.x() + bounds.width() * 0.1,
            bounds.y() + bounds.height() * 0.7,
            bounds.x() + bounds.width() - bounds.width() * 0.1,
            bounds.y() + bounds.height() * 0.7
        ))