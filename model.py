from app import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    surname = db.Column(db.String(200), nullable=False)
    patronymic = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    passw = db.Column(db.String(250), nullable=False)
    message = db.relationship("Message", backref='type', uselist=False)
    type_user = db.Column(db.Integer, db.ForeignKey('type.id'))

    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Users {}>'.format(self.email)

class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    users_id = db.relationship("Users", backref='type', uselist=False)

    def __init__(self, *args, **kwargs):
        super(Type, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Type {}>'.format(self.title)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(200), nullable=False)
    file_url = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status= db.Column(db.String(200), nullable=False)
    sender = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient =  db.Column(db.Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        super(Message, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Message {}>'.format(self.file_name)