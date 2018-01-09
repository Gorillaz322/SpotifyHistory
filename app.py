import logging
import time
import os

from gi.repository import Playerctl, GLib

location = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

if not os.path.exists('local'):
    os.makedirs('local')

logger = logging.getLogger('spotify-history')

file_logging = logging.FileHandler(os.path.join(location, 'local/logs.txt'))
console_logging = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

file_logging.setFormatter(formatter)
console_logging.setFormatter(formatter)

logger.addHandler(file_logging)
logger.addHandler(console_logging)

logger.setLevel(logging.INFO)

import views

while True:
    player = Playerctl.Player()
    try:
        player.on('play', views.on_play)
        player.on('pause', views.on_pause)
        break
    except GLib.Error:
        logger.warning('Spotify was not found | Trying again in 10 seconds')
        time.sleep(10)

logger.info('Spotify found')

# TODO: handle initialisation of app
# views.on_track_change(player)
