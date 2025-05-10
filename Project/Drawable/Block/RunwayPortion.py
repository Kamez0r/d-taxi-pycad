from PyQt6.QtCore import QRectF, QLineF

from Project.Data.Runway import Runway
from Project.Drawable.Block.BlockPhysical import BlockPhysical
from Project.GeoCoordinate import GeoCoordinate


class RunwayPortion(BlockPhysical):

    parent_runway: Runway

    def __init__(self, serialized_data: dict):
        super().__init__()
        self.load_from_serialized(serialized_data)

        self.header_text = "Runway Portion"
        self.title_text = "RWY " + str(self.parent_runway.get_designator()) + "/" + str(self.parent_runway.get_inverse_designator())
        self.footer_text = ""

    def get_serialized(self) -> dict:
        return {
            "parent_runway": self.parent_runway.get_serialized(),
        }

    @staticmethod
    def check_valid_data(serialized_data: dict):
        if not "parent_runway" in serialized_data:
            return False

        if not Runway.check_valid_data(serialized_data["parent_runway"]):
            return False

        return True

    def load_from_serialized(self, sdata: dict):
        #sdata alias for serialized_data
        if not self.check_valid_data(sdata):
            raise ValueError("Invalid runway data provided")

        # Init Parent Runway
        self.parent_runway = Runway(sdata["parent_runway"]["magnetic_variation"])
        self.parent_runway.init_from_threshold_threshold(
            GeoCoordinate.from_tuple(sdata["parent_runway"]["threshold1"]),
            GeoCoordinate.from_tuple(sdata["parent_runway"]["threshold2"]),
        )

    def get_runway(self):
        return self.parent_runway

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