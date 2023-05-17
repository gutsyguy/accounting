from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import cv2
import json
import numpy as np
import pandas as pd
import requests
from base64 import b64encode
from IPython.display import Image
from matplotlib.pylab import rcParams
from google.cloud import vision
import matplotlib.pyplot as plt
from postgres_rest_api import Postgres as db



app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

rcParams['figure.figsize'] = 10, 20

def make_image_data(imgpath):
    img_req = None
    with open(imgpath, 'rb') as f:
        ctxt = b64encode(f.read()).decode()
        img_req = {
            'image': {
                'content': ctxt
            },
            'features': [{
                'type': 'DOCUMENT_TEXT_DETECTION',
                'maxResults': 1
            }]
        }
    return json.dumps({"requests": img_req}).encode()


def request_ocr(url, api_key, imgpath):
    imgdata = make_image_data(imgpath)
    response = requests.post(url,
                             data=imgdata,
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})
    return response

with open('vision_api.json') as f:
    data = json.load(f)

ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
api_key = data["api_key"]
img_loc = "uploads/4.jpg"


Image(img_loc)


result = request_ocr(ENDPOINT_URL, api_key, img_loc)


if result.status_code != 200 or result.json().get('error'):
    print("Error")
else:
    result = result.json()['responses'][0]['textAnnotations']


result

def extract_words_with_numbers(result):
    words_with_numbers = []
    for index in range(1, len(result)):
        description = result[index]["description"]
        prev_word = result[index - 1]["description"]
        if prev_word.lower() in ["cash", "credit", "debit"]:
            if description.isdigit():
                words_with_numbers.append((prev_word, float(description)))
    return words_with_numbers

found_words_with_numbers = extract_words_with_numbers(result)

def gen_cord(result):
    cord_df = pd.DataFrame(result['boundingPoly']['vertices'])
    x_min, y_min = np.min(cord_df["x"]), np.min(cord_df["y"])
    x_max, y_max = np.max(cord_df["x"]), np.max(cord_df["y"])
    return result["description"], x_max, x_min, y_max, y_min


text, x_max, x_min, y_max, y_min = gen_cord(result[-1])
image = cv2.imread(img_loc)
cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
print("Text Detected = {}".format(text))

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
        db.Add_Data('7/20/2023', text,text, text)
        print(file_path)


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