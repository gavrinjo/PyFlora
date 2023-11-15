import os
import json
from datetime import datetime
from hashlib import md5
from time import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from sqlalchemy import event
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    address = db.Column(db.String(64), index=True)
    postcode = db.Column(db.String(64), index=True)
    city = db.Column(db.String(64), index=True)
    country = db.Column(db.String(64), index=True)
    phone = db.Column(db.String(64), index=True)
    mobile = db.Column(db.String(64), index=True)
    about_me = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
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
    photo = db.Column(db.String(64))
    description = db.Column(db.String(1024))
    soil_texture = db.Column(db.String(64))
    substrate = db.Column(db.String(256))
    wiki_url = db.Column(db.String(256))
    other_url = db.Column(db.String(256))
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


@login.user_loader
def load_user(id):
    return User.query.get(id)

@event.listens_for(User.__table__, 'after_create')
def add_users(*args, **kwargs):
    admin = User()
    admin.username='admin'
    admin.email='administrator@email.com'
    admin.is_admin = True
    admin.set_password('0000')
    db.session.add(admin)
    db.session.commit()

@event.listens_for(Plant.__table__, 'after_create')
def add_plants(*args, **kwargs):
    statis_path = current_app.config['UPLOADS_DEFAULT_DEST']
    with open(os.path.join(statis_path, 'plants.json'), "r") as file:
        data = json.load(file)
        for plant_item in data:
            plant = Plant()
            plant.name = plant_item['name']
            plant.description = plant_item['description']
            plant.soil_texture = plant_item['soil_texture']
            plant.substrate = plant_item['substrate']
            plant.wiki_url = plant_item['wiki_url']
            plant.other_url = plant_item['other_url']
            plant.photo = plant_item['photo']
            db.session.add(plant)
        db.session.commit()

@event.listens_for(Value.__table__, 'after_create')
def add_plant_values(*args, **kwargs):
    statis_path = current_app.config['UPLOADS_DEFAULT_DEST']
    # plant = Plant.query.get(1)
    with open(os.path.join(statis_path, 'plants.json'), "r") as file:
        data = json.load(file)
        for plant in data:
            plant_id = Plant.query.get(plant['id'])
            for plant_value in plant['values']:
                value = Value()
                value.indicator = plant_value['indicator']
                value.min_value = plant_value['min_value']
                value.max_value = plant_value['max_value']
                value.unit = plant_value['unit']
                value.plant = plant_id
                db.session.add(value)
        db.session.commit()

@event.listens_for(Pot.__table__, 'after_create')
def add_pot(*args, **kwargs):
    user = User.query.get(1)
    pot = Pot()
    pot.name = 'Default empty pot'
    pot.owner = user
    db.session.add(pot)
    db.session.commit()

@event.listens_for(Sensor.__table__, 'after_create')
def add_pot(*args, **kwargs):
    pot = Pot.query.get(1)
    for sensor_indicator in current_app.config['MEASURES']:
        sensor = Sensor()
        sensor.indicator = sensor_indicator
        sensor.pot = pot
        db.session.add(sensor)
    db.session.commit()

@event.listens_for(Gauge.__table__, 'after_create')
def create_gauge(*args, **kwargs):
    statis_path = current_app.config['UPLOADS_DEFAULT_DEST']
    with open(os.path.join(statis_path, 'gauge.json')) as file:
        data = json.load(file)
        for item in data:
            gauge = Gauge()
            gauge.name = item['name']
            gauge.min_value = item['min_value']
            gauge.max_value = item['max_value']
            gauge.avg_value = item['avg_value']
            gauge.off_value = item['off_value']
            gauge.unit = item['unit']
            db.session.add(gauge)
        db.session.commit()
