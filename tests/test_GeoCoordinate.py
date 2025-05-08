import unittest
from Project.GeoCoordinate import GeoCoordinate  # Adjust path as needed


class TestGeoCoordinate(unittest.TestCase):

    def test_latitude_longitude_setters_getters(self):
        geo = GeoCoordinate()
        geo.setLatitude(45.1234)
        geo.setLongitude(23.5678)

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


if __name__ == '__main__':
    unittest.main()
