from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QFont, QDoubleValidator
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QWidget, QScrollArea, QPushButton

import CFG
from GUI.ProjectEditor.CoordPicker import CoordPicker
from GUI.ProjectEditor.PEWidgets import PELabel, PELineEdit
from GUI.ProjectEditor.RunwayList import RunwayList
from GUI.ProjectEditor.StandList import StandList
from GUI.ProjectEditor.TaxiwayList import TaxiwayList
from Project import Project
from Project.Data import Stand


class ProjectEditorWindow(QMainWindow):
    update_button: QPushButton
    runway_list_layout: RunwayList
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

    def allow_update(self):
        self.update_button.setEnabled(True)

    def force_update(self):
        self.update_button.setEnabled(False)

        self.project.airport_data.aerodrome_icao = self.icao_input.text()
        self.project.airport_data.aerodrome_name = self.aerodrome_name_input.text()

        if self.mag_var_input.text() != "":
            self.project.airport_data.magnetic_variation = float(self.mag_var_input.text())
        self.project.airport_data.aerodrome_location = self.aerodrome_location_layout.location

        self.force_update_runways()
        self.force_update_taxiways()
        self.force_update_stands()

    def force_update_runways(self):
        pass

    def force_update_taxiways(self):
        pass

    def force_update_stands(self):
        table_map = {}
        json_map = {}

        index_of_designator = self.stand_list_layout.column_keys.index("designator")
        index_of_position = self.stand_list_layout.column_keys.index("position")
        for row in self.stand_list_layout.values:
            designator = (row[index_of_designator])
            table_map[designator] = row

        for stand in self.project.airport_data.stands:
            json_map[stand.get_designator()] = stand

        # Check creation
        for designator in table_map:
            if designator not in json_map:
                pass # creation found
                self.project.airport_data.add_stand(Stand(
                    designator=table_map[designator][index_of_designator],
                    position=table_map[designator][index_of_position],
                ))
        # Check deletion
        for designator in json_map:
            if designator not in table_map:
                # self.project.airport_data.stands[]
                pass


    def generate_fields(self):


        self.main_layout = QVBoxLayout()


        self.main_layout.setContentsMargins(20, 30, 20, 30)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.update_button = QPushButton("Update")
        self.update_button.setFont(QFont("Consolas", 36))
        self.update_button.setEnabled(False)
        self.update_button.clicked.connect(self.force_update)
        self.main_layout.addWidget(self.update_button)

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
        self.icao_input.textChanged.connect(self.allow_update)
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
        self.mag_var_input.textChanged.connect(self.allow_update)
        self.first_H_layout.addWidget(self.mag_var_input)

        self.main_layout.addLayout(self.first_H_layout)

        # Seconds Row

        self.aerodrome_name_label = PELabel("Aerodrome Name:")
        self.main_layout.addWidget(self.aerodrome_name_label)

        self.aerodrome_name_input = PELineEdit()
        self.aerodrome_name_input.textChanged.connect(self.allow_update)
        self.main_layout.addWidget(self.aerodrome_name_input)

        self.generate_fields_location()

        self.stand_list_layout = StandList(self.project)
        self.stand_list_layout.layout_title.setText("Stand List")
        self.stand_list_layout.dataset_changed.connect(self.allow_update)
        self.main_layout.addLayout(self.stand_list_layout)

        self.runway_list_layout = RunwayList(self.project)
        self.runway_list_layout.layout_title.setText("Runway List")
        self.runway_list_layout.dataset_changed.connect(self.allow_update)
        self.main_layout.addLayout(self.runway_list_layout)

        self.taxiway_list_layout = TaxiwayList(self.project)
        self.taxiway_list_layout.layout_title.setText("Taxiway List")
        self.taxiway_list_layout.dataset_changed.connect(self.allow_update)
        self.main_layout.addLayout(self.taxiway_list_layout)


        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.main_widget.setMaximumWidth(CFG.PROJECT_EDITOR_WIDTH)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.main_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumSize(QSize(CFG.PROJECT_EDITOR_WIDTH, CFG.PROJECT_EDITOR_HEIGHT))
        self.setCentralWidget(self.scroll_area)

    def generate_fields_location(self):
        # Third Row
        self.aerodrome_location_layout = CoordPicker()
        self.aerodrome_location_layout.setLocationLabel("Aerodrome Location:")
        self.aerodrome_location_layout.location_changed.connect(self.allow_update)
        self.main_layout.addLayout(self.aerodrome_location_layout)

    def populate_fields(self):
        self.icao_input.setText(self.project.airport_data.aerodrome_icao)
        self.mag_var_input.setText(str(self.project.airport_data.magnetic_variation))
        self.aerodrome_name_input.setText(self.project.airport_data.aerodrome_name)
        self.aerodrome_location_layout.setLocation(self.project.airport_data.aerodrome_location)
