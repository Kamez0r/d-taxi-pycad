import json
import sys

from PyQt6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QApplication

from Project import Project, GeoCoordinate
from Project.Data import Runway, Taxiway


class DemoWindow(QMainWindow):

    def _create_demo_project(self):
        demo_project = Project(self.viewport)

        demo_project.airport_data.aerodrome_icao = "LROP"
        demo_project.airport_data.aerodrome_name = "Aeroportul International HENRI COANDA, Bucuresti"
        demo_project.airport_data.magnetic_variation = 5
        # demo_project.airport_data.aerodrome_location = GeoCoordinate.from_tuple((44.571111,26.085))
        demo_project.airport_data.aerodrome_location = GeoCoordinate.from_tuple((
            GeoCoordinate.DMStoDEC(44, 34, 16),
            GeoCoordinate.DMStoDEC(26, 5, 6),
        ))

        rwy_north = Runway(
            magnetic_variation=demo_project.airport_data.magnetic_variation,
            direction_suffix="L"
        )
        rwy_north.init_from_threshold_magnetic_len(
            threshold1=GeoCoordinate.from_tuple((
                GeoCoordinate.DMStoDEC(44, 34, 36),
                GeoCoordinate.DMStoDEC(26, 5, 3)
            )),
            course_magnetic=79,
            rwy_len_meters=3499
        )
        demo_project.airport_data.add_runway(rwy_north)

        rwy_south = Runway(
            magnetic_variation=demo_project.airport_data.magnetic_variation,
            direction_suffix="R"
        )
        rwy_south.init_from_threshold_magnetic_len(
            threshold1=GeoCoordinate.from_tuple((
                GeoCoordinate.DMStoDEC(44, 33, 53),
                GeoCoordinate.DMStoDEC(26, 4, 36)
            )),
            course_magnetic=79,
            rwy_len_meters=3501
        )
        demo_project.airport_data.add_runway(rwy_south)

        twyQ = Taxiway("Q")
        twyN = Taxiway("N")
        twyW = Taxiway("W")
        twyV = Taxiway("V")
        demo_project.airport_data.add_taxiway(twyQ)
        demo_project.airport_data.add_taxiway(twyN)
        demo_project.airport_data.add_taxiway(twyW)
        demo_project.airport_data.add_taxiway(twyV)

        twyG = Taxiway("G")
        twyC = Taxiway("C")
        twyD = Taxiway("D")
        demo_project.airport_data.add_taxiway(twyG)
        demo_project.airport_data.add_taxiway(twyC)
        demo_project.airport_data.add_taxiway(twyD)

        demo_project.airport_data.add_conflict_point_runway_taxiway(rwy_north, twyN)
        demo_project.airport_data.add_conflict_point_runway_taxiway(rwy_north, twyV)
        demo_project.airport_data.add_conflict_point_runway_taxiway(rwy_north, twyW)
        demo_project.airport_data.add_conflict_point_runway_taxiway(rwy_north, twyQ)

        demo_project.airport_data.add_conflict_point_runway_taxiway(rwy_south, twyG)
        demo_project.airport_data.add_conflict_point_runway_taxiway(rwy_south, twyD)

        demo_project.airport_data.add_conflict_point_taxiway_taxiway(twyN, twyQ)
        demo_project.airport_data.add_conflict_point_taxiway_taxiway(twyQ, twyW)
        demo_project.airport_data.add_conflict_point_taxiway_taxiway(twyQ, twyV)

        demo_project.airport_data.add_conflict_point_taxiway_taxiway(twyN, twyG)
        demo_project.airport_data.add_conflict_point_taxiway_taxiway(twyN, twyC)
        demo_project.airport_data.add_conflict_point_taxiway_taxiway(twyG, twyC)
        demo_project.airport_data.add_conflict_point_taxiway_taxiway(twyC, twyD)

        return demo_project

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo Window")
        self.resize(1000, 1000)
        self.viewport = DemoCanvas()
        self.setCentralWidget(self.viewport)

        demo_project = self._create_demo_project()


        file = open("demo_project.json", "w")
        file.write(json.dumps(demo_project.get_serialized(), indent=4))


class DemoCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene())


def main():
    app = QApplication(sys.argv)

    window = DemoWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()