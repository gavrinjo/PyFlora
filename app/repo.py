# import matplotlib.pyplot as plt
import os
import json
import io
import base64
import secrets
from datetime import datetime
import numpy as np
import pandas as pd
from requests import get
from contextlib import closing
from matplotlib.figure import Figure
import xmltodict

from app import db
from sqlalchemy.inspection import inspect
from .functions import bp
from app.models import User, Plant, Pot, SensorMeasurements, Gauge
from flask import current_app, request, abort


COLUMNS = ['sunlight', 'temperature', 'moisture', 'reaction', 'nutrient', 'salinity']

class PyGraf(Figure):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _save(self, file_name):
        self.savefig(f'{file_name}.png', format='png')

    def represent_chart(self):
        buf = io.BytesIO()
        self.savefig(buf, format="png")
        return base64.b64encode(buf.getbuffer()).decode("ascii")


class Line(PyGraf):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_tight_layout(True)
        self.ax = self.subplots()
    
    def plot(self, x_axis, y_axis, color, label):
        # print(x_axis[0])
        # print(type(x_axis[0]))
        fdates = [x.strftime('%d-%m-%Y\n%H:%M:%S.%f') for x in x_axis]
        # fmt = mdates.DateFormatter('%S.%f')
        self.ax.grid(True)
        self.ax.plot(fdates, y_axis, marker='.' , color=color, label=label) # line chart
        # self.ax.xaxis.set_major_formatter(fmt)
        # self.autofmt_xdate(rotation=45)
        self.ax.set_xticklabels(fdates, rotation=45, ha='right', color="grey", size=6)
        # self.ax.xaxis.set_major_locator(dates.MicrosecondLocator(interval=10000000, tz=None))
        # self.ax.xaxis.set_ticks(data['measured'])
        # self.ax.yaxis.set_ticks(y_axis)
        # self.ax.margins(x=0, y=0)
        self.ax.legend()
    
    def build(self, pot, metrics, column, color):
        columns = ['measured', 'temperature', 'moisture', 'salinity', 'reaction', 'sunlight', 'nutrient']
        query = (
            metrics.query
            .with_entities(
                metrics.measured,
                metrics.temperature,
                metrics.moisture,
                metrics.salinity,
                metrics.reaction,
                metrics.sunlight,
                metrics.nutrient
            )
            .filter_by(pot_id=pot.id)
            .order_by(metrics.measured.desc()).limit(7)
        )
        df = pd.DataFrame(query, columns=columns)

        return self.plot(df['measured'], df[column], color, column.capitalize())



class Histogram(PyGraf):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_tight_layout(True)
        self.ax = self.subplots()
    
    def plot(self, values, bins, label):
        self.ax.grid(True, linestyle=':', linewidth=1)
        self.ax.hist(values, bins=bins, label=label, edgecolor='black') # hist chart
        self.ax.axvline(29, color='red', label='avg medan')
        # self.ax.margins(x=0, y=0)
        self.ax.legend()


class Radar(PyGraf):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ax = self.subplots(subplot_kw=dict(polar=True))
        # self.angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    

    def plot(self, labels, values, color, text):
        
        N = len(labels)
        values = values
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]
        # ax = self.subplots(subplot_kw=dict(polar=True))
        self.ax.set_theta_offset(np.pi / 2)
        self.ax.set_theta_direction(-1)
        self.ax.set_thetagrids(np.degrees(angles[:-1]), labels, size=10, fontweight="bold")
        self.ax.tick_params(pad=10, grid_linestyle=':')
        self.ax.set_rticks(range(0, 10, 2), range(0, 10, 2), color="grey", size=8, fontweight="bold")
        self.ax.set_rlim(bottom=0, top=10)
        self.ax.set_rlabel_position(180 / N)
        self.ax.plot(angles, values, color=color, linewidth=1, label=text)
        self.ax.fill(angles, values, color=color, alpha=0.25)
        self.ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))


class Weather(): # nepotrebno

    GEO_LOCATION_URL = 'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={api_key}'
    WEATHER_DATA_URL = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'

    def __init__(self, city) -> None:
        self.city = city
        self.cwd = self.parse_xml_raw()
        self.temperature = {'value': self.cwd['temperature']['@value'], 'max': self.cwd['temperature']['@max'], 'min': self.cwd['temperature']['@min'], 'unit': self.cwd['temperature']['@unit']}
        self.feels_like = (self.cwd['feels_like']['@value'], self.cwd['feels_like']['@unit'])
        self.humidity = (self.cwd['humidity']['@value'], self.cwd['humidity']['@unit'])
        self.pressure = (self.cwd['pressure']['@value'], self.cwd['pressure']['@unit'])
        self.wind_speed = (self.cwd['wind']['speed']['@value'], self.cwd['wind']['speed']['@unit'], self.cwd['wind']['speed']['@name'])
        try:
            self.wind_direction = (self.cwd['wind']['direction']['@value'], self.cwd['wind']['direction']['@code'])
        except TypeError:
            self.wind_direction = None
        self.clouds = (self.cwd['clouds']['@name'])
        self.weather = (self.cwd['weather']['@number'], self.cwd['weather']['@value'], self.cwd['weather']['@icon'])
        self.precipitation = (self.cwd['precipitation']['@mode'])
        self.lastupdate = datetime.now().strftime('%Y.%m.%d - %H:%M:%S')


    def get_url(self, url):
        with closing(get(url, stream=True)) as source:
            if self.response_check(source):
                return source.content
            else:
                self.log_error(source)
    
    def response_check(self, check):
        content_type = check.headers["Content-Type"].lower()
        return check.status_code == 200 and content_type is not None

    def log_error(self, error):
        exit(f"ERROR, check your URLs, invalid response code \"{error.status_code}\"")
    
    def location(self):
        content = self.get_url(self.GEO_LOCATION_URL.format(city_name=self.city, limit=1, api_key=current_app.config['WEATHER_API']))
        content = json.loads(content)
        lat = content[0]['lat']
        lon = content[0]['lon']
        return lat, lon

    def parse_json_raw(self):
        location = self.location()
        content = self.get_url(self.WEATHER_DATA_URL.format(lat=location[0], lon=location[1], api_key=current_app.config['WEATHER_API']))
        return json.loads(content)
    
    def parse_xml_raw(self):
        location = self.location()
        content = self.get_url(self.WEATHER_DATA_URL.format(lat=location[0], lon=location[1], api_key=current_app.config['WEATHER_API']) + '&mode=xml')
        return xmltodict.parse(content)['current']







# testiranje (cod dolje)

# histogram plot
ages = [18, 19, 21, 25, 26, 26, 30, 32, 38, 45, 55]
bins = range(10, 61, 10)


# radar plot
employee = ["Sam", "Rony", "Albert", "Chris", "Jahrum"]
actual = [7, 3, 5, 6, 14]
actual2 = [3, 4, 2, 8, 5]

# line plot
x = np.arange(0, 10)
y1 = np.array([r**2 for r in x])
y2 = np.array([r**3 for r in x])


# chart = Radar()
# chart.plot(employee, actual, 'red', 'test1')
# chart.plot(employee, actual2, 'blue', 'test2')
# chart._save('test2')

# lchar = Line()
# lchar.plot(x, y1, 'blue', 'test')
# lchar.plot(x, y2, 'red', 'test2')
# lchar._save('test_03')

# hchart = Histogram()
# hchart.plot(ages, bins, 'test')
# hchart._save('hist_02')

# db.session.execute(db.slect(User)).first() -> ovo radi, objašnjeno (https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/), query je stari način

# dodavanje bulk u tablicu baze
# db.session.execute(Pot.__table__.insert(), dict) -> gdje je dict python dictionary object (ili lista dictionarija)

# a radi i ovako gdje je dict python dictionary object
# obj_data = Pot(**dict)   
# db.session.add(obj_data)

def build_gauge(filename, path): # potrebno
    # funkcija za popunjavanje gauge tablice u bazi, potrebna joj je JSON datoteka '_gauge.json' nalazi se u static mapi
    with open(os.path.normpath(os.path.join(path, filename)), 'r') as json_data:
        data = json.load(json_data)
        db.session.execute(Gauge.__table__.insert(), data)
        db.session.commit()


def columns(model_query): # nepotrebno, nalazi se već u SensorSim klasi
        cols = []
        for c in db.inspect(model_query).attrs:
            if c.key.endswith("status"):
                cols.append(c.key)
        return cols

def plant_needs():
    attribs =  {}
    for column in COLUMNS:
        vals = Gauge.query.filter_by(name=column).all()
        attribs[column] = [(i.id, i.description) for i in vals]
    return attribs


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


def form_data(form):

    try:
        return form.split(';')
    except:
        return None, None
    
def build2(pot):
    cols = SensorMeasurements.__table__.columns.keys()[1:-2]
    
    df = pd.read_sql_query("SELECT * FROM sensor_measurements", current_app.config['SQLALCHEMY_DATABASE_URI']) 
    df = df.sort_values(by=['measured'], ascending=False)
    df = df[df['pot_id']==pot]
    df = df.fillna(0)

    dataset = []
    for column in cols:
        dataset.append(df[column].tolist())

    labels = df['measured'].tolist()

    # for col in cols:
    #     query = measurement_query(pot, col)
    #     # query = db.select(getattr(SensorMeasurements, col)).filter_by(pot_id=pot.id).order_by(SensorMeasurements.measured.desc())
    #     for val in db.session.execute(query).all():
    #         if val[0] is None:
    #             dataset.append(0)
    #             break
    #         else:
    #             dataset.append(val[0])
    #             break
    #     # dataset.append([val[0] for val in db.session.execute(query).all()])
    
    # labels = [val[0].strftime('%d/%m/%Y, %H:%M:%S-%f') for val in db.session.execute(measurement_query(pot, 'measured')).all()]


    return {'columns': cols, 'labels':labels, 'data': dataset}
# c = SensorMeasurements.__table__.columns.keys()[1:-2]
# a = pd.DataFrame(db.session.execute(db.select(SensorMeasurements).filter_by(pot_id=pot.id).order_by(SensorMeasurements.measured.desc())).all())
def measurement_query(pot, field):
    return (
        db.select(
            getattr(SensorMeasurements, field)
        )
        .filter_by(pot_id=pot)
        .order_by(SensorMeasurements.measured.desc())
    )