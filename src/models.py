from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime

Base = declarative_base()

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Actor(Base):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    director = Column(String)
    duration_minutes = Column(Float)
    age_rating = Column(String)
    country = Column(String)
    synopsis = Column(String)
    rating = Column(Float)

class Showtime(Base):
    __tablename__ = "showtimes"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

class HasGenre(Base):
    __tablename__ = "has_genre"
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)

class HasActor(Base):
    __tablename__ = "has_actor"
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id"), primary_key=True)
