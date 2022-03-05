import json
import os
import requests
from bs4 import BeautifulSoup


def update_local(season):
    stored_files = set(os.listdir(os.path.join("web_pages", season)))
    with open("db_helper.json", "r") as f:
        url = json.load(f)["competition_urls"][season]

    web_match_ids = set()
    with requests.Session() as s:
        r = BeautifulSoup(s.get(url).text, "html.parser")
        rows = r.find_all("td", {"data-stat": "score"})
        for row in rows:
            link = row.find("a")
            if link:
                web_match_ids.add(link["href"].split(
                    "matches/")[1].split("/")[0])
            else:
                continue

    missing_match_ids = web_match_ids - stored_files
    n = len(missing_match_ids)

    if n > 0:
        print(f"Fetching {n} {'matches' if n > 1 else 'match'}")
        with requests.Session() as s:
            for match_id in missing_match_ids:
                print(f"Fetching match with id {match_id}")
                url = f"https://fbref.com/en/matches/{match_id}/"
                resp = s.get(url).text

                with open(os.path.join("web_pages", season, match_id), 'w') as f:
                    f.write(resp)
    else:
        print("Local files are up to date")
