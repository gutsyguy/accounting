from postgres_rest_api import Postgres as db
from flask import Flask, render_template, request, send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


app = Flask(__name__)
app.config["SECRET_KEY"] = 'asldfkjlj'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'images only'),
            FileRequired('Field should not be empty')
        ]
    )
    submit = SubmitField('Upload')


@app.route('/', methods=["GET", "POST"])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = None
    return render_template('index.html', form=form, file_url=file_url)


@app.route('/upload/<filename>')
def get_file(filename):
    return send_from_directory(app.config["UPLOADED_PHOTO_DEST"], filename)


@app.route('/update')
def update():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = None
        db.Update_Data('5/7/2023', 400, 200, 200)
    return render_template('update_data.html', form=form, file_url=file_url)


@app.route('/add')
def add():
    # Sends client informtion to the server
    date = request.form.get('date')
    cash = request.form.get('cash')
    credit = request.form.get('credit')
    other = request.form.get('other')
    db.Add_Data(date, cash, credit, other)

    # Upload file
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = None
    return render_template('add_data.html', form=form, file_url=file_url)


@app.route('/submit_add', methods=["POST"])
def submit_add():
    date = request.form.get('date')
    cash = request.form.get('cash')
    credit = request.form.get('credit')
    other = request.form.get('other')
    print(date, cash, credit, other)
    db.Add_Data(date, cash, credit, other)
    return render_template('add_data.html')


@app.route('/delete')
def delete():
    date = request.form.get('date')
    db.Delete_Data(date)
    # Upload file

    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = None
    return render_template('delete_data.html', form=form, file_url=file_url)


@app.route('/getAll', methods=["GET"])
def get_All():
    data = db.Get_All_Data()
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = None
    return render_template('get_all_data.html', form=form, data=data, file_url=file_url, rows=data)


@app.route('/getOne', methods=["GET"])
def get_One():
    date = request.form.get('date')
    data = db.Get_Data(date)
    if data == None:
        return print("L")

    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = None
    return render_template('get_data.html', form=form, data=data, file_url=file_url, row=data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4002)
