import unittest

from parking_lot.constants import ParkingSpotType
from parking_lot.parking_spot import ParkingSpot, FourWheelerSpot


class TestParkingSpot(unittest.TestCase):
    def test_parking_spot(self):
        for i in range(1, 11):
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
        parking_spot = FourWheelerSpot()
        parking_spot.occupy_spot()
        self.assertFalse(parking_spot.is_free())

    def test_free_up_spot(self):
        parking_spot = FourWheelerSpot()
        parking_spot.free_up_spot()
        self.assertTrue(parking_spot.is_free())
