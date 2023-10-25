import logging
import sys
import os
from logging.handlers import SMTPHandler, TimedRotatingFileHandler, RotatingFileHandler
from logging.config import dictConfig

FORMATTER = logging.Formatter("\n%(levelname)s - %(asctime)s - %(message)s", datefmt="T(%d.%m.%Y. %H:%M)")
# FORMATTER = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]', datefmt='T(%d.%m.%Y. %H:%M)')
# LOG_FILE = "Logger"

def get_mail_handler(app):

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


def get_console_handler():

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(FORMATTER)
    stream_handler.setLevel(logging.INFO)

    return stream_handler


def get_file_handler(file):

    file_handler = RotatingFileHandler(f"{file}.log", maxBytes=10240, encoding='utf-8', backupCount=10)
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.INFO)

    return file_handler


def get_logger(app, log_file, path='logs'):
    
    # logger = logging.getLogger(log_file)
    # logger.setLevel(logging.DEBUG)
    if not app.debug:
        if app.config['MAIL_SERVER']:
            app.logger.addHandler(get_mail_handler(app), )
        
        if app.config['LOG_TO_STDOUT']:
            app.logger.addHandler(get_console_handler())
        else:
            if not os.path.exists(path):
                os.mkdir(path)
            app.logger.addHandler(get_file_handler(os.path.join(path, log_file)))

        app.logger.propagate = False
        app.logger.setLevel(logging.INFO)
        app.logger.info('pyFlora startup')
    # return logger


# def get_logger_st():
#     logger = logging.getLogger()
#     logger.setLevel(logging.DEBUG)
#     logger.addHandler(get_console_handler())
#     logger.propagate = False
#     return logger



# log_file = "error_logfile"
# log = get_logger(log_file)

# log.exception(f"error copy", exc_info=False) # primjer pozivanja