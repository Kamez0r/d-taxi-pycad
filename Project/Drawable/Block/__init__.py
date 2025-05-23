from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar, QMenu


class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()

        # File Menu
        file_menu = QMenu("File", self)
        self.addMenu(file_menu)

        self.new_action = QAction("New", self)
        self.open_action = QAction("Open...", self)
        self.save_action = QAction("Save", self)
        self.save_as_action = QAction("Save As", self)
        self.quit_action = QAction("Quit", self)

        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)

        # Project Menu
        project_menu = QMenu("Project", self)
        self.addMenu(project_menu)

        self.project_settings_action = QAction("Settings", self)
        self.project_export_action = QAction("Export", self)

        project_menu.addAction(self.project_settings_action)
        project_menu.addAction(self.project_export_action)

        # Action Menu
        action_menu = QMenu("Action", self)
        self.addMenu(action_menu)

        self.action_settings_action = QAction("Settings", self)
        action_menu.addAction(self.action_settings_action)

        # New Block Physical submenu
        new_block_physical_menu = action_menu.addMenu("New Block Physical Menu")
        self.runway_portion_action = QAction("Runway Portion", self)
        self.runway_intersection_action = QAction("Runway Intersection", self)
        self.taxi_portion_action = QAction("Taxi Portion", self)
        self.taxi_intersection_action = QAction("Taxi Intersection", self)
        self.holding_point_action = QAction("Holding Point", self)
        self.parking_stand_action = QAction("Parking Stand", self)

        new_block_physical_menu.addActions([
            self.runway_portion_action,
            self.runway_intersection_action,
            self.taxi_portion_action,
            self.taxi_intersection_action,
            self.holding_point_action,
            self.parking_stand_action
        ])

        # new_block_physical_action = action_menu.addMenu(new_block_physical_menu)
        action_menu.addMenu(new_block_physical_menu)
        # new_block_physical_action.setText("New Block Physical")

        # New Block Logical submenu
        new_block_logical_menu = QMenu("New Block Logical", self)
        self.not_implemented_action = QAction("NOT_IMPLEMENTED", self)
        self.not_implemented_action.setEnabled(False)
        new_block_logical_menu.addAction(self.not_implemented_action)

        new_block_logical_action = action_menu.addMenu(new_block_logical_menu)
        # new_block_logical_action.setText("New Block Logical")

        # Remaining actions
        action_menu.addSeparator()
        self.new_link_logical_action = QAction("New Link Logical", self)
        self.new_link_physical_action = QAction("New Link Physical", self)
        action_menu.addAction(self.new_link_logical_action)
        action_menu.addAction(self.new_link_physical_action)
        action_menu.addSeparator()

        self.delete_action = QAction("Delete", self)
        action_menu.addAction(self.delete_action)

