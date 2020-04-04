from abc import ABC, abstractmethod

from parking_lot import FourWheelerParkingLotBuilder, ParkingLotDirector
from parking_lot.parking_lot import FourWheelerParkingLot
from parking_lot.vehicle import Car


class FourWheelerParkingLotCommand(ABC):
    _parking_lot = None

    def __init__(self):
        self._parking_lot: FourWheelerParkingLot = None
    
    @classmethod
    def get_parking_lot_(cls):
        return cls._parking_lot

    @classmethod
    def create_parking_lot(cls, max_four_wheeler_spots: int):
        if not cls._parking_lot:
            parking_lot_builder = FourWheelerParkingLotBuilder()
            parking_lot_director = ParkingLotDirector(parking_lot_builder)
            parking_lot_director.build_parking_lot(max_four_wheeler_spots)
            cls._parking_lot = parking_lot_director.get_parking_lot()

    @abstractmethod
    def execute(self):
        pass

class CreateFourWheelerParkingLot(FourWheelerParkingLotCommand):
    def __init__(self, max_four_wheeler_spots: int):
        self._max_four_wheeler_spots = max_four_wheeler_spots
    
    def execute(self):
        """
        Create four-wheeler parking-lot.
        """
        FourWheelerParkingLotCommand.create_parking_lot(self._max_four_wheeler_spots)
        
        if FourWheelerParkingLotCommand.get_parking_lot_():
            return f"Created a parking lot with {self._max_four_wheeler_spots} slots"

class ParkFourWheelerCommand(FourWheelerParkingLotCommand):
    def __init__(self, registration_number: str, color: str):
        self._vehicle = Car(registration_number, color)

    def execute(self):
        """
        Park four-wheeler.
        """
        if FourWheelerParkingLotCommand._parking_lot.allocate_parking_spot(self._vehicle):
            return f"Allocated slot number: {self._vehicle.parking_spot.id_}"
        return "Sorry, parking lot is full"

class LeaveFourWheelerParkingLotCommand(FourWheelerParkingLotCommand):
    def __init__(self, parking_spot_id: int):
        self._parking_spot_id = parking_spot_id
    
    def execute(self):
        """
        Exit four-wheeler-parking-lot.
        """
        if FourWheelerParkingLotCommand._parking_lot.free_up_parking_spot(self._parking_spot_id):
            return f"Slot number {self._parking_spot_id} is free"
        return "Sorry, parking spot is not freed"

class FourWheelerParkingLotStatus(FourWheelerParkingLotCommand):
    def execute(self):
        """
        Return state of four-wheeler-parking-lot
        """
        status = FourWheelerParkingLotCommand._parking_lot.get_parking_lot_status()
        if len(status) < 2:  # excluding header
            return ""
        
        res = '\t'.join(status[0]) + '\n'
        for r in status[1:]:
            res += '\t'.join(r) + '\n'

        return res

class FourWheeelerRegNosWithColor(FourWheelerParkingLotCommand):
    def __init__(self, color: str):
        self._color = color

    def execute(self):
        """
        Return list of four-wheelers' reg-nos with given color.
        """
        reg_nos_list = \
            FourWheelerParkingLotCommand._parking_lot.get_registration_numbers_of_vehicle_with_color(self._color)
        
        if not reg_nos_list:
            return "Not Found"
        return ', '.join(reg_nos_list)

class FourWheelerParkingSpotNosFromVehicleColor(FourWheelerParkingLotCommand):
    def __init__(self, color: str):
        self._color = color

    def execute(self):
        """
        Return list of four-wheelers' parking-spot-ids with given color.
        """
        parking_spots_nos = \
            FourWheelerParkingLotCommand._parking_lot.get_parking_spot_numbers_of_vehicles_with_color(self._color)
        
        if not parking_spots_nos:
            return "Not Found"
        return ', '.join(parking_spots_nos)

class FourWheelerParkingSpotNoFromRegNo(FourWheelerParkingLotCommand):
    def __init__(self, registration_number: str):
        self._registration_number = registration_number
    
    def execute(self):
        """
        Return parking-spot number of vehicle.
        """
        parking_spot_id = \
            FourWheelerParkingLotCommand._parking_lot.get_vehicle_spot_number(self._registration_number)
        
        if parking_spot_id is None:
            return "Not found"
        return parking_spot_id
