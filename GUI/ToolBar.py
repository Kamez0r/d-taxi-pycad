from PyQt6.QtCore import QSize, pyqtSignal, Qt
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QToolBar
import CFG


class ToolBar(QToolBar):

    def __init__(self):
        super().__init__()
        self.setIconSize(QSize(CFG.TOOLBAR_ICON_SIZE_W, CFG.TOOLBAR_ICON_SIZE_H))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.action_new = pyqtSignal()
        button_new = QAction(QIcon(CFG.ICON_ADD), "New", self)
        button_new.setStatusTip("Create Blank Project")
        button_new.setCheckable(False)
        self.addAction(button_new)

        self.action_project_settings = QAction(QIcon(CFG.ICON_WRENCH), "Project Settings", self)
        self.action_project_settings.setStatusTip("Project Settings")
        self.action_project_settings.setCheckable(False)
        self.addAction(self.action_project_settings)