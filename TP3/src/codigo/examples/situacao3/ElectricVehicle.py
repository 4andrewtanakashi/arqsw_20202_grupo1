from Vehicle import Vehicle

class ElectricVehicle(Vehicle):

    horse_power = 100

    def __init__(self, brand, model, type):
        super().__init__(brand, model, type)
        self.battery_size = 85
        self.charge_level = 0

    speed_run = 200
    print("Show me now !")

    def charge(self):
        self.charge_level = 100
        print('The vehicle is now charged.')

    def fuel_up(self):
        print('This vehicle has no fuel tank!')

    def power():
        print("HP: {}, speed: {}".format(str(ElectricVehicle.horse_power), str(ElectricVehicle.speed_run)))

ElectricVehicle.power()
