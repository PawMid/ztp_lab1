import sqlite3
from sqlite3 import Connection

# Podłączenie do bazy
db_file = 'library.db'


def connect():
    db_con = sqlite3.connect(db_file)
    db_con.row_factory = sqlite3.Row
    return db_con


# Inicjalizacja przykładowej bazy danych

def init():
    db_con = sqlite3.connect(db_file)
    db_con.row_factory = sqlite3.Row
    with open(r'doc/create_library_db.sql', 'r') as f:
        db_con.executescript(f.read())
        db_con.commit()
