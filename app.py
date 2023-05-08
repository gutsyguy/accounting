from flask import Flask, render_template
# import sys
# sys.path.append('data/Postgres/config.py')
# from config import Postgres as db
from postgres_rest_api import Postgres as db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/delete')
def delete():
    db.Delete_Data('5/5/2023')
    print('success')
    return render_template('index.html')

@app.route('/getAll')
def get_All():
    db.Get_All_Data()
    return render_template('index.html')

@app.route('/getOne')
def get_One():
    db.Get_Data('5/6/2023')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000) 