from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()


class InvalidSearchParamExc(Exception):
    pass


def get_or_create(session, cls, search_param=None, **kwargs):
    """
    Get or create instance of given class
    :param session:
    :param cls:
    :param search_param:
    :param kwargs:
    :return:
    """
    if search_param is None or not isinstance(search_param, dict):
        raise InvalidSearchParamExc()

    try:
        obj = session.query(cls).filter_by(**search_param).one()
    except NoResultFound:
        obj = cls(**kwargs)
        session.add(obj)

    return obj


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)

    albums = relationship("Album", back_populates="artist")


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    img = Column(String(256))

    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)
    artist = relationship("Artist", back_populates="albums")

    songs = relationship("Song", back_populates="album")


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    length = Column(Integer)

    spotify_id = Column(String(128), nullable=False)

    album_id = Column(Integer, ForeignKey('albums.id'), nullable=False)
    album = relationship("Album", back_populates="songs")

    plays = relationship("Play", back_populates="song")


class Play(Base):
    __tablename__ = 'plays'

    id = Column(Integer, primary_key=True)
    duration = Column(Integer, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    song_id = Column(Integer, ForeignKey('songs.id'), nullable=False)
    song = relationship("Song", back_populates="plays")
