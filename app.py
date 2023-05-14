from postgres_rest_api import Postgres as db
from flask import Flask, render_template, send_from_directory
from flask_uploads import UploadSet, IMAGES

import sys
sys.path.insert(0, 'data/Postgres/postgres_rest_api.py')

app = Flask(__name__)
app.config["SECRET_KEY"] = 'asldfkjlj'
app.config['UPLOADED_PHOTO_DEST'] = 'uploads'

photos = UploadSet('photos', IMAGES)

app.config['SECRET_KEY'] = 'asldfkjlj'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos')



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/update')
def update():
    db.Update_Data('5/7/2023', 400, 200, 200)
    return


@app.route('/add', methods=["PUT"])
def add():
    date = '5/10/2023'
    cash = 1000
    credit = 1000000
    other = 1
    db.Add_Data(date, cash, credit, other)
    return render_template('index.html')


@app.route('/delete')
def delete():
    db.Delete_Data('5/5/2023')
    print('success')
    return render_template('index.html')


@app.route('/getAll', methods=["GET"])
def get_All():
    db.Get_All_Data()
    return render_template('index.html')


@app.route('/getOne', methods=["GET"])
def get_One():
    db.Get_Data('5/6/2023')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4001)
