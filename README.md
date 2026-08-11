# cinema-epl-pipeline
Automated ETL pipeline that scrapes local cinema showtimes, cleans the data, and loads it into a relational database on a daily schedule, with a stack including Python, BeautifulSoup, pandas and SQLAlchemy.

## Database schema

```mermaid
erDiagram
  MOVIES ||--o{ HAS_GENRE : ""
  GENRES ||--o{ HAS_GENRE : ""
  MOVIES ||--o{ HAS_ACTOR : ""
  ACTORS ||--o{ HAS_ACTOR : ""
  MOVIES ||--o{ SHOWTIMES : ""

  MOVIES {
    int id PK
    string title
    string director
    int duration_minutes
    string age_rating
    string country
    string synopsis
    float rating
  }
  GENRES {
    int id PK
    string name
  }
  HAS_GENRE {
    int movie_id FK
    int genre_id FK
  }
  ACTORS {
    int id PK
    string name
  }
  HAS_ACTOR {
    int movie_id FK
    int actor_id FK
  }
  SHOWTIMES {
    int id PK
    int movie_id FK
    datetime start_time
    datetime end_time
  }
```