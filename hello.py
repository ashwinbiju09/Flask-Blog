from flask import Flask, render_template,url_for
from matplotlib.pyplot import title

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

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title='About')


if __name__ == '__main__':
    app.run(debug=True)

