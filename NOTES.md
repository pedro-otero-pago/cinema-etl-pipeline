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