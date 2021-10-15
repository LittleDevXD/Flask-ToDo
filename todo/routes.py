from todo import app, db
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from todo.form import CompleteForm, DeleteForm, LoginForm, RegisterForm, TodoForm, UncompleteForm
from todo.models import FinishToDo, User, ToDo
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/todo", methods=["GET", "POST"])
@login_required
def todo_page():
    form = TodoForm()
    delete_form = DeleteForm()
    complete_form = CompleteForm()
    uncomplete_form = UncompleteForm()

    if request.method == "POST":
        # Adding initial Task
        if form.validate_on_submit():
            task = ToDo(task=form.task.data)
            task.user = current_user.id
            db.session.add(task)
            db.session.commit()
        
        # Move the completed task to FinishToDo Database
        if complete_form.validate_on_submit():
            # Delete Completed Task from ToDo db
            completed_tasks = request.form.get("completed_task")
            c_task_obj = ToDo.query.filter_by(task=completed_tasks).first()
            if c_task_obj:
                # Transfer the task into FinishToDo db
                task = c_task_obj.task
                finished_task = FinishToDo(task=task)
                finished_task.user = c_task_obj.user
                # Commiting to Database
                db.session.add(finished_task)
                db.session.delete(c_task_obj)
                db.session.commit()

        # Move the uncompleted tasks back to ToDo Database
        if uncomplete_form.validate_on_submit():
            # Delete Completed Task from FinishToDo db
            uncomplete_tasks = request.form.get("uncomplete_task")
            print(uncomplete_tasks)
            uc_task_obj = FinishToDo.query.filter_by(task=uncomplete_tasks).first()
            
            if uc_task_obj:
                # Transfer the task into ToDo db
                task = uc_task_obj.task
                unfinished_task = ToDo(task=task)
                unfinished_task.user = uc_task_obj.user
                # Commiting to Database
                db.session.add(unfinished_task)
                db.session.delete(uc_task_obj)
                db.session.commit()

        # Delete the finished task from the database
        if delete_form.validate_on_submit():
            deleted_task = request.form.get("deleted_task")
            d_task_obj = FinishToDo.query.filter_by(task=deleted_task).first()
            if d_task_obj:
                db.session.delete(d_task_obj)
                db.session.commit()

        return redirect(url_for("todo_page"))
        
    if request.method == "GET":
        tasks = ToDo.query.filter_by(user=current_user.id)
        completed_tasks = FinishToDo.query.filter_by(user=current_user.id)

    return render_template("todo.html", form=form, tasks=tasks, 
                            delete_form=delete_form, complete_form=complete_form, 
                            f_tasks=completed_tasks, uncomplete_form=uncomplete_form)

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
        for error in form.errors.values():
            flash(f"There was an error creating the user: {error}", category="danger")
    return render_template("register.html", form=form)

# Logout
@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have logged out.", category="info")
    return redirect(url_for("home_page"))