import json
import os
import time

import requests
from bs4 import BeautifulSoup


def update_local(competition, season):
    # set of matches to ignore for various reasons
    # currently, most matches in here are those that are in the bundesliga/ligue1 relegation playoff phases
    # I have decided to ignore these as they are not part of the regular season, and
    # FBRef has no player data for these matches anyway
    # Other matches that have been abandoned are also included, such as Bochum vs. Monchengladbach,
    # where the game was abandoned after an assistant referee was hit by something thrown from the stands
    bundesliga_relegation = {
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
        "2c791569",
        "f9a47a86",
    }

    ligue1_relegation = {
        "f927719d",
        "06517ea5",
        "bfd434c1",
        "ea5db1c4",
        "621f8a81",
        "28ce9808",
        "f1560d55",
        "78ed8c0d",
    }

    serie_a_relegation = {"e0449015"}

    other_ignore = {
        "e0a20cfe",  # SerieA_2020-2021 - Verona:Roma - Result Awarded - Registration Error
        "c34bbc21",  # Bundesliga_2021-2022 - Bochum:Monchengladbach - Abandoned - Fan Trouble
    }

    ignored_matches = (
        bundesliga_relegation | ligue1_relegation | serie_a_relegation | other_ignore
    )

    if not os.path.exists("web_pages"):
        os.mkdir("web_pages")
    if not os.path.exists(os.path.join("web_pages", competition)):
        os.mkdir(os.path.join("web_pages", competition))
    if not os.path.exists(os.path.join("web_pages", competition, season)):
        os.mkdir(os.path.join("web_pages", competition, season))

    stored_files = set(os.listdir(os.path.join("web_pages", competition, season)))
    with open("db_helper.json", "r") as f:
        competition_id = json.load(f)["competition_ids"][competition]
        url = f"https://fbref.com/en/comps/{competition_id}/{season}/schedule/"

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
        return

    print(f"Fetching {n} {'matches' if n > 1 else 'match'}")
    with requests.Session() as s:
        for number, match_id in enumerate(missing_match_ids):
            time.sleep(6)
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
