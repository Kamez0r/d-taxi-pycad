from PyQt6.QtCore import QRectF, QLineF

from Project.Data.Taxiway import Taxiway
from Project.Drawable.Block.BlockPhysical import BlockPhysical


class TaxiPortion(BlockPhysical):

    parent_taxiway:Taxiway


    def __init__(self, serialized_data: dict):
        super().__init__()
        self.load_from_serialized(serialized_data)

        self.header_text = "Taxiway Portion"
        self.title_text = "TWY " + str(self.parent_taxiway.get_designator())
        self.footer_text = "Portion Index: []\nUUID: []"

    def get_serialized(self):

        return {
            "parent_taxiway" : self.parent_taxiway.get_serialized()
        }

    @staticmethod
    def check_valid_data(serialized_data: dict):
        if not "parent_taxiway" in serialized_data:
            return False

        if not Taxiway.check_valid_data(serialized_data["parent_taxiway"]):
            return False

        return True

    def load_from_serialized(self, serialized: dict):
        if not self.check_valid_data(serialized):
            raise TypeError("Invalid serialized data")

        self.parent_taxiway = Taxiway(serialized["parent_taxiway"]["designator"])

    def get_taxiway(self):
        return self.parent_taxiway

    def paint_graphics(self, painter, option, widget, bounds: QRectF):
        painter.drawLine(QLineF(
            bounds.x() + bounds.width() * 0.1,
            bounds.y() + bounds.height() * 0.5,
            bounds.x() + bounds.width() - bounds.width() * 0.1,
            bounds.y() + bounds.height() * 0.5
        ))