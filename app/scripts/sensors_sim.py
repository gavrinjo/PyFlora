
import numpy as np
from random import randint
from app import db
from app.models import Gauge, Sensor, Reading
from app.scripts.weather import Weather



class SensorSim():

    def __init__(self, pot) -> None:
        self.pot = pot
        self.sensors = Sensor.query.filter_by(pot_id=pot.id)


    def get_ref_values(self, query: object) -> tuple:
        min_array = [getattr(x, 'min_value') for x in query] # array of minimum values column
        min_median = np.median(min_array) # median value of minimum values array, used as minimum value
        max_array = [getattr(x, 'max_value') for x in query] # array of maximum values column
        max_median = np.median(max_array) # median value of maximum values array, used as maximum value
        std_value = np.ceil(np.median([min_median, max_median])) # median value over minimum and maximum values, used as standard value
        off_value = np.ceil(std_value * 0.1) # 10% of median value over minimum and maximum values, used as offset value
        return min(min_array), max(max_array), std_value, off_value


    def get_random_value(self, value: int, min_value: int, max_value: int, offset: int) -> int:

        if value <= min_value:
            mi = min_value
        else:
            mi = value - offset

        if value >= max_value:
            mx = max_value
        else:
            mx = value + offset

        return randint(mi, mx)
    

    def generate(self) -> object:

        for sensor in self.sensors:
            if sensor.active:
                if sensor.indicator != 'temperature':
                    query = Gauge.query.filter_by(name=sensor.indicator).all()
                    ds = self.get_ref_values(query)
                    try:
                        value = self.get_random_value(sensor.last_reading(sensor.id).value, ds[0], ds[1], ds[3])
                    except:
                        value = self.get_random_value(ds[2], ds[0], ds[1], ds[3])

                    reading = Reading()
                    reading.value = value
                    # reading.unit = sensor.unit
                    reading.sensor = sensor
                else:
                    value = round(float(Weather('Zagreb').temperature['value']))
                db.session.add(reading)
                db.session.commit()
