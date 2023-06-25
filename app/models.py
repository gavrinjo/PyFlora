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

    about_me = db.Column(db.String(256))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

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
    # photo = db.Column(db.LargeBinary) # ovo ću naknadno napraviti
    # Requirements
    salinity = db.Column(db.String(64)) # None, Low, Medium, High (postoji senzor)
    temperature = db.Column(db.Integer) # ~20 (celzijevih) (senzor temperature i vlažnisti zraka, postoji rpi)
    ph_range = db.Column(db.String(64)) # 6-8 (senzot pH vrijednosti tla, postoji rpi)
    moisture = db.Column(db.String(64)) #  Low, Medium, High (senzor za vlažnost tla, postoji rpi)

    shade = db.Column(db.String(64)) # Intolerant, Intermediate, Tolerant (senzor za svjetlo, photoresistor)
    # drought = db.Column(db.String(64)) # None, Low, Medium, High (ovo nam ne treba za seminarski)
    soil_texture = db.Column(db.String(64)) # fine, medium, coarse
    # precipitation = db.Column(db.Integer) # 8-26
    substrate = db.Column(db.String(128)) # recomendation
    description = db.Column(db.String(256))
    
    pots = db.relationship('Pot', backref='pot', lazy='dynamic')

    def __repr__(self):
        return f'<Plant {self.name}>'

class Pot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'))

    def __repr__(self):
        return f'<Pot {self.name}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))