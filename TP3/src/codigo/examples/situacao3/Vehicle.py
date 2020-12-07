class Vehicle:
    def __init__(self, brand, model, type):
        self.brand = brand
        self.model = model
        self.type = type
        self.gas_tank_size = 14
        self.fuel_level = 0
 
    def fuel_up(self):
        self.fuel_level = self.gas_tank_size
        print('Gas tank is now full.')
 
    def drive(self):
        print(f'The {self.model} is now driving.') 
