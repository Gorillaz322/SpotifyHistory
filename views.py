from datetime import datetime, timedelta

import app
import models

logger = app.logger

song_to_write = None


def on_track_change(pl, session):
    global song_to_write

    if song_to_write is not None \
            and datetime.now() - song_to_write['start_time'] > timedelta(seconds=4):

        artist = models.get_or_create(
            session,
            models.Artist,
            search_param={
                'name': song_to_write['xesam:artist'][0]
            },
            name=song_to_write['xesam:artist'][0])

        album = models.get_or_create(
            session,
            models.Album,
            search_param={
                'name': song_to_write['xesam:album']
            },
            name=song_to_write['xesam:album'],
            img=song_to_write['mpris:artUrl'],
            artist=artist)

        song = models.get_or_create(
            session,
            models.Song,
            search_param={
                'name': song_to_write['xesam:title']
            },
            name=song_to_write['xesam:title'],
            length=int(song_to_write['mpris:length']/1000000),
            album=album,
            spotify_id=song_to_write['mpris:trackid'].split(':')[2])

        play = models.Play(
            duration=((datetime.now() - song_to_write['start_time']) - song_to_write['paused_time']).seconds,
            start_time=song_to_write['start_time'],
            end_time=datetime.now(),
            song=song)

        logger.info("Writing playback - {artist} - {title} | Duration of playback - {playing_time} sec".format(
            artist=artist.name,
            title=song.name,
            playing_time=play.duration
        ))

    logger.info("Current song - {song} - {title}".format(
        song=pl.get_artist(),
        title=pl.get_title()
    ))

    song_to_write = dict(
        start_time=datetime.now(),
        paused_time=timedelta(seconds=0)
    )
    song_to_write.update(dict(pl.props.metadata))

pause_start = None


def on_pause(pl):
    global pause_start
    pause_start = datetime.now()
    logger.info("Song paused")


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

        logger.info("Continuing playback - duration of pause: {}".format(datetime.now() - pause_start))

        pause_start = None

    global previous_song

    if previous_song != pl.get_title():
        previous_song = pl.get_title()
        with app.session_scope() as session:
            on_track_change(pl, session)

