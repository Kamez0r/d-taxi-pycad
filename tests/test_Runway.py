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
                "threshold1": (45.8117, 21.3333),
                "threshold2": (45.8028, 21.4373),
                "mag_var": 4.0,
                "expected": (11, 29)
            },
            {
                "name": "KJFK 04L/22R",
                "threshold1": (40.6398, -73.7789),
                "threshold2": (40.6516, -73.7514),
                "mag_var": -13.0,
                "expected": (4, 22)
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
