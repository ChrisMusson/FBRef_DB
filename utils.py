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
    q_marks = ','.join(['?'] * len(data[0]))
    cursor.executemany(f"INSERT INTO {table_name} VALUES ({q_marks})", data)


def get_matches_in_database(cursor, competition, season):
    matches = cursor.execute(
            f"""SELECT DISTINCT s.match_id
		    FROM Summary s
		    LEFT JOIN Match m
		    ON s.match_id = m.match_id
	        WHERE m.competition = ? AND m.season = ?""", (competition, season)).fetchall()
    return set([x[0] for x in matches])
