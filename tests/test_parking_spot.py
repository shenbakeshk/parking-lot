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
        for i in range(1, 11):
            parking_spot = FourWheelerSpot()
            self.assertIs(
                parking_spot.parking_spot_type, 
                ParkingSpotType.FOUR_WHEELER)
