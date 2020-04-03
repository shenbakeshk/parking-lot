from abc import ABC, abstractmethod


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
