from pymongo import MongoClient
import json


client = MongoClient('mongodb://localhost:27017/')

# Создаем базу данных и коллекцию
db = client['books_db']
collection = db['books']

# Удаляем коллекцию, если она уже существует
if 'books' in db.list_collection_names():
    db.drop_collection('books')
    print("🗑️ Существующая коллекция удалена.")

# Загрузка данных из JSON файла, который мы получили после скрейпинга сайта с книгами
file_path = r'C:\Users\Саша - Лютый\Desktop\DataEng\HW_2\books.json'

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        books_data = json.load(file)
except FileNotFoundError:
    print(f"❌ Файл не найден: {file_path}")
    exit()
except json.JSONDecodeError as e:
    print(f"❌ Ошибка чтения JSON: {e}")
    exit()

# Проверка структуры данных
if not isinstance(books_data, list):
    print("❌ Ожидался список книг в JSON файле.")
    exit()

# Загружаем данные в MongoDB
try:
    collection.insert_many(books_data)
    print(f"✅ Загружено книг: {len(books_data)}")
except Exception as e:
    print(f"⚠️ Ошибка при загрузке данных: {e}")

# Примеры запросов к базе данных
print("\n🔎 Примеры запросов:")

# 1. Найти книгу по названию
title_query = collection.find_one({'title': 'A Light in the Attic'})
print(f"📘 Книга с названием 'A Light in the Attic': {title_query}\n")

# 2. Найти все книги с рейтингом выше 4.5
high_rating_books = list(collection.find({'rating': {'$gt': 4.5}}))
print(f"⭐ Книги с рейтингом выше 4.5: {len(high_rating_books)}")

# 3. Найти книги дешевле 20 фунтов
cheap_books = list(collection.find({'price': {'$lt': 20}}))
print(f"💷 Книги дешевле 20 фунтов: {len(cheap_books)}")

# 4. Подсчитать количество книг в каждой категории
categories = collection.aggregate([
    {"$group": {"_id": "$category", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
])
print("📚 Количество книг по категориям:")
for category in categories:
    print(f" - {category['_id']}: {category['count']}")

# 5. Найти самую дорогую книгу
most_expensive = collection.find_one(sort=[("price", -1)])
print(f"💎 Самая дорогая книга: {most_expensive}")

print("\n🎉 Все запросы выполнены успешно!")
