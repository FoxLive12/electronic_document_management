from app import app, login_manager, ALLOWED_EXTENSIONS
from flask import render_template, request, flash, url_for
from flask_login import login_user, login_required, current_user, logout_user
from model import *
from werkzeug.utils import redirect, secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from func import send_email, allowed_file, rename_file
from config import Configuration
import os
import datetime

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.route('/')
@login_required
def index():
    return render_template('base.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        passw = request.form['password']
        if email and passw:
            user = Users.query.filter_by(email=email).first()
            if user != None:
                if check_password_hash(user.passw, passw):
                    rm = True if request.form.get('remember') else False
                    login_user(user, remember = rm)
                    return redirect('/')
                else:
                    flash('Введён неверный пароль')
            else:
                flash('Пользователь с такой электронной почтой не найден')
        else:
            flash('Введён неверный пароль')

    return render_template('login.html', user=current_user)

@app.route('/login/registration', methods=['GET', 'POST'])
def registation():
    user_type = Type.query.all()
    if request.method == 'POST':
        surname = request.form['surname']
        name = request.form['name']
        patronymic = request.form['patronymic']
        email = request.form['email']
        passw = request.form['password']
        re_passw = request.form['re-password']
        user_role_id = int(Type.query.filter_by(title=str(request.form.get('user_type'))).first().id)
        if surname and name and patronymic and email and passw and re_passw:
            user = Users.query.filter_by(email=email).first()
            if user:
                flash('Эта электронная почта уже используется')
                return redirect('/login/registration')
            else:
                if passw == re_passw:
                    user = Users(surname=surname, name=name, patronymic=patronymic, email=email, passw=generate_password_hash(passw), type_user=user_role_id)
                    db.session.add(user)
                    db.session.commit()
                    os.mkdir(f'projects/{email}')
                    return redirect('/login')
                else:
                    flash('Пароли не совпадают')
                    return redirect('/login/registration')
        else:
            flash('Вы заполнили не все поля')
            return redirect('/login/registration')
    return render_template('registration.html', user=current_user, type = user_type)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(('/'))

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email'].split()
        user = Users.query.filter_by(email=email[0]).first()
        if user != None:
            sender = Configuration.MAIL_DEFAULT_SENDER
            send_email(sender, email, user.name)
        else:
            flash('Пользователь с такой электронной почтой не найден')
           

    return render_template('forgot.html', user=current_user)

@app.route('/password/recovery', methods=['GET', 'POST'])
def recovery():
    if request.method == 'POST':
        passw = request.form['password']
        re_passw = request.form['re-password']
        email = request.args['email']
        if passw == re_passw:
            user = Users.query.filter_by(email=email).first()
            user.passw = generate_password_hash(passw)
            db.session.add(user)
            db.session.commit()

            return redirect('/login')
        else:
            flash('Пароли не совпадают')

    return render_template('password_recovery.html', user=current_user)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/add-document', methods=['GET', 'POST'])
@login_required
def add_doc():
    users = Users.query.filter(Users.id != current_user.id).all()
    if request.method == 'POST':
        user = request.form['user_type']
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/add-document')
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            return redirect('/add-document')
        if f and allowed_file(f.filename, ALLOWED_EXTENSIONS):
            f.save(os.path.join(f'projects/{current_user.email}/', secure_filename(str(rename_file(f.filename, datetime.datetime.now())))))
            message = Message(file_name=f.filename, file_url=f'projects/{current_user.email}/{f.filename}', date=str(datetime.datetime.now()), status='Send', sender=current_user.id, recipient=user)
            db.session.add(message)
            db.session.commit()
            return redirect('/')
        else:
            flash('Недопустимое расширение файла')
            return redirect('/add-document')
    return render_template('add_doc.html', user=current_user, recipient = users)

@app.route('/outgoing')
@login_required
def outgoing():
    msg = Message.query.filter_by(sender = current_user.id).all()
    return render_template('outgoing.html', user=current_user, msg = msg)

@app.route('/incoming')
@login_required
def ingoing():
    msg = Message.query.filter_by(recipient = current_user.id).all()
    sender_list = []
    for i in msg:
        user = Users.query.filter_by(id=i.sender).first()
        sender_list.append(user.surname + " " + user.name[0] + ". " + user.patronymic[0] + ".")
    return render_template('incoming.html', user=current_user, msg = msg, sender = zip(sender_list, msg))

@app.route('/message')
@login_required
def message():
    id = request.args['name']
    msg = Message.query.filter_by(id = id).first()
    return render_template('message.html', user=current_user, msg=msg)