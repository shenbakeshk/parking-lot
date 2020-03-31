import unittest

from parking_lot.constants import VehicleType
from parking_lot.parking_spot import FourWheelerSpot
from parking_lot.parking_ticket import FourWheelerParkingTicket
from parking_lot.vehicle import Car

class TestVehicle(unittest.TestCase):
    cars_config = (
        ("KA-01-HH-1234", "White"), 
        ("KA-01-HH-9999", "White"), 
        ("KA-01-BB-0001", "Black"), 
        ("KA-01-HH-7777", "Red"), 
        ("KA-01-HH-2701", "Blue"), 
        ("KA-01-HH-3141", "Black"),
    )

    def test_vehicle_color_is_lower_case(self):
        """
        Assert if car's color is lower-case.
        """
        for car_config in TestVehicle.cars_config:
            car = Car(*car_config)
            self.assertTrue(car.color.islower())
    
    def test_vehicle_reg_no_is_upper_case(self):
        """
        Assert if car's registration number is upper-case.
        """
        for car_config in TestVehicle.cars_config:
            car = Car(*car_config)
            self.assertTrue(car.registration_number.isupper())

    def test_vehicle_type(self):
        """
        Assert if vehicle(car) type is VehicleType.
        """
        for car_config in TestVehicle.cars_config:
            car = Car(*car_config)
            self.assertIsInstance(car.type_, VehicleType)
    
    def test_vehicle_parking_ticket_assignment(self):
        assigned_ticket_ids = set()
        for car_config in TestVehicle.cars_config:
            car = Car(*car_config)
            parking_ticket = FourWheelerParkingTicket()
            car.ticket = parking_ticket
            self.assertNotIn(parking_ticket.id_, assigned_ticket_ids)

    def test_type_predicate(self):
        for car_config in TestVehicle.cars_config:
            car = Car(*car_config)
            self.assertTrue(car.type_predicate(VehicleType.CAR))

    def test_allocate_parking_spot(self):
        for car_config in TestVehicle.cars_config:
            car = Car(*car_config)
            parking_spot = FourWheelerSpot()

            # check vehicle's parking-spot before allocation
            self.assertFalse(car.is_vehicle_parked())

            # check vehicle's parking-spot after allocation
            car.allocate_parking_spot = parking_spot
            self.assertTrue(car.is_vehicle_parked())

    def test__deallocate_parking_spot(self):
        for car_config in TestVehicle.cars_config:
            car = Car(*car_config)
            parking_spot = FourWheelerSpot()

            # allocate parking-spot
            car.allocate_parking_spot = parking_spot

            # parking-spot deallocation
            car._deallocate_parking_spot()
            self.assertFalse(car.is_vehicle_parked())
            self.assertIsNone(car.parking_spot)
            self.assertIsNone(car.ticket)

    def test_is_vehicle_parked(self):
        for car_config in TestVehicle.cars_config:
            car = Car(*car_config)
            parking_spot = FourWheelerSpot()

            # check parking-spot allocation
            car.allocate_parking_spot = parking_spot
            self.assertTrue(car.is_vehicle_parked())

            # check parking-spot deallocation
            car._deallocate_parking_spot()
            self.assertFalse(car.is_vehicle_parked())
