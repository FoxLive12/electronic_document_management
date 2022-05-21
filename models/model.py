from app import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    surname = db.Column(db.String(200), nullable=False)
    patronymic = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    watermark_url = db.Column(db.String(200), nullable=False)
    passw = db.Column(db.String(250), nullable=False)
    message = db.relationship("Message", backref='type', uselist=False)
    type_user = db.Column(db.Integer, db.ForeignKey('type.id'))
    watermark_id = db.Column(db.Integer, db.ForeignKey('watermark.id'))

    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Users {}>'.format(self.email)

class Watermark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(200), nullable=False)
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_until = db.Column(db.DateTime, nullable=False)
    user_id = db.relationship("Users", backref='watermark', uselist=False)
    
    def __init__(self, *args, **kwargs):
        super(Watermark, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Watermark {}>'.format(self.file_name)

class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    users_id = db.relationship("Users", backref='type', uselist=False)

    def __init__(self, *args, **kwargs):
        super(Type, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Type {}>'.format(self.title)

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    message_id = db.relationship("Message", backref='status', uselist=False)

    def __init__(self, *args, **kwargs):
        super(Status, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Status {}>'.format(self.title)

class Doc_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    message_id = db.relationship("Message", backref='doc_type', uselist=False)

    def __init__(self, *args, **kwargs):
        super(Doc_type, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Doc_type {}>'.format(self.title)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(200), nullable=False)
    file_url = db.Column(db.String(200), nullable=False)
    watermark_file_url = db.Column(db.String(200))
    date = db.Column(db.DateTime, nullable=False)
    status_mess = db.Column(db.Integer, db.ForeignKey('status.id'))
    doctype = db.Column(db.Integer, db.ForeignKey('doc_type.id'))
    sender = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient =  db.Column(db.Integer, nullable=False)
    message = db.relationship("Comment")

    def __init__(self, *args, **kwargs):
        super(Message, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Message {}>'.format(self.file_name)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.String(400), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))

    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Comment {}>'.format(self.title)