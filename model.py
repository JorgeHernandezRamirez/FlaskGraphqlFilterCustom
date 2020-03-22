from flask_sqlalchemy import SQLAlchemy

from app import app

db = SQLAlchemy(app)


class UserModel(db.Model):
    __tablename__ = 'user'

    userid = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(256))

    surname = db.Column(db.String(256))

    age = db.Column(db.Integer)

    def __repr__(self):
        return '<User {} {} {} {}>'.format(self.id, self.name, self.surname, self.age)
