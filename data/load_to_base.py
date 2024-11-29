"""Example to migrate data to db."""
import csv
import sqlite3


# Создаём подключение к базе данных.
con = sqlite3.connect("/backend/foodgram/db.sqlite3")

cur = con.cursor()

# Импорт данныех из файла category.csv
# Считываем данные из csv файла.
with open('ingredients.csv', encoding='utf-8') as file:
    data = csv.DictReader(file)
    # Преобразуем данные в список кортежей при помощи list comprehension.
    to_base = [(i['абрикосовое варенье'], i['г']) for i in data]
    for i in to_base:
        # Методом executemany вставляем данные в базу данных.
        cur.executemany(
            "INSERT INTO recipes_ingredient (name, measurement_unit) VALUES (?, ?);",
            [i]
        )

# # # Импорт данныех из файла comments.csv
# with open('comments.csv', encoding='utf-8') as file:
#     data = csv.DictReader(file)
#     to_base = [
#         (i['id'],
#          i['text'],
#          i['review_id'],
#          i['pub_date'],
#          i['author']) for i in data]
#     for i in to_base:
#         cur.executemany(
#             "INSERT INTO reviews_comment (id, text, review_id, pub_date, author_id) VALUES (?, ?, ?, ?, ?);",
#             [i]
#         )

# # Импорт данныех из файла genre_title.csv
# with open('genre_title.csv', encoding='utf-8') as file:
#     data = csv.DictReader(file)
#     to_base = [
#         (i['id'],
#          i['genre_id'],
#          i['title_id']
#          ) for i in data]
#     for i in to_base:
#         cur.executemany(
#             "INSERT INTO reviews_genretitle (id, genre_id, title_id) VALUES (?, ?, ?);",
#             [i]
#         )

# # Импорт данныех из файла genre.csv
# with open('genre.csv', encoding='utf-8') as file:
#     data = csv.DictReader(file)
#     to_base = [
#         (i['id'],
#          i['name'],
#          i['slug']
#          ) for i in data]
#     for i in to_base:
#         cur.executemany(
#             "INSERT INTO reviews_genre (id, name, slug) VALUES (?, ?, ?);",
#             [i]
#         )

# # Импорт данныех из файла review.csv
# with open('review.csv', encoding='utf-8') as file:
#     data = csv.DictReader(file)
#     to_base = [
#         (i['id'],
#          i['text'],
#          i['pub_date'],
#          i['score'],
#          i['author'],
#          i['title_id']
#          ) for i in data]
#     for i in to_base:
#         cur.executemany(
#             "INSERT INTO reviews_review (id, text, pub_date, score, author_id, title_id_id) VALUES (?, ?, ?, ?, ?, ?);",
#             [i]
#         )

# # Импорт данныех из файла titles.csv
# with open('titles.csv', encoding='utf-8') as file:
#     data = csv.DictReader(file)
#     to_base = [
#         (i['id'],
#          i['name'],
#          i['year'],
#          i['category']
#          ) for i in data]
#     for i in to_base:
#         cur.executemany(
#             "INSERT INTO reviews_review (id, name, year, score, author_id, title_id_id) VALUES (?, ?, ?, ?, ?, ?);",
#             [i]
#         )

con.commit()
con.close()
