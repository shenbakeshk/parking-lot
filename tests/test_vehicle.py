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
