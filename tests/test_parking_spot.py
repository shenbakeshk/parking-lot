import unittest

from parking_lot import FourWheelerParkingLotBuilder, ParkingLotDirector
from parking_lot.constants import ParkingSpotType
from parking_lot.parking_spot import ParkingSpot, FourWheelerSpot
from parking_lot.vehicle import Car


class TestParkingSpot(unittest.TestCase):
    def test_parking_spot(self):
        curr_parking_spot = next(FourWheelerSpot.spot_counter)
        start = curr_parking_spot + 1
        end = start + 100
        for i in range(start, end):
            parking_spot = FourWheelerSpot()
            self.assertIsInstance(parking_spot, ParkingSpot)
            self.assertEqual(i, parking_spot.id_)

    def test_parking_spot_type(self):
        for __ in range(1, 11):
            parking_spot = FourWheelerSpot()
            self.assertIs(
                parking_spot.parking_spot_type, 
                ParkingSpotType.FOUR_WHEELER)

    def test_occupy_spot(self):
        four_wheeler_parking_lot_builder = FourWheelerParkingLotBuilder()
        director = ParkingLotDirector(four_wheeler_parking_lot_builder)
        director.build_parking_lot(10)
        parking_lot = director.get_parking_lot()
        car = Car("dummy_reg_no", "dummy_color")
        parking_spot = FourWheelerSpot()
        parking_spot.occupy_spot(car)
        self.assertFalse(parking_spot.is_free())

    def test_free_up_spot(self):
        parking_spot = FourWheelerSpot()
        parking_spot.free_up_spot()
        self.assertTrue(parking_spot.is_free())
