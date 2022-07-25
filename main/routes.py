import email,secrets,os
from PIL import Image
from fileinput import filename
from flask import render_template,url_for,flash,redirect,request
from main import app,db, bcrypt
from main.forms import RegistrationForm, LoginForm, Update
from main.models import User,Post
from flask_login import login_user,logout_user,login_required,current_user

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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ ,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)

    output_size=(125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/Account",methods=['GET','POST'])
@login_required
def Account():
    form = Update()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.img_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated', category='success')
        return redirect(url_for('Account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    img_file = url_for('static', filename='profile_pics/' + current_user.img_file)
    return render_template('account.html', title='Account', img_file=img_file ,form=form)
