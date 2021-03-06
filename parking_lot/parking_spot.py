from abc import ABC
import itertools

from parking_lot.constants import ParkingSpotType


class ParkingSpot(ABC):
    spot_counter = itertools.count(start=1)
    def __init__(self, parking_spot_type):
        self._id = next(ParkingSpot.spot_counter)
        self._free = True
        self._vehicle = None
        self._parking_spot_type = parking_spot_type

    @property
    def id_(self):
        return self._id

    def is_free(self):
        return self._free

    @property
    def vehicle(self):
        return self._vehicle

    @property
    def parking_spot_type(self):
        return self._parking_spot_type

    def occupy_spot(self, vehicle) -> None:
        """
        Occupy parking-spot.
        """
        self._vehicle = vehicle
        self._free = False

    def free_up_spot(self) -> None:
        """
        Free up parking-spot.
        """
        self._vehicle = None
        self._free = True


class FourWheelerSpot(ParkingSpot):
    def __init__(self):
        super().__init__(ParkingSpotType.FOUR_WHEELER)
