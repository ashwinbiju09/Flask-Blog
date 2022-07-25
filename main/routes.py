import secrets,os
from turtle import pos
from PIL import Image
from flask import render_template,url_for,flash,redirect,request,abort
from matplotlib.pyplot import legend
from main import app,db, bcrypt
from main.forms import RegistrationForm, LoginForm, Update,PostForm
from main.models import User,Post
from flask_login import login_user,logout_user,login_required,current_user


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
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


@app.route('/Post/new',methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Created !',category='success')
        return redirect(url_for('home'))
    return render_template('create_post.html',title='New Post',form=form,legend='Update Post')


@app.route('/Post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)


@app.route('/Post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Update Successful',category='success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method =='GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route('/Post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted',category='success')
    return redirect(url_for('home'))