from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired,Email

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    first_name = StringField('First Name', validators=[Length(min=2, max=50), DataRequired()])
    last_name = StringField('Last Name', validators=[Length(min=2, max=50), DataRequired()])
    password1 = PasswordField('Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label = 'Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField(label = 'password', validators = [DataRequired()])
    submit = SubmitField(label = 'Sign In')