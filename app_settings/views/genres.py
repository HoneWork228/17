from flask import request, redirect
from flask_restx import Resource, Namespace

from app_settings.DAO.models.genres import Genres
from app_settings.Schemas import genres_schema
from app_settings.constants import Constants
from app_settings.database import db

genres_ns = Namespace('genres')


@genres_ns.route('/')
class GenresView(Resource):
    @staticmethod
    def get():
        try:
            return genres_schema.dump(Genres.query.all(), many=True), 200
        except Exception:
            return Constants.server_error, 500

    @staticmethod
    def post():
        try:
            try:
                data = request.get_json()
                print(data)
                genres = Genres(
                    name=data.get('name'),
                )
                db.session.add(genres)
                db.session.commit()
                return redirect(f'{request.base_url}{Genres.query.count()}', 201)
            except Exception:
                return Constants.bad_request, 400
        except Exception:
            return Constants.server_error, 500


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    @staticmethod
    def get(gid: int):
        try:
            genre = genres_schema.dump(db.session.query(Genres).filter(Genres.id == gid).first())
            if not genre:
                return '404 Not found', 404
            return genre, 200
        except Exception:
            return Constants.server_error, 500

    @staticmethod
    def delete(gid):
        try:
            genre = db.session.query(Genres).filter(Genres.id == gid).delete()
            if not genre:
                return Constants.not_found, 404
            db.session.commit()
            return '', 204
        except Exception:
            return Constants.server_error, 500

    @staticmethod
    def put(gid):
        try:
            data = request.get_json()
            genre = db.session.query(Genres).filter(Genres.id == gid).first()
            if not genre:
                return Constants.not_found, 404
            genre.name = data.get('name')
            db.session.commit()
            return redirect(request.base_url, 200)
        except Exception:
            return Constants.server_error, 500
