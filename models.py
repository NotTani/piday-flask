from db import db


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.Text())
    digits = db.Column(db.Float())
