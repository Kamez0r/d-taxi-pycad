from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QFont, QDoubleValidator, QIntValidator
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QWidget, QScrollArea

import CFG
from GUI.ProjectEditor.CoordPicker import CoordPicker
from GUI.ProjectEditor.PEWidgets import PELabel, PELineEdit
from GUI.ProjectEditor.RunwayList import RunwayList
from GUI.ProjectEditor.StandList import StandList
from GUI.ProjectEditor.TaxiwayList import TaxiwayList
from Project import Project, GeoCoordinate


class ProjectEditorWindow(QMainWindow):
    scroll_area: QScrollArea
    aerodrome_location_label: QLabel | QLabel
    main_widget: QWidget
    third_H_layout: QHBoxLayout | QHBoxLayout
    aerodrome_longitude: QLabel | QLabel
    aerodrome_latitude: QLabel | QLabel
    aerodrome_name_input: QLineEdit | QLineEdit
    aerodrome_name_label: QLabel | QLabel
    mag_var_validator: QDoubleValidator | QDoubleValidator
    mag_var_input: QLineEdit | QLineEdit
    mag_var_label: QLabel | QLabel
    icao_input: QLineEdit
    icao_label: QLabel
    first_row_font: QFont | QFont
    first_H_layout: QHBoxLayout
    project: Project
    main_layout: QVBoxLayout
    
    def __init__(self, parent, project: Project):
        super().__init__(parent)

        self.setWindowTitle(CFG.PROJECT_EDITOR_WINDOW_TITLE)
        self.setWindowIcon(QIcon(CFG.ICON_WRENCH))
        # self.resize(QSize(CFG.PROJECT_EDITOR_WIDTH, CFG.PROJECT_EDITOR_HEIGHT))
        # self.setFixedSize(QSize(CFG.PROJECT_EDITOR_WIDTH, CFG.PROJECT_EDITOR_HEIGHT))

        self.project = project

        self.generate_fields()
        self.populate_fields()

        self.show()

    def generate_fields(self):


        self.main_layout = QVBoxLayout()


        self.main_layout.setContentsMargins(20, 30, 20, 30)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # First Row
        self.first_H_layout = QHBoxLayout()
        self.first_H_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.first_row_font = QFont("Consolas", 24)
        self.icao_label = QLabel("ICAO:")
        self.icao_label.setFont(self.first_row_font)
        self.first_H_layout.addWidget(self.icao_label)

        self.icao_input = QLineEdit()
        self.icao_input.setMaxLength(4)
        self.icao_input.setFixedWidth(96)
        self.icao_input.setFont(self.first_row_font)
        self.first_H_layout.addWidget(self.icao_input)

        self.first_H_layout.addSpacing(40)

        self.mag_var_label = QLabel("MAG/VAR(DEG):")
        self.mag_var_label.setFont(self.first_row_font)
        self.mag_var_label.setToolTip("Current magnetic variation (accounting yearly). East is positive, West is negative")
        self.first_H_layout.addWidget(self.mag_var_label)

        self.mag_var_input = QLineEdit()
        self.mag_var_validator = QDoubleValidator()
        self.mag_var_validator.setDecimals(2)
        self.mag_var_input.setValidator(self.mag_var_validator)
        self.mag_var_input.setFont(self.first_row_font)
        self.mag_var_input.setFixedWidth(84)
        self.first_H_layout.addWidget(self.mag_var_input)

        self.main_layout.addLayout(self.first_H_layout)

        # Seconds Row

        self.aerodrome_name_label = PELabel("Aerodrome Name:")
        self.main_layout.addWidget(self.aerodrome_name_label)

        self.aerodrome_name_input = PELineEdit()
        self.main_layout.addWidget(self.aerodrome_name_input)

        self.generate_fields_location()

        self.runway_list_layout = RunwayList(self.project)
        self.runway_list_layout.layout_title.setText("Runway List")

        self.taxiway_list_layout = TaxiwayList(self.project)
        self.taxiway_list_layout.layout_title.setText("Taxiway List")

        self.stand_list_layout = StandList(self.project)
        self.stand_list_layout.layout_title.setText("Stand List")

        self.main_layout.addLayout(self.runway_list_layout)
        self.main_layout.addLayout(self.taxiway_list_layout)
        self.main_layout.addLayout(self.stand_list_layout)


        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.main_widget.setFixedWidth(CFG.PROJECT_EDITOR_WIDTH)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.main_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedSize(QSize(CFG.PROJECT_EDITOR_WIDTH, CFG.PROJECT_EDITOR_HEIGHT))
        self.setCentralWidget(self.scroll_area)

    def generate_fields_location(self):
        # Third Row
        self.aerodrome_location_layout = CoordPicker()
        self.aerodrome_location_layout.setLocationLabel("Aerodrome Location:")
        self.main_layout.addLayout(self.aerodrome_location_layout)

    def populate_fields(self):
        pass