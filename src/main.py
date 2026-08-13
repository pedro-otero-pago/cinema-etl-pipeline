from scraper import fetch_html
from parser import parse_movies
from transformer import transform_movies
from database import Session, upsert_movie, add_showtime, get_or_create_genre, link_movie_genre, get_or_create_actor, link_movie_actor
from config import CINEMA_URL

html = fetch_html(CINEMA_URL)
movies = parse_movies(html)
df = transform_movies(movies)

session = Session()

for index, row in df.iterrows():
    movie = upsert_movie(session, row.to_dict())

    if row["end_time"] is not None:
        for start_time, end_time in zip(row["showtimes"], row["end_time"]):
            add_showtime(session, movie, start_time, end_time)
    else:
        for start_time in row["showtimes"]:
            add_showtime(session, movie, start_time, None)

    if row["genre"] is not None:
        genre = get_or_create_genre(session, row["genre"])
        link_movie_genre(session, movie, genre)

    for actor_name in row["cast"]:
        actor = get_or_create_actor(session, actor_name)
        link_movie_actor(session, movie, actor)

session.close()