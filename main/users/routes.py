from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from main import db, bcrypt
from main.models import User, Post
from main.users.forms import RegistrationForm, LoginForm, Update,RequestResetForm, ResetPasswordForm
from main.users.utils import save_picture,reset_email

users = Blueprint('users',__name__)

@users.route("/Register",methods=['GET','POST'])
def Register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Account created ! Please Login !','success')
        return redirect(url_for('Users.Login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/Login",methods=['GET','POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page= request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Try again !','danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/Logout")
def Logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/Account",methods=['GET','POST'])
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
        return redirect(url_for('users.Account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    img_file = url_for('static', filename='profile_pics/' + current_user.img_file)
    return render_template('account.html', title='Account', img_file=img_file ,form=form)

@users.route("/user/<string:username>")
def user_post(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page',1,type=int)
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page ,per_page=5)
    return render_template('user_post.html',posts=posts,user=user)

@users.route("/reset_password",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        reset_email(user)
        flash('Check Email for further Instructions to Reset Password','info')
        return redirect(url_for('users.Login'))
    return render_template('reset.html',title='Reset Password',form=form)


@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Inavlid or Expired Token','warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        flash('Password Updated ! Please Login !','success')
        return redirect(url_for('users.Login'))
    return render_template('reset_token.html',title='Reset Password', form=form)