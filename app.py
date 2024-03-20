from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_restx import Api, Resource
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
api = Api(app)

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
    rating = db.Column(db.Float, nullable=False)
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

    @staticmethod
    def post():
        data = request.get_json()
        with db.session.begin():
            movie = Movies(
                title=data['title'],
                description=data['description'],
                trailer=data['trailer'],
                year=data['year'],
                rating=data['rating'],
                genre_id=data['genre_id'],
                director_id=data['director_id']
            )
            db.session.add(movie)
            db.session.commit()
        return redirect(f'{request.base_url}{Movies.query.count()}', 201)


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    @staticmethod
    def get(mid: int):
        return movies_schema.dump(db.session.query(Movies).filter(Movies.id == mid).first()), 200

    @staticmethod
    def delete(mid: int):
        with db.session.begin():
            db.session.query(Movies).filter(Movies.id == mid).delete()
            db.session.commit()
        return '', 204

    @staticmethod
    def put(mid: int):
        data = request.get_json()
        with db.session.begin():
            movie = db.session.query(Movies).filter(Movies.id == mid).first()
            movie.title = data['title']
            movie.description = data['description']
            movie.trailer = data['trailer']
            movie.year = data['year']
            movie.rating = data['rating']
            movie.genre_id = data['genre_id']
            movie.director_id = data['director_id']

            db.session.add(movie)
            db.session.commit()
        return redirect(request.base_url, 200)


@directors_ns.route('/')
class DirectorsView(Resource):
    @staticmethod
    def get():
        return directors_schema.dump(Directors.query.all(), many=True), 200


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    @staticmethod
    def get(did: int):
        return directors_schema.dump(db.session.query(Directors).filter(Directors.id == did).first()), 200

    @staticmethod
    def delete(did: int):
        db.session.query(Directors).filter(Directors.id == did).delete()
        return '', 204


@genres_ns.route('/')
class GenresView(Resource):
    @staticmethod
    def get():
        return genres_schema.dump(Genres.query.all(), many=True), 200


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    @staticmethod
    def get(gid: int):
        return genres_schema.dump(db.session.query(Genres).filter(Genres.id == gid).first()), 200

    @staticmethod
    def delete(gid):
        db.session.query(Genres).filter(Genres.id == gid).delete()
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)
