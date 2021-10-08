import os
from os.path import basename
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
import random
import string
from flask_sqlalchemy import SQLAlchemy
from flask_sessionstore import Session
from flask_session_captcha import FlaskSessionCaptcha

CURRENT_PATH = os.path.dirname(__file__)
UPLOAD_FOLDER = f'{CURRENT_PATH}/uploads'
ALLOWED_EXTENTIONS = {'png', 'jpg'}


def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits)
              for i in range(n)]
   return ''.join(randlst)


app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 6
app.config['CAPTCHA_WIDTH'] = 160
app.config['CAPTCHA_HEIGHT'] = 60

# Session(app)
captcha = FlaskSessionCaptcha(app)

db = SQLAlchemy(app)


class Imgs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(50), nullable=False)
    page = db.Column(db.Integer, nullable=False)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part.')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if captcha.validate():
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f'{randomname(10)}.{file_ext}'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                count = len([i for i in os.listdir('./uploads/')])
                new_img = Imgs(img_url=filename, page=count//15)
                db.session.add(new_img)
                db.session.commit()
                return redirect(url_for('uploaded_file', filename=filename))
            else:
                flash('captcha failed.')
        else:
            flash('Selected file extention is not available.')
            return redirect(request.url)

    return render_template('index.html', title='Simple Image Uploader')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/uploads')
def uploads_list():
    # files_path = glob.glob(f'{CURRENT_PATH}/uploads/*')
    # files_name = [os.path.basename(file) for file in files_path]
    page = request.args.get('p', default=0, type=int)
    imgs = Imgs.query.filter_by(page=page).all()
    return render_template('uploads.html', _files_name=imgs, title='Uploaded Images', page=page)


if __name__ == '__main__':
    app.run(port=4000)
