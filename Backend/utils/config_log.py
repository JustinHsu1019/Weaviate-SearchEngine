import configparser
import logging

CONFIG_PATH = 'Backend/CSconfig.ini'
LOGGING_PATH = 'Backend/logs/CsLogger.log'

def setup_config_and_logging():
    config = configparser.ConfigParser()

    logger = logging.getLogger()
    logger.setLevel('INFO')
    handler = logging.FileHandler(LOGGING_PATH, mode='a', encoding='utf-8')
    handler.setFormatter(logging.Formatter("[%(levelname)s] - %(asctime)s - %(pathname)s:%(lineno)d\n%(message)s"))
    console_handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.addHandler(console_handler)

    return config, logger, CONFIG_PATH
