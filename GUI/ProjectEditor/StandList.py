from PyQt6.QtWidgets import QVBoxLayout

from GUI.ProjectEditor.CRUDLayout import CRUDLayout
from Project import Project, GeoCoordinate


class StandList(CRUDLayout):
    project: Project
    def __init__(self, project: Project):
        super().__init__()
        self.project = project

        self.add_column(
            column_key="id",
            column_title="#",
            column_type="ID",
            default_value=None
        )

        self.add_column(
            column_key="designator",
            column_title="Designator",
            column_type="STRING",
            default_value=None
        )

        self.add_column(
            column_key="position",
            column_title="Location",
            column_type="COORD",
            default_value=GeoCoordinate.from_tuple((0,0))
        )
