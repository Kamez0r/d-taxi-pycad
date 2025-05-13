from Project.GeoCoordinate import GeoCoordinate
from .Runway import Runway
from .Taxiway import Taxiway
from .Stand import Stand

class Airport:

    aerodrome_icao: str

    magnetic_variation: float
    aerodrome_location: GeoCoordinate

    runways: list["Runway"]
    taxiways: list["Taxiway"]
    stands: list["Stand"]

    def __init__(self,
                 aerodrome_icao: str,
                 aerodrome_name: str,
                 aerodrome_location: GeoCoordinate,
                 magnetic_variation: float):
        self.aerodrome_icao = aerodrome_icao
        self.aerodrome_name = aerodrome_name

        self.aerodrome_location = aerodrome_location
        self.magnetic_variation = magnetic_variation

        self.runways = []
        self.taxiways = []
        self.stands = []

    @staticmethod
    def check_valid_data(serialized_data: dict):

        if not "magnetic_variation" in serialized_data:
            return False

        if not type(serialized_data["magnetic_variation"]) == float:
            return False

        if not "aerodrome_icao" in serialized_data:
            return False

        if not type(serialized_data["aerodrome_icao"]) == str:
            return False

        if not "aerodrome_name" in serialized_data:
            return False

        if not type(serialized_data["aerodrome_name"]) == str:
            return False

        if not "aerodrome_location" in serialized_data:
            return False

        if not GeoCoordinate.check_valid_data(serialized_data["aerodrome_location"]):
            return False

        if not "runways" in serialized_data:
            return False

        if not type(serialized_data["runways"]) == list:
            return False

        if not "taxiways" in serialized_data:
            return False

        if not type(serialized_data["taxiways"]) == list:
            return False

        if not "stands" in serialized_data:
            return False

        if not type(serialized_data["stands"]) == list:
            return False

        return True

    def get_serialized(self):
        rws = []
        for rw in self.runways:
            rws.append(rw.get_serialized())

        tws = []
        for tw in self.taxiways:
            tws.append(tw.get_serialized())

        sts = []
        for st in self.stands:
            sts.append(st.get_serialized())

        return {
            "aerodrome_icao": self.aerodrome_icao,
            "aerodrome_name": self.aerodrome_name,
            "magnetic_variation": float(self.magnetic_variation),
            "aerodrome_location": self.aerodrome_location.get_serialized(),
            "runways": rws,
            "taxiways": tws,
            "stands": sts
        }

    def init_from_serialized(self, sdata: dict):
        if not self.check_valid_data(sdata):
            raise TypeError("Invalid data provided")

        self.aerodrome_icao = sdata["aerodrome_icao"]
        self.aerodrome_name = sdata["aerodrome_name"]

        self.magnetic_variation = sdata["magnetic_variation"]
        self.aerodrome_location = GeoCoordinate.from_tuple(sdata["aerodrome_location"])

        self.runways = []
        self.taxiways = []
        self.stands = []

        # First pass, init empty endpoints
        for rw in sdata["runways"]:
            inst = Runway.from_serialized_data(rw)
            self.add_runway(inst)
            rw["designator"] = inst.get_designator()


        for tw in sdata["taxiways"]:
            self.add_taxiway(Taxiway.from_serialized_data(tw))

        for st in sdata["stands"]:
            self.add_stand(Stand.from_serialized_data(st))

        # Second pass, add conflicting points
        for rw in sdata["runways"]:
            own_instance = self.get_runway_by_designator(rw["designator"])
            for other_runway in rw["intersecting_runways"]:
                self.add_conflict_point_runway_runway(
                    own_instance,
                    self.get_runway_by_designator(other_runway),
                )
            for other_taxiway in rw["access_to_taxiways"]:
                self.add_conflict_point_runway_taxiway(
                    own_instance,
                    self.get_taxiway_by_designator(other_taxiway),
                )

        for tw in sdata["taxiways"]:
            own_instance = self.get_taxiway_by_designator(tw["designator"])

            for other_runway in tw["access_to_runways"]:
                self.add_conflict_point_runway_taxiway(
                    self.get_runway_by_designator(other_runway),
                    own_instance,
                )

            for other_taxiway in tw["access_to_taxiways"]:
                self.add_conflict_point_taxiway_taxiway(
                    own_instance,
                    self.get_taxiway_by_designator(other_taxiway),
                )

            for other_stand in tw["access_to_stands"]:
                self.add_conflict_point_taxiway_stand(
                    own_instance,
                    self.get_stand_by_designator(other_stand),
                )

        for st in sdata["stands"]:
            own_instance = self.get_stand_by_designator(st["designator"])
            access_taxiway = self.get_taxiway_by_designator(st["access_taxiway"])

            if access_taxiway:
                self.add_conflict_point_taxiway_stand(
                    access_taxiway,
                    own_instance,
                )

            for other_stand in st["conflict_stands"]:
                self.add_conflict_point_stand_stand(
                    own_instance,
                    self.get_stand_by_designator(other_stand)
                )

    def add_runway(self, runway: Runway):
        self.runways.append(runway)

    def add_taxiway(self, taxiway: Taxiway):
        self.taxiways.append(taxiway)

    def add_stand(self, stand: Stand):
        self.stands.append(stand)

    def get_runway_by_designator(self, runway_designator: str):
        for runway in self.runways:
            if runway_designator == runway.get_designator() \
            or runway_designator == runway.get_inverse_designator():
                return runway
        raise KeyError("Invalid runway designator")

    def get_taxiway_by_designator(self, taxiway_designator: str):
        for taxiway in self.taxiways:
            if taxiway_designator == taxiway.get_designator():
                return taxiway
        # raise KeyError("Invalid taxiway designator")
        return None
    def get_stand_by_designator(self, stand_designator: str):
        for stand in self.stands:
            if stand_designator == stand.get_designator():
                return stand
        raise KeyError("Invalid stand designator")

    def add_conflict_point_runway_runway(self, runway1: Runway, runway2: Runway):
        for runwayA in self.runways:
            if runwayA.get_designator() == runway1.get_designator():
                for runwayB in self.runways:
                    if runwayB.get_designator() == runway2.get_designator():
                        runwayA.add_intersecting_runway(runwayB)
                        runwayB.add_intersecting_runway(runwayA)
                        return
                raise Exception("runway 2 not found in defined runways")
        raise Exception("runway 1 not found in defined runways")

    def add_conflict_point_runway_taxiway(self, runway: Runway, taxiway: Taxiway):
        for runwayA in self.runways:
            if runwayA.get_designator() == runway.get_designator():
                for taxiwayB in self.taxiways:
                    if taxiwayB.get_designator() == taxiway.get_designator():
                        runwayA.add_access_to_taxiway(taxiway)
                        taxiwayB.add_access_to_runway(runway)
                        return
                raise Exception("taxiway not found in defined taxiways")
        raise Exception("runway not found in defined runways")

    def add_conflict_point_taxiway_taxiway(self, taxiway1:Taxiway, taxiway2: Taxiway):
        for taxiwayA in self.taxiways:
            if taxiwayA.get_designator() == taxiway1.get_designator():
                for taxiwayB in self.taxiways:
                    if taxiwayB.get_designator() == taxiway2.get_designator():
                        taxiwayA.add_access_to_taxiway(taxiway2)
                        taxiwayB.add_access_to_taxiway(taxiway1)
                        return
                raise Exception("taxiway 2 not found in defined taxiways")
        raise Exception("taxiway 1 not found in defined taxiways")

    def add_conflict_point_taxiway_stand(self, taxiway: Taxiway, stand: Stand):
        for taxiwayA in self.taxiways:
            if taxiwayA.get_designator() == taxiway.get_designator():
                for standB in self.stands:
                    if standB.get_designator() == stand.get_designator():
                        taxiwayA.add_access_to_stand(stand)
                        if standB.has_access_to_any_taxiway() and standB.access_taxiway.get_designator() != taxiway.get_designator():
                            raise Exception("stand already has access to taxiway")
                        standB.set_access_taxiway(taxiway)
                        return
                raise Exception("stand not found in defined stands")
        raise Exception("taxiway not found in defined taxiways")


    def add_conflict_point_stand_stand(self, stand1: Stand, stand2: Stand):
        for standA in self.stands:
            if standA.get_designator() == stand1.get_designator():
                for standB in self.stands:
                    if standB.get_designator() == stand2.get_designator():
                        standA.add_conflicting_stand(stand2)
                        standB.add_conflicting_stand(stand1)
                        return
                    raise Exception("stand2 not found in defined stands")
        raise Exception("stand1 not found in defined stands")