from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene


class MainCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
