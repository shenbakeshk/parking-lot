from datetime import datetime
import unittest

from parking_lot.constants import ParkingSpotType
from parking_lot.parking_ticket import FourWheelerParkingTicket

class TestParkingTicket(unittest.TestCase):
    def test_four_wheeler_parking_ticket(self):
        curr_parking_spot = next(FourWheelerParkingTicket.ticket_counter)
        start = curr_parking_spot + 1
        end = start + 100
        for i in range(start, end):
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
