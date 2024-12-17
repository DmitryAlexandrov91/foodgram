import os

from dotenv import load_dotenv

load_dotenv()


def debug_bool_check():
    debug = os.getenv('DEBUG', 'False')
    return debug.lower() == 'true'


def get_allowed_hosts():
    allowed_hosts = os.getenv('ALLOWED_HOSTS', 'localhost, 127.0.0.1')
    return [host.strip() for host in allowed_hosts.split(',')]


def load_to_base():
    import csv
    import sqlite3

    con = sqlite3.connect("db.sqlite3")

    cur = con.cursor()

    with open('ingredients.csv', encoding='utf-8') as file:
        data = csv.DictReader(file)
        to_base = [(i['name'], i['measurement_unit']) for i in data]
        for i in to_base:
            cur.executemany(
                "INSERT INTO recipes_ingredient (name, measurement_unit) VALUES (?, ?);",
                [i]
            )

    con.commit()
    con.close()
