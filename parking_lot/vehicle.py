from abc import ABC

from parking_lot.constants import VehicleType


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

