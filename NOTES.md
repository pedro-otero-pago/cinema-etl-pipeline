## Choosing the data source

The first part of this project was deciding which website I was going to
extract data from on a regular basis. For this purpose, it could not be
a website with too many blockers, so I've opted for a local cinema page
instead of the official Cinesa website, which relies more heavily on
JavaScript and a booking engine. The aggregator page I chose is a plain
HTML page, which makes it simpler to scrape.

## Checking robots.txt

After reviewing the robots.txt, I found the following rules:

​```
User-agent: *
Disallow: /u/
Disallow: /admin/
Disallow: /admin-n/
Disallow: /cron/
Disallow: /robots/
Disallow: /ajax/
Disallow: /cines/comprar/
Disallow: /fotos/*/original/
​```

It is fairly permissive. The only rule relevant to this project is
`Disallow: /cines/comprar/`, which I will avoid entirely during scraping.
The rest of the disallowed paths are unrelated to this project.

## Scope

The only URL that matters for this project is `/cines/cinesa-marineda-city/`,
from which I will extract the data needed for the pipeline: title, director,
cast, genre, duration, age rating, country, synopsis, showtimes, and rating.

I decided to leave out trailer and photo links, since they are media content
rather than structured data useful for analysis.

## Database schema

See the entity-relation diagram in README.md.

I feel the need to clarify that `end_time` is a derived attribute: it is
calculated by adding the movie's duration to the showtime's start time,
both of which are already stored in the database.

I wanted to use this attribute to help the cinema coordinate session times
across theatres, by preventing a movie from starting in a room before
another movie showing there had finished. However, this data source does
not provide information on which room each movie will be shown in, so this
validation is out of scope for now.

Note on notation: the schema was designed using classic Chen notation
(entities as rectangles, relationships as diamonds, single/double lines
for cardinality), but the diagram in README.md uses Mermaid's crow's-foot
syntax instead, since that is what GitHub renders natively. Both represent
the same schema.

## Scraper findings

After inspecting the actual HTML of the cinema listing page, I confirmed
selectors for every field defined in the database schema except synopsis,
which is not available on this page. Some fields (age rating, duration)
are missing for some movies and will have to be handled as optional.

I initially thought showtimes were loaded via JavaScript/AJAX, since the
first movie card I inspected had an empty sessions list. This was wrong:
showtimes are present in the static HTML, they were just empty for that
specific movie on that day. The time is available directly as a
`data-session-time` attribute on each session link, so no parsing of link
text is needed.

I also found that the country, genre, duration, and age rating fields
(inside `p.data`) do not hold a fixed position — for example, age rating
might be the third span in one movie and the fourth in another. Because
of this, each span will have to be classified by its shape (e.g. ends in
"min." → duration, starts with "+" or equals "TP" → age rating) instead
of relying on its position in the list.

Finally, the synopsis is confirmed to be missing from this page. Getting
it will require a second request to each movie's individual page.

## Parser: country and genre classification

While writing parser.py, I ran into a problem with country and genre:
there was no reliable pattern to distinguish them from the raw text,
unlike duration or age rating, which have a clear shape.

The solution I found was creating a separate file, constants.py, with
sets of known countries and genres. Each text is classified by checking
whether it belongs to one of these sets, instead of relying on its
position or classifying it by elimination.

Any text is compared in lowercase (using .lower()) against the sets, to
avoid mismatches caused by different capitalization, while the original
text (not the lowercased version) is the one actually stored.

Any text that doesn't match duration, age rating, a known country, or a
known genre triggers a warning printed to the console, so unclassified
values can be reviewed and the catalogs expanded over time.

## Transformer: cleaning and derived fields

For missing fields (duration, rating, age rating, country, genre), I
decided not to fill them with default values, even when a reasonable
guess existed (e.g. assuming a missing age rating means "suitable for
all audiences"). Keeping them as explicit nulls is more honest to what
the source actually provided.

For duration, I extracted the number and stripped the " min." part using
a regex, then converted it to float (not int) so that missing values
(NaN) can coexist in the same column without breaking the conversion.

For showtimes, I added today's date to each session's start time, since
the pipeline runs once a day, so all showtimes scraped in a single run
belong to that same execution date.

For end_time, I added the movie's duration to each start time using
timedelta, skipping the calculation (returning None) when duration is
missing, since it can't be derived without it.

I also added a line that removes duplicate movies within the same
scraping run, as a safety net — even though duplicates shouldn't occur
in a single run, and the actual day-to-day upsert logic will live in the
database layer, not here.

## Models and database engine choice

I decided to start with SQLite instead of a real database engine like 
PostgreSQL, since it requires no external setup (just a local file) and 
makes the project easy to clone and run for anyone reviewing it. Because 
SQLAlchemy abstracts the underlying engine, switching to PostgreSQL 
later would only require changing the connection string in database.py, 
not models.py.

Each entity from the ER diagram was translated directly into a
SQLAlchemy class inheriting from Base: Genre, Actor, Movie, Showtime,
and the two junction tables, HasGenre and HasActor, which use composite
primary keys (movie_id + genre_id / actor_id) matching the N:M
relationships from the schema.

## Database persistence: upsert logic and helper functions

For database.py, I used SQLAlchemy's engine + Session pattern: the
engine handles the low-level connection to SQLite, while the Session is
what actually reads and writes data, similar to how git add/commit work
(stage changes, then confirm them together).

I implemented separate upsert logic depending on the entity, matching
the decision made earlier for the schema: upsert_movie checks whether a
movie with the same title already exists — if so, it updates its fields
by direct attribute assignment (SQLAlchemy tracks the change
automatically); if not, it creates a new row. add_showtime always
inserts a new row and never updates, since each session on each day is
a genuinely different record, not a duplicate.

For genres and actors, I used a get-or-create pattern: look up by name,
return the existing row if found, otherwise create it. Linking a movie
to a genre or actor also checks whether that specific link already
exists before inserting, to avoid duplicate rows in the junction tables
when the same movie is scraped again on a later day.