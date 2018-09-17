from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from google.cloud import storage

from app.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.main.routes import main
    from app.processo.routes import processo
    from app.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(processo)
    implicit()
    return app


def implicit():
    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)
