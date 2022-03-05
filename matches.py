import json
import requests
from bs4 import BeautifulSoup
from utils import *


def get_match_data(season):
    data = []
    with open("db_helper.json", "r") as f:
        url = json.load(f)["competition_urls"][season]

    with requests.Session() as s:
        table = BeautifulSoup(s.get(url).text, "html.parser").find("table")
        rows = table.find_all("tr")
        for row in rows[1:]:
            if row.find_all("td")[-3].text == "":  # if referee field is blank
                continue
            match_id = row.find_all("a")[-1]["href"].split("/")[3]
            row = [x.text.strip() for x in row.find_all("td")][:-2]

            # convert each field to the correct datatype
            p1 = [match_id] + row[:4]
            p2 = [float(row[4])] + \
                list(map(int, row[5].split("–"))) + [float(row[6])]
            p3 = [row[7]] + [int(row[8].replace(",", ""))
                             if row[8] != "" else ""] + row[9:]

            data.append([season] + p1 + p2 + p3)
    return data


def update_matches(season, cursor):
    cursor.execute(f"DELETE FROM Match WHERE season = ?", (season,))
    match_data = get_match_data(season)
    insert(cursor, "Match", match_data)
