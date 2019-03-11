import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from wtforms import SelectField
from flask_wtf import FlaskForm

import sqlite3




# указываем папку, в которую будут загружаться файлы
UPLOAD_FOLDER = 'D:/Program Files/Uploaded files'
# указываем допустимые расширения
ALLOWED_EXTENSIONS = set(['txt', 'fb2'])

# указываем класс name, чтобы фласк понимал, с чем мы работаем
app = Flask(__name__)
app.config['SECRET_KEY'] = 'child_lit'
# указываем фласку на папку, заданную нами ранее
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# проверяем соответствует ли расширение файла разрешенным
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# указываем url который будет вызывать функцию, в нашем случае это стартовая страница "/"
@app.route('/', methods=['GET', 'POST'])
# request method  POST нужен для того чтобы загружать файлы
def upload_file():
    if request.method == 'POST':
        # указываем что такое file, у нас file это то, что сайт запрашивает у юзера
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # сохраняем в выбранную папку под оригинальным именем 'filename'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/Digest')
    return render_template('upload_file.html')


class Form(FlaskForm):
    Booktype = SelectField('Booktype', choices=[('Dg', 'Digest'), ('Bk', 'Book')])



@app.route('/choice', methods=['GET', 'POST'])
def choice():
    form = Form()
    if request.method == 'POST':
        if form.Booktype.choices == 'Digest':
            return render_template('digest.html')
        else:
            return render_template('book.html')



    return render_template('choice.html', form=form)








@app.route('/Digest', methods=['GET', 'POST'])
def project():

    digest_created = False
    error_message = ""

    if request.method == 'POST':
        digest = {}
        digest['link'] = request.form.get('link')
        digest['name'] = request.form.get('name')
        digest['author'] = request.form.get('author')

        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute("SELECT * FROM digest_info where name='%s'" % digest['name'] )
        if c.fetchone():
            error_message = "Book_already_in_database"
        else:
            c.execute("INSERT INTO digest_info "
                  "('link', 'name', 'author')"
                  "VALUES "
                  "('{link}','{name}','{author}')"
                  "".format(**digest))
            conn.commit()
            digest_created = True
        conn.close()
        return redirect('/')
    return(render_template('digest.html'))




app.route('/book', methods=['GET', 'POST'])
def project():

    book_created = False
    error_message = ""

    if request.method == 'POST':
        book = {}
        book['link'] = request.form.get('link')
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute("INSERT INTO book_info "
                  "('link')"
                  "VALUES "
                  "('{link}')"
                  "".format(**book))
        conn.commit()
        book_created = True
        conn.close()
        return redirect('/')


@app.route('/Success', methods=['GET', 'POST'])
def success():
    return render_template("Success.html")



app.run()
