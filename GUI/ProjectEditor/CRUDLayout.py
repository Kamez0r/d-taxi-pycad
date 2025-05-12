from PyQt6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QTableWidget, QTableWidgetItem

from GUI.ProjectEditor.PEWidgets import PELabel, PELineEdit


class CRUDLayout(QVBoxLayout):
    layout_title: PELabel

    able_view = False
    able_edit = False
    able_delete = False

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

        self.table.setRowCount(0)
        self.table.setColumnCount(0)

        self.addWidget(self.table)

    def action_called(self, action_column_key):
        pass

    def add_column(self, column_key: str, column_title: str, column_type: str, default_value=None):
        if column_key in self.column_keys:
            raise ValueError("Column name already exists")

        if column_type not in self.known_column_types:
            raise TypeError("Column type is not valid")

        self.column_keys.append(column_key)
        self.column_titles.append(column_title)
        self.column_types.append(column_type)
        self.column_defaults.append(default_value)

        self.table.setColumnCount(len(self.column_keys))
        self.table.setHorizontalHeaderLabels(self.column_titles)

    def add_value(self, one_row_values: dict):
        new_row = []
        for column_key in self.column_keys:
            if not column_key in one_row_values:
                column_index = self.column_keys.index(column_key)
                one_row_values[column_key] = self.column_defaults[column_index]
            new_row.append(one_row_values[column_key])
            self.table.setItem(0, 0, QTableWidgetItem(text="ASD"))

        self.values.append(new_row)
        # self.table.setRowCount(len(self.values))

        for column_key in one_row_values:
            if not column_key in self.column_keys:
                continue
            column_value = one_row_values[column_key]



    def add_values(self, value_list: list):
        for value in value_list:
            self.add_value(value)

    def remove_column(self, column_key: str):
        index = self.column_keys.index(column_key)
        del self.column_keys[index]
        del self.column_titles[index]
        del self.column_types[index]

        self.table.setColumnCount(len(self.column_keys))
        self.table.setHorizontalHeaderLabels(self.column_titles)

    def set_able_view(self, new_state):
        if new_state != self.able_view:
            if new_state:
                self.add_column(
                    column_key="action_view",
                    column_title="View",
                    column_type="ACTION",
                    default_value=None
                )
            else:
                self.remove_column(column_key="action_view")
        self.able_view = new_state

    def set_able_edit(self, new_state):
        if new_state != self.able_edit:
            if new_state:
                self.add_column(
                    column_key="action_edit",
                    column_title="Edit",
                    column_type="ACTION",
                    default_value=None
                )
            else:
                self.remove_column(column_key="action_edit")
        self.able_edit = new_state

    def set_able_delete(self, new_state):
        if new_state != self.able_delete:
            if new_state:
                self.add_column(
                    column_key="action_delete",
                    column_title="Delete",
                    column_type="ACTION",
                    default_value=None
                )
            else:
                self.remove_column(column_key="action_delete")
        self.able_delete = new_state
