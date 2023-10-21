# import matplotlib.pyplot as plt
import os
import secrets
from flask import current_app, abort


# db.session.execute(db.select(User)).first() -> ovo radi, objašnjeno (https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/), query je stari način

# dodavanje bulk u tablicu baze
# db.session.execute(Pot.__table__.insert(), dict) -> gdje je dict python dictionary object (ili lista dictionarija)

# a radi i ovako gdje je dict python dictionary object
# obj_data = Pot(**dict)   
# db.session.add(obj_data)

def upload_image(form_image, folder): #nova funkcija, za uploadanje slika, potrebno
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
