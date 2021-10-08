import os
from os.path import basename
import glob
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, send_from_directory
from sqlalchemy.sql import base
from wsgi import Imgs

CURRENT_PATH = os.path.dirname(__file__)
UPLOAD_FOLDER = f'{CURRENT_PATH}/uploads'

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

files_path = glob.glob(f'{CURRENT_PATH}/uploads/*')
for key, file in enumerate(files_path):
    add_img = basename(file)
    print(basename(file))
    update_img = Imgs(img_url=add_img, page=key//15)
    db.session.add(update_img)

db.session.commit()
