from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_restx import Api, Resource
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
api = Api(app)
api.app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4, }

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

    genre = relationship('Genres', foreign_keys=genre_id)
    director = relationship('Directors', foreign_keys=director_id)


class MoviesSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


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

        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        movie_query = Movies.query

        if director_id:
            movie_query = movie_query.filter(Movies.director_id == director_id)
        if genre_id:
            movie_query = movie_query.filter(Movies.genre_id == genre_id)

        return movies_schema.dump(movie_query, many=True), 200


@movies_ns.route('/<int:mid>')
class MovieView(Resource):

    def get(self, mid):
        return movies_schema.dump(db.session.query(Movies).filter(Movies.id == mid).first()), 200

    def delete(self, mid):
        db.session.query(Movies).filter(Movies.id == mid).delete()
        return '', 204


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        return directors_schema.dump(Directors.query.all(), many=True), 200


@directors_ns.route('/<int:did>')
class DirectorView(Resource):

    def get(self, did):
        return directors_schema.dump(db.session.query(Directors).filter(Directors.id == did).first()), 200

    def delete(self, did):
        db.session.query(Directors).filter(Directors.id == did).delete()
        return '', 204


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        return genres_schema.dump(Genres.query.all(), many=True), 200


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid):
        return genres_schema.dump(db.session.query(Genres).filter(Genres.id == gid).first()), 200

    def delete(self, gid):
        db.session.query(Genres).filter(Genres.id == gid).delete()
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)
