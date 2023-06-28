from random import choice, uniform, random

class SensorData():
    """
    traži id posude i zadnji datum mjerenja,
        1. ako mjerenje ne postoji, onda postavlje neutralne vrijednosti.
        2. ako mjerenje postoji, onda uzima random vrijednost u rasponu od +-1 od zadnjeg mjerenja. 
    """

    def __init__(self, mesurement) -> None:
        self.mesurement = mesurement
        # self.salinity = self.soil_slinity_scale() #choice(range(1, 32))
        # self.ph_range = choice(range(1, 15))
        # self.moisture = choice(range(1, 50))



    def soil_salinity(self):
        # soil salinity scale
        # 0-2 -> None -> very sensitive crop
        # 2-4 -> Low -> sensitive crop
        # 4-8 -> Medium -> medium sensitive crop
        # 8-16 -> High -> medium resistant crop
        # > 16 -> Severe -> resistant crop
        try:
            self.mesurement.salinity
        except AttributeError:
            new_value = 8
        else:
            ref_value = self.mesurement.salinity
            new_value = choice(range(ref_value-1, ref_value+2))
        return new_value
    
    def soil_moisture(self):
        # soil moisture scale
        # 0     extremely dry soil
        # 0,1   extremely dry soil
        # 0,2   well drained soil
        # 0,3   well drained soil
        # 0,4   moist soil
        # 0,5   moist soil
        # 0,6   moist soil
        # 0,7   wet soil
        # 0,8   wet soil
        # 0,9   extremely wet soil
        # 1     extremely wet soil

        try:
            self.mesurement.moisture
        except AttributeError:
            new_value = 0.5
        else:
            ref_value = float(self.mesurement.moisture)
            new_value = uniform(ref_value-0.1, ref_value+0.2)
        return new_value
    
    def soil_ph(self):
        # soil pH
        # <7 - acidic
        # =7 - neutral
        # >7 - alkaline

        try:
            self.mesurement.ph_range
        except AttributeError:
            new_value = 7
        else:
            ref_value = self.mesurement.ph_range
            new_value = choice(range(ref_value-1, ref_value+2))
        return new_value
            