from flask import Flask, render_template,url_for,flash,redirect
from forms import RegistrationForm, LoginForm

 
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


app = Flask(__name__)

app.config['SECRET_KEY'] = 'd7659fef2c1feeb0577f780687697ce9'


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


