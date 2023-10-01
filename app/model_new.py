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
        return f'User {self.username}'
    
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
    values = db.relationship('Value', backref='plant', lazy='dynamic')

    def __repr__(self):
        return f'plant {self.name}'


class Value(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64)) # sunlight, temperature, moisture, reaction, nutrient, salinity
    min_value = db.Column(db.Integer)
    max_value = db.Column(db.Integer)
    unit = db.Column(db.String(64))
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'))


class Pot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(256))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'))
    sensors = db.relationship('Sensor', backref='pot', lazy='dynamic')

    def __repr__(self):
        return f'pot {self.name}'
    
    def get_plant(self, id):
        return Plant.query.get(id)
    
    def get_user(self, id):
        return User.query.get(id)


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64)) # sunlight, temperature, moisture, reaction, nutrient, salinity
    active = db.Column(db.Boolean, default=False) # senzor aktivan -> True / False
    pot_id = db.Column(db.Integer, db.ForeignKey('pot.id'))
    readings = db.relationship('Reading', backref='sensor', lazy='dynamic')


class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer) # vrijednost očitanja senzora
    unit = db.Column(db.String(64)) # mjerna jedinica očitanja
    created = db.Column(db.DateTime, default=datetime.utcnow) # vrijeme mjerenja
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))


class Gauge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False) # indicator value (1-10)
    name = db.Column(db.String(64))
    min_value = db.Column(db.Integer, nullable=False) # min value for given 'level'
    max_value = db.Column(db.Integer, nullable=False) # max value for given 'level'
    unit = db.Column(db.String(64)) # measuring unit
    description = db.Column(db.String(128))

@login.user_loader
def load_user(id):
    return User.query.get(id)


p = Plant()
p.name = 'ime'
p.description = 'opis'
p.substrate = 'supstrati'
db.session.add(p)
db.session.flush()
v = Value()
v.name = 'salinity'
v.min_value = 15
v.max_value = 25
v.unit = "%"
v.plant_id = p
db.session.add(v)
db.session.commit()