from datetime import datetime
import unittest

from parking_lot.parking_ticket import FourWheelerParkingTicket

class TestParkingTicket(unittest.TestCase):
    def test_four_wheeler_parking_ticket(self):
        for i in range(1, 11):
            ticket = FourWheelerParkingTicket()
            self.assertEqual(i, ticket.id_)
            self.assertIsInstance(ticket, FourWheelerParkingTicket)
            self.assertIsInstance(ticket.entry_time, datetime)
