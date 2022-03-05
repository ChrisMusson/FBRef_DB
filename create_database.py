import json


def create_database(cursor, helper_file="db_helper.json", database_file="test_build.db"):
    with open(helper_file, "r") as f:
        data = json.load(f)["column_names"]

    for table_name, fields in data.items():
        statement = ", ".join([" ".join([field, datatype])
                              for field, datatype in fields.items()])
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({statement})")
