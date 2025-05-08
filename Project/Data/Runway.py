import math

from Project.GeoCoordinate import GeoCoordinate


class Runway:

    magnetic_variation: float
    threshold1: GeoCoordinate
    threshold2: GeoCoordinate

    def init_from_threshold_threshold(self, threshold1: GeoCoordinate, threshold2: GeoCoordinate,
                                      magnetic_variation: float = 0.0):
        self.magnetic_variation = magnetic_variation

        self.threshold1 = threshold1
        self.threshold2 = threshold2

    def get_course(self) -> float:
        """
        :returns "True" runway course from threshold 1 to threshold 2
        :return:
        """
        return GeoCoordinate.get_true_course_delta_coord(self.threshold1, self.threshold2)

    def get_inverse_course(self) -> float:
        """
        :returns "True" runway course from threshold 2 to threshold 1
        :return:
        """
        return (self.get_course() + 180 ) % 360

    def get_course_magnetic(self) -> float:
        return GeoCoordinate.apply_magnetic_variation(self.get_course(), self.magnetic_variation)

    def get_inverse_course_magnetic(self) -> float:
        return GeoCoordinate.apply_magnetic_variation(self.get_inverse_course(), self.magnetic_variation)

    def get_runway_designator(self) -> int:
        """
        Returns the runway designator based on magnetic course from threshold 1 to 2.
        Rounded to nearest 10°, divided by 10.
        """
        mag_course = self.get_course_magnetic()
        return int(round(mag_course / 10.0)) % 36 or 36  # 0 becomes 36

    def get_inverse_runway_designator(self) -> int:
        """
        Returns the inverse runway designator (threshold 2 to 1).
        """
        inverse_mag_course = self.get_inverse_course_magnetic()
        return int(round(inverse_mag_course / 10.0)) % 36 or 36
