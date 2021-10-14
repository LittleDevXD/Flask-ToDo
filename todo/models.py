from todo import app, db, login_manager, bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password_hash = db.Column(db.String(1000), nullable=False)
    todos = db.relationship("ToDo", backref=db.backref("owned_user", lazy=True))
    todo_comp = db.relationship("FinishToDo", backref=db.backref("person", lazy=True))

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def correct_pwd(self, attempted_pwd):
        return bcrypt.check_password_hash(self.password_hash, attempted_pwd)

class ToDo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    task = db.Column(db.String(10000), nullable=False)
    user = db.Column(db.Integer(), db.ForeignKey("user.id"))

class FinishToDo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    task = db.Column(db.String(10000), nullable=False)
    user = db.Column(db.Integer(), db.ForeignKey("user.id"))
