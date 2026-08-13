import pandas as pd
from datetime import date
from datetime import timedelta

def transform_movies(movies):
    df = pd.DataFrame(movies)

    df["duration"] = df["duration"].str.extract(r"(\d+)").astype(float)

    today = date.today().isoformat()
    df["showtimes"] = df["showtimes"].apply(
        lambda times: [pd.to_datatime(f"{today} {t}") for t in times]
    )

    df["end_time"] = df.apply(
        lambda row: [t + timedelta(minutes=row["duration"]) for t in row["showtimes"]] if pd.notna(row["duration"]) else None,
        axis=1
    )

    df = df.drop_duplicates(subset=["title"])

    return df