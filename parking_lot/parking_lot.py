import itertools
from typing import List

from parking_lot.constants import VehicleType, ParkingLotEvent
from parking_lot.parking_spot import ParkingSpot
from parking_lot.parking_ticket import FourWheelerParkingTicket
from parking_lot.vehicle import Vehicle


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

    def allocate_parking_spot(self, vehicle: Vehicle) -> None:
        """
        Allocate parking spot to incoming vehicle.
        """
        if not vehicle.is_vehicle_parked() \
            and self._is_parking_spot_available(vehicle.type_):
            parking_event = ParkingLotEvent.PARK
            self._update_parking_lot(parking_event, vehicle)

    def free_up_parking_spot(self, vehicle: Vehicle) -> None:
        """
        Change state of vehicle, parking-spot 
        and parking-lot on vehicle's EXIT.
        """
        if vehicle.is_vehicle_parked():
            unparking_event = ParkingLotEvent.UNPARK
            self._update_parking_lot(unparking_event, vehicle)

    def _update_parking_lot(
        self, event: ParkingLotEvent, vehicle: Vehicle
    ) -> None:
        """
        Update parking-lot on ENTRY/EXIT of vehicles
        """
        if event is ParkingLotEvent.PARK:
            self._park_vehicle(vehicle)
        elif event is ParkingLotEvent.UNPARK:
            self._unpark_vehicle(vehicle)

    def _is_parking_spot_available(self, vehicle_type: VehicleType) -> bool:
        """
        Check availability of spot for incoming vehicle.
        Return bool value.
        """
        if vehicle_type is VehicleType.CAR:
            # check if there is any parking available
            return self._is_four_wheeler_spot_available()
        else:
            raise Exception("Invalid vehicle type request")

    def _is_four_wheeler_spot_available(self):
        """
        Check if any four-wheeler parking-spot available.
        """
        any_four_wheeler_spot = self._curr_four_wheelers_parked \
                < self._max_four_wheeler_spots
        is_next_spot_counter_valid = self._next_four_wheeler_spot > 0
        return any_four_wheeler_spot and is_next_spot_counter_valid

    def _park_vehicle(self, vehicle: Vehicle) -> None:
        """
        Park vehicle in parking-lot.
        """
        self._allocate_ticket_to_incoming_vehicle(vehicle)
        self._issue_new_parking_ticket(vehicle)
        self._increment_spot_count(vehicle.type_)

    def _allocate_ticket_to_incoming_vehicle(self, vehicle: Vehicle) -> None:
        """
        Allocate ticket to incoming vehicle.
        """
        vehicle_type = vehicle.type_
        parking_spot = self._select_next_available_parking_spot(vehicle_type)
        parking_spot.occupy_spot()
        vehicle.parking_spot = parking_spot

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

    def _issue_new_parking_ticket(self, vehicle: Vehicle) -> None:
        """
        Assign ticket to vehicle(owner) based on 
        vehicle type.
        """
        if vehicle.type_ is VehicleType.CAR:
            vehicle.ticket = FourWheelerParkingTicket()

    def _prefetch_next_available_parking_spot(
        self, parking_spots: List[ParkingSpot]
    ) -> int:
        """
        Pick the next available parking-spot from a given list of 
        parking-spots.
        Return free parking-spot's index(zero based) 
        in given list of parking-spots. 
        If no parking-spots available return -1.
        """
        for i, parking_spot in enumerate(parking_spots):
            if parking_spot.is_free():
                return i
        return -1

    def _increment_spot_count(self, vehicle_type: VehicleType) -> None:
        """
        Update parking-lot state on new vehicle's entry.
        """
        if vehicle_type is VehicleType.CAR:
            curr_count = self._curr_four_wheelers_parked
            self._curr_four_wheelers_parked = \
                min(self._max_four_wheeler_spots, curr_count + 1)
            self._next_four_wheeler_spot = \
                self._prefetch_next_available_parking_spot(
                    self._four_wheeler_spots
                )
        else:
            raise Exception("Invalid vehicle type request")

    def _unpark_vehicle(self, vehicle: Vehicle) -> None:
        """
        Unpark vehicle from parking lot.
        """
        parking_spot = vehicle.parking_spot
        parking_spot.free_up_spot()

        # this will remove ref to allocated ticket
        # and be gc'ed
        vehicle._deallocate_parking_spot()
        self._decrement_spot_count(vehicle.type_)

    def _decrement_spot_count(self, vehicle_type: VehicleType) -> None:
        """
        Update parking-lot state on vehicle's exit.
        """
        if vehicle_type is VehicleType.CAR:
            curr_count = self._curr_four_wheelers_parked
            self._curr_four_wheelers_parked = max(0, curr_count - 1)
            self._next_four_wheeler_spot = \
                self._prefetch_next_available_parking_spot(
                    self._four_wheeler_spots
                )
        else:
            raise Exception("Invalid vehicle type request")
