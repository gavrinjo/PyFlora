from random import choice

class SensorData():

    def __init__(self, mesurement) -> None:
        self.mesurement = mesurement


    def data(self):
        """Randomize and return multi sensor data set

        Returns:
            tuple: Resturns tuple of sensor data in particular order (ph, salinity, moisture)
        """

        if self.mesurement is None:
            return (7, 8, 0.5)

        else:
            ph_range = self.randomizer(1, 14, 1, int(self.mesurement.ph_range))
            salinity = self.randomizer(1,32, 1, int(self.mesurement.salinity))
            moisture = self.randomizer(0, 1, 0.1, float(self.mesurement.moisture))
        
            return (ph_range, salinity, moisture)


    def randomizer(self, minimal, maximal, offset, value):
        """Random sensor data

        Args:
            minimal (int, float): Minimal sensor value
            maximal (int, float): Maximal sensor value
            offset (int, float): Offset from measured value in both directions
            value (int, float): Existing or default measured value

        Returns:
            int,float: randomized value
        """
        if value <= minimal:
            mi = minimal
        else:
            mi = value - offset

        if value >= maximal:
            mx = maximal
        else:
            mx = value + offset

        return choice([mi, value, mx])

