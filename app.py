from flask import Flask, url_for, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:prud_30.01.2002@localhost/py_first'
db = SQLAlchemy(app)


class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    breed = db.Column(db.String(32), nullable=False)
    location_x = db.Column(db.String(32), nullable=False)
    location_y = db.Column(db.String(32), nullable=False)

    def __init__(self, name, breed, location_x, location_y):
        self.name = name.strip()
        self.breed = breed.strip()
        self.location_x = location_x
        self.location_y = location_y

db.create_all()


@app.route('/main', methods=["GET"])
def main():
    return render_template('main.html', cats=Cat.query.all())


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', cats=Cat.query.all())


@app.route('/deletion', methods=['GET'])
def deletion():
    return render_template('deletion.html', cats=Cat.query.all())


@app.route('/cat_delete', methods=['POST'])
def cat_delete():
    name = request.form['name']
    cat = Cat.query.filter_by(name=name).first()

    db.session.delete(cat);
    db.session.commit()

    return redirect(url_for('deletion'))


@app.route('/add_cat', methods=['POST'])
def add_cat():
    name = request.form['name']
    breed = request.form['breed']
    location_x = request.form['loc_x']
    location_y = request.form['loc_y']

    db.session.add(Cat(name, breed, location_x, location_y))
    db.session.commit()

    return redirect(url_for('main'))

