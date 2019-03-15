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



meta_authors = [
    {'author_id': 1,
     'last': 'Драгунский',
     'first': 'Виктор',
     'middle': 'Юзефович',
     'sex': 'М',
     'birth_year': '1913',
     'death_year': '1972'
     },
]

for meta_info_a in meta_authors:
    c.execute("INSERT INTO meta_authors "
              "('author_id', 'last', 'first', 'middle', 'sex', 'birth_year', 'death_year')"
              "VALUES "
              "('{author_id}', '{last}', '{first}', '{middle}', '{sex}', '{birth_year}', '{death_year}')".format(**meta_info_a))
    conn.commit()


c.execute('''
    INSERT INTO meta_authors (author_id, last, first, middle, sex, birth_year, death_year)
    VALUES
    (2, "Гайдар", "Аркадий", "Петрович", "М", 1904, 1941)
''')
conn.commit()




conn.close()



