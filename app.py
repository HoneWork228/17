from flask import Flask
from flask_restx import Api
from app_settings.config import Config
from app_settings.database import db
from app_settings.views.directors import directors_ns
from app_settings.views.genres import genres_ns
from app_settings.views.movies import movies_ns


def create_app(config: Config) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()

    return application


def configure_api(application: Flask):
    db.init_app(application)
    api = Api(application)
    api.add_namespace(movies_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)


if __name__ == '__main__':
    app = create_app(Config)
    configure_api(app)
    app.run()
