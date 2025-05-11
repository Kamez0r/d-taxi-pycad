from PyQt6.QtWidgets import QVBoxLayout

from GUI.ProjectEditor.CRUDLayout import CRUDLayout
from Project import Project


class TaxiwayList(CRUDLayout):
    project: Project
    def __init__(self, project: Project):
        super().__init__()
        self.project = project