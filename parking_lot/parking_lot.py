import itertools
from typing import List

from parking_lot.constants import VehicleType
from parking_lot.parking_spot import ParkingSpot


class ParkingLot:
    """
    Parking-lot, a composition of multiple components like,
    parking-spots, parking-tickets, vehicles.
    
    Parking lot to park FourWheeler vehicles.
    Supported operations:
    1. park vehicles:
        1.1. allocate parking-spot to incoming vehicle,
        1.2. allocate parking-ticket.
    2. unpark vehicles:
        2.1. deallocate parking-spots for vehicles exiting,
        2.2. terminate parking-ticket's validity.
    3. util functions:
        3.1. get registration numbers of vehicle with particular given color,
        3.2. get parking-spot numbers of vehicle with particular given color,
        3.3. fetch parking-spot number of a given parked vehicle.
    """
    parking_lot_counter = itertools.count(start=1)

    # _instance = None

    # def __new__(cls, *args, **kwargs):
    #     """
    #     Singleton handler of parking lot
    #     """
    #     if not cls._instance:
    #         cls._instance = super().__new__(cls)
    #     return cls._instance

    def __init__(self):
        self._id = next(ParkingLot.parking_lot_counter)

        # four wheeler parking spots
        self._max_four_wheeler_spots = None
        self._four_wheeler_spots = None
        self._curr_four_wheelers_parked = None
        self._next_four_wheeler_spot = None

        # data store
        self._color_vehicles_map = None
        self._parked_vehicles = None

    @property
    def id_(self):
        return self._id

    def _is_parking_spot_available(self, vehicle_type: VehicleType) -> bool:
        """
        Check availability of spot for incoming vehicle.
        Return bool value.
        """
        if vehicle_type is VehicleType.CAR:
            # check if there is any parking available
            return self._curr_four_wheelers_parked \
                < self._max_four_wheeler_spots
        else:
            raise Exception("Invalid vehicle type request")

    def _select_next_available_parking_spot(
        self, vehicle_type: VehicleType
    ) -> ParkingSpot:
        """
        Select and return next available parking-spot based on vehicle type. 
        Return parking-spot.
        """
        if vehicle_type is VehicleType.CAR:
            parking_spot = self._four_wheeler_spots[
                self._next_four_wheeler_spot]
        return parking_spot
