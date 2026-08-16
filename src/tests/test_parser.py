import pytest
from parser import parse_movies, parse_synopsis


def load_fixture(filename):
    with open(f"fixtures/{filename}", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def cartelera_html():
    return load_fixture("cartelera.html")


@pytest.fixture
def movie_detail_html():
    return load_fixture("movie_detail.html")


@pytest.fixture
def parsed_movies(cartelera_html):
    return parse_movies(cartelera_html)


# --- parse_movies: overall structure ---

def test_parse_movies_extracts_expected_number_of_movies(parsed_movies):
    assert len(parsed_movies) == 12


def test_parse_movies_returns_list_of_dicts(parsed_movies):
    assert isinstance(parsed_movies, list)
    assert all(isinstance(movie, dict) for movie in parsed_movies)


def test_parse_movies_each_movie_has_all_expected_keys(parsed_movies):
    expected_keys = {
        "title", "movie_url", "director", "duration", "age_rating",
        "country", "genre", "cast", "rating", "showtimes",
    }
    for movie in parsed_movies:
        assert expected_keys.issubset(movie.keys())


# --- parse_movies: fixed-position fields (title, director, cast, url) ---

def test_parse_movies_extracts_title_and_url(parsed_movies):
    movie = parsed_movies[0]
    assert isinstance(movie["title"], str)
    assert len(movie["title"]) > 0
    assert movie["movie_url"].startswith("http")


def test_parse_movies_extracts_director_as_string(parsed_movies):
    movie = parsed_movies[0]
    assert isinstance(movie["director"], str)


def test_parse_movies_extracts_cast_as_list(parsed_movies):
    movie = parsed_movies[0]
    assert isinstance(movie["cast"], list)
    assert all(isinstance(actor, str) for actor in movie["cast"])


def test_parse_movies_known_movie_fields(parsed_movies):
    la_odisea = next(m for m in parsed_movies if m["title"] == "La Odisea")
    assert la_odisea["director"] == "Christopher Nolan"
    assert la_odisea["duration"] == "172 min."
    assert la_odisea["country"] == "EE.UU."
    assert la_odisea["genre"] == "Acción"
    assert la_odisea["rating"] == "9.2"
    assert "Matt Damon" in la_odisea["cast"]


# --- parse_movies: variable-position fields (duration, age_rating, country, genre) ---

def test_parse_movies_duration_matches_expected_pattern_or_is_none(parsed_movies):
    for movie in parsed_movies:
        duration = movie["duration"]
        assert duration is None or duration.endswith("min.")


def test_parse_movies_age_rating_matches_expected_pattern_or_is_none(parsed_movies):
    for movie in parsed_movies:
        age_rating = movie["age_rating"]
        assert age_rating is None or age_rating == "TP" or age_rating.startswith("+")


def test_parse_movies_handles_movie_with_missing_fields(parsed_movies):
    movie_without_duration = next(m for m in parsed_movies if m["title"] == "El último mono")
    assert movie_without_duration["duration"] is None


# --- parse_movies: showtimes ---

def test_parse_movies_showtimes_is_always_a_list(parsed_movies):
    for movie in parsed_movies:
        assert isinstance(movie["showtimes"], list)


def test_parse_movies_showtimes_are_time_strings(parsed_movies):
    for movie in parsed_movies:
        for showtime in movie["showtimes"]:
            assert isinstance(showtime, str)
            assert ":" in showtime


def test_parse_movies_movie_with_no_sessions_has_empty_showtimes(parsed_movies):
    movie_without_sessions = next(m for m in parsed_movies if m["title"] == "El último mono")
    assert movie_without_sessions["showtimes"] == []


# --- parse_movies: rating ---

def test_parse_movies_rating_is_string_or_none(parsed_movies):
    for movie in parsed_movies:
        assert movie["rating"] is None or isinstance(movie["rating"], str)


# --- parse_synopsis ---

def test_parse_synopsis_extracts_text(movie_detail_html):
    synopsis = parse_synopsis(movie_detail_html)
    assert isinstance(synopsis, str)
    assert len(synopsis) > 0


def test_parse_synopsis_does_not_include_ad_placeholder(movie_detail_html):
    synopsis = parse_synopsis(movie_detail_html)
    assert "apwrap" not in synopsis
    assert "intext" not in synopsis


def test_parse_synopsis_returns_none_when_section_missing():
    html_without_synopsis = "<html><body><div>No synopsis here</div></body></html>"
    assert parse_synopsis(html_without_synopsis) is None