import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import sqlite3





def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


UPLOAD_FOLDER = 'C:/UploFiles'

ALLOWED_EXTENSIONS = set(['txt', 'fb2'])


app_child = Flask(__name__)
app_child.config['SECRET_KEY'] = 'child_lit'

app_child.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app_child.route('/upload_file', methods=['GET', 'POST'])

def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app_child.config['UPLOAD_FOLDER'], filename))
            conn = sqlite3.connect('child.sqlite')
            conn.row_factory = dict_factory
            c = conn.cursor()
            return redirect('/add_user')
    return render_template('upload_file.html')


@app_child.route('/', methods=['GET','POST'])
def add_book():
    if request.method == 'POST':
        meta_info = {}
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
        meta_info['age_category'] = request.form.get('age_category')
        meta_info_a = {}
        meta_info_a['author_id'] = request.form.get('author_id')
        meta_info_a['last'] = request.form.get('last')
        meta_info_a['first'] = request.form.get('first')
        meta_info_a['middle'] = request.form.get('middle')
        meta_info_a['sex'] = request.form.get('sex')
        meta_info_a['birth_year'] = request.form.get('birth_year')
        meta_info_a['death_year'] = request.form.get('death_year')
        meta_edit = {}
        meta_edit['author_name'] = request.form.get('author_name')
        meta_edit['title'] = request.form.get('title')
        meta_edit['book_id'] = request.form.get('book_id')
        meta_pseud = {}
        meta_pseud['last_p'] = request.form.get('last_p')
        meta_pseud['first_p'] = request.form.get('first_p')
        meta_pseud['middle_p'] = request.form.get('middle_p')

        conn = sqlite3.connect('child.sqlite')
        c = conn.cursor()
        c.execute("INSERT INTO meta_books "
                  "('booktitle', 'year', 'city', 'publisher', 'publisher_unified', 'printrun', 'kid', 'junior', 'youth')"
                  "VALUES "
                  "('{booktitle}', '{year}', '{city}', '{publisher}', '{publisher_unified}', '{printrun}', '{kid}', '{junior}', '{youth}' )"
                  "".format(**meta_info))
        c.execute("INSERT INTO meta_editions "
                  "('author_name', 'title', 'book_id')"
                  "VALUES "
                  "('{author_name}', '{title}', (SELECT last_insert_rowid()))"
                  "".format(**meta_edit))
        c.execute("INSERT INTO meta_authors "
                  "('last', 'first', 'middle', 'sex', 'birth_year', 'death_year')"
                  "VALUES "
                  "('{last}', '{first}', '{middle}', '{sex}', '{birth_year}', '{death_year}')"
                  "".format(**meta_info_a))
        c.execute("INSERT INTO meta_pseudo "
                  "('last_p', 'first_p', 'middle_p', 'author_id')"
                  "VALUES "
                  "('{last_p}', '{first_p}', '{middle_p}', (SELECT last_insert_rowid()))"
                  "".format(**meta_pseud))

        conn.commit()
        conn.close()
        return redirect('/upload_file')
    return render_template('add_book.html')




@app_child.route('/add_user', methods=['GET','POST'])
def add_user():
    user_created = False
    error_message = ""
    if request.method == 'POST':
        meta_user = {}
        meta_user['email'] = request.form.get('email')
        meta_user['name'] = request.form.get('name')
        conn = sqlite3.connect('child.sqlite')
        c = conn.cursor()
        c.execute("SELECT * FROM users where email='%s'" % meta_user['email'])
        if c.fetchone():
            error_message = "user_exists"
        else:
            c.execute("INSERT INTO users "
                      "(email, name) "
                      "VALUES "
                      "('{email}','{name}')"
                      "".format(**meta_user))
            conn.commit()
            user_created = True
        conn.commit()
        conn.close()
        return redirect('/Success')
    return render_template('add_user.html',
                           user_created = user_created,
                           error_message = error_message)


@app_child.route('/Success', methods=['GET', 'POST'])
def success():
    return render_template("Success.html")


app_child.run()
