import os
import sqlite3
import time

from create_database import create_database
from matches import update_matches
from players import insert_players
from update_local import update_local
from utils import get_matches_in_database


def main(database_file, competitions=["Premier_League"], seasons=["2021-2022"]):
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    create_database(cursor)

    for competition in competitions:
        for season in seasons:
            update_local(competition, season)
            update_matches(cursor, competition, season)

            db_matches = get_matches_in_database(cursor, competition, season)
            local_matches = set(
                os.listdir(os.path.join("web_pages", competition, season))
            )

            matches_to_add = local_matches - db_matches
            insert_players(cursor, competition, season, list(matches_to_add))

            connection.commit()

            if len(matches_to_add) <= 20:
                print(
                    "Didn't need to add many files to the database. Sleeping to avoid rate limit"
                )
                """
                I have done lots of testing to see what sleep length is required to not get put in FBRef jail.
                It's annoying and slow, but 7 seconds is required
                """
                time.sleep(7)

    connection.close()


if __name__ == "__main__":
    competitions = ["Premier_League", "Bundesliga", "La_Liga", "Ligue_1", "Serie_A"]
    seasons = [
        # "2017-2018",
        # "2018-2019",
        # "2019-2020",
        # "2020-2021",
        # "2021-2022",
        # "2022-2023",
        # "2023-2024",
        "2024-2025",
    ]
    main("master.db", competitions=competitions, seasons=seasons)
