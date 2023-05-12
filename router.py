from postgres_rest_api import Postgres as db
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/update')
def update():
    db.Update_Data('5/7/2023', 400, 200, 200)
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    cash = request.form['cash']
    credit = request.form['credit']
    other = request.form['other']
    db.Add_Data(date, int(cash), int(credit), int(other))
    return redirect(url_for('index'))



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
