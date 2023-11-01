from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "some_random_string_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/site.db"

db = SQLAlchemy(app)

from app import routes, models
