import sys


from PyQt6.QtWidgets import QMainWindow, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem

from Project.Drawable.Block import TaxiPortion, RunwayPortion


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
        new_item = TaxiPortion({})
        new_item.setPos(800, 0)
        self.scene().addItem(new_item)


        new_new_item = TaxiPortion({})
        new_new_item.setPos(0, 800)
        self.scene().addItem(new_new_item)

        new_new_item = RunwayPortion({})
        new_new_item.setPos(800, 800)
        self.scene().addItem(new_new_item)


def main():
    app = QApplication(sys.argv)

    demo_item = TaxiPortion({})
    demo_item.setPos(0,0)

    window = DemoWindow(demo_item)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
