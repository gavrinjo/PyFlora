# import matplotlib.pyplot as plt
import os
import secrets
from flask import current_app, abort
from app import db
from app.models import Gauge
import json


# db.session.execute(db.select(User)).first() -> ovo radi, objašnjeno (https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/), query je stari način

# dodavanje bulk u tablicu baze
# db.session.execute(Pot.__table__.insert(), dict) -> gdje je dict python dictionary object (ili lista dictionarija)

# a radi i ovako gdje je dict python dictionary object
# obj_data = Pot(**dict)   
# db.session.add(obj_data)

def upload_image(form_image, folder): #nova funkcija, za uploadanje slika, potrebno
    if form_image:
        random_hex = secrets.token_hex(8)
        file_ext = os.path.splitext(form_image.filename)[1]
        if file_ext not in current_app.config['UPLOADED_FILES_ALLOW']:
            abort(400)
        else:
            filename = random_hex + file_ext
            filename_path = os.path.normpath(os.path.join(current_app.config['UPLOADS_DEFAULT_DEST'], folder, filename))
            form_image.save(filename_path)
            return filename

# c = SensorMeasurements.__table__.columns.keys()[1:-2]
# a = pd.DataFrame(db.session.execute(db.select(SensorMeasurements).filter_by(pot_id=pot.id).order_by(SensorMeasurements.measured.desc())).all())

def load_gauge():
    base_dir = current_app.config['UPLOADS_DEFAULT_DEST']
    db.session.execute(Gauge.__table__.insert(), json.loads(open(os.path.join(base_dir, 'gauge.json')).read()))
    db.session.commit()

def json2sql():
    import sqlite3
    import json
    from werkzeug.security import generate_password_hash
    basedir = os.path.abspath(os.path.dirname(__file__))
    db = os.path.join(basedir, "app.db")
    resources = os.path.normpath(os.path.join(basedir, 'app/resources'))
    connection = sqlite3.connect(db)

    # dodaj ADMIN korisnika u bazu
    connection.execute(
        "INSERT INTO user (username, email, password_hash, is_admin, created) VALUES (?, ?, ?, 1, CURRENT_TIMESTAMP)",
        'admin', 'admin@email.com', generate_password_hash('0000')
    )
    connection.commit()

    # dodaj prazan lonac u bazu
    connection.execute(
        "INSERT INTO pot (name, created) VALUES (?, CURRENT_TIMESTAMP)",
        'dummy pot'
    )
    connection.commit()
    
    # dodaj 10 predefiniranih biljaka i njihovih vrijednosti u bazu
    with open(os.path.join(resources, 'plants.json'), "r") as file:
        data = json.load(file)
        for item in data:
            connection.execute(
                "INSERT INTO plant (id, name, photo, description, substrate, created) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                item['id'], item['name'], item['photo'], item['description'], item['substrate']
            )
            connection.commit()
            for value in item['values'] :
                connection.execute(
                    "INSERT INTO value (indicator, min_value, max_value, unit, plant_id) VALUES (?, ?, ?, ?, ?)",
                    value['indicator'], value['min_value'], value['max_value'], value['unit'], value['plant_id']
                )
                connection.commit()
    
    # dodaj nominalne vrijednosti u bazu
    with open(os.path.join(resources, 'gauge.json')) as file:
        data = json.load(file)
        for item in data:
            connection.execute(
                "INSERT INTO gauge (name, min_value, max_value, avg_value, off_value, unit) VALUES (?, ?, ?, ?, ?, ?)",
                item['name'], item['min_value'], item['max_value'], item['avg_value'], item['off_value'], item['unit']
            )
            connection.commit()
    connection.close()
