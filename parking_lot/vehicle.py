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
    def parking_spot(
        self, parking_spot: ParkingSpot
    ):
        self._parking_spot = parking_spot

    def _deallocate_parking_spot(self):
        def deallocate_ticket():
            if self._ticket:
                self._ticket = None

        deallocate_ticket()
        self._parking_spot = None

    @property
    def ticket(self) -> ParkingTicket:
        return self._ticket

    @ticket.setter
    def ticket(self, ticket: ParkingTicket):
        if not self._ticket:
            self._ticket = ticket
        return self._ticket

    def is_vehicle_parked(self) -> bool:
        """
        check if vehicle is alloted with parking spot
        """
        return True if self._parking_spot else False

    def type_predicate(
        self, vehicle_type: VehicleType
    ):
        return True if self._type is vehicle_type else False


class Car(Vehicle):
    def __init__(self, registration_number: str, color: str):
        super().__init__(
            registration_number, color, VehicleType.CAR)
