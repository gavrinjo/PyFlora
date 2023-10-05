
import numpy as np
from random import randint
from app import db
from app.models import Gauge, Sensor, Reading
from app.scripts.weather import Weather



class SensorSim():

    def __init__(self, pot) -> None:
        self.pot = pot
        self.sensors = Sensor.query.filter_by(pot_id=pot.id)

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
        weather = Weather('Zagre')
        for sensor in self.sensors:
            if sensor.active:
                if sensor.indicator != 'temperature':
                    gauge = Gauge.query.filter_by(name=sensor.indicator).first()
                    try:
                        value = self.get_random_value(sensor.last_reading(sensor.id).value, gauge.min_value, gauge.max_value, gauge.off_value)
                    except:
                        value = self.get_random_value(gauge.avg_value, gauge.min_value, gauge.max_value, gauge.off_value)
                    unit = gauge.unit
                else:
                    value = round(float(weather.temperature['value']))
                    unit = '°C'
                reading = Reading()
                reading.value = value
                reading.unit = unit
                reading.sensor = sensor
                db.session.add(reading)
                db.session.commit()
