from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
import pytesseract
from google.cloud import vision
from recognition import Handwriting_Recognizer
from postgres_rest_api import Postgres as db
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/', methods=["POST"])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(file_path)

        Handwriting_Recognizer

        return render_template('index.html', filename=filename)

    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/update', methods=['GET', "POST"])
def update():
    if request.method == "POST":
        date = request.form.get('date')
        cash = request.form.get('cash')
        credit = request.form.get('credit')
        other = request.form.get('other')
        db.Update_Data(date, cash, credit, other)
        print("success")
    else:
        print('fails')
    return render_template('update_data.html')


@app.route('/add', methods=["GET", "POST"])
def add():
    # Sends client informtion to the server
    date = request.form.get('date')
    cash = request.form.get('cash')
    credit = request.form.get('credit')
    other = request.form.get('other')
    db.Add_Data(date, cash, credit, other)
    return render_template('add_data.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    date = None
    if request.method == 'POST':
        date = request.form.get('date')
        db.Delete_Data(date)

    return render_template('delete_data.html', date=date)


@app.route('/getAll', methods=["GET"])
def get_All():
    data = db.Get_All_Data()
    return render_template('get_all_data.html', rows=data)


@app.route('/getOne', methods=["GET", "POST"])
def get_One():
    date = request.args.get('date')
    row = db.Get_Data(date)
    return render_template('get_data.html', row=row)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4002)
