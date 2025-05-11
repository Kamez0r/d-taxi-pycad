import json

from PyQt6.QtGui import QIcon, QShortcut, QKeySequence
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QFileDialog
import CFG
from GUI.MainCanvas import MainCanvas
from GUI.MenuBar import MenuBar
from GUI.StatusBar import StatusBar
from GUI.ToolBar import ToolBar
from Project import Project


class MainWindow(QMainWindow):
    project: Project

    def __init__(self):
        super().__init__()
        self.setWindowTitle(CFG.WINDOW_TITLE)
        self.resize(CFG.WINDOW_WIDTH, CFG.WINDOW_HEIGHT)
        self.setWindowIcon(QIcon(CFG.DEFAULT_ICON))

        self.viewport = MainCanvas()
        self.setCentralWidget(self.viewport)

        self.menu_bar = MenuBar()
        self.setMenuBar(self.menu_bar)

        self.tool_bar = ToolBar()
        self.addToolBar(self.tool_bar)

        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)

        # Connect File Menu Actions
        self.menu_bar.new_project.triggered.connect(self.new_project)
        self.menu_bar.open_action.triggered.connect(self.open_file)
        self.menu_bar.save_action.triggered.connect(self.save_project)
        self.menu_bar.save_as_action.triggered.connect(self.save_as_project)
        self.menu_bar.quit_action.triggered.connect(self.close)

        QShortcut(QKeySequence.StandardKey.Save, self).activated.connect(self.save_project)
        QShortcut(QKeySequence.StandardKey.New, self).activated.connect(self.new_project)


        # Connect Toolbar Actions
        # self.tool_bar.action_new.triggered.connect(self.new_file)

        self._create_new_project()

    def _create_new_project(self):
        self.project = Project(self.viewport)
        print("Blank project created")

    def new_project(self):
        prompt = "Are you sure you want to create new project?\nUnsaved progress will be lost"

        response = QMessageBox.question(self, "New Project", prompt)
        if response == QMessageBox.StandardButton.Yes:
            self._create_new_project()
            self.status_bar.showMessage("New project created", 2000)

    def open_file(self):
        self.status_bar.showMessage("Opening file...", 2000)
        self.status_bar.show_progress(25)  # Simulate progress
        # Add real logic here
        self.status_bar.show_progress(100)

    def save_as_project(self):

        file_name, filter = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save As Project",
            directory="./untitled.json",
            filter="(*.json)",
            initialFilter="(*.json)"
        )

        if not file_name:
            return False

        print(file_name)
        self.project.project_path = file_name
        return self.save_project()

    def save_project(self):
        if not self.project.project_path:
            return self.save_as_project()

        save_path = self.project.project_path

        self.status_bar.showMessage("Saving...", 2000)
        self.status_bar.show_progress(10)  # Simulate progress
        file = open("test_blank.json", "w")
        self.status_bar.show_progress(25)
        file.write(json.dumps(self.project.get_serialized(), indent=4))
        self.status_bar.show_progress(90)
        file.close()
        self.status_bar.hide_progress()
        return True

    def exit_application(self):
        print("Exit application triggered")
        self.close()
