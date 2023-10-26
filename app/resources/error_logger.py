import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask

# FORMATTER = logging.Formatter("\n%(levelname)s - %(asctime)s - %(message)s", datefmt="T(%d.%m.%Y. %H:%M)")
FORMATTER = logging.Formatter('\n%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]', datefmt='%d.%m.%Y. %H:%M')

# handlers
def get_mail_handler(app: Flask):
    auth = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TLS']:
        secure = ()
    mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr='no-reply@' + app.config['MAIL_SERVER'],
        toaddrs=app.config['ADMINS'], subject='pyFlora Failure',
        credentials=auth, secure=secure)
    mail_handler.setFormatter(FORMATTER)
    mail_handler.setLevel(logging.ERROR)
    return mail_handler

def get_file_handler(file):
    file_handler = RotatingFileHandler(f"{file}.log", maxBytes=10240, encoding='utf-8', backupCount=10)
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.INFO)
    return file_handler

def get_console_handler():
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(FORMATTER)
    console_handler.setLevel(logging.INFO)
    return console_handler

#loggers
def exception_errors(app: Flask):
    logger = logging.getLogger()
    if app.config['LOG_TO_STDOUT']:
            logger.addHandler(get_console_handler())
            logger.propagate = False
        
    if not app.debug:
        if app.config['MAIL_SERVER']:
            logger.addHandler(get_mail_handler(app))
            logger.propagate = False

        if app.config['LOG_TO_FILE']:
            if not os.path.exists(app.config['LOGFILES']):
                os.mkdir(app.config['LOGFILES'])
            logger.addHandler(get_file_handler(os.path.join(app.config['LOGFILES'], 'logfile')))
            logger.propagate = False
    
    return logger 

def app_errors(app: Flask):

    if not app.debug:
        if app.config['MAIL_SERVER']:
            app.logger.addHandler(get_mail_handler(app))
            app.logger.propagate = False

        if app.config['LOG_TO_FILE']:
            if not os.path.exists(app.config['LOGFILES']):
                os.mkdir(app.config['LOGFILES'])
            app.logger.addHandler(get_file_handler(os.path.join(app.config['LOGFILES'], 'logfile')))
            app.logger.propagate = False
