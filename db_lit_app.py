import sqlite3


conn = sqlite3.connect('app_child.db')

c = conn.cursor()


c.execute('''
CREATE TABLE book_information(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    year INTEGER,
    city TEXT,
    publisher TEXT,
    printrun INTEGER,
    kid INTEGER,
    junior INTEGER,
    youth INTEGER
)
''')
conn.commit()

book_information = [
    {'title': 'Денискины Рассказы',
     'year': '1970',
     'city': 'Москва',
     'publisher': 'Детгиз',
     'printrun': '30000',
     'kid': '1',
     'junior': '1',
     'youth': '0'
     },
    {'title': 'Денискины Рассказы',
     'year': '1970',
     'city': 'Москва',
     'publisher': 'Детгиз',
     'printrun': '30000',
     'kid': '1',
     'junior': '1',
     'youth': '0'
     },

]

for book_info in book_information:
    c.execute("INSERT INTO book_information "
              "( 'title', 'year', 'city', 'publisher', 'printrun', 'kid', 'junior', 'youth')"
              "VALUES "
              "('{title}', '{year}', '{city}', '{publisher}', '{printrun}', '{kid}', '{junior}', '{youth}' )".format(**book_info))
    conn.commit()


c.execute('''
    INSERT INTO book_information (title, year, city, publisher, printrun, kid, junior, youth)
    VALUES
    ("Денискины Рассказы1", 1970, "Москва", "Детгиз", 30000, 1, 1, 1)
''')
conn.commit()
conn.close()



