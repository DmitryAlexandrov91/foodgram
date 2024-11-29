"""Example to migrate data to db."""
import csv
import sqlite3


# Создаём подключение к базе данных.
con = sqlite3.connect("db.sqlite3")

cur = con.cursor()

# Импорт данныех из файла category.csv
# Считываем данные из csv файла.
with open('ingredients.csv', encoding='utf-8') as file:
    data = csv.DictReader(file)
    # Преобразуем данные в список кортежей при помощи list comprehension.
    to_base = [(i['name'], i['measurement_unit']) for i in data]
    for i in to_base:
        # Методом executemany вставляем данные в базу данных.
        cur.executemany(
            "INSERT INTO recipes_ingredient (name, measurement_unit) VALUES (?, ?);",
            [i]
        )

con.commit()
con.close()
