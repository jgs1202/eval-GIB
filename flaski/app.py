from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False)
    gender = db.Column(db.String(80), unique=False)
    age = db.Column(db.String(20), unique=False)
    groupSize = db.Column(db.String(80), unique=False)
    pgroup = db.Column(db.String(80), unique=False)
    pout = db.Column(db.String(80), unique=False)
    file = db.Column(db.String(80), unique=False)
    choice = db.Column(db.String(80), unique=False)
    # choice2 = db.Column(db.String(80), unique=False)

    def __init__(self, username, gender, age, groupSize, pgroup, pout, file, choice):
        self.username = username
        self.gender = gender
        self.age = age
        self.groupSize= groupSize
        self.pgroup = pgroup
        self.pout = pout
        self.file = file
        self.choice = choice
        # self.choice2 = choice2

    def __repr__(self):
        return '<User %r>' % self.username
