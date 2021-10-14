from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password1 = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField("Create Account")

class LogoutForm(FlaskForm):
    submit = SubmitField("Logout")

class TodoForm(FlaskForm):
    task = StringField("Your Todo Here", validators=[DataRequired()])
    submit = SubmitField("Create Task")