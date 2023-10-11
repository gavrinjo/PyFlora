from datetime import datetime
from hashlib import md5
from time import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    about_me = db.Column(db.String(256))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    pots = db.relationship('Pot', backref='owner', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    photo = db.Column(db.String(64), nullable=False, default='default.jpg') # ovo ću naknadno napraviti
    description = db.Column(db.String(256))
    substrate = db.Column(db.String(128)) # recomendation
    # soil_texture = db.Column(db.String(64)) # fine, medium, coarse ovo nam možda i neće trebati
    created = db.Column(db.DateTime, default=datetime.utcnow)
    pots = db.relationship('Pot', backref='plant', lazy='dynamic')
    values = db.relationship('Value', backref='plant', lazy='dynamic', cascade='all, delete')

    def __repr__(self):
        return f'<Plant {self.name}>'


class Value(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String(64)) # sunlight, temperature, moisture, reaction, nutrient, salinity
    min_value = db.Column(db.Integer)
    max_value = db.Column(db.Integer)
    unit = db.Column(db.String(64))
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)


class Pot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(256))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    synced = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'))
    sensors = db.relationship('Sensor', backref='pot', lazy='dynamic', cascade='all, delete')

    def __repr__(self):
        return f'<Pot {self.name}>'
    
    def get_plant(self, id):
        return Plant.query.get(id)
    
    def get_user(self, id):
        return User.query.get(id)


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String(64)) # sunlight, temperature, moisture, reaction, nutrient, salinity
    active = db.Column(db.Boolean, default=False) # senzor aktivan -> True / False
    pot_id = db.Column(db.Integer, db.ForeignKey('pot.id'), nullable=False)
    readings = db.relationship('Reading', backref='sensor', lazy='dynamic', cascade='all, delete')

    def last_reading(self, id):
        return Reading.query.filter_by(sensor_id=id).order_by(Reading.measured.desc()).first()


class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer) # vrijednost očitanja senzora
    unit = db.Column(db.String(64)) # mjerna jedinica očitanja
    measured = db.Column(db.DateTime, default=datetime.utcnow) # vrijeme mjerenja
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)


class Gauge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    min_value = db.Column(db.Integer, nullable=False) # minimum value in measurnig scale
    max_value = db.Column(db.Integer, nullable=False) # maximum value in measuring scale
    avg_value = db.Column(db.Integer, nullable=False) # average value in measurnig scale
    off_value = db.Column(db.Integer, nullable=False) # +-offset of measured or average value
    unit = db.Column(db.String(64)) # measuring unit


""" stara Gauge klasa, nepotrebno
class Gauge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ei = db.Column(db.String(64), nullable=False) # ellenberg indicator [L,T,F,R,N,S]
    eiv = db.Column(db.Integer, nullable=False) # ellenberg indicator value
    name = db.Column(db.String(64))
    min_value = db.Column(db.Integer, nullable=False) # min value for given 'EIV'
    max_value = db.Column(db.Integer, nullable=False) # max value for given 'EIV'
    unit = db.Column(db.String(64)) # measuring unit
    description = db.Column(db.String(128))
"""


""" stara Measurement klasa, nepotrebno
class Measurements(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sensor = db.Column(db.String(64))
    value = db.Column(db.Integer)
    unit = db.Column(db.String(64))
    measured = db.Column(db.DateTime)
    pot_id = db.Column(db.Integer, db.ForeignKey('pot.id'))

    def __repr__(self):
        return f'< {self.sensor} : {self.value}[{self.unit}], Measured at : {self.measured}, Pot : {self.pot_id} >'

    @property
    def serialize(self):
        data = {
            'x_dataset': self.measured.strftime('%d.%m.%Y - %H:%M:%S.%f'), #.isoformat() + 'Z'
            'y_dataset': {self.sensor : self.value}
        }
        return data
"""


""" stara SensorMeasurements klasa, nepotrebno
class SensorMeasurements(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    sunlight = db.Column(db.Integer) # [lux]
    temperature = db.Column(db.Integer) # [°C]
    moisture = db.Column(db.Integer) # [%]
    reaction = db.Column(db.Integer) # [pH]
    nutrient = db.Column(db.Integer) # [%]
    salinity = db.Column(db.Integer) # [%]

    measured = db.Column(db.DateTime)

    pot_id = db.Column(db.Integer, db.ForeignKey('pot.id'))

    def __repr__(self):
        return f'<Measured at {self.measured} -> {self.sunlight}/{self.temperature}/{self.moisture}/{self.reaction}/{self.nutrient}/{self.salinity} >'

    def get_pot(self, id):
        return Pot.query.get(id)
    
    @staticmethod
    def map_values(value, min_value, max_value):
        return [value, np.interp(value, [min_value, max_value], [1, 10])]

    @property
    def sunlight_prop(self):
        data = {'x': self.measured.strftime('%d.%m.%Y - %H:%M:%S.%f'), 'y': self.sunlight}
        return data

    @property
    def serialize(self):
        data = {
            'x_dataset': self.measured.strftime('%d.%m.%Y - %H:%M:%S.%f'), #.isoformat() + 'Z'
            'y_dataset': {
                'sunlight' : self.map_values(self.sunlight, 1, 100000),
                'temperature': self.map_values(self.temperature, -20, 60),
                'moisture': self.map_values(self.moisture, 0, 100),
                'reaction': self.map_values(self.reaction, 0, 14),
                'nutrient': self.map_values(self.nutrient, 0, 100),
                'salinity': self.map_values(self.salinity, 0, 16)
            }
        }
        return data
"""





@login.user_loader
def load_user(id):
    return User.query.get(id)