import os
from bs4 import BeautifulSoup
from utils import *


def get_match_data(competition, season, match_id):
    with open(
        os.path.join("web_pages", competition, season, match_id), "r", encoding="utf-8"
    ) as f:
        return BeautifulSoup(f.read(), "lxml").find_all("table")


def get_player_info(match_id, tables):
    data = []
    # summary table for each team (includes goalkeepers)
    for table_num in [3, 10]:
        # first 2 rows are just headers
        rows = tables[table_num].find_all("tr")[2:-1]
        for row in rows:
            player_id = row.find("th").find("a")["href"].split("/")[3]
            player_name = row.find("a").text
            home_away = "H" if table_num < 10 else "A"
            rest_of_row = clean_row([x.text for x in row.find_all("td")][:5])
            data.append([match_id, player_id, player_name, home_away] + rest_of_row)
    return data


def get_goalkeeper(match_id, tables):
    data = []
    for table_num in [9, 16]:
        # first 2 rows are just headers
        rows = tables[table_num].find_all("tr")[2:]
        for row in rows:
            player_id = row.find("th").find("a")["href"].split("/")[3]
            rest_of_row = clean_row([x.text for x in row.find_all("td")][3:])
            data.append([match_id, player_id] + rest_of_row)
    return data


def get_data(match_id, tables, i):
    data = []
    for table_num in [3 + i, 10 + i]:
        # first 2 rows are just headers
        rows = tables[table_num].find_all("tr")[2:-1]
        for row in rows:
            player_id = row.find("th").find("a")["href"].split("/")[3]
            rest_of_row = clean_row([x.text for x in row.find_all("td")][5:])
            data.append([match_id, player_id] + rest_of_row)
    return data


def handle_insert_player_error(match_id):
    print(f"\nProblem with match ID {match_id} - Not enough tables in the web page.")
    print(f"https://fbref.com/en/matches/{match_id}/")
    print(
        "This could be because the match was abandoned, never played, or otherwise affected"
    )
    print(
        "If the match was not abandoned, you believe this should work, and this problem persists, please raise an issue at"
    )
    print("https://github.com/ChrisMusson/FBRef_DB/issues")
    return


def insert_players(cursor, competition, season, match_ids):
    if match_ids == []:
        print(f"Database is up to date for {competition} {season}\n")
        return
    player_info = []
    goalkeeper = []
    db_tables = [
        "summary",
        "passing",
        "pass_types",
        "defensive_actions",
        "possession",
        "miscellaneous",
    ]

    season_data = {}
    for t in db_tables:
        season_data[t] = []

    for number, match_id in enumerate(match_ids):
        print(
            f"{competition} {season} - Parsing match number {number + 1} of {len(match_ids)} - ID: {match_id}"
        )
        match_data = get_match_data(competition, season, match_id)
        if len(match_data) < 10:
            handle_insert_player_error(match_id)
            continue

        player_info += get_player_info(match_id, match_data)
        goalkeeper += get_goalkeeper(match_id, match_data)

        for i, t in enumerate(db_tables):
            season_data[t] += get_data(match_id, match_data, i)

    print(f"Inserting player data for {competition} {season}")
    insert(cursor, "Player_info", player_info)
    insert(cursor, "Goalkeeper", goalkeeper)

    for k, v in season_data.items():
        insert(cursor, k.title(), v)

    print("Insertion finished\n\n")
