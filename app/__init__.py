from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = "some_random_string_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/site.db"

db = SQLAlchemy(app)

migrate = Migrate(app, db)


from app import routes, models
