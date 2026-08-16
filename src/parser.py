from bs4 import BeautifulSoup
from constants import KNOWN_COUNTRIES, KNOWN_GENRES
import re

def parse_movies(html):
    soup = BeautifulSoup(html, "html.parser")
    movie_cards = soup.find_all("div", class_="titem")

    movies =[]

    for card in movie_cards:
        title = card.find("p", class_="tit").find("a").text.strip()
        movie_url = card.find("p", class_="tit").find("a")["href"]
        director = card.find("p", class_="dir").find("a").text.strip()
        data_spans = card.find("p", class_="data").find_all("span")
        data_texts = [span.text.strip() for span in data_spans]
        cast = [a.text.strip() for a in card.find("p", class_="cast").find_all("a")]
        showtimes = [a["data-session-time"] for a in card.find("div", class_="sessions").find_all("a")]

        rating_tag = card.find("div", class_="tdata").find("div", class_="tscore")
        if rating_tag:
            rating = rating_tag.find("span").text.strip()
        else:
            rating = None

        duration = None
        age_rating = None
        country = None
        genre = None
        for text in data_texts:
            if re.match(r"\d+ min\.", text):
                duration = text
            elif re.match(r"\+\d+", text) or text == "TP":
                age_rating = text
            elif text.lower() in KNOWN_COUNTRIES:
                country = text
            elif text.lower() in KNOWN_GENRES:
                genre = text
            else:
                print(f"Warning: unclassified data field '{text}' for movie '{title}'")

        movies.append({
            "title": title,
            "movie_url": movie_url,
            "director": director,
            "duration": duration,
            "age_rating": age_rating,
            "country": country,
            "genre": genre,
            "cast": cast,
            "rating": rating,
            "showtimes": showtimes,
        })

    return movies

def parse_synopsis(html):
    soup = BeautifulSoup(html, "html.parser")
    synopsis_div = soup.find("div", class_="f-txt")

    if synopsis_div:
        return synopsis_div.get_text(separator=" ", strip=True)
    else:
        return None