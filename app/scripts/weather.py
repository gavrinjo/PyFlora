
import json
import xmltodict
from requests import get
from contextlib import closing
from datetime import datetime
from flask import current_app


class Weather():

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

