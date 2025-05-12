from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QWidget

from GUI.ProjectEditor.CoordPicker import CoordPicker
from Project import GeoCoordinate


class CoordPickerWindow(QMainWindow):

    on_value_set = pyqtSignal(GeoCoordinate)

    def __init__(self, parent = None):
        super().__init__(parent)

        self.main_layout = CoordPicker()

        self.main_layout.location_changed.connect(self.trigger_signal)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.show()

    def setLocation(self, location:GeoCoordinate):
        self.main_layout.setLocation(location)

    def trigger_signal(self):
        self.on_value_set.emit(self.main_layout.location)
