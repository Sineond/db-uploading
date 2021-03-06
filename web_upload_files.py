import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import sqlite3





def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# указываем папку, в которую будут загружаться файлы
UPLOAD_FOLDER = 'C:/UploFiles'
# указываем допустимые расширения
ALLOWED_EXTENSIONS = set(['txt', 'fb2'])

# указываем класс name, чтобы фласк понимал, с чем мы работаем
app_child = Flask(__name__)
app_child.config['SECRET_KEY'] = 'child_lit'
# указываем фласку на папку, заданную нами ранее
app_child.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# проверяем соответствует ли расширение файла разрешенным
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# указываем url который будет вызывать функцию, в нашем случае это стартовая страница "/"
@app_child.route('/', methods=['GET', 'POST'])
# request method  POST нужен для того чтобы загружать файлы
def upload_file():
    conn = sqlite3.connect('childlit_new.sqlite')
    conn.row_factory = dict_factory
    c = conn.cursor()
    if request.method == 'POST':
        # указываем что такое file, у нас file это то, что сайт запрашивает у юзера
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # сохраняем в выбранную папку под оригинальным именем 'filename'
            file.save(os.path.join(app_child.config['UPLOAD_FOLDER'], filename))
            return redirect('/add_book')

    return render_template('upload_file.html')




@app_child.route('/add_book', methods=['GET','POST'])
def add_book():
    book_created = False
    error_message = ""
    if request.method == 'POST':
        meta_info = {}
        meta_edit = {}
        meta_info['book_id'] = request.form.get('book_id')
        meta_info['booktitle'] = request.form.get('booktitle')
        meta_info['year'] = request.form.get('year')
        meta_info['city'] = request.form.get('city')
        meta_info['publisher'] = request.form.get('publisher')
        meta_info['publisher_unified'] = request.form.get('publisher_unified')
        meta_info['printrun'] = request.form.get('printrun')
        meta_info['kid'] = request.form.get('kid')
        meta_info['junior'] = request.form.get('junior')
        meta_info['youth'] = request.form.get('youth')
        conn = sqlite3.connect('childlit_new.sqlite')
        c = conn.cursor()

        c.execute("SELECT * FROM meta_books WHERE booktitle='%s'" % meta_info['booktitle'])
        if c.fetchone():
            error_message = "book_exists"
        else:
            c.execute("PRAGMA foreign_keys = ON")
            c.execute("INSERT INTO meta_books "
                  "('booktitle', 'year', 'city', 'publisher', 'publisher_unified', 'printrun', 'kid', 'junior', 'youth')"
                  "VALUES "
                  "('{booktitle}', '{year}', '{city}', '{publisher}', '{publisher_unified}', '{printrun}', '{kid}', '{junior}', '{youth}' )"
                  "".format(**meta_info))

            c.execute("INSERT INTO meta_editions "
                      "('book_id')"
                      "VALUES "
                      "('{book_id}'')"
                      "".format(**meta_edit))
            conn.commit()

            book_created = True
        conn.close()
        return redirect("/add_author")
    return render_template('add_book.html',
                           book_created=book_created,
                           error_message=error_message)



@app_child.route('/add_author', methods=['GET', 'POST'])
def add_author():
    author_created = False
    error_message1 = ""
    if request.method == 'POST':
        meta_info_a = {}
        meta_info_a['author_id'] = request.form.get('author_id')
        meta_info_a['last'] = request.form.get('last')
        meta_info_a['first'] = request.form.get('first')
        meta_info_a['middle'] = request.form.get('middle')
        meta_info_a['sex'] = request.form.get('sex')
        meta_info_a['birth_year'] = request.form.get('birth_year')
        meta_info_a['death_year'] = request.form.get('death_year')


        conn = sqlite3.connect('childlit_new.sqlite')
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("SELECT * FROM meta_authors WHERE last='%s'" % meta_info_a['last'])
        if c.fetchone():
            error_message1 = "author_exists"
        else:
            c.execute("PRAGMA foreign_keys = ON")
            c.execute("INSERT INTO meta_authors "
                      "('last', 'first', 'middle', 'sex', 'birth_year', 'death_year')"
                      "VALUES "
                      "('{last}', '{first}', '{middle}', '{sex}', '{birth_year}', '{death_year}')"
                      "".format(**meta_info_a))
            conn.commit()
            author_created = True
        conn.close()
        return redirect("/add_edition")
    return render_template('add_author.html',
                           author_created=author_created,
                           error_message1=error_message1)


@app_child.route('/add_edition', methods=['GET', 'POST'])
def add_edition():
    if request.method == 'POST':
        meta_edit = {}
        meta_edit['author_name'] = request.form.get('author_name')
        meta_edit['title'] = request.form.get('title')
        meta_edit['book_id'] = request.form.get('book_id')

        conn = sqlite3.connect('childlit_new.sqlite')
        c = conn.cursor()
        c.execute("INSERT INTO meta_editions "
                      "('author_name', 'title')"
                      "VALUES "
                      "('{author_name}', '{title}')"
                      "".format(**meta_edit))

        conn.commit()
        conn.close()
        return redirect("/Success")
    return render_template('add_edition.html')


@app_child.route('/Success', methods=['GET', 'POST'])
def success():
    return render_template("Success.html")


app_child.run()
