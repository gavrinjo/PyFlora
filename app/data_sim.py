import numpy as np
from datetime import datetime
from random import randint
from app import db
from app.models import Gauge, SensorMeasurements
from app.repo import Weather

class Sensor():

    def __init__(self, pot, measurement) -> None:
        self.pot = pot
        self.measurement = measurement

    def build(self):
        attribs = {}
        columns = self.columns(self.pot)
        for column in columns:
            if getattr(self.pot, column) == 1:
                default_value, min_value, max_value, off_value = self.gauge_values(column)
                measured_value = getattr(self.measurement, column[:column.find('_')])
                if measured_value is not None:
                    val = self.simulate(measured_value, min_value, max_value, off_value)
                else:
                    val = self.simulate(default_value, min_value, max_value, off_value)
            else:
                val = None
            attribs[column] = val
        temperature = round(Weather('Zagreb').temperature)
        measurement = SensorMeasurements(
            sunlight=attribs['sunlight'],
            moisture=attribs['moisture'],
            reaction=attribs['reaction'],
            nutrient=attribs['nutrient'],
            salinity=attribs['salinity'],
            temperature=temperature)
        measurement.measured = datetime.utcnow()
        measurement.pot = self.pot
        return measurement
        

    def columns(self, pot):
        cols = []
        for c in db.inspect(pot).attrs:
            if c.key.endswith("status"):
                cols.append(c.key)
        return cols
    
    def gauge_values(self, column):

        data = db.session.execute(db.select(Gauge).filter_by(name=column[:column.find('_')], eiv=5)).scalar_one()
        max_value = data.max_value
        min_value = data.min_value
        avg_value = int(np.floor((max_value + min_value) / 2))
        off_value = int(np.floor(np.log10(max_value) * 2))

        return avg_value, min_value, max_value, off_value

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

