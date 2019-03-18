CREATE TABLE meta_books (book_id INTEGER PRIMARY KEY AUTOINCREMENT, booktitle VARCHAR, year INTEGER, city VARCHAR, publisher VARCHAR, publisher_unified VARCHAR, printrun INTEGER, kid INTEGER, junior INTEGER, youth INTEGER);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE meta_authors (author_id INTEGER PRIMARY KEY AUTOINCREMENT, last VARCHAR, first VARCHAR, middle VARCHAR, sex VARCHAR, birth_year INTEGER, death_year INTEGER);
CREATE TABLE meta_pseudo (auth_id INTEGER, last VARCHAR, first VARCHAR, middle VARCHAR, pseudo_id INTEGER, FOREIGN KEY (auth_id) REFERENCES meta_authors (author_id));
CREATE TABLE text_author (pseudo_id INTEGER, auth_id INTEGER, uu VARCHAR,  FOREIGN KEY (auth_id) REFERENCES meta_authors (author_id),  FOREIGN KEY (uu) REFERENCES meta_editions (uuid), FOREIGN KEY (pseudo_id) REFERENCES meta_pseudo(pseudo_id));
CREATE TABLE meta_editions (book_id INTEGER, author_name VARCHAR, title VARCHAR, uuid VARCHAR, filename VARCHAR, FOREIGN KEY (book_id) REFERENCES meta_books (book_id));
