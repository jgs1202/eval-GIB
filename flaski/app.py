from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=False)
    data = db.Column(db.String(80), unique=False)
    choice1 = db.Column(db.String(80), unique=False)
    choice2 = db.Column(db.String(80), unique=False)

    def __init__(self, username, email, data, choice1, choice2):
        self.username = username
        self.email = email
        self.data = data
        self.choice1 = choice1
        self.choice2 = choice2

    def __repr__(self):
        return '<User %r>' % self.username
