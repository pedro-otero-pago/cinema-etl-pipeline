from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Movie, Genre, Actor, Showtime, HasGenre, HasActor

engine = create_engine("sqlite:///cinema.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def upsert_movie(session, movie_data):
    existing_movie = session.query(Movie).filter_by(title=movie_data["title"]).first()

    if existing_movie:
        existing_movie.director = movie_data["director"]
        existing_movie.duration_minutes = movie_data["duration"]
        existing_movie.age_rating = movie_data["age_rating"]
        existing_movie.country = movie_data["country"]
        existing_movie.synopsis = movie_data.get("synopsis")
        existing_movie.rating = movie_data["rating"]
        movie_obj = existing_movie
    else:
        new_movie = Movie(
            title=movie_data["title"],
            director=movie_data["director"],
            duration_minutes=movie_data["duration"],
            age_rating=movie_data["age_rating"],
            country=movie_data["country"],
            synopsis=movie_data.get("synopsis"),
            rating=movie_data["rating"],
        )
        session.add(new_movie)
        movie_obj = new_movie

    session.commit()
    return movie_obj

def add_showtime(session, movie, start_time, end_time):
    new_showtime = Showtime(
        movie_id=movie.id,
        start_time=start_time,
        end_time=end_time,
    )
    session.add(new_showtime)
    session.commit() 

def get_or_create_genre(session, name):
    genre = session.query(Genre).filter_by(name=name).first()
    if not genre:
        genre = Genre(name=name)
        session.add(genre)
        session.commit()
    return genre

def link_movie_genre(session, movie, genre):
    existing_link = session.query(HasGenre).filter_by(movie_id=movie.id, genre_id=genre.id).first()
    if not existing_link:
        session.add(HasGenre(movie_id=movie.id, genre_id=genre.id))
        session.commit()

def get_or_create_actor(session, name):
    actor = session.query(Actor).filter_by(name=name).first()
    if not actor:
        actor = Actor(name=name)
        session.add(actor)
        session.commit()
    return actor

def link_movie_actor(session, movie, actor):
    existing_link = session.query(HasActor).filter_by(movie_id=movie.id, actor_id=actor.id).first()
    if not existing_link:
        session.add(HasActor(movie_id=movie.id, actor_id=actor.id))
        session.commit()