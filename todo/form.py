from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from todo.models import User

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")

class RegisterForm(FlaskForm):

    # Custom Build
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists! Please choose another one.")

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError("There is already an account with this email address.")

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

class CompleteForm(FlaskForm):
    submit = SubmitField("Complete")

class UncompleteForm(FlaskForm):
    submit = SubmitField("Uncomplete")

class DeleteForm(FlaskForm):
    submit = SubmitField("Delete Task")

