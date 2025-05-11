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

        self.items: list[Drawable] = []
        self.working_path: str | None = None
        self.airport_data = Airport(
            aerodrome_icao="",
            aerodrome_name="",
            aerodrome_location=GeoCoordinate.from_tuple((0,0)),
            magnetic_variation=0,
        )


    def load_from_file(self, path_to_file: str):
        raise NotImplementedError("Loading from file not implemented yet")

    def get_serialized(self) -> dict:
        items_serialized = []
        for item in self.items:
            items_serialized.append(item.get_serialized())

        return {
            "date_saved": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            # other project data like project name, airport, location, IDK
            "airport_data": self.airport_data.get_serialized(),
            "items": items_serialized
        }

    def save(self):
        if not self.working_path:
            raise ValueError("No working path set. Use save_as(path) first.")
        with open(self.working_path, "w", encoding="utf-8") as file:
            json.dump(self.get_serialized(), file, default=str)

    def save_as(self, path_to_file: str):
        self.working_path = path_to_file
        self.save()

    def export_to(self, path_to_file: str, settings:dict):
        raise NotImplementedError("Method not implemented")
