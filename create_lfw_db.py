import sqlite3

conn = sqlite3.connect('Lfw_Database4.db')

c = conn.cursor()

sql = """
DROP TABLE IF EXISTS users;
CREATE TABLE users (
           id integer unique primary key autoincrement,
           name text,
           embedding text
);
"""
c.executescript(sql)

conn.commit()

conn.close()
