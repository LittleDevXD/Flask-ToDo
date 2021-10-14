from todo import app, db
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from todo.form import LoginForm, RegisterForm, TodoForm
from todo.models import User, ToDo
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/todo", methods=["GET", "POST"])
@login_required
def todo_page():
    form = TodoForm()
    if request.method == "POST":
        task = ToDo(task=form.task.data)
        task.user = current_user.id
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("todo_page"))

    if request.method == "GET":
        tasks = ToDo.query.filter_by(user=current_user.id)
    return render_template("todo.html", form=form, tasks=tasks)

# Login
@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = form.username.data
        attempted_password = form.password.data
        user = User.query.filter_by(username=attempted_user).first()
        if user and user.correct_pwd(attempted_password):
            login_user(user)
            flash(f"You have successfully logged in as {user.username}", category="success")
            return redirect(url_for("todo_page"))
        else:
            flash("Username and password do not match! Please try again.", category="danger")
    return render_template("login.html", form=form)

# Register
@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password1.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("todo_page"))
    elif form.errors != {}:
        for error in form.errors:
            flash(f"There was an error creating the user: {error}", category="danger")
    return render_template("register.html", form=form)

# Logout
@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have logged out.", category="info")
    return redirect(url_for("home_page"))