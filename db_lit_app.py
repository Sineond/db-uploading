import sqlite3


conn = sqlite3.connect('childlit.sqlite')

c = conn.cursor()




meta_books = [
    {'book_id': 1,
     'booktitle': 'Денискины Рассказы',
     'year': '1970',
     'city': 'Москва',
     'publisher': 'Детгиз',
     'printrun': '30000',
     'kid': '1',
     'junior': '1',
     'youth': '0'
     },
    {'book_id': 2,
     'booktitle': 'Денискины Рассказы',
     'year': '1970',
     'city': 'Москва',
     'publisher': 'Детгиз',
     'printrun': '30000',
     'kid': '1',
     'junior': '1',
     'youth': '0'
     },

]

for meta_info in meta_books:
    c.execute("INSERT INTO meta_books "
              "('book_id', 'booktitle', 'year', 'city', 'publisher', 'printrun', 'kid', 'junior', 'youth')"
              "VALUES "
              "('{book_id}', '{booktitle}', '{year}', '{city}', '{publisher}', '{printrun}', '{kid}', '{junior}', '{youth}' )".format(**meta_info))
    conn.commit()


c.execute('''
    INSERT INTO meta_books (book_id, booktitle, year, city, publisher, printrun, kid, junior, youth)
    VALUES
    (3, "Денискины Рассказы1", 1970, "Москва", "Детгиз", 30000, 1, 1, 1)
''')
conn.commit()
conn.close()



