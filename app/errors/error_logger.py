import logging
import sys
import os
from logging.handlers import SMTPHandler, TimedRotatingFileHandler, RotatingFileHandler

FORMATTER = logging.Formatter("\n%(levelname)s - %(asctime)s - %(message)s", datefmt="T(%d.%m.%Y. %H:%M)")
# LOG_FILE = "Logger"


def get_mail_handler():
    pass


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(file):

    # file_handler = RotatingFileHandler('logs/logfile.log', maxBytes=10240, backupCount=10)
    # file_handler.setFormatter(logging.Formatter(
    #     '%(asctime)s %(levelname)s: %(message)s '
    #     '[in %(pathname)s:%(lineno)d]'))
    # file_handler.setLevel(logging.INFO)
    # app.logger.addHandler(file_handler)

    file_handler = RotatingFileHandler(f"{file}.log", maxBytes=10240, encoding='utf-8', backupCount=10)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name, path=None):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    if path is None:
        logger.addHandler(get_file_handler(logger_name))
    else:
        logger.addHandler(get_file_handler(os.path.join(path, logger_name)))

    logger.propagate = False
    return logger


def get_logger_st():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.propagate = False
    return logger



log_file = "error_logfile"
log = get_logger(log_file)

log.exception(f"error copy", exc_info=False) # primjer pozivanja