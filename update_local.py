import json
import os
import requests
from bs4 import BeautifulSoup


def update_local(competition, season):
    stored_files = set(os.listdir(os.path.join("web_pages", competition, season)))
    with open("db_helper.json", "r") as f:
        url = json.load(f)["competition_urls"][competition][season]

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
            for number, match_id in enumerate(missing_match_ids):
                print(f"{competition} {season}: Fetching match number {number + 1} of {n} - ID: {match_id}")
                url = f"https://fbref.com/en/matches/{match_id}/"
                resp = s.get(url).text

                if "Advanced data not yet available" in resp:
                    print(f"Full data for {competition} {season} match {match_id} is not yet available\n")
                    continue

                with open(os.path.join("web_pages", competition, season, match_id), 'w') as f:
                    f.write(resp)
    else:
        print(f"Local files are up to date for {competition} {season}")
