from PyQt6.QtWidgets import QStatusBar, QProgressBar


class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        self.addPermanentWidget(self.progress_bar)

    def show_progress(self, value: int):
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(value)

    def hide_progress(self):
        self.progress_bar.setVisible(False)
