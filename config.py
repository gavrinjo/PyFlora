import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(basedir, "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT'))
    EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    EMAIL_SENDER = os.environ.get('EMAIL_SENDER') or 'no-reply@pyflora.com'
    EMAIL_USE_STARTLS = os.environ.get('EMAIL_USE_STARTLS') or True
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') or True
    LOG_TO_FILE = os.environ.get('LOG_TO_FILE') or True
    LOGFILES = os.path.join(basedir, 'logs')
    ADMINS = ['admin@pyflora.com']
    UPLOADED_FILES_ALLOW = ['.jpg', '.jpeg', '.png']
    UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'app/static')
    WEATHER_API = os.environ.get('WEATHER_API') or None
    MEASURES = ['sunlight', 'temperature', 'moisture', 'reaction', 'nutrient', 'salinity']