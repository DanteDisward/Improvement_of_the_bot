import sqlite3
import os.path


def initiate_db():
    connection = sqlite3.connect("Bot.db")
    cursor = connection.cursor()

    cursor.execute('''
    DROP TABLE IF EXISTS Products
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER
    )
    ''')

    for i in range(1, 5):
        cursor.execute(f"INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                       (f"Продукт{i}", f"Описание{i}", f"{i * 100}"))
    connection.commit()
    connection.close()


def get_all_products():
    title_db = 'Bot.db'
    if not os.path.exists(title_db):
        initiate_db()
    connection = sqlite3.connect(title_db)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Products")
    products = cursor.fetchall()
    connection.close()
    return products
