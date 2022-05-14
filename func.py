from app import mail, app
from flask_mail import Message
from decorators import asyn
from flask import render_template

@asyn
def send_async_email(msg):
    with app.app_context():
        mail.send(msg)

def send_email(sender, email, username):
    msg = Message("Electronicworkflows - восстановление пароля", sender=sender,  recipients=email)
    msg.html = render_template('passw_mail.html', name = username, email = email)
    send_async_email(msg)

def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def rename_file(filename, date):
    return filename.rsplit('.', 1)[0] + str(date) + "." + filename.rsplit('.', 1)[1]