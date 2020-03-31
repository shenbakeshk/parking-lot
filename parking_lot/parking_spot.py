from abc import ABC

from parking_lot.constants import ParkingSpotType


class ParkingSpot(ABC):
    def __init__(
        self, spot_id: int, 
        parking_spot_type: ParkingSpotType
    ):
        self._id = spot_id
        self._free = True
        self._parking_spot_type = parking_spot_type

    @property
    def id_(self):
        return self._id

    def is_free(self):
        return self._free

    @property
    def parking_spot_type(self):
        return self._parking_spot_type


class FourWheelerSpot(ParkingSpot):
    def __init__(self, spot_id: int):
        super().__init__(
            spot_id, ParkingSpotType.FOUR_WHEELER)
