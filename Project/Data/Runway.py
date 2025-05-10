import math

from Project.GeoCoordinate import GeoCoordinate

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Project.Data.Taxiway import Taxiway

class Runway:

    # Used to distinguish between L C R ...
    direction_modifier: int
    direction_suffix: str

    magnetic_variation: float
    threshold1: GeoCoordinate
    threshold2: GeoCoordinate

    intersecting_runways: list["Runway"]
    access_to_taxiways: list["Taxiway"]

    def __init__(self, magnetic_variation:float, direction_modifier:int = 0, direction_suffix:str=""):
        self.direction_modifier = direction_modifier
        self.direction_suffix = direction_suffix

        self.magnetic_variation = magnetic_variation
        self.intersecting_runways = []
        self.access_to_taxiways = []


    @staticmethod
    def from_serialized_data(sdata:dict) -> "Runway":
        if not Runway.check_valid_data(sdata):
            raise TypeError("Invalid data provided")

        new_instance = Runway(sdata["magnetic_variation"])
        new_instance.init_from_threshold_threshold(
            GeoCoordinate.from_tuple(sdata["threshold1"]),
            GeoCoordinate.from_tuple(sdata["threshold2"]),
        )
        return new_instance

    def get_serialized(self):
        rws = []
        for rw in self.intersecting_runways:
            rws.append(rw.get_designator())

        tws = []
        for tw in self.access_to_taxiways:
            tws.append(tw.get_designator())

        return {
            "__comment_designator": self.get_designator(),
            "__comment_opposite": self.get_inverse_designator(),
            "direction_modifier": self.direction_modifier,
            "direction_suffix": self.direction_suffix,
            "magnetic_variation": self.magnetic_variation,
            "threshold1": self.threshold1.get_serialized(),
            "threshold2": self.threshold2.get_serialized(),
            "intersecting_runways": rws,
            "access_to_taxiways": tws
        }

    @staticmethod
    def check_valid_data(serialized_data: dict):
        if not "direction_modifier" in serialized_data:
            return False

        if not type(serialized_data["direction_modifier"]) == int:
            return False

        if not "direction_suffix" in serialized_data:
            return False

        if not type(serialized_data["direction_suffix"]) == str:
            return False

        if not "magnetic_variation" in serialized_data:
            return False

        if type(serialized_data["magnetic_variation"]) is not float:
            return False

        if not "threshold1" in serialized_data:
            return False

        if not GeoCoordinate.check_valid_data(serialized_data["threshold1"]):
            return False

        if not "threshold2" in serialized_data:
            return False

        if not GeoCoordinate.check_valid_data(serialized_data["threshold2"]):
            return False

        if not "intersecting_runways" in serialized_data:
            return False

        if not type(serialized_data["intersecting_runways"]) is list:
            return False

        if not "access_to_taxiways" in serialized_data:
            return False

        if not type(serialized_data["access_to_taxiways"]) is list:
            return False

        return True


    def init_from_threshold_threshold(self, threshold1: GeoCoordinate, threshold2: GeoCoordinate):
        self.threshold1 = threshold1
        self.threshold2 = threshold2

    def init_from_threshold_magnetic_len(self, threshold1: GeoCoordinate, course_magnetic:float, rwy_len_meters:float):
        return self.init_from_threshold_course_len(
            threshold1,
            GeoCoordinate.remove_magnetic_variation(course_magnetic, self.magnetic_variation),
            rwy_len_meters
        )

    def init_from_threshold_course_len(self, threshold1: GeoCoordinate, course: float, rwy_len_meters: float):
        self.threshold1 = threshold1

        # Convert course to radians
        bearing_rad = math.radians(course)

        # Angular distance (radians) over the Earth's surface
        delta = rwy_len_meters / GeoCoordinate.EarthRadiusMeters

        lat1 = math.radians(threshold1.getLatitude())
        lon1 = math.radians(threshold1.getLongitude())

        lat2 = math.asin(
            math.sin(lat1) * math.cos(delta) +
            math.cos(lat1) * math.sin(delta) * math.cos(bearing_rad)
        )

        lon2 = lon1 + math.atan2(
            math.sin(bearing_rad) * math.sin(delta) * math.cos(lat1),
            math.cos(delta) - math.sin(lat1) * math.sin(lat2)
        )

        # Normalize lon2 to [-180, 180]
        lon2 = (lon2 + 3 * math.pi) % (2 * math.pi) - math.pi

        self.threshold2 = GeoCoordinate()
        self.threshold2.setLatitude(math.degrees(lat2))
        self.threshold2.setLongitude(math.degrees(lon2))

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

    def get_designator(self) -> str:
        return str(self.get_intended_designator() + self.direction_modifier) + self.direction_suffix

    def get_intended_designator(self) -> int:
        """
        Returns the runway designator based on magnetic course from threshold 1 to 2.
        Rounded to nearest 10°, divided by 10.
        """
        mag_course = self.get_course_magnetic()
        return int(round(mag_course / 10.0)) % 36 or 36  # 0 becomes 36

    def get_inverse_direction_suffix(self) -> str:
        if self.direction_suffix == "L":
            return "R"
        elif self.direction_suffix == "R":
            return "L"
        else:
            return self.direction_suffix

    def get_inverse_designator(self) -> str:
        return str(self.get_inverse_intended_designator() - self.direction_modifier) + self.get_inverse_direction_suffix()

    def get_inverse_intended_designator(self) -> int:
        """
        Returns the inverse runway designator (threshold 2 to 1).
        """
        inverse_mag_course = self.get_inverse_course_magnetic()
        return int(round(inverse_mag_course / 10.0)) % 36 or 36

    def add_access_to_taxiway(self, taxiway: "Taxiway"):
        if taxiway not in self.access_to_taxiways:
            self.access_to_taxiways.append(taxiway)

    def has_access_to_taxiway(self, taxiway_designator: str) -> bool:
        for taxiway in self.access_to_taxiways:
            if taxiway.get_designator() == taxiway_designator:
                return True

        return False

    def add_intersecting_runway(self, intersecting_runway: "Runway"):
        if intersecting_runway not in self.intersecting_runways:
            self.intersecting_runways.append(intersecting_runway)

    def is_intersecting_runway(self, runway_designator: int) -> bool:
        for runway in self.intersecting_runways:
            if runway.get_designator() == runway_designator:
                return True
        return False