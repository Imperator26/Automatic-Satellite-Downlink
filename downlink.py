import logging
import threading
import subprocess as sp

from datetime import datetime, timedelta
from pytz import timezone
from skyfield.api import Topos, Loader

from utils.load_settings import load_settings

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


def scheduler(satellite):
    return


def schedule_recording(satellite):
    satellite = satellites[satellite]
    logger.info(satellite)

    t, events = satellite.find_events(
        station,
        ts.utc(datetime.now(tz)),
        ts.utc(datetime.now(tz) + timedelta(days=1)),
        altitude_degrees=15
    )
    for t, e in zip(t, events):
        if e == 0:
            logger.info(t.astimezone(tz))
            logger.info(t.astimezone(tz) < datetime.now(tz))
            if t.astimezone(tz) > datetime.now(tz):
                pass
                #decode_apt(record_pass(satellite, frequency, sample_rate))


def record_pass(satellite, frequency, sample_rate):
    filename = f'{satellite.name}-{datetime.now(tz).strftime("%Y-%m-%d %H:%M")}'
    sp.run([
        'timeout',
        '',
        'rtl_fm',
        '-f', frequency,
        '-s', sample_rate,
        f'recordings/{filename}.wav'
    ])
    return filename


def decode_apt(filename):
    sp.run([
        'noaa-apt',
        f'recordings/{filename}.wav',
        '-o', f'images/{filename}.png'
    ])


if __name__ == '__main__':
    # Load settings
    settings = load_settings()

    # Timezone
    tz = timezone(settings['timezone'])

    # Station
    station = Topos(
        latitude=settings['station']['latitude'],
        longitude=settings['station']['longitude'],
        elevation_m=settings['station']['elevation_m']
    )

    logger.info('Position set to:')
    logger.info(f'Latitude: {settings["station"]["latitude"]}')
    logger.info(f'Longitude: {settings["station"]["longitude"]}')
    logger.info(f'Elevation: {settings["station"]["elevation_m"]}')

    # Load skyfield
    load = Loader(
        'skyfield/',
        verbose=True,
        expire=True
    )
    ts = load.timescale()

    satellites = load.tle('http://celestrak.com/NORAD/elements/weather.txt')
    logger.info('TLEs loaded.')

    # Create threads
    threads = dict()

    for satellite in settings['satellites']:
        logger.info(f'Creating thread for {satellite}')
        x = threading.Thread(target=scheduler, args=(satellite,), daemon=True)
        threads[satellite] = x
        x.start()

    try:
        while True:
            continue
    except KeyboardInterrupt:
        logging.info('Killing threads...')

        for satellite, thread in threads.items():
            logging.info(f'Killing {satellite} thread')
            thread.join()
        pass
