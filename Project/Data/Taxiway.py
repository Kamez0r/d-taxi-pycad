
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Project.Data.Runway import Runway
    from Project.Data.Stand import Stand


class Taxiway:
    designator: str

    access_to_runways: list["Runway"]
    access_to_taxiways: list["Taxiway"]
    access_to_stands: list["Stand"]

    def __init__(self, designator: str):
        self.designator = designator
        self.access_to_runways = []
        self.access_to_taxiways = []
        self.access_to_stands = []

    @staticmethod
    def from_serialized_data(serialized_data: dict):
        if not Taxiway.check_valid_data(serialized_data):
            raise TypeError("Invalid data provided")

        new_instance = Taxiway(serialized_data["designator"])
        return new_instance

    def get_serialized(self):
        rws = []
        for rw in self.access_to_runways:
            rws.append(rw.get_designator())

        tws = []
        for tw in self.access_to_taxiways:
            tws.append(tw.get_designator())

        sts = []
        for st in self.access_to_stands:
            sts.append(st.get_designator())

        return {
            "designator": self.designator,
            "access_to_runways": rws,
            "access_to_taxiways": tws,
            "access_to_stands": sts
        } # TODO implement function

    @staticmethod
    def check_valid_data(serialized_data: dict):
        if not "designator" in serialized_data:
            return False

        if not "access_to_runways" in serialized_data:
            return False

        if not type(serialized_data["access_to_runways"]) is list:
            return False

        if not "access_to_taxiways" in serialized_data:
            return False

        if not type(serialized_data["access_to_taxiways"]) is list:
            return False

        if not "access_to_stands" in serialized_data:
            return False

        if not type(serialized_data["access_to_stands"]) is list:
            return False

        return True

    def get_designator(self):
        return self.designator

    def add_access_to_runway(self, runway: "Runway"):
        if runway not in self.access_to_runways:
            self.access_to_runways.append(runway)

    def has_access_to_runway(self, runway_designator: int):
        for runway in self.access_to_runways:
            if runway_designator == runway.get_designator() \
            or runway_designator == runway.get_designator():
                return True

        return False

    def add_access_to_taxiway(self, taxiway: "Taxiway"):
        if taxiway not in self.access_to_taxiways:
            self.access_to_taxiways.append(taxiway)

    def has_access_to_taxiway(self, taxiway_designator: str):
        for taxiway in self.access_to_taxiways:
            if taxiway_designator == taxiway.get_designator():
                return True

        return False

    def add_access_to_stand(self, stand: "Stand"):
        if stand not in self.access_to_stands:
            self.access_to_stands.append(stand)

    def has_access_to_stand(self, stand_designator: str):
        for stand in self.access_to_stands:
            if stand.get_designator() == stand_designator:
                return True

        return False