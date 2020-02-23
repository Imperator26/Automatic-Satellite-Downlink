import logging
import yaml
import subprocess as sp

from datetime import datetime, timedelta, timezone
from pytz import timezone
from skyfield.api import Topos, Loader


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

fh = logging.FileHandler('logs/downlink.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)


# Timezone
tz = timezone('Europe/Rome')

with open('settings.yaml', 'r') as file:
    try:
        settings = yaml.safe_load(file)
    except yaml.YAMLError as e:
        logger.error(e)

logger.info('Position set to:')
logger.info(f'Latitude: {settings["latitude"]}')
logger.info(f'Longitude: {settings["longitude"]}')
logger.info(f'Elevation: {settings["elevation_m"]}')


station = Topos(
    latitude=settings['latitude'],
    longitude=settings['longitude'],
    elevation_m=settings['elevation_m']
)

load = Loader(
    'skyfield/',
    verbose=True,
    expire=True
)
ts = load.timescale()

satellites = load.tle('http://celestrak.com/NORAD/elements/weather.txt')
logger.info('TLEs loaded.')

satellite = satellites['NOAA 19']
logger.info(satellite)

t, events = satellite.find_events(
    station,
    ts.utc(datetime.now(tz)),
    ts.utc(datetime.now(tz) + timedelta(days=1)),
    altitude_degrees=15
)

logger.info(t)
logger.info(events)
