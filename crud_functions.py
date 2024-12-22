import sqlite3
import os.path


def initiate_db():
    connection = sqlite3.connect("Bot.db")
    cursor = connection.cursor()

    # ===================================================== Table Product ==============================================
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

    # ===================================================== Table Users ================================================
    # cursor.execute('''
    #     DROP TABLE IF EXISTS Users
    #     ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username  TEXT NOT NULL,
        email  TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
        ''')

    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('Bot.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Products")
    products = cursor.fetchall()
    connection.close()
    return products


def add_user(username, email, age):
    connection = sqlite3.connect('Bot.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, 1000)",
                   (username, email, age))
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect('Bot.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(id) FROM Users WHERE username = '{username}'")
    if cursor.fetchone()[0] == 1:
        a = True
    else:
        a = False
    connection.close()
    return a
