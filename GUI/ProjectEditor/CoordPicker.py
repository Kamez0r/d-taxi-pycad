from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QIcon, QFont
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel

import CFG
from GUI.ProjectEditor.PEWidgets import PELabel, PELineEdit
from Project import GeoCoordinate


class CoordPicker(QVBoxLayout):

    location_longitude: PELabel
    location_latitude: PELabel
    layout_location: QHBoxLayout | QHBoxLayout
    location_label: QLabel
    location_label_text: str
    location: GeoCoordinate

    def __init__(self):
        super().__init__()
        self.location = GeoCoordinate()

        self.location_label_text = ""

        self.generate_fields()

    def setLocation(self, location: GeoCoordinate):
        self.location = location

    def setLocationLabel(self, location_label_text: str):
        self.location_label_text = location_label_text
        self.location_label.setText(self.location_label_text)

    def generate_fields(self):
        # Third Row
        self.location_label = PELabel(self.location_label_text)
        self.addWidget(self.location_label)

        self.layout_location = QHBoxLayout()
        self.location_latitude = PELabel("Latitude: --.----")
        self.layout_location.addWidget(self.location_latitude)
        self.location_longitude = PELabel("Longitude: --.----")
        self.layout_location.addWidget(self.location_longitude)
        self.addLayout(self.layout_location)

        self.fourth_H_layout = QHBoxLayout()
        # LAT DEG
        self.lat_dms_deg_label = PELabel("LAT DEG:")
        self.lat_dms_deg_input = PELineEdit()
        self.lat_dms_deg_input.setValidator(QIntValidator(-90, 90))

        # LAT MIN
        self.lat_dms_min_label = PELabel("MIN:")
        self.lat_dms_min_input = PELineEdit()
        self.lat_dms_min_input.setValidator(QIntValidator(0, 59))

        # LAT SEC
        self.lat_dms_sec_label = PELabel("SEC:")
        self.lat_dms_sec_input = PELineEdit()
        self.lat_dms_sec_input.setValidator(QDoubleValidator(0, 60, 32))

        # LON DEG
        self.lon_dms_deg_label = PELabel("/LON DEG:")
        self.lon_dms_deg_input = PELineEdit()
        self.lon_dms_deg_input.setValidator(QIntValidator(-180, 180))

        # LON MIN
        self.lon_dms_min_label = PELabel("MIN:")
        self.lon_dms_min_input = PELineEdit()
        self.lon_dms_min_input.setValidator(QIntValidator(0, 59))

        # LON SEC
        self.lon_dms_sec_label = PELabel("SEC:")
        self.lon_dms_sec_input = PELineEdit()
        self.lon_dms_sec_input.setValidator(QDoubleValidator(0, 60, 32))

        # Button
        self.set_location_from_dms = QPushButton("Set")
        self.set_location_from_dms.setIcon(QIcon(CFG.ICON_CALCULATOR))
        self.set_location_from_dms.setIconSize(QSize(32, 32))
        self.set_location_from_dms.setFont(QFont("Consolas", 16))

        # Add widgets to layout
        self.fourth_H_layout.addWidget(self.lat_dms_deg_label)
        self.fourth_H_layout.addWidget(self.lat_dms_deg_input)
        self.fourth_H_layout.addWidget(self.lat_dms_min_label)
        self.fourth_H_layout.addWidget(self.lat_dms_min_input)
        self.fourth_H_layout.addWidget(self.lat_dms_sec_label)
        self.fourth_H_layout.addWidget(self.lat_dms_sec_input)

        self.fourth_H_layout.addWidget(self.lon_dms_deg_label)
        self.fourth_H_layout.addWidget(self.lon_dms_deg_input)
        self.fourth_H_layout.addWidget(self.lon_dms_min_label)
        self.fourth_H_layout.addWidget(self.lon_dms_min_input)
        self.fourth_H_layout.addWidget(self.lon_dms_sec_label)
        self.fourth_H_layout.addWidget(self.lon_dms_sec_input)

        self.fourth_H_layout.addWidget(self.set_location_from_dms)
        self.addLayout(self.fourth_H_layout)

        self.fifth_H_layout = QHBoxLayout()

        # LAT
        self.lat_label = PELabel("LAT:")
        self.lat_input = PELineEdit()
        self.lat_input.setValidator(QDoubleValidator(-90.0, 90.0, 32))

        # LON
        self.lon_label = PELabel("LON:")
        self.lon_input = PELineEdit()
        self.lon_input.setValidator(QDoubleValidator(-180.0, 180.0, 32))

        # Button
        self.set_location_from_dec = QPushButton("Set")
        self.set_location_from_dec.setIcon(QIcon(CFG.ICON_CALCULATOR))
        self.set_location_from_dec.setIconSize(QSize(32, 32))
        self.set_location_from_dec.setFont(QFont("Consolas", 16))

        # Add widgets to layout
        self.fifth_H_layout.addWidget(self.lat_label)
        self.fifth_H_layout.addWidget(self.lat_input)
        self.fifth_H_layout.addWidget(self.lon_label)
        self.fifth_H_layout.addWidget(self.lon_input)
        self.fifth_H_layout.addWidget(self.set_location_from_dec)

        # Add to main layout
        self.addLayout(self.fifth_H_layout)