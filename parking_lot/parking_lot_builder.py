from abc import ABC, abstractmethod

from parking_lot.parking_lot import ParkingLot
from parking_lot.parking_spot import FourWheelerSpot


class ParkingLotBuilder(ABC):
    @abstractmethod
    def add_four_wheeler_parking_spots(self):
        pass

    @abstractmethod
    def init_parking_lot_data_store(self):
        pass

    @abstractmethod
    def get_parking_lot(self):
        pass

class FourWheelerParkingLotBuilder(ParkingLotBuilder):
    def __init__(self):
        self._parking_lot = ParkingLot()

    def add_four_wheeler_parking_spots(
        self, max_four_wheeler_spots: int
    ) -> None:
        """
        Add four wheeler spots to parking_lot.
        """
        four_wheeler_spots = [None] * max_four_wheeler_spots
        for i, __ in enumerate(range(max_four_wheeler_spots), 0):
            four_wheeler_spots[i] = FourWheelerSpot()

        # initialize four wheeler parking-spots config
        self._parking_lot._four_wheeler_spots = four_wheeler_spots
        self._parking_lot._max_four_wheeler_spots = max_four_wheeler_spots
        self._parking_lot._curr_four_wheelers_parked = 0
        self._parking_lot._next_four_wheeler_spot = 0

    def init_parking_lot_data_store(self) -> None:
        """
        Initialize local data store.
        """
        self._parking_lot._color_vehicles_map = {}
        self._parking_lot._parked_vehicles = {}

    def get_parking_lot(self):
        return self._parking_lot

class ParkingLotDirector:
    def __init__(self, parking_lot_builder: ParkingLotBuilder):
        self.parking_lot_builder = parking_lot_builder
        self.parking_lot = None

    def build_parking_lot(self, max_four_wheeler_spots: int) -> ParkingLot:
        """
        Build parking-lot.
        """
        self.parking_lot_builder.add_four_wheeler_parking_spots(max_four_wheeler_spots)
        self.parking_lot_builder.init_parking_lot_data_store()
        self.parking_lot = self.parking_lot_builder.get_parking_lot()

    def get_parking_lot(self) -> ParkingLot:
        """
        Return built parking-lot.
        """
        return self.parking_lot
