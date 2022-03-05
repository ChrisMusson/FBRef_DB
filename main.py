import os
import sqlite3

from create_database import create_database
from matches import update_matches
from players import insert_players
from update_local import update_local
from utils import *


def main(database_file, season="2021-2022"):
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    create_database(cursor)
    update_local(season)
    update_matches(season, cursor)

    db_matches = get_matches_in_database(season, cursor)
    local_matches = set(os.listdir(os.path.join("web_pages", season)))

    matches_to_add = local_matches - db_matches
    insert_players(season, list(matches_to_add), cursor)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    main("master.db")
