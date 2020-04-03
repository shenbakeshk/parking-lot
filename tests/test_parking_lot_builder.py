import unittest

from parking_lot import FourWheelerParkingLotBuilder, ParkingLotDirector


class TestParkingLotBuilder(unittest.TestCase):
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

    def test_parking_lot_builder(self):
        parking_lot = self._build_default_parking_lot()
        for i, spot in enumerate(parking_lot._four_wheeler_spots, 1):
            self.assertEqual(spot.id_, i)
        