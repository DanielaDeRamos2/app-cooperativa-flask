from flask import Flask
from .sqlalchemy_db_manager import DBManager
from .models.base import db

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    DBManager.init_app(app)

    return app
