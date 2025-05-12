import json

from PyQt6.QtGui import QIcon, QShortcut, QKeySequence
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QFileDialog
import CFG
from GUI.MainCanvas import MainCanvas
from GUI.MenuBar import MenuBar
from GUI.ProjectEditor.ProjectEditorWindow import ProjectEditorWindow
from GUI.StatusBar import StatusBar
from GUI.ToolBar import ToolBar
from Project import Project


class MainWindow(QMainWindow):
    project: Project

    project_editor_open: bool = False

    project_editor_window: ProjectEditorWindow

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
        self.menu_bar.open_action.triggered.connect(self.open_project)
        self.menu_bar.save_action.triggered.connect(self.save_project)
        self.menu_bar.save_as_action.triggered.connect(self.save_as_project)
        self.menu_bar.quit_action.triggered.connect(self.close)

        self.tool_bar.action_project_settings.triggered.connect(self.open_project_editor)
        self.menu_bar.project_settings_action.triggered.connect(self.open_project_editor)

        QShortcut(QKeySequence.StandardKey.Save, self).activated.connect(self.save_project)
        QShortcut(QKeySequence.StandardKey.Open, self).activated.connect(self.open_project)
        QShortcut(QKeySequence.StandardKey.New, self).activated.connect(self.new_project)

        # Connect Toolbar Actions
        # self.tool_bar.action_new.triggered.connect(self.new_file)

        self._create_new_project()

    def open_project_editor(self):
        if self.project_editor_open:
            return

        ProjectEditorWindow(self, self.project)

    def _create_new_project(self):
        self.project = Project(self.viewport)
        print("Blank project created")

    def new_project(self):
        prompt = "Are you sure you want to create new project?\nUnsaved progress will be lost"

        response = QMessageBox.question(self, "New Project", prompt)
        if response == QMessageBox.StandardButton.Yes:
            self._create_new_project()
            self.status_bar.showMessage("New project created", 2000)


    def _open_project_from_path(self, path_to_file: str):

        self.project = Project(self.viewport)

        self.status_bar.showMessage("Opening file...", 2000)
        self.status_bar.show_progress(25)  # Simulate progress

        file = open(path_to_file)
        serialized_data = json.load(file)
        self.project.load_from_serialized_data(serialized_data)
        self.status_bar.show_progress(90)
        self.project.project_path = path_to_file
        self.status_bar.show_progress(100)
        return True

    def _open_project(self):
        file_name, filter = QFileDialog.getOpenFileName(
            parent= self,
            caption="Browse to project file",
            filter="(*.json)",
            initialFilter="(*.json)"
        )

        if not file_name:
            return False

        return self._open_project_from_path(file_name)

    def open_project(self):
        prompt = "Are you sure you want to open another project?\nUnsaved progress will be lost"

        response = QMessageBox.question(self, "Open Project", prompt)
        if response == QMessageBox.StandardButton.Yes:
            self._open_project()
            self.status_bar.showMessage("Project loaded", 2000)


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

        self.status_bar.showMessage("Saving...", 2000)
        self.status_bar.show_progress(10)  # Simulate progress
        file = open(self.project.project_path, "w")
        self.status_bar.show_progress(25)
        file.write(json.dumps(self.project.get_serialized(), indent=4))
        self.status_bar.show_progress(90)
        file.close()
        self.status_bar.hide_progress()
        return True

    def exit_application(self):
        print("Exit application triggered")
        self.close()
