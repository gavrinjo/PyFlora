import sqlite3
import json
import os
from werkzeug.security import generate_password_hash

def json2sql():
    basedir = os.path.abspath(os.path.dirname('__name__'))
    db = os.path.join(basedir, "app.db")
    resources = os.path.normpath(os.path.join(basedir, 'app/static'))
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    # dodaj ADMIN korisnika u bazu
    cursor.execute(
        "INSERT INTO user (username, email, password_hash, is_admin, created) VALUES (?, ?, ?, 1, CURRENT_TIMESTAMP)",
        ('admin', 'admin@email.com', generate_password_hash('0000'))
    )
    connection.commit()

    # dodaj prazan lonac u bazu
    cursor.execute(
        "INSERT INTO pot (name, created, user_id) VALUES ('dummy_pot', CURRENT_TIMESTAMP, 1)"
    )
    connection.commit()
    
    # dodaj 10 predefiniranih biljaka i njihovih vrijednosti u bazu
    with open(os.path.join(resources, 'plants.json'), "r") as file:
        data = json.load(file)
        for item in data:
            cursor.execute(
                "INSERT INTO plant (id, name, photo, description, soil_texture, substrate, wiki_url, other_url, created) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                (item['id'], item['name'], item['photo'], item['description'], item['soil_texture'], item['substrate'], item['wiki_url'], item['other_url'])
            )
            connection.commit()
            for value in item['values'] :
                cursor.execute(
                    "INSERT INTO value (indicator, min_value, max_value, unit, plant_id) VALUES (?, ?, ?, ?, ?)",
                    (value['indicator'], value['min_value'], value['max_value'], value['unit'], value['plant_id'])
                )
                connection.commit()
    
    # dodaj nominalne vrijednosti u bazu
    with open(os.path.join(resources, 'gauge.json')) as file:
        data = json.load(file)
        for item in data:
            cursor.execute(
                "INSERT INTO gauge (name, min_value, max_value, avg_value, off_value, unit) VALUES (?, ?, ?, ?, ?, ?)",
                (item['name'], item['min_value'], item['max_value'], item['avg_value'], item['off_value'], item['unit'])
            )
            connection.commit()
    connection.close()


if __name__ == '__main__':
    json2sql()
