from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QFont, QDoubleValidator
from PyQt6.QtWidgets import *

import CFG
from Project import Project


class ProjectEditorWindow(QMainWindow):
    project: Project
    def __init__(self, parent, project: Project):
        super().__init__(parent)

        self.setWindowTitle(CFG.PROJECT_EDITOR_WINDOW_TITLE)
        self.setWindowIcon(QIcon(CFG.ICON_WRENCH))
        self.resize(QSize(CFG.PROJECT_EDITOR_WIDTH, CFG.PROJECT_EDITOR_HEIGHT))

        self.project = project

        self.generate_fields()
        self.populate_fields()

        self.show()

    def generate_fields(self):


        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 30, 20, 30)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.general_font = QFont("Consolas", 16)

        # First Row
        self.first_H_layout = QHBoxLayout()
        self.first_H_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.first_row_font = QFont("Consolas", 20)
        self.icao_label = QLabel("ICAO:")
        self.icao_label.setFont(self.first_row_font)
        self.first_H_layout.addWidget(self.icao_label)

        self.icao_input = QLineEdit()
        self.icao_input.setMaxLength(4)
        self.icao_input.setFixedWidth(84)
        self.icao_input.setFont(self.first_row_font)
        self.first_H_layout.addWidget(self.icao_input)

        self.first_H_layout.addSpacing(30)

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

        self.aerodrome_name_label = QLabel("Aerodrome Name:")
        self.aerodrome_name_label.setFont(self.general_font)
        self.main_layout.addWidget(self.aerodrome_name_label)

        self.aerodrome_name_input = QLineEdit()
        self.aerodrome_name_input.setFont(self.general_font)
        self.main_layout.addWidget(self.aerodrome_name_input)

        # Third Row
        self.aerodrome_latitude = QLabel("Latitude: 12.3")
        self.aerodrome_longitude = QLabel("26.3")

        self.third_H_layout = QHBoxLayout()


        self.main_layout.addLayout(self.third_H_layout)


        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def populate_fields(self):
        pass