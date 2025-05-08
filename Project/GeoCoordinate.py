

class GeoCoordinate:

    latitude: float
    longitude: float

    def __init__(self):
        pass

    # TODO implement relation to screen position

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