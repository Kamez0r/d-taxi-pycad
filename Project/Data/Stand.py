
from Project.GeoCoordinate import GeoCoordinate

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from Project.Data.Taxiway import Taxiway

class Stand:

    designator: str
    position: GeoCoordinate

    access_taxiway: Union["Taxiway", None]
    conflict_stands: list["Stand"]

    def __init__(self, designator: str, position: GeoCoordinate):
        self.designator = designator
        self.position = position
        self.access_taxiway = None
        self.conflict_stands = []

    @staticmethod
    def from_serialized_data(sdata: dict):
        if not Stand.check_valid_data(sdata):
            raise ValueError("Invalid stand data")

        instance = Stand(sdata["designator"], GeoCoordinate.from_tuple(sdata["position"]))
        return instance

    @staticmethod
    def check_valid_data(serialized_data: dict):
        if not "designator" in serialized_data:
            return False

        if not type(serialized_data["designator"]) == str:
            return False

        if not "position" in serialized_data:
            return False

        if not GeoCoordinate.check_valid_data(serialized_data["position"]):
            return False

        if not "access_taxiway" in serialized_data:
            return False

        if not type(serialized_data["access_taxiway"]) not in [str, None]:
            return False

        if not "conflict_stands" in serialized_data:
            return False

        if not type(serialized_data["conflict_stands"]) == list:
            return False

        return True

    def get_serialized(self):
        sts = []
        for st in self.conflict_stands:
            sts.append(st.get_serialized())

        access_taxiway = None
        if self.access_taxiway is not None:
            access_taxiway = self.access_taxiway.get_designator()

        return {
            "designator": self.designator,
            "position": self.position.get_serialized(),
            "access_taxiway": access_taxiway,
            "conflict_stands": sts
        }

    def get_designator(self) -> str:
        return self.designator

    def set_access_taxiway(self, taxiway: "Taxiway"):
        self.access_taxiway = taxiway

    def has_access_to_any_taxiway(self) -> bool:
        return self.access_taxiway is not None

    def has_access_to_taxiway(self, taxiway_designator: str) -> bool:
        if self.access_taxiway is None:
            return False
        elif self.access_taxiway.designator == taxiway_designator:
            return True
        else:
            return False

    def is_in_conflict_with_stand(self, stand_designator: str):
        for stand in self.conflict_stands:
            if stand.get_designator() == stand_designator:
                return True

        return False

    def add_conflicting_stand(self, stand: "Stand"):
        if stand not in self.conflict_stands:
            self.conflict_stands.append(stand)