ignore = {
    "bundesliga": {
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
    },
    "ligue_1": {
        "f927719d",
        "06517ea5",
        "bfd434c1",
        "ea5db1c4",
        "621f8a81",
        "28ce9808",
        "f1560d55",
        "78ed8c0d",
    },
    "serie_a": {"e0449015"},
    "primeira_liga": {
        "3f514a62",
        "9c028e7e",
        "c8cd6748",
        "65aab877",
        "fb49ed3b",
        "b4f01c0d",
    },
    "other":{
        "e0a20cfe",  # SerieA_2020-2021 - Verona:Roma - Result Awarded - Registration Error
        "c34bbc21",  # Bundesliga_2021-2022 - Bochum:Monchengladbach - Abandoned - Fan Trouble}
    }
}

def clean_row(row):
    for i, d in enumerate(row):
        if d == "":
            row[i] = None
        elif "." in d:
            row[i] = float(d)
        else:
            try:
                row[i] = int(d)
            except ValueError:
                continue
    return row


def insert(cursor, table_name, data):
    if data == [] or len(data[0]) == 0:
        return
    q_marks = ",".join(["?"] * len(data[0]))
    cursor.executemany(f"INSERT INTO {table_name} VALUES ({q_marks})", data)


def get_matches_in_database(cursor, competition, season):
    matches = cursor.execute(
        """SELECT DISTINCT s.match_id
            FROM Summary s
            LEFT JOIN Match m
            ON s.match_id = m.match_id
            WHERE m.competition = ? AND m.season = ?""",
        (competition, season),
    ).fetchall()
    return set([x[0] for x in matches])
