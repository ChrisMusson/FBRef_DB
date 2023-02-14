import json
import os
import requests
from bs4 import BeautifulSoup
import time


def update_local(competition, season):

    # set of matches to ignore for various reasons
    # currently, all matches in here are those that are in the bundesliga/ligue1 relegation playoff
    # I have decided to ignore these as they are not part of the regular season, and
    # FBRef has no player data for these matches anyway
    bundesliga_ignore = set(
        [
            "5dc40876",
            "9c6a24db",
            "e262266b",
            "f5e7a5c2",
            "434865ef",
            "2f2a35fa",
            "dc47142c",
            "948872ab",
            "ac3eb7f6",
            "d50b48fe",
        ]
    )

    ligue1_ignore = set(
        [
            "f927719d",
            "06517ea5",
            "bfd434c1",
            "ea5db1c4",
            "621f8a81",
            "28ce9808",
            "f1560d55",
            "78ed8c0d",
        ]
    )

    ignored_matches = bundesliga_ignore | ligue1_ignore

    stored_files = set(os.listdir(os.path.join("web_pages", competition, season)))
    with open("db_helper.json", "r") as f:
        url = json.load(f)["competition_urls"][competition][season]

    web_match_ids = set()
    with requests.Session() as s:
        r = BeautifulSoup(s.get(url).text, "lxml")
        rows = r.find_all("td", {"data-stat": "score"})
        for row in rows:
            if row.text == "":
                continue
            link = row.find("a")
            if link:
                web_match_ids.add(link["href"].split("matches/")[1].split("/")[0])
            else:
                continue

    missing_match_ids = web_match_ids - stored_files - ignored_matches
    n = len(missing_match_ids)

    if n == 0:
        print(f"Local files are up to date for {competition} {season}")
        time.sleep(5)
        return

    print(f"Fetching {n} {'matches' if n > 1 else 'match'}")
    with requests.Session() as s:
        for number, match_id in enumerate(missing_match_ids):
            time.sleep(3)
            print(
                f"{competition} {season}: Fetching match number {number + 1} of {n} - ID: {match_id}"
            )
            url = f"https://fbref.com/en/matches/{match_id}/"
            resp = s.get(url).text

            if "Advanced data not yet available" in resp:
                print(
                    f"Full data for {competition} {season} match {match_id} is not yet available\n"
                )
                continue

            with open(
                os.path.join("web_pages", competition, season, match_id),
                "w",
                encoding="utf-8",
            ) as f:
                f.write(resp)
