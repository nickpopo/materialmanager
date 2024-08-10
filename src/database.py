import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("data/materials_db.sqlite")
        return conn
    except Error as e:
        print(e)
    return conn

def create_tables(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL)''')

        c.execute('''CREATE TABLE IF NOT EXISTS materials (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        barcode TEXT NOT NULL UNIQUE,
                        quantity INTEGER NOT NULL,
                        unit TEXT NOT NULL)''')

        conn.commit()
    except Error as e:
        print(e)
