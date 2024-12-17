"""Скрипт записи ингредиентов в базу данных."""
import csv
import sqlite3

from django.conf import settings


con = sqlite3.connect("db.sqlite3")

cur = con.cursor()

file_path = 'C:\\Users\\AlDmAl\\Desktop\\Python\\VSC\\Dev\\Final_projects_for_review\\foodgram\\data\\ingredients.csv'

with open(file_path, encoding='utf-8') as file:
    data = csv.DictReader(file)
    to_base = [(i['name'], i['measurement_unit']) for i in data]
    for i in to_base:
        cur.executemany(
            "INSERT INTO recipes_ingredient (name, measurement_unit) VALUES (?, ?);",
            [i]
        )

con.commit()
con.close()
