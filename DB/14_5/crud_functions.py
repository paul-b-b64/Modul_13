import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    );
    ''')
def get_all_products():
    all_prod = cursor.execute('SELECT * FROM Products;').fetchall()
    connection.commit()
    return all_prod

def add_user(username, email, age):
    cursor.execute('INSERT INTO Users(username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'{username}', f'{email}', f'{age}', '1000'))
    connection.commit()

def is_included(username):
    check_user = True
    if cursor.execute('SELECT * FROM Users WHERE username=?', (username,)).fetchone() is None:
        check_user = False
    connection.commit()
    return check_user


