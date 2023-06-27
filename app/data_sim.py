from random import choice

class SensorData():

    def __init__(self) -> None:
        self.salinity = choice(range(1, 50))
        self.ph_range = choice(range(1, 15))
        self.moisture = choice(range(1, 50))


