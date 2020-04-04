from collections import defaultdict
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
    _parking_lot = None

    def _build_default_parking_lot(self):
        # default four_wheeler spots count
        max_four_wheeler_spots: int = 10

        # Pythonic way to check if attr exists
        if TestParkingLot._parking_lot is None:
            four_wheeler_parking_lot_builder = FourWheelerParkingLotBuilder()
            director = ParkingLotDirector(four_wheeler_parking_lot_builder)
            director.build_parking_lot(max_four_wheeler_spots)
            TestParkingLot._parking_lot = director.get_parking_lot()
        return TestParkingLot._parking_lot

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
        for config in TestParkingLot.cars_config:
            car = Car(*config)
            parking_lot.allocate_parking_spot(car)
            self.assertEqual(
                parking_lot.get_vehicle_spot_number(car.registration_number), 
                car.parking_spot.id_
            )

    def test_get_registration_numbers_of_vehicle_with_color(self):
        parking_lot = self._build_default_parking_lot()
        colors_map = defaultdict(set)
        for config in TestParkingLot.cars_config:
            car = Car(*config)
            colors_map[config[1]].add(car)
            parking_lot.allocate_parking_spot(car)
            colors_map[config[1].lower()].add(car)

        for color in colors_map:
            vehicle_registration_numbers = \
                set(parking_lot.get_registration_numbers_of_vehicle_with_color(color))
            self.assertEqual(len(colors_map[color]), len(vehicle_registration_numbers))
            for car in colors_map[color]:
                self.assertIn(car.registration_number, vehicle_registration_numbers)

    def test_get_parking_spot_numbers_of_vehicles_with_color(self):
        self.clean_up_parking_spot()
        parking_lot = self._build_default_parking_lot()
        colors_map = defaultdict(set)
        for config in TestParkingLot.cars_config:
            car = Car(*config)
            colors_map[config[1]].add(car)
            parking_lot.allocate_parking_spot(car)
            colors_map[config[1].lower()].add(car)

        for color in colors_map:
            parking_spot_ids = parking_lot.get_parking_spot_numbers_of_vehicles_with_color(color)
            self.assertEqual(len(colors_map[color]), len(parking_spot_ids))
            for car in colors_map[color]:
                self.assertIn(car.parking_spot.id_, set(parking_spot_ids))

    def test_get_parking_lot_status_1(self):
        parking_lot = self._build_default_parking_lot()
        expected_results = [('Slot No.', 'Registration No', 'Colour')]
        for config in TestParkingLot.cars_config:
            car = Car(*config)
            parking_lot.allocate_parking_spot(car)
            parking_spot_id = car.parking_spot.id_
            row = (parking_spot_id, car.registration_number, car.color.capitalize())
            expected_results.append(row)

        status = parking_lot.get_parking_lot_status()
        self.assertListEqual(expected_results, status)

    def test_get_parking_lot_status_2(self):
        parking_lot = self._build_default_parking_lot()
        for config in TestParkingLot.cars_config:
            car = Car(*config)
            parking_lot.allocate_parking_spot(car)

        status = parking_lot.get_parking_lot_status()
        expected_results = [('Slot No.', 'Registration No', 'Colour')]
        for row in status[1:]:
            spot_id = row[0]
            if spot_id % 2 == 0:
                parking_lot.free_up_parking_spot(spot_id)
                continue
            expected_results.append(row)

        status = parking_lot.get_parking_lot_status()
        self.assertListEqual(expected_results, status)
