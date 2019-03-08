import sqlite3

conn = sqlite3.connect('app.db')

c = conn.cursor()
c.execute('''
drop TABLE digest_info''')

c.execute('''
CREATE TABLE digest_info(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    link TEXT,
    name TEXT,
    author TEXT,
    Booktype TEXT
)
''')

digest_info = [
    {'id': '1',
     'link': 'clck.ru/FKbY9',
     'name': 'Deniskini Rasskazi',
     'author': 'Viktor Dragunskiy',
     'Booktype': 'Digest'
     }]

for digest in digest_info:
    c.execute("INSERT INTO digest_info "
              "('id', 'link', 'name', 'author', 'Booktype')"
              "VALUES "
              "('{id}','{link}', '{name}', '{author}', '{Booktype}')".format(**digest))
    conn.commit()





c.execute('''
CREATE TABLE book_info(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    link TEXT,
    Booktype TEXT
)
''')

book_info = [
    {'id': '1',
     'link': 'clck.ru/FKbY9',
     'Booktype': 'Book'
     }]

for book in book_info:
    c.execute("INSERT INTO book_info "
              "('id', 'link', 'Booktype')"
              "VALUES "
              "('{id}','{link}', 'Booktype')".format(**book))
    conn.commit()


