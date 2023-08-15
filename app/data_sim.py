from random import randint
from app import db

class Sensor():

    def __init__(self, pot, measurement) -> None:
        self.pot = pot
        self.measurement = measurement

    def columns(self, pot):
        cols = []
        for c in db.inspect(pot).attrs:
            if c.key.endswith("status"):
                cols.append(c.key)
        return cols
    
    def status(self, columns):
        for c in columns:
            if getattr(self.pot, c) == 0:
                print()
                # self.simulate()

    def simulate(self, value, min_value, max_value, offset):
        """Randomize and return multi sensor data set

        Returns:
            tuple: Resturns tuple of sensor data in particular order (ph, salinity, moisture)
        """
        if value is None:
            return (value, min_value, max_value)

        else:
            if value <= min_value:
                mi = min_value
            else:
                mi = value - offset

            if value >= max_value:
                mx = max_value
            else:
                mx = value + offset

            return randint(mi, mx)
            # return self.randomizer(value, min_value, max_value, offset)
            # ph_range = self.randomizer(1, 14, 1, int(self.mesurement.ph_range))
            # salinity = self.randomizer(1,32, 1, int(self.mesurement.salinity))
            # moisture = self.randomizer(0, 1, 0.1, float(self.mesurement.moisture))
        
            # return (ph_range, salinity, moisture)


    # def randomizer(self, value, min_value, max_value, offset):
    #     """Random sensor data
    
    # for c in db.inspect(Pot).attrs:     
    #     if c.key.endswith("status"):
    #         print(c.key)

    #     Args:
    #         minimal (int, float): Minimal sensor value
    #         maximal (int, float): Maximal sensor value
    #         offset (int, float): Offset from measured value in both directions
    #         value (int, float): Existing or default measured value

    #     Returns:
    #         int,float: randomized value
    #     """
    #     if value <= min_value:
    #         mi = min_value
    #     else:
    #         mi = value - offset

    #     if value >= max_value:
    #         mx = max_value
    #     else:
    #         mx = value + offset

    #     return choice([mi, value, mx])

