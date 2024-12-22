"""Скрипт для быстрой записи ингредиентов и тегов в базу данных sqlite3."""
import csv
import sqlite3


con = sqlite3.connect("db.sqlite3")

cur = con.cursor()

ingredients = ('data\\ingredient.csv')
tags = ('data\\tag.csv')

with open(ingredients, encoding='utf-8') as file:
    data = csv.DictReader(file)
    to_base = [(i['name'], i['measurement_unit']) for i in data]
    for i in to_base:
        cur.executemany(
            "INSERT INTO recipes_ingredient"
            "(name, measurement_unit) VALUES (?, ?);",
            [i]
        )

with open(tags, encoding='utf-8') as file:
    data = csv.DictReader(file)
    to_base = [(i['name'], i['slug']) for i in data]
    for i in to_base:
        cur.executemany(
            "INSERT INTO recipes_tag (name, slug) VALUES (?, ?);",
            [i]
        )


con.commit()
con.close()
