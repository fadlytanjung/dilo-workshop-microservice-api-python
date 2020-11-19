"""
Extensions module

Each extension is initialized when app is created.
"""
import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Import config
from config import config_env

db = SQLAlchemy()

bcrypt = Bcrypt()
migrate = Migrate()
cors = CORS()

jwt = JWTManager()
ma = Marshmallow()


from app.routes import api as baseRoute

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_env[config_name])

    register_extensions(app)
    app.register_blueprint(baseRoute.blueprint)

    return app


def register_extensions(app):
    # Registers flask extensions

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)