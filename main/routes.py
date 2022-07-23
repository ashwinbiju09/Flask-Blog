import email
from flask import render_template,url_for,flash,redirect,request
from main import app,db, bcrypt
from main.forms import RegistrationForm, LoginForm
from main.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required

posts = [
    {
        'author' : 'Creator 1',
        'title' : 'Post 1',
        'content' : 'First Post'
    },
    {
        'author' : 'Creator 2',
        'title' : 'Post 2',
        'content' : 'Second Post'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title='About')

@app.route("/Register",methods=['GET','POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Account created ! Please Login !','success')
        return redirect(url_for('Login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/Login",methods=['GET','POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page= request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Try again !','danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/Logout")
def Logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/Account")
@login_required
def Account():
        return render_template('account.html', title='Account')
