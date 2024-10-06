import os
import sqlite3

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
    connection.close()


if __name__ == "__main__":
    competitions = [
        "Premier_League",
        # "Bundesliga",
        # "La_Liga",
        # "Ligue_1",
        # "Serie_A",
        # "Primeira_Liga",
        # "Championship",
        # "Eredivisie",
        # "Belgian_Pro_League",
    ]
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

    special_comps = [
        # "Argentine_Copa_de_la_Liga",
        # "Brazilian_Serie_A",
    ]
    special_seasons = [
        # "2021",
        # "2022",
        # "2023",
        # "2024",
    ]
    main("master.db", competitions=special_comps, seasons=special_seasons)
