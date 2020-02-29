import logging
import yaml

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '[%(asctime)s] - %(funcName)s: %(message)s',
    '%H:%M:%S'
)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

fh = logging.FileHandler('logs/load_settings.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)


def load_settings():
    try:
        with open('settings.yaml', 'r') as file:
            try:
                settings = yaml.safe_load(file)
            except yaml.YAMLError as e:
                logger.error(e)
                raise
            else:
                return settings
    except FileNotFoundError as e:
        logger.error(e)
        raise
