import cmd

from parking_lot.parking_lot_command import (
    FourWheelerParkingLotCommand, 
    CreateFourWheelerParkingLot, ParkFourWheelerCommand, 
    LeaveFourWheelerParkingLotCommand, FourWheelerParkingLotStatus, 
    FourWheeelerRegNosWithColor, FourWheelerParkingSpotNosFromVehicleColor, 
    FourWheelerParkingSpotNoFromRegNo
)

class ParkingLotPrompt(cmd.Cmd):
    prompt = 'parking-lot$ '
    file = None

    def execute(self, command: FourWheelerParkingLotCommand):
        print(command.execute())

    def do_create_parking_lot(self, max_four_wheeler_spots):
        'Create parking-lot:  create_parking_lot <MAX-NUMBER-OF-FOUR-WHEELER-SPOTS>'
        max_four_wheeler_spots = int(max_four_wheeler_spots)
        command = CreateFourWheelerParkingLot(max_four_wheeler_spots)
        self.execute(command)
        # print(FourWheelerParkingLotCommand.create_parking_lot(max_four_wheeler_spots))

    def do_park(self, args):
        registration_number, color = args.split(' ')
        'Park vehicle:  park <VEHICLE-REGISTRATION-NUMBER> <VEHICLE-COLOR>'
        command = ParkFourWheelerCommand(registration_number, color)
        self.execute(command)

    def do_leave(self, parking_spot_id):
        'Unpark vehicle:  leave <PARKING-SPOT-NUMBER>'
        parking_spot_id = int(parking_spot_id)
        command = LeaveFourWheelerParkingLotCommand(parking_spot_id)
        self.execute(command)

    def do_status(self, *args):
        'Status of parking-lot:  status'
        command = FourWheelerParkingLotStatus()
        self.execute(command)

    def do_registration_numbers_for_cars_with_colour(self, color):
        'Print registration numbers of cars with given particular color:  registration_numbers_for_cars_with_colour <VEHICLE-COLOR>'
        command = FourWheeelerRegNosWithColor(color)
        self.execute(command)

    def do_slot_numbers_for_cars_with_colour(self, color):
        'Print parking-slot numbers of cars with given particular color:  slot_numbers_for_cars_with_colour <VEHICLE-COLOR>'
        command = FourWheelerParkingSpotNosFromVehicleColor(color)
        self.execute(command)

    def do_slot_number_for_registration_number(self, registration_number):
        'Print slot-number for car with given registration number:  slot_number_for_registration_number <VEHICLE-REGISTRATION-NUMBER>'
        command = FourWheelerParkingSpotNoFromRegNo(registration_number)
        self.execute(command)

    def do_exit(self, *args, **kwargs):
        'Terminate the shell and exit: exit'
        return True

    # ----- playback -----
    def do_playback(self, arg):
        'Playback commands from a file:  playback <file-path>'
        self.close()
        with open(arg) as f:
            self.cmdqueue.extend(f.read().splitlines())

    def close(self):
        if self.file:
            self.file.close()
            self.file = None

if __name__ == '__main__':
    ParkingLotPrompt().cmdloop()
