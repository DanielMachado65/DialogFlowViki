from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from google.cloud import storage

from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = 'warning'
login_manager.login_message = "Por favor faça o cadastro no sistema primeiramente! : )"
list_chamada = {}


# HACK: vai fazer a inicialização da aplicação
# IDEA: caso você precisa cadastrar novas rotas, é aqui onde você vai colocar as rotas
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.main.routes import main
    from app.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)
    implicit()
    return app


# HACK: faz as configurações da chave da aplicação.
# TODO: não mexer, porque ela já está organizada
def implicit():
    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
