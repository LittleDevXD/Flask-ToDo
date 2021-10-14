from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "a613cd92ab5de8dc61437c36b634ccbdfb3bf63cbb90a7de"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "/login"
login_manager.login_message = "Please login to get access."
login_manager.login_message_category = "info"
bcrypt = Bcrypt(app)

from todo import routes
