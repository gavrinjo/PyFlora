
import json
import xmltodict
from requests import get
from contextlib import closing
# from flask import current_app




class Weather():

    GEO_LOCATION_URL = 'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={api_key}'
    WEATHER_DATA_URL = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'

    def __init__(self, city, app=None) -> None:
        self.city = city
        self.temperature = None
        self.feels_like = None
        self.humidity = None
        self.pressure = None
        self.wind_speed = None
        self.wind_direction = None
        self.clouds = None
        self.weather = None
        self.precipitation = None
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['weather'] = self
        cwd = self.parse_xml_raw(app)
        self.temperature = (cwd['temperature']['@value'], cwd['temperature']['@unit'])
        self.feels_like = (cwd['feels_like']['@value'], cwd['feels_like']['@unit'])
        self.humidity = (cwd['humidity']['@value'], cwd['humidity']['@unit'])
        self.pressure = (cwd['pressure']['@value'], cwd['pressure']['@unit'])
        self.wind_speed = (cwd['wind']['speed']['@value'], cwd['wind']['speed']['@unit'], cwd['wind']['speed']['@name'])
        try:
            self.wind_direction = (cwd['wind']['direction']['@name'])
        except TypeError:
            self.wind_direction = None
        self.clouds = (cwd['clouds']['@name'])
        self.weather = (cwd['weather']['@number'], cwd['weather']['@value'], cwd['weather']['@icon'])
        self.precipitation = (cwd['precipitation']['@mode'])
    
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
    
    def location(self, app):
        content = self.get_url(self.GEO_LOCATION_URL.format(city_name=self.city, limit=1, api_key=app.config['WEATHER_API']))
        content = json.loads(content)
        lat = content[0]['lat']
        lon = content[0]['lon']
        return lat, lon

    # def parse_json_raw(self):
    #     location = self.location()
    #     content = self.get_url(self.WEATHER_DATA_URL.format(lat=location[0], lon=location[1], api_key=current_app.config['WEATHER_API']))
    #     return json.loads(content)
    
    def parse_xml_raw(self, app):
        location = self.location(app)
        content = self.get_url(self.WEATHER_DATA_URL.format(lat=location[0], lon=location[1], api_key=app.config['WEATHER_API']) + '&mode=xml')
        return xmltodict.parse(content)['current']

