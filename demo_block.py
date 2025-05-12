import sys


from PyQt6.QtWidgets import QMainWindow, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem

from Project import GeoCoordinate
from Project.Data import Taxiway, Runway
from Project.Drawable.Block import TaxiPortion, RunwayPortion


class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo Window")
        self.resize(600, 600)
        self.viewport = DemoCanvas()
        self.setCentralWidget(self.viewport)

class DemoCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))


        twyB = Taxiway("B")

        new_item = TaxiPortion({
            "parent_taxiway": twyB.get_serialized()
        })
        # new_item = TaxiPortion()
        new_item.setPos(800, 0)
        self.scene().addItem(new_item)


        new_new_item = TaxiPortion({
            "parent_taxiway": twyB.get_serialized()
        })
        new_new_item.setPos(0, 800)
        self.scene().addItem(new_new_item)
        rw = Runway(magnetic_variation=5)
        rw.init_from_threshold_threshold(GeoCoordinate.from_tuple((0,0)), GeoCoordinate.from_tuple((1,1)))

        print (rw.get_serialized())

        new_new_item = RunwayPortion({
            "parent_runway": rw.get_serialized()
        })
        new_new_item.setPos(800, 800)
        self.scene().addItem(new_new_item)


def main():
    app = QApplication(sys.argv)

    window = DemoWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
