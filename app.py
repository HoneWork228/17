from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_restx import Api, Resource
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
api = Api(app)
db = SQLAlchemy(app)

movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')


class Genres(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Directors(db.Model):
    __tablename__ = 'director'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Movies(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String)
    trailer = db.Column(db.String)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'), nullable=False)

    genre = relationship('Genres')
    director = relationship('Directors')


class MoviesSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenresSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movies_schema = MoviesSchema()
directors_schema = DirectorSchema()
genres_schema = GenresSchema()


@movies_ns.route('/')
class MoviesView(Resource):
    @staticmethod
    def get():
        with app.app_context():
            return movies_schema.dump(Movies.query.all(), many=True)


@movies_ns.route('/<int:mid>')
class MovieView(Resource):

    def get(self):
        return


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        return


@directors_ns.route('/<int:did>')
class DirectorView(Resource):

    def get(self):
        return


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        return


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self):
        return


if __name__ == '__main__':
    app.run(debug=True)
