import logging
import os
from django.conf import settings
LOG_DIR = os.path.join(settings.BASE_DIR, 'logs')


def get_logger(name, logfile='debug'):
    """
    Return a logger object.
    Parameters:
        name: name of the logger usually __file__
        logfile: name of the log file can be test or debug
    """
    path_to_log = os.path.join(LOG_DIR, logfile)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create a file handler
    handler = logging.FileHandler(f'{path_to_log}.log', mode='w')
    handler.setLevel(logging.DEBUG)
    # create a logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    return logger


LOG_DIR = os.path.join(settings.BASE_DIR, 'logs')


def get_logger(name, logfile='debug'):
    """
    Return a logger object.
    Parameters:
        name: name of the logger usually __file__
        logfile: name of the log file can be test or debug
    """
    path_to_log = os.path.join(LOG_DIR, logfile)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create a file handler
    handler = logging.FileHandler(f'{path_to_log}.log', mode='w')
    handler.setLevel(logging.DEBUG)
    # create a logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    return logger
