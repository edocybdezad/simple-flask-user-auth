from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

from forms import RegistrationForm, LoginForm, AccountForm

import random

from models import *

app = Flask(__name__)

app.config['SECRET_KEY'] = "mySuperSecretKey"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

 
@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/login",  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            return redirect(url_for('account'))
        else:
            flash('Usuario o password invalidos')
    return render_template("login.html",form=form)

@app.route("/register",  methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))    
    form=RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Nombre de usuario no disponible')
            return redirect(url_for('register'))
        if email:
            flash('El email ingresado esta asociado a otra cuenta')
            return redirect(url_for('register'))
        user = User(name=form.name.data, username=form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Cuenta creada con exito. Ya puede conectarse')    
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route("/account",  methods=['GET', 'POST'])
@login_required
def account():
    form=AccountForm()
    city = random.choice(['Lima', 'New York', 'Tokyo', 'Paris','London'])
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.picture = form.avatar.data
        db.session.commit()
        flash('Perfil actualizado')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    foto_perfil = url_for('static', filename='images/' + current_user.picture)
    return render_template("account.html", 
                           foto_perfil=foto_perfil, 
                           city=city,
                           form=form)
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))
