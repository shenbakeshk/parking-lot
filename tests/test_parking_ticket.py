from datetime import datetime
import unittest

from parking_lot.constants import ParkingSpotType
from parking_lot.parking_ticket import FourWheelerParkingTicket

class TestParkingTicket(unittest.TestCase):
    def test_four_wheeler_parking_ticket(self):
        for i in range(1, 11):
            ticket = FourWheelerParkingTicket()
            self.assertEqual(i, ticket.id_)
            self.assertIsInstance(ticket, FourWheelerParkingTicket)
            self.assertIsInstance(ticket.entry_time, datetime)

    def test_four_wheeler_parking_ticket_spot_type(self):
        four_wheeler_parking_ticket = FourWheelerParkingTicket()
        self.assertIsInstance(
            four_wheeler_parking_ticket.parking_spot_type,
            ParkingSpotType   
        )
        self.assertEqual(
            four_wheeler_parking_ticket.parking_spot_type,
            ParkingSpotType.FOUR_WHEELER
        )
