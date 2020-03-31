from abc import ABC

from parking_lot.constants import VehicleType
from parking_lot.parking_spot import ParkingSpot
from parking_lot.parking_ticket import ParkingTicket


class Vehicle(ABC):
    def __init__(
        self, registration_number: str, 
        color: str, vehicle_type: VehicleType
    ):
        self._registration_number = registration_number.upper()
        self._type = vehicle_type
        self._color = color.lower()
        self._ticket = None
        self._parking_spot = None

    @property
    def registration_number(self) -> str:
        return self._registration_number

    @property
    def type_(self) -> VehicleType:
        return self._type

    @property
    def color(self) -> str:
        return self._color

    @property
    def parking_spot(self):
        return self._parking_spot

    @parking_spot.setter
    def allocate_parking_spot(
        self, parking_spot: ParkingSpot
    ):
        self._parking_spot = parking_spot


class Car(Vehicle):
    def __init__(self, registration_number: str, color: str):
        super().__init__(
            registration_number, color, VehicleType.CAR)
