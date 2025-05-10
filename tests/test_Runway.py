import unittest
from Project.Data import Runway
from Project.GeoCoordinate import GeoCoordinate


class TestRunway(unittest.TestCase):

    def create_coord(self, lat, lon):
        return GeoCoordinate.from_tuple((lat,lon))

    def test_init_from_threshold_course_len_from_existing(self):
        test_cases = [
            {
                "name": "LROP 08L/26R",
                "threshold1": (44.5767, 26.08417),
                "true_course": 84.0,
                "mag_course": 79.0,
                "length_m": 3500.0,
                "mag_var": 5.0,
                "expected": ("8L", "26R"),
                "direction_suffix": "L"
            },
            {
                "name": "LRTR 11/29",
                "threshold1": (45.815111, 21.316811),
                "true_course": 109.0,
                "mag_course": 105.0,
                "length_m": 3500.0,
                "mag_var": 4.0,
                "expected": ("11", "29")
            },
            {
                "name": "LRBV 03/21",
                "threshold1": (45.696019, 25.512837),
                "true_course": 36.0,
                "mag_course": 30.0,
                "length_m": 2820.0,
                "mag_var": 6.0,
                "expected": ("3", "21")
            },
        ]

        for case in test_cases:
            with self.subTest(case=case["name"]):
                t1 = self.create_coord(*case["threshold1"])
                if "direction_suffix" in case:
                    runway = Runway(case["mag_var"], direction_suffix=case["direction_suffix"])
                else:
                    runway = Runway(case["mag_var"])
                runway.init_from_threshold_course_len(t1, case["true_course"], case["length_m"])

                self.assertEqual(runway.get_designator(), case["expected"][0])
                self.assertEqual(runway.get_inverse_designator(), case["expected"][1])

                self.assertAlmostEqual(runway.get_course(), case["true_course"], places=3)
                self.assertAlmostEqual(runway.get_course_magnetic(), case["mag_course"], places=3)

    def test_real_world_runway_designators(self):
        test_cases = [
            {
                "name": "LROP 08L/26R",
                "threshold1": (44.5767, 26.08417),
                "threshold2": (44.58, 26.1278),
                "mag_var": 5.0,
                "expected": (8, 26)
            },
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

                runway = Runway(case["mag_var"])
                runway.init_from_threshold_threshold(t1, t2)

                self.assertEqual(runway.get_intended_designator(), case["expected"][0])
                self.assertEqual(runway.get_inverse_intended_designator(), case["expected"][1])


if __name__ == '__main__':
    unittest.main()
