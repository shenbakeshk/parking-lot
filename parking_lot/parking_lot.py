from collections import defaultdict
import itertools
from typing import List, Set

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

    @property
    def color_vehicles_map(self):
        return self._color_vehicles_map

    def initialize_color_vehicles_map(self):
        if self._color_vehicles_map is None:
            self._color_vehicles_map = defaultdict(set)

    @property
    def parked_vehicles(self):
        return self._parked_vehicles

    def initialize_parked_vehicles(self):
        if self._parked_vehicles is None:
            self._parked_vehicles = {}

    def _is_vehicle_parked_in_parking_lot(self, vehicle: Vehicle) -> bool:
        """
        Check if vehicle is parked in parking-lot.
        Return bool.
        """
        # initialize flags iterable
        flags = []

        # check if vehicle part of data stores
        if vehicle.is_vehicle_parked():
            return True
        if vehicle.registration_number in self._parked_vehicles:
            return True
        if vehicle.registration_number in self._color_vehicles_map.get(vehicle.color, {}):
            return True

        return False

    def allocate_parking_spot(self, vehicle: Vehicle) -> None:
        """
        Allocate parking spot to incoming vehicle.
        """
        if not self._is_vehicle_parked_in_parking_lot(vehicle) \
            and self._is_parking_spot_available(vehicle.type_):
            parking_event = ParkingLotEvent.PARK
            self._update_parking_lot(parking_event, vehicle)

    def free_up_parking_spot(self, parking_spot: ParkingSpot) -> None:
        """
        Change state of vehicle, parking-spot 
        and parking-lot on vehicle's EXIT.
        """
        if not parking_spot.is_free():
            vehicle: Vehicle = parking_spot.vehicle
            if self._is_vehicle_parked_in_parking_lot(vehicle):
                unparking_event = ParkingLotEvent.UNPARK
                self._update_parking_lot(unparking_event, vehicle)

    def _add_vehicle_details(
        self, vehicle: Vehicle
    ) -> None:
        """
        Add vehicle details to parking-lot data store on parking vehicle.
        """
        self._parked_vehicles[vehicle.registration_number] = vehicle
        self._color_vehicles_map[vehicle.color].add(vehicle.registration_number)

    def _remove_vehicle_details(
        self, vehicle: Vehicle
    ) -> None:
        """
        Remove vehicle details from parking-lot data store on vehicle exit.
        """
        if vehicle.registration_number in self._parked_vehicles:
            del self._parked_vehicles[vehicle.registration_number]
        if (
            vehicle.color in self._color_vehicles_map 
            and vehicle.registration_number in self._color_vehicles_map.get(vehicle.color, set())
        ):
            self._color_vehicles_map[vehicle.color].remove(vehicle.registration_number)

    def _update_parking_lot(
        self, event: ParkingLotEvent, vehicle: Vehicle
    ) -> None:
        """
        Update parking-lot on ENTRY/EXIT of vehicles
        """
        if event is ParkingLotEvent.PARK:
            self._park_vehicle(vehicle)
            self._increment_spot_count(vehicle.type_)
            self._add_vehicle_details(vehicle)
        elif event is ParkingLotEvent.UNPARK:
            self._unpark_vehicle(vehicle)
            self._decrement_spot_count(vehicle.type_)        
            self._remove_vehicle_details(vehicle)

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
        is_next_spot_counter_valid = self._next_four_wheeler_spot >= 0
        return any_four_wheeler_spot and is_next_spot_counter_valid

    def _park_vehicle(self, vehicle: Vehicle) -> None:
        """
        Park vehicle in parking-lot.
        """
        self._allocate_parking_spot_to_incoming_vehicle(vehicle)
        self._issue_new_parking_ticket(vehicle)

    def _allocate_parking_spot_to_incoming_vehicle(
        self, vehicle: Vehicle
    ) -> None:
        """
        Allocate ticket to incoming vehicle.
        """
        vehicle_type = vehicle.type_
        parking_spot = self._select_next_available_parking_spot(vehicle_type)
        parking_spot.occupy_spot(vehicle)
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

    def get_registration_numbers_of_vehicle_with_color(
        self, color: str, vehicle_type: VehicleType = None
    ) -> List[str]:
        """
        Scan list of vehicles(of particular type if provided) 
        with particular color.
        Return list of vehicles' registration numbers.
        """
        res = []
        vehicles_reg_no_set: Set[Vehicle] = self._color_vehicles_map.get(color.lower(), set())
        for reg_no in vehicles_reg_no_set:
            vehicle = self._parked_vehicles[reg_no]
            if not vehicle_type or vehicle.type_predicate(vehicle_type):
                res.append(vehicle.registration_number)
        return res

    def get_parking_spot_numbers_of_vehicles_with_color(
        self, color: str, vehicle_type: VehicleType = None
    ) -> List[int]:
        """
        Return all parking-spot numbers(id).
        """
        res = []
        vehicles_reg_no_set: Set[str] = self._color_vehicles_map.get(color.lower(), set())
        for reg_no in vehicles_reg_no_set:
            vehicle: Vehicle = self._parked_vehicles[reg_no]
            if not vehicle_type or vehicle.type_predicate(vehicle_type):
                res.append(vehicle.parking_spot.id_)
        return res

    def get_vehicle_spot_number(
        self, vehicle_registration_number: str
    ) -> ParkingSpot:
        """
        Return vehicle's parking spot number.
        """
        if not(
            isinstance(vehicle_registration_number, str)
            and vehicle_registration_number.isupper()
        ):
            return

        vehicle: Vehicle = self._parked_vehicles.get(vehicle_registration_number)
        if not vehicle:
            return
        parking_spot: ParkingSpot = vehicle.parking_spot
        return parking_spot.id_
