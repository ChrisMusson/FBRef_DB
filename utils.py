ignore = {
    "bundesliga": {
        "5dc40876",  # 17-18 relegation/promotion leg 1
        "9c6a24db",  # 17-18 relegation/promotion leg 2
        "e262266b",  # 18-19 relegation/promotion leg 1
        "f5e7a5c2",  # 18-19 relegation/promotion leg 2
        "434865ef",  # 19-20 relegation/promotion leg 1
        "2f2a35fa",  # 19-20 relegation/promotion leg 2
        "dc47142c",  # 20-21 relegation/promotion leg 1
        "948872ab",  # 20-21 relegation/promotion leg 2
        "ac3eb7f6",  # 21-22 relegation/promotion leg 1
        "d50b48fe",  # 21-22 relegation/promotion leg 2
        "2c791569",  # 22-23 relegation/promotion leg 1
        "f9a47a86",  # 22-23 relegation/promotion leg 2
        "9156fa34",  # 23-24 relegation/promotion leg 1
        "723ffa45",  # 23-24 relegation/promotion leg 2
        "ea16299e",  # 24-25 relegation/promotion leg 1
        "933eae7f",  # 24-25 relegation/promotion leg 2
        "c34bbc21",  # 21-22 - Bochum:Monchengladbach - Abandoned - Fan Trouble
        "171e1d37",  # 24-25 - Union_Berlin:Bochum - Abandoned - Fan Trouble
    },
    "ligue_1": {
        "f927719d",  # 17-18 relegation/promotion leg 1
        "06517ea5",  # 17-18 relegation/promotion leg 2
        "bfd434c1",  # 18-19 relegation/promotion leg 1
        "ea5db1c4",  # 18-19 relegation/promotion leg 2
        "621f8a81",  # 20-21 relegation/promotion leg 1
        "28ce9808",  # 20-21 relegation/promotion leg 2
        "f1560d55",  # 21-22 relegation/promotion leg 1
        "78ed8c0d",  # 21-22 relegation/promotion leg 1
        "febd4e01",  # 23-24 relegation/promotion leg 1
        "7f01f697",  # 23-24 relegation/promotion leg 2
        "111651be",  # 24-25 relegation/promotion leg 1
        "5e063c64",  # 24-25 relegation/promotion leg 2
        "15ee650c",  # 24-25 - Montpellier:Saint_Etienne - Abandoned - Fan Trouble
    },
    "serie_a": {
        "e0449015",  # 22-23 relegation tie-breaker
        "e0a20cfe",  # 20-21 - Hellas_Verona:Roma - Result Awarded - Registration Error
        "f7e35659",  # 24-25 - Fiorentina:Inter - Match Suspended - Player Injury
    },
    "primeira_liga": {
        "3f514a62",  # 20-21 relegation/promotion leg 1
        "9c028e7e",  # 20-21 relegation/promotion leg 2
        "c8cd6748",  # 21-22 relegation/promotion leg 1
        "65aab877",  # 21-22 relegation/promotion leg 2
        "fb49ed3b",  # 22-23 relegation/promotion leg 1
        "b4f01c0d",  # 22-23 relegation/promotion leg 2
        "f889dc95",  # 23-24 relegation/promotion leg 1
        "0ede3890",  # 23-24 relegation/promotion leg 2
        "12b7459d",  # 24-25 relegation/promotion leg 1
        "1be42753",  # 24-25 relegation/promotion leg 2
    },
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
