from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)

movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')


@movies_ns.route('/')
class Movies(Resource):
    def get(self):
        return


@movies_ns.route('/<int:mid>')
class Movie(Resource):

    def get(self):
        return


@directors_ns.route('/')
class Directors(Resource):
    def get(self):
        return


@directors_ns.route('/<int:did>')
class Director(Resource):

    def get(self):
        return


@genres_ns.route('/')
class Genres(Resource):
    def get(self):
        return


@genres_ns.route('/<int:gid>')
class Genre(Resource):
    def get(self):
        return


if 'name' == '__main__':
    app.run(debug=True)
