import math


class GeoCoordinate:

    EarthRadiusMeters = 6371000.0

    latitude: float
    longitude: float

    def __init__(self):
        pass

    # TODO implement relation to screen position

    @staticmethod
    def check_valid_data(serialized_data: tuple[float,float]):
        if not (isinstance(serialized_data, tuple) and len(serialized_data) == 2):
            return False

        lat, lon = serialized_data
        if not (isinstance(lat, (int, float)) and isinstance(lon, (int, float))):
            return False

        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return False

        return True

    def get_serialized(self):
        return self.getLatitude(), self.getLongitude()

    @staticmethod
    def from_serialized_data(serial_data: tuple[float, float]) -> "GeoCoordinate":
        if not GeoCoordinate.check_valid_data(serial_data):
            raise TypeError("Serial data is not valid")

        instance = GeoCoordinate()
        instance.latitude, instance.longitude = serial_data
        return instance

    @staticmethod
    def from_tuple(lat_lon: tuple[float, float]) -> "GeoCoordinate":
        instance = GeoCoordinate()
        instance.latitude, instance.longitude = lat_lon
        return instance

    ## Getters and Setters
    def setLatitude(self, latitude: float):
        self.latitude = latitude

    def getLatitude(self) -> float:
        return self.latitude

    def setLongitude(self, longitude: float):
        self.longitude = longitude

    def getLongitude(self) -> float:
        return self.longitude


    ## Static converters
    @staticmethod
    def DECtoDMS(angle: float) -> (int, int, float):
        mult = -1 if angle < 0 else 1
        mnt, sec = divmod(abs(angle) * 3600, 60)
        deg, mnt = divmod(mnt, 60)

        return mult * deg, mult * mnt, mult * sec

    @staticmethod
    def DMStoDEC(deg: int, mnt: int, sec: float) -> float:
        sign = -1 if deg < 0 or mnt < 0 or sec < 0 else 1
        deg_abs = abs(deg)
        mnt_abs = abs(mnt)
        sec_abs = abs(sec)

        return sign * (deg_abs + mnt_abs / 60 + sec_abs / 3600)

    @staticmethod
    def get_true_course_delta_coord(c_start: "GeoCoordinate", c_end: "GeoCoordinate") -> float:
        """
        returns "True" runway course from threshold1 to threshold2
        :return:
        """
        lat1 = c_start.getLatitude()
        lon1 = c_start.getLongitude()

        lat2 = c_end.getLatitude()
        lon2 = c_end.getLongitude()

        # Convert degrees to radians
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lon_rad = math.radians(lon2 - lon1)

        # Compute initial bearing
        x = math.sin(delta_lon_rad) * math.cos(lat2_rad)
        y = math.cos(lat1_rad) * math.sin(lat2_rad) - \
            math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon_rad)
        initial_bearing = math.atan2(x, y)

        # Convert from radians to degrees and normalize
        bearing_deg = (math.degrees(initial_bearing) + 360) % 360
        return bearing_deg

    @staticmethod
    def apply_magnetic_variation(true_course, mag_var) -> float:
        """
        applies magnetic variation
        :param true_course: true course to be adjusted
        :param mag_var: magnetic variation in degrees. Positive for east, negative for east
        :return:
        """
        magnetic_course = (true_course - mag_var) % 360
        return magnetic_course

    @staticmethod
    def remove_magnetic_variation(mag_course, mag_var) -> float:
        return GeoCoordinate.apply_magnetic_variation(mag_course, -mag_var)