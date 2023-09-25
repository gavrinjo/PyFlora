
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import xmltodict

from requests import get
from contextlib import closing

# from ipychart import Chart
from random import randint
from datetime import datetime
from flask import current_app
from app.models import Gauge, Pot, SensorMeasurements, Plant
from app.repo import Weather
from app import db



def plot_config(fig: go.Figure, df: pd.DataFrame):

    columns = list(set(df.columns.tolist()) - set(['id', 'pot_id', 'measured']))
    data = []
    for column in columns:
        if column == 'temperature':
            yy = df[column]
        else:
            yy = mapper(df[column], column)['mapped_value']
        text = [f'{column.capitalize()} : {val}' for val in df[column]]
        data.append(go.Scatter(x=df['measured'], y=yy, name=column, line_shape='spline', hovertext=text, hoverinfo='x + text')) # np.interp(df[column], [0,100], [1,10])
    fig.add_traces(data)
    fig.update_xaxes(type='category', showticklabels=True)#, showspikes=True, spikemode="across", spikesnap="cursor")
    fig.update_traces(mode="lines+markers", hovertemplate=None)
    fig.update_layout(
        yaxis_range=[0,10],
        autosize= True,
        hovermode="x unified",
        hoverlabel=dict(
            font_size=11
        ),
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="top",
            xanchor="center",
            y=1.2,
            x=0.5
        )
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)




# dataset = {
#   'labels': ['Data 1', 'Data 2', 'Data 3', 'Data 4', 
#              'Data 5', 'Data 6', 'Data 7', 'Data 8'],
#   'datasets': [{'data': [14, 22, 36, 48, 60, 90, 28, 12]}]
# }
# options= {
#         'scales': {
#             'y': {
#                 'ticks': {
#                     # Include a dollar sign in the ticks
#                     'callback': '''function(value, index, values) {
#                         return '$' + value;
#                     }'''
#                 }
#             }
#         },
#     }

# mychart = Chart(data=dataset, kind='line', options=options)
# print(mychart.get_html_template())


def mapper(value, column: str):
    miv = Gauge.query.filter_by(name=column).order_by(Gauge.min_value).first()
    mav = Gauge.query.filter_by(name=column).order_by(Gauge.max_value.desc()).first()
    av = Gauge.query.filter_by(name=column, eiv=5).first()
    if column not in ['sunlight', 'temperature']:
        mapped_value = np.interp(value, [miv.min_value, mav.max_value], [1, 10])
    elif column == 'sunlight':
        mapped_value = np.interp(np.log10(value)*20, [np.log10(miv.min_value)*20, np.log10(mav.max_value)*20], [1, 10])

    
    return {
        'mapped_value': mapped_value,
        'value': value,
        'min_value': miv.min_value,
        'max_value': mav.max_value,
        'avg_value': (av.min_value + av.max_value) / 2
    }


class SensorSim():

    def __init__(self, pot, last_measurement) -> None:
        self.pot = pot
        self.last_measurement = last_measurement
        self.columns = self.get_columns(self.pot)

    
    def get_columns(self, pot: object) -> list:
            columns = []
            for column in db.inspect(pot).attrs:
                if column.key.endswith("status"):
                    columns.append(column.key)
            return columns

    def get_ref_values(self, query: object) -> tuple:
        min_array = [getattr(x, 'min_value') for x in query] # array of minimum values column
        min_median = np.median(min_array) # median value of minimum values array, used as minimum value
        max_array = [getattr(x, 'max_value') for x in query] # array of maximum values column
        max_median = np.median(max_array) # median value of maximum values array, used as maximum value
        std_value = np.ceil(np.median([min_median, max_median])) # median value over minimum and maximum values, used as standard value
        off_value = np.ceil(std_value * 0.1) # 10% of median value over minimum and maximum values, used as offset value
        return min(min_array), max(max_array), std_value, off_value


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
        new_measurement = SensorMeasurements()

        # columns = self.get_columns(self.pot.id)
        
        for column in self.columns:
            column = column[:column.find('_')]
            query = Gauge.query.filter_by(name=column).all()
            if getattr(self.pot, column + '_status'):
                if column != 'temperature':
                    ds = self.get_ref_values(query) # dataset
                    if self.last_measurement is None:
                        sensor = self.get_random_value(ds[2], ds[0], ds[1], ds[3])
                    else:
                        sensor = self.get_random_value(getattr(self.last_measurement, column), ds[0], ds[1], ds[3])
                else:
                    sensor = round(float(Weather('Zagreb').temperature['value']))
            else:
                sensor = None
            setattr(new_measurement, column, sensor)
        
        new_measurement.measured = datetime.utcnow()
        new_measurement.pot = self.pot

        return new_measurement


class Weather(): # treba

    GEO_LOCATION_URL = 'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={api_key}'
    WEATHER_DATA_URL = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'

    def __init__(self, city) -> None:
        self.city = city
        self.cwd = self.parse_xml_raw()
        self.temperature = {
            'value': self.cwd['temperature']['@value'],
            'max': self.cwd['temperature']['@max'],
            'min': self.cwd['temperature']['@min'],
            'unit': self.cwd['temperature']['@unit']
        }
        self.feels_like = {
            'value': self.cwd['feels_like']['@value'],
            'unit': self.cwd['feels_like']['@unit']
        }
        self.humidity = {
            'value': self.cwd['humidity']['@value'],
            'unit': self.cwd['humidity']['@unit']
        }
        self.pressure = {
            'value': self.cwd['pressure']['@value'],
            'unit': self.cwd['pressure']['@unit']
        }
        self.wind_speed = {
            'value': self.cwd['wind']['speed']['@value'],
            'unit': self.cwd['wind']['speed']['@unit'],
            'name': self.cwd['wind']['speed']['@name']
        }
        try:
            self.wind_direction = {
                'value': self.cwd['wind']['direction']['@value'],
                'code': self.cwd['wind']['direction']['@code']
            }
        except TypeError:
            self.wind_direction = None
        self.clouds = {
            'name': self.cwd['clouds']['@name']
        }
        self.weather = {
            'number': self.cwd['weather']['@number'],
            'value': self.cwd['weather']['@value'],
            'icon': self.cwd['weather']['@icon']
        }
        self.precipitation = {
            'mode': self.cwd['precipitation']['@mode']
        }
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


def graph_data(pot):
    columns = []
    for column in db.inspect(pot).attrs:
        if column.key.endswith("status"):
            columns.append(column.key)
    measurements = SensorMeasurements.query.filter_by(pot_id=pot.id).all()
    data = {}
    for column in columns:
        column = column[:column.find('_')]
        min_val, max_val = getattr(Plant.query.get(pot.plant_id), column).split(';')
        data[column] = {'measured':{}, 'min_value': {}, 'max_value': {}}
        for item in measurements:
            data[column]['measured'][item.measured.strftime("%d.%m.%Y, %H:%M:%S.%f")] = getattr(item, column)
            data[column]['min_value'][item.measured.strftime("%d.%m.%Y, %H:%M:%S.%f")] = min_val
            data[column]['max_value'][item.measured.strftime("%d.%m.%Y, %H:%M:%S.%f")] = max_val
    return data

