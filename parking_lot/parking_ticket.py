from abc import ABC
import itertools
from datetime import datetime

from parking_lot.constants import ParkingSpotType


class ParkingTicket(ABC):
    ticket_counter = itertools.count(start=1)
    def __init__(
        self, parking_spot_type: ParkingSpotType
    ):
        self._id = next(ParkingTicket.ticket_counter)
        self._parking_spot_type = parking_spot_type
        self._entry_time = datetime.now()

    @property
    def id_(self):
        return self._id

    @property
    def parking_spot_type(self):
        return self._parking_spot_type

    @property
    def entry_time(self):
        return self._entry_time

class FourWheelerParkingTicket(ParkingTicket):
    def __init__(self):
        super().__init__(ParkingSpotType.FOUR_WHEELER)
