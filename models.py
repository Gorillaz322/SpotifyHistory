from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    img = Column(String(64))

    artist_id = Column(Integer, ForeignKey('artists.id'))
    artist = relationship("Artist", back_populates="albums")


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    length = Column(Integer)

    album_id = Column(Integer, ForeignKey('albums.id'))
    album = relationship("Album", back_populates="songs")


class Play(Base):
    __tablename__ = 'plays'

    id = Column(Integer, primary_key=True)
    duration = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    song_id = Column(Integer, ForeignKey('songs.id'))
    song = relationship("Song", back_populates="plays")
