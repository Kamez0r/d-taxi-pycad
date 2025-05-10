import unittest
from math import isclose
from Project.GeoCoordinate import GeoCoordinate  # adjust path as needed


class TestGeoCoordinate(unittest.TestCase):

    def test_latitude_longitude_setters_getters(self):
        geo = GeoCoordinate.from_tuple((45.1234, 23.5678))

        self.assertAlmostEqual(geo.getLatitude(), 45.1234)
        self.assertAlmostEqual(geo.getLongitude(), 23.5678)

    def test_DECtoDMS_positive(self):
        deg, mnt, sec = GeoCoordinate.DECtoDMS(45.7625)
        self.assertEqual(deg, 45)
        self.assertEqual(mnt, 45)
        self.assertAlmostEqual(sec, 45.0, places=2)

    def test_DECtoDMS_negative(self):
        deg, mnt, sec = GeoCoordinate.DECtoDMS(-45.7625)
        self.assertEqual(deg, -45)
        self.assertEqual(mnt, -45)
        self.assertAlmostEqual(sec, -45.0, places=2)

    def test_DMStoDEC_positive(self):
        dec = GeoCoordinate.DMStoDEC(45, 45, 45.0)
        self.assertAlmostEqual(dec, 45.7625, places=4)

    def test_DMStoDEC_negative(self):
        dec = GeoCoordinate.DMStoDEC(-45, 45, 45.0)
        self.assertAlmostEqual(dec, -45.7625, places=4)

    def test_round_trip_conversion(self):
        original = -12.345678
        d, m, s = GeoCoordinate.DECtoDMS(original)
        result = GeoCoordinate.DMStoDEC(d, m, s)
        self.assertAlmostEqual(result, original, places=6)

    def test_true_course_delta_coord(self):
        # From roughly north to south
        c1 = GeoCoordinate.from_tuple((48, 2)) # near Paris
        c2 = GeoCoordinate.from_tuple((47, 2))
        course = GeoCoordinate.get_true_course_delta_coord(c1, c2)
        self.assertTrue(170 <= course <= 190)  # Roughly south

    def test_true_course_diagonal(self):
        c1 = GeoCoordinate()
        c2 = GeoCoordinate()
        c1.setLatitude(45.0)
        c1.setLongitude(5.0)

        c2.setLatitude(46.0)
        c2.setLongitude(6.0)

        course = GeoCoordinate.get_true_course_delta_coord(c1, c2)
        self.assertTrue(30 <= course <= 70)  # NE-ish

    def test_apply_magnetic_variation_east(self):
        true_course = 90  # East
        mag_var = 10      # East variation = subtract
        magnetic_course = GeoCoordinate.apply_magnetic_variation(true_course, mag_var)
        self.assertEqual(magnetic_course, 80)

    def test_apply_magnetic_variation_wraparound(self):
        true_course = 5
        mag_var = 10
        magnetic_course = GeoCoordinate.apply_magnetic_variation(true_course, mag_var)
        self.assertEqual(magnetic_course, 355)


if __name__ == '__main__':
    unittest.main()
