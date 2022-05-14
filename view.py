from operator import and_
from queue import Empty
from app import app, login_manager, ALLOWED_EXTENSIONS, admin
from flask import render_template, request, flash, send_from_directory
from flask_login import login_user, login_required, current_user, logout_user
from models.model import *
from werkzeug.utils import redirect, secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from func import send_email, allowed_file, rename_file
from config import Configuration
import os
import datetime
from models.adminModel import AdminView, RedirectView

login_manager.login_view = 'login'

admin.add_view(AdminView(Users, db.session))
admin.add_view(AdminView(Type, db.session))
admin.add_view(AdminView(Status, db.session))
admin.add_view(AdminView(Doc_type, db.session))
admin.add_view(AdminView(Message, db.session))
admin.add_view(AdminView(Comment, db.session))
admin.add_view(RedirectView(name='На главную'))

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

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
@login_required
def registation():
    if current_user.type_user == 1:
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
                        os.mkdir(f'static/projects/{email}')
                        return redirect('/')
                    else:
                        flash('Пароли не совпадают')
                        return redirect('/login/registration')
            else:
                flash('Вы заполнили не все поля')
                return redirect('/login/registration')
        return render_template('registration.html', user=current_user, type = user_type)
    else:
        return redirect("/")

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
    doctypes = Doc_type.query.all()
    if request.method == 'POST':
        user = request.form['user_type']
        docType = request.form['doc_type']
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/add-document')
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            return redirect('/add-document')
        if f and allowed_file(f.filename, ALLOWED_EXTENSIONS):
            f_name = secure_filename(str(rename_file(f.filename, datetime.datetime.now())))
            f.save(os.path.join(f'static/projects/{current_user.email}/', f_name))
            message = Message(file_name=f.filename, file_url=f'projects/{current_user.email}/' + f_name, date=str(datetime.datetime.now()), status_mess = 1, doctype = docType, sender=current_user.id, recipient=user)
            db.session.add(message)
            db.session.commit()
            return redirect('/')
        else:
            flash('Недопустимое расширение файла')
            return redirect('/add-document')
    return render_template('add_doc.html', user=current_user, recipient = users, type = doctypes)

@app.route('/outgoing', methods=['GET', 'POST'])
@login_required
def outgoing():
    msg = Message.query.filter_by(sender = current_user.id).all()
    status = Status.query.all()
    docType = Doc_type.query.all()
    if request.method == 'POST':
        status_id = request.form['status']
        docType_id = request.form['doc-type']
        dateFrom = request.form['date-from']
        dateBefore = request.form['date-before']
        msg = Message.query.filter(Message.sender == current_user.id).\
            filter(Message.status_mess == status_id if status_id else Message.status_mess).\
            filter(Message.doctype == docType_id if docType_id else Message.doctype).\
            filter(Message.date >= dateFrom if dateFrom else Message.date).\
            filter(Message.date <= dateBefore if dateBefore else Message.date).\
            all()
    return render_template('outgoing.html', user=current_user, msg = list(reversed(msg)), status = status, docType = docType, date=datetime.datetime.now())

@app.route('/outgoing/message', methods=['GET', 'POST'])
@login_required
def you_message():
    id = request.args['name']
    msg = Message.query.filter_by(id = id).first()
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/outgoing/message')
        f = request.files['file']
        text_comm = request.form['comment']
        if f.filename == '' or text_comm == '':
            flash('Не выбран файл/Не заполнен комментарий')
            return redirect(f'/outgoing/message?name={id}')
        if f and allowed_file(f.filename, ALLOWED_EXTENSIONS):
            f_name = msg.file_url.split('/')[-1]
            f.save(os.path.join(f'static/{msg.file_url}'))
            msg.file_name=f.filename 
            msg.date=str(datetime.datetime.now())
            msg.status_mess=4
            db.session.add(msg)
            db.session.commit()
            comment = Comment(title="Изменено", text = text_comm, date = str(datetime.datetime.now()), message_id = msg.id)
            db.session.add(comment)
            db.session.commit()
            return redirect('/outgoing')
        else:
            flash('Недопустимое расширение файла')
            return redirect('/add-document')
    return render_template('you_messages.html', user=current_user, msg = msg, comment = list(reversed(msg.message)))

@app.route('/incoming', methods=['GET', 'POST'])
@login_required
def ingoing():
    msg = Message.query.filter_by(recipient = current_user.id).all()
    sender_list = []
    status = Status.query.all()
    docType = Doc_type.query.all()
    if request.method == 'POST':
        status_id = request.form['status']
        docType_id = request.form['doc-type']
        dateFrom = request.form['date-from']
        dateBefore = request.form['date-before']
        msg = Message.query.filter(Message.recipient == current_user.id).\
            filter(Message.status_mess == status_id if status_id else Message.status_mess).\
            filter(Message.doctype == docType_id if docType_id else Message.doctype).\
            filter(Message.date >= dateFrom if dateFrom else Message.date).\
            filter(Message.date <= dateBefore if dateBefore else Message.date).\
            all()
    for i in msg:
        user = Users.query.filter_by(id=i.sender).first()
        sender_list.append(user.surname + " " + user.name[0] + ". " + user.patronymic[0] + ".")
    return render_template('incoming.html', user=current_user, msg = list(reversed(msg)), sender = zip(list(reversed(sender_list)), list(reversed(msg))), status = status, docType = docType)

@app.route('/incoming/message', methods=['GET', 'POST'])
@login_required
def message():
    id = request.args['name']
    msg = Message.query.filter_by(id = id).first()
    if msg.status_mess == 1 or msg.status_mess == 4:
            msg.status_mess = 2
            db.session.add(msg)
            db.session.commit()
    if request.method == 'POST':
        text_comm = request.form['comment']
        comment = Comment(title="Отклонён", text = text_comm, date = str(datetime.datetime.now()), message_id = msg.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(f"/reject?id={msg.id}")
    return render_template('message.html', user=current_user, msg=msg, comment = list(reversed(msg.message)))

@app.route('/reject')
@login_required
def reject():
    id = request.args['id']
    msg = Message.query.filter_by(id = id).first()
    msg.status_mess = 3
    db.session.add(msg)
    db.session.commit()
    return redirect(f"/incoming")

@app.route('/sign')
@login_required
def sign():
    id = request.args['id']
    msg = Message.query.filter_by(id = id).first()
    msg.status_mess = 6
    db.session.add(msg)
    db.session.commit()
    comment = Comment(title="Ожидает подписи", text = "Подписан", date = str(datetime.datetime.now()), message_id = msg.id)
    db.session.add(comment)
    db.session.commit()
    return redirect(f"/incoming")

@app.route('/approve')
@login_required
def approve():
    id = request.args['id']
    msg = Message.query.filter_by(id = id).first()
    msg.status_mess = 5
    db.session.add(msg)
    db.session.commit()
    comment = Comment(title="Ожидает подписи", text = "Ожидает подписи", date = str(datetime.datetime.now()), message_id = msg.id)
    db.session.add(comment)
    db.session.commit()
    return redirect(f"/incoming")

@app.route('/download/', methods=['GET', 'POST'])
@login_required
def download():
    url = request.args['url']
    return send_from_directory(app.static_folder, url, as_attachment=True)