from datetime import datetime
from flask import Flask, render_template,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd7659fef2c1feeb0577f780687697ce9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    img_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)


    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.img_file}')"


class Post(db.Model):
        id = db.Column(db.Integer,primary_key = True)
        title = db.Column(db.String(100),nullable=False)
        date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
        content = db.Column(db.String,nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

        def __repr__(self):
            return f"Post('{self.title}','{self.date_posted}')"
 
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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data }!','success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/Login",methods=['GET','POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'a@gmail.com' and form.password.data == '123' :
            flash('Successfully Logged in !','success')
            return redirect(url_for('home'))
        else:
            flash('Try again !','danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)


