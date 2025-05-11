from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow
import CFG
from GUI.MainCanvas import MainCanvas
from GUI.MenuBar import MenuBar
from GUI.StatusBar import StatusBar
from GUI.ToolBar import ToolBar


class MainWindow(QMainWindow):
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
        self.menu_bar.new_action.triggered.connect(self.new_file)
        self.menu_bar.open_action.triggered.connect(self.open_file)
        self.menu_bar.save_action.triggered.connect(self.save_file)
        self.menu_bar.quit_action.triggered.connect(self.close)

        # Connect Toolbar Actions
        # self.tool_bar.action_new.triggered.connect(self.new_file)

    def new_file(self):
        self.status_bar.showMessage("New file created", 2000)

    def open_file(self):
        self.status_bar.showMessage("Opening file...", 2000)
        self.status_bar.show_progress(25)  # Simulate progress
        # Add real logic here
        self.status_bar.show_progress(100)

    def save_file(self):
        self.status_bar.showMessage("Saving...", 2000)
        self.status_bar.show_progress(50)  # Simulate progress
        # Add real logic here
        self.status_bar.hide_progress()

    def exit_application(self):
        print("Exit application triggered")
        self.close()
