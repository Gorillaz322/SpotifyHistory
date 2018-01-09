#!/usr/bin/env python3
from datetime import datetime, timedelta

import app

logger = app.logger

song_to_write = None


def on_track_change(pl):
    global song_to_write

    if song_to_write is not None \
            and datetime.now() - song_to_write['start_time'] > timedelta(seconds=4):

        time_played = (datetime.now() - song_to_write['start_time']) - song_to_write['paused_time']
        log_data = "{artist} - {title} | Time played - {playing_time}".format(
            artist=song_to_write['artist'],
            title=song_to_write['title'],
            playing_time=str(time_played).split(".")[0],
            time=song_to_write['start_time'].strftime("%d-%m-%Y %H:%M:%S")
        )

        logger.info("Writing song - " + log_data)

    logger.info("Current song - {song} - {title}".format(
        song=pl.get_artist(),
        title=pl.get_title()
    ))

    song_to_write = dict(
        artist=pl.get_artist(),
        title=pl.get_title(),
        start_time=datetime.now(),
        paused_time=timedelta(seconds=0)
    )

pause_start = None


def on_pause(pl):
    global pause_start
    pause_start = datetime.now()
    logger.info("Paused song")


previous_song = None


def on_play(pl):
    global pause_start
    global song_to_write

    if pause_start is not None:
        if song_to_write is None:
            song_to_write = dict(
                artist=pl.get_artist(),
                title=pl.get_title(),
                start_time=datetime.now(),
                paused_time=timedelta(seconds=0)
            )

        song_to_write['paused_time'] += (datetime.now() - pause_start)

        logger.info("Continue song - paused time: {}".format(datetime.now() - pause_start))

        pause_start = None

    global previous_song

    if previous_song != pl.get_title():
        previous_song = pl.get_title()
        on_track_change(pl)

