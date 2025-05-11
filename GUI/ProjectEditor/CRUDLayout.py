from PyQt6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QTableWidget

from GUI.ProjectEditor.PEWidgets import PELabel, PELineEdit


class CRUDLayout(QVBoxLayout):
    layout_title: PELabel

    column_keys: list[str]
    column_titles: list[str]
    column_types: list[str]
    column_defaults: list
    values: list[list]

    known_column_types = [
        "ID",
        "STRING",
        "INTEGER",
        "FLOAT",
        "COORD",
        "ACTION"
    ]

    def __init__(self):
        super().__init__()

        self.column_keys = []
        self.column_titles = []
        self.column_types = []
        self.column_defaults = []

        self.layout_title = PELabel("<Layout Title>")


        self.addWidget(self.layout_title)

        self.search_bar = PELineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.addWidget(self.search_bar)

        self.table = QTableWidget()
        self.table.setMinimumHeight(300)
        self.addWidget(self.table)

    def add_column(self, column_key: str, column_title: str, column_type: str, default_value=None):
        if column_key in self.column_keys:
            raise ValueError("Column name already exists")

        if column_type not in self.known_column_types:
            raise TypeError("Column type is not valid")

        self.column_keys.append(column_key)
        self.column_titles.append(column_title)
        self.column_types.append(column_type)
        self.column_defaults.append(default_value)

