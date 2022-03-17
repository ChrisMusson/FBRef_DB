import json
import requests
from bs4 import BeautifulSoup
from utils import *


def get_match_data(competition, season):
    # Note that matches where the full match data is not yet available will still be picked up here and inserted
    # This is okay because every record is deleted from the specified (competition, season) pair each time, so the newly
    # updated matches will be put back into the Match table when they get updated
    data = []
    with open("db_helper.json", "r") as f:
        url = json.load(f)["competition_urls"][competition][season]

    with requests.Session() as s:
        table = BeautifulSoup(s.get(url).text, "html.parser").find("table")
        rows = table.find_all("tr")

        # for the bundesliga, e.g., the first column of the table is dedicated to either 'regular season'
        # or promotion-relegation playoff. This has to be taken into account when deciding which
        # columns to look at
        multistage: bool = rows[0].find("th")["data-stat"] == "round"

        for row in rows[1:]:
            if row.find_all("td")[-3].text == "":  # if referee field is blank
                continue
            match_id = row.find_all("a")[-1]["href"].split("/")[3]

            # if the season has multiple stages, start from column index 1 instead of 0
            row = [x.text.strip() for x in row.find_all("td")][multistage:-2]

            # convert each field to the correct datatype
            p1 = [match_id] + row[:4]
            p2 = float(row[4]) if row[4] != "" else None
            p3 = list(map(int, row[5].split("–")))
            p4 = float(row[6]) if row[6] != "" else None
            p5 = [row[7]] + [int(row[8].replace(",", ""))
                             if row[8] != "" else ""] + row[9:]

            data.append([competition, season] + p1 + [p2] + p3 + [p4] + p5)
    return data


def update_matches(cursor, competition, season):
    cursor.execute(f"DELETE FROM Match WHERE competition = ? AND season = ?", (competition, season))
    match_data = get_match_data(competition, season)
    insert(cursor, "Match", match_data)
