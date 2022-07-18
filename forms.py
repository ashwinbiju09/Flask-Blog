from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),Length(min=5,max=10)]) 

    email = StringField('Email',
                            validators=[DataRequired(), Email()])

    password = PasswordField('Password',
                            validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):

    email = StringField('Email',
                            validators=[DataRequired(), Email()])

    password = PasswordField('Password',
                            validators=[DataRequired()])
    
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')