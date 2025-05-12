from PyQt6.QtWidgets import QVBoxLayout

from GUI.ProjectEditor.CRUDLayout import CRUDLayout
from Project import Project, GeoCoordinate


class StandList(CRUDLayout):
    project: Project
    def __init__(self, project: Project):
        super().__init__()
        self.project = project

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

        self.set_able_view(True)
        self.set_able_edit(True)
        self.set_able_delete(True)

        self.add_value({
            "designator": "131",
            "position": GeoCoordinate.from_tuple((13,31)),
        })

    def action_called(self, row_index, action_column_key):
        print("CALL FOR", row_index, action_column_key)

        if action_column_key == "action_create":
            self.add_value({
                "designator": "ABC",
                "position": GeoCoordinate.from_tuple((0,0)),
            })
