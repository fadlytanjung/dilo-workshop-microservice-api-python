import os
from datetime import timedelta

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Change the secret key in production run.
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = False

    # JWT Extended config
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ## Set the token to expire every week
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    ENV = os.getenv('ENV')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'.format(
        DB_USER=os.environ.get('DB_USER'),
        DB_PASS=os.environ.get('DB_PASS'),
        DB_HOST=os.environ.get('DB_HOST'),
        DB_NAME=os.environ.get('DB_NAME')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add logger


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    # In-memory SQLite for testing
    SQLALCHEMY_DATABASE_URI = ""
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_env = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    default=DevelopmentConfig,
)
