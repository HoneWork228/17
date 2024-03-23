from flask import request, redirect
from flask_restx import Resource, Namespace

from app_settings.DAO.models.movies import Movies
from app_settings.Schemas import movies_schema
from app_settings.constants import Constants
from app_settings.database import db

movies_ns = Namespace('movies')


@movies_ns.route('/')
class MoviesView(Resource):
    @staticmethod
    def get():
        try:
            director_id = request.args.get('director_id')
            genre_id = request.args.get('genre_id')
            movie_query = db.session.query(Movies)

            if director_id:
                movie_query = movie_query.filter(Movies.director_id == director_id)
            if genre_id:
                movie_query = movie_query.filter(Movies.genre_id == genre_id)

            return movies_schema.dump(movie_query, many=True), 200
        except Exception():
            return Constants.server_error, 500

    @staticmethod
    def post():
        try:
            try:
                data = request.get_json()
                movie = Movies(
                    title=data.get('title'),
                    description=data.get('description'),
                    trailer=data.get('trailer'),
                    year=data.get('year'),
                    rating=data.get('rating'),
                    genre_id=data.get('genre_id'),
                    director_id=data.get('director_id'),
                )
                db.session.add(movie)
                db.session.commit()
                return redirect(f'{request.base_url}{Movies.query.count()}', 201)
            except Exception:
                return Constants.bad_request, 400
        except Exception:
            return Constants.server_error, 500


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    @staticmethod
    def get(mid: int):
        try:
            movie = movies_schema.dump(db.session.query(Movies).filter(Movies.id == mid).first())
            if not movie:
                return not Constants.not_found, 404
            return movie, 200
        except Exception:
            return Constants.server_error, 500

    @staticmethod
    def delete(mid: int):
        try:
            if not db.session.query(Movies).filter(Movies.id == mid).delete():
                return Constants.not_found, 404
            db.session.commit()
            return '', 204
        except Exception:
            return Constants.server_error, 500

    @staticmethod
    def put(mid: int):
        try:
            try:
                data = request.get_json()
                movie = db.session.query(Movies).filter(Movies.id == mid).first()
                if not movie:
                    return Constants.not_found, 404
                movie.title = data.get('title')
                movie.description = data.get('description')
                movie.trailer = data.get('trailer')
                movie.year = data.get('year')
                movie.rating = data.get('rating')
                movie.genre_id = data.get('genre_id')
                movie.director_id = data.get('director_id')
                db.session.add(movie)
                db.session.commit()
                return redirect(request.base_url, 200)
            except Exception:
                return Constants.bad_request, 400
        except Exception:
            return Constants.server_error, 500

    @staticmethod
    def patch(mid: int):
        try:
            data = request.get_json()
            movie = db.session.query(Movies).filter(Movies.id == mid).first()
            if not movie:
                return Constants.not_found, 404
            try:
                keys = [key for key in data.keys() if hasattr(movie, key)]
                if len(keys) == 0:
                    return Constants.bad_request, 400
                for key in keys:
                    setattr(movie, key, data[key])
                db.session.add(movie)
                db.session.commit()
                return redirect(request.base_url, 200)
            except Exception:
                return Constants.bad_request, 400
        except Exception:
            return Constants.server_error, 500
