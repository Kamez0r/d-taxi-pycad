import sys


from PyQt6.QtWidgets import QMainWindow, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem

from Project.Drawable.Block import TaxiPortion


class DemoWindow(QMainWindow):
    def __init__(self, demo_item:QGraphicsItem):
        super().__init__()
        self.setWindowTitle("Demo Window")
        self.resize(600, 600)
        self.viewport = DemoCanvas(demo_item)
        self.setCentralWidget(self.viewport)

class DemoCanvas(QGraphicsView):
    def __init__(self, demo_item:QGraphicsItem):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.scene().addItem(demo_item)


def main():
    app = QApplication(sys.argv)

    demo_item = TaxiPortion({})
    demo_item.setPos(0,0)

    window = DemoWindow(demo_item)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
