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
UPLOAD_FOLDER = 'D:/Program Files/Uploaded Files'
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
    conn = sqlite3.connect('childlit.sqlite')
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
        meta_info['booktitle'] = request.form.get('booktitle')
        meta_info['year'] = request.form.get('year')
        meta_info['city'] = request.form.get('city')
        meta_info['publisher'] = request.form.get('publisher')
        meta_info['printrun'] = request.form.get('printrun')
        meta_info['kid'] = request.form.get('kid')
        meta_info['junior'] = request.form.get('junior')
        meta_info['youth'] = request.form.get('youth')

        conn = sqlite3.connect('childlit.sqlite')
        c = conn.cursor()
        c.execute("SELECT * FROM meta_books WHERE booktitle='%s'" % meta_info['booktitle'])
        if c.fetchone():
            error_message = "book_exists"
        else:
            c.execute("INSERT INTO meta_books "
                  "('booktitle', 'year', 'city', 'publisher', 'printrun', 'kid', 'junior', 'youth')"
                  "VALUES "
                  "('{booktitle}', '{year}', '{city}', '{publisher}', '{printrun}', '{kid}', '{junior}', '{youth}' )"
                  "".format(**meta_info))
            conn.commit()
            book_created = True
        conn.close()
        return redirect("/Success")
    return render_template('add_book.html',
                           book_created=book_created,
                           error_message=error_message)

@app_child.route('/Success', methods=['GET', 'POST'])
def success():
    return render_template("Success.html")

app_child.run()
