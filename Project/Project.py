import datetime
import json

from PyQt6.QtWidgets import QGraphicsView

from .Data import Airport
from .Drawable import *
from .GeoCoordinate import GeoCoordinate


class Project:

    project_path: str | None
    airport_data: Airport

    def __init__(self, canvas: QGraphicsView, project_path: str = None):
        self.canvas: QGraphicsView = canvas
        self.project_path = project_path

        self.drawables: list[Drawable] = []

        self.airport_data = Airport(
            aerodrome_icao="",
            aerodrome_name="",
            aerodrome_location=GeoCoordinate.from_tuple((0,0)),
            magnetic_variation=0,
        )


    @staticmethod
    def check_valid_data(sdata: dict):
        if not "date_saved" in sdata:
            return False

        if not "airport_data" in sdata:
            return False

        if not Airport.check_valid_data(sdata["airport_data"]):
            return False

        if not "drawables" in sdata:
            return False

        return True

    def load_from_serialized_data(self, sdata: dict):
        if not self.check_valid_data(sdata=sdata):
            raise TypeError("Invalid data provided")

        self.airport_data.init_from_serialized(sdata["airport_data"])
        # Load drawable items...
        # raise NotImplementedError("Loading from file not implemented yet")

    def get_serialized(self) -> dict:
        drawables_serialized = []
        for drawables in self.drawables:
            drawables_serialized.append(drawables.get_serialized())

        return {
            "date_saved": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            # other project data like project name, airport, location, IDK
            "airport_data": self.airport_data.get_serialized(),
            "drawables": drawables_serialized
        }

    def export_to(self, path_to_file: str, settings:dict):
        raise NotImplementedError("Method not implemented")
