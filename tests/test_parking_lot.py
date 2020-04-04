import unittest

from parking_lot import FourWheelerParkingLotBuilder, ParkingLotDirector
from parking_lot.parking_spot import FourWheelerSpot, ParkingSpot
from parking_lot.parking_ticket import FourWheelerParkingTicket, ParkingTicket
from parking_lot.vehicle import Car


class TestParkingLot(unittest.TestCase):
    cars_config = (
        ("KA-01-HH-1234", "White"), 
        ("KA-01-HH-9999", "White"), 
        ("KA-01-BB-0001", "Black"), 
        ("KA-01-HH-7777", "Red"), 
        ("KA-01-HH-2701", "Blue"), 
        ("KA-01-HH-3141", "Black"),
    )

    def _build_default_parking_lot(self):
        # default four_wheeler spots count
        max_four_wheeler_spots: int = 10

        # Pythonic way to check if attr exists
        try:
            return self.parking_lot
        except AttributeError:
            four_wheeler_parking_lot_builder = FourWheelerParkingLotBuilder()
            director = ParkingLotDirector(four_wheeler_parking_lot_builder)
            director.build_parking_lot(max_four_wheeler_spots)
            self.parking_lot = director.get_parking_lot()
        return self.parking_lot

    def test_allocate_parking_spot(self):
        parking_lot = self._build_default_parking_lot()
        car = Car("KA-01-HH-1234", "White")
        parking_lot.allocate_parking_spot(car)
        self.assertIsInstance(car.parking_spot, (FourWheelerSpot, ParkingSpot))
        self.assertIsInstance(car.ticket, (FourWheelerParkingTicket, ParkingTicket))
        parking_spot = car.parking_spot
        ticket = car.ticket
        for __ in range(100):
            parking_lot.allocate_parking_spot(car)
            self.assertIs(car.parking_spot, parking_spot)
            self.assertIs(car.ticket, ticket)
            self.assertIsNotNone(car.ticket)
            self.assertIsNotNone(car.parking_spot)
            self.assertFalse(car.parking_spot.is_free())
            self.assertTrue(car.is_vehicle_parked())

    def test_free_up_parking_spot(self):
        parking_lot = self._build_default_parking_lot()
        car = Car("KA-01-HH-1234", "White")
        parking_lot.allocate_parking_spot(car)
        parking_spot = car.parking_spot
        parking_lot.free_up_parking_spot(parking_spot)
        self.assertIsNone(car.ticket)
        self.assertIsNone(car.parking_spot)
        self.assertFalse(car.is_vehicle_parked())

    def test_get_vehicle_spot_number(self):
        parking_lot = self._build_default_parking_lot()
        car = Car("KA-01-HH-1234", "White")
        parking_lot.allocate_parking_spot(car)
        spot_number = parking_lot.get_vehicle_spot_number(car.registration_number)
        self.assertEqual(car.parking_spot.id_, spot_number)
