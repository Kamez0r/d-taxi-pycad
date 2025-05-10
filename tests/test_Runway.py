import unittest
from Project.Data import Runway
from Project.GeoCoordinate import GeoCoordinate


class TestRunway(unittest.TestCase):

    def create_coord(self, lat, lon):
        coord = GeoCoordinate()
        coord.setLatitude(lat)
        coord.setLongitude(lon)
        return coord

    def test_real_world_runway_designators(self):
        test_cases = [
            {
                "name": "LROP 08L/26R",
                "threshold1": (44.5767, 26.08417),
                "threshold2": (44.58, 26.1278),
                "mag_var": 5.0,
                "expected": (8, 26)
            },

            ## TODO use correct data bellow
            {
                "name": "LRTR 11/29",
                "threshold1": (45.815111, 21.316811),
                "threshold2": (45.804688, 21.358363),
                "mag_var": 4.0,
                "expected": (11, 29)
            },
            {
                "name": "LRBV 04/22",
                "threshold1": (45.696019, 25.512837),
                "threshold2": (45.716409, 25.534182),
                "mag_var": 6.0,
                "expected": (3, 21)
            },
        ]

        for case in test_cases:
            with self.subTest(case=case["name"]):
                t1 = self.create_coord(*case["threshold1"])
                t2 = self.create_coord(*case["threshold2"])

                runway = Runway.Runway()
                runway.init_from_threshold_threshold(t1, t2, case["mag_var"])

                self.assertEqual(runway.get_runway_designator(), case["expected"][0])
                self.assertEqual(runway.get_inverse_runway_designator(), case["expected"][1])


if __name__ == '__main__':
    unittest.main()
