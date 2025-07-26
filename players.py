import os
from concurrent.futures import ProcessPoolExecutor, as_completed

from bs4 import BeautifulSoup
from tqdm import tqdm

from utils import clean_row, insert


def get_player_info(match_id, tables):
    data = []
    for table_num in [3, 10]:
        rows = tables[table_num].find_all("tr")[2:-1]
        for row in rows:
            player_id = row.find("th").find("a")["href"].split("/")[3]
            player_name = row.find("a").text
            home_away = "H" if table_num < 10 else "A"
            started_match = row.text[0].isalpha()
            rest_of_row = clean_row([x.text for x in row.find_all("td")][:5])
            data.append([match_id, player_id, player_name, home_away, started_match] + rest_of_row)
    return data


def get_goalkeeper(match_id, tables):
    data = []
    for table_num in [9, 16]:
        rows = tables[table_num].find_all("tr")[2:]
        for row in rows:
            player_id = row.find("th").find("a")["href"].split("/")[3]
            rest_of_row = clean_row([x.text for x in row.find_all("td")][3:])
            data.append([match_id, player_id] + rest_of_row)
    return data


def get_data(match_id, tables, i):
    data = []
    for table_num in [3 + i, 10 + i]:
        rows = tables[table_num].find_all("tr")[2:-1]
        for row in rows:
            player_id = row.find("th").find("a")["href"].split("/")[3]
            rest_of_row = clean_row([x.text for x in row.find_all("td")][5:])
            data.append([match_id, player_id] + rest_of_row)
    return data


def handle_insert_player_error(match_id):
    print(f"\nProblem with match ID {match_id} - Not enough tables in the web page.")
    print(f"https://fbref.com/en/matches/{match_id}/")
    print("This could be because the match was abandoned, never played, or otherwise affected")
    print("If the match was not abandoned, you believe this should work, and this problem persists, please raise an issue at")
    print("https://github.com/ChrisMusson/FBRef_DB/issues")
    return


def process_single_match(match_id, competition, season, db_tables):
    filepath = os.path.join("web_pages", competition, season, match_id)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return match_id, None, None, None

    soup = BeautifulSoup(html_content, "lxml")
    tables = soup.find_all("table")

    if len(tables) < 10:
        return match_id, None, None, None

    player_info = get_player_info(match_id, tables)
    goalkeeper = get_goalkeeper(match_id, tables)

    season_data = {}
    for i, t in enumerate(db_tables):
        season_data[t] = get_data(match_id, tables, i)

    return match_id, season_data, player_info, goalkeeper


def insert_players(cursor, competition, season, match_ids):
    if not match_ids:
        print(f"Database is up to date for {competition} {season}\n")
        return

    db_tables = [
        "summary",
        "passing",
        "pass_types",
        "defensive_actions",
        "possession",
        "miscellaneous",
    ]

    all_player_info = []
    all_goalkeepers = []
    season_data_agg = {t: [] for t in db_tables}

    print(f"Starting match processing for {len(match_ids)} matches...")

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_single_match, match_id, competition, season, db_tables) for match_id in match_ids]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Parsing matches"):
            try:
                match_id, season_data, player_info, goalkeeper = future.result()
                if season_data is None:
                    handle_insert_player_error(match_id)
                    continue

                all_player_info.extend(player_info)
                all_goalkeepers.extend(goalkeeper)
                for t in db_tables:
                    season_data_agg[t].extend(season_data[t])

            except Exception as e:
                # If an exception happens, get match_id if possible from the future,
                # else just log it generically.
                # Unfortunately, future.result() raises here so we can't get match_id cleanly.
                # One approach: wrap process_single_match to catch and return errors with match_id.
                print(f"\nError processing a match: {e}")
                # Optionally print traceback:
                import traceback

                traceback.print_exc()

                # We can't get match_id here, so just print generic message.
                print("Problem processing a match (match ID unknown).")

    print(f"Inserting player data for {competition} {season}")
    insert(cursor, "Player_info", all_player_info)
    insert(cursor, "Goalkeeper", all_goalkeepers)

    for k, v in season_data_agg.items():
        insert(cursor, k.title(), v)

    print("Insertion finished\n\n")
