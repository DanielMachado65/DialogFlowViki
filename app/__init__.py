from flask import Flask

from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.main.routes import main
    from app.processo.routes import processo
    from app.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(processo)

    return app