"""Example to migrate data to db."""
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
