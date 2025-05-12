from PyQt6.QtWidgets import QVBoxLayout

from GUI.ProjectEditor.CRUDLayout import CRUDLayout
from Project import Project, GeoCoordinate


class RunwayList(CRUDLayout):
    project: Project

    def __init__(self, project: Project):
        super().__init__()
        self.project = project

        self.add_column(
            column_key="direction_modifier",
            column_title="Main Name Offset",
            column_type="INTEGER",
            default_value=0
        )

        self.add_column(
            column_key="direction_suffix",
            column_title="Main Name Side(L/C/R)",
            column_type="STRING",
            default_value=""
        )

        self.add_column(
            column_key="threshold1",
            column_title="Threshold",
            column_type="COORD",
            default_value=GeoCoordinate.from_tuple((0,0))
        )

        self.add_column(
            column_key="threshold2",
            column_title="Opposite Threshold",
            column_type="COORD",
            default_value=GeoCoordinate.from_tuple((90,90))
        )

        self.set_able_view(False)
        self.set_able_edit(False)
        self.set_able_delete(True)

    def action_called(self, row_index, action_column_key):
        if action_column_key == "action_create":
            self.add_value({})
        elif action_column_key == "action_delete":
            self.remove_value(row_index)
        else:
            print("action not recognized")