from flask import request, redirect
from flask_restx import Resource, Namespace

from app_settings.DAO.models.directors import Directors
from app_settings.Schemas import directors_schema
from app_settings.constants import Constants
from app_settings.database import db

directors_ns = Namespace('directors')


@directors_ns.route('/')
class DirectorsView(Resource):
    @staticmethod
    def get():
        try:
            return directors_schema.dump(Directors.query.all(), many=True), 200
        except Exception:
            return Constants.server_error, 500

    @staticmethod
    def post():
        try:
            try:
                data = request.get_json()
                directors = Directors(
                    name=data.get('name'),
                )
                db.session.add(directors)
                db.session.commit()
                return redirect(f'{request.base_url}{Directors.query.count()}', 201)
            except Exception:
                return Constants.bad_request, 400
        except Exception:
            return Constants.server_error, 500


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    @staticmethod
    def get(did: int):
        try:
            director = directors_schema.dump(db.session.query(Directors).filter(Directors.id == did).first())
            if not director:
                return '404 Not found', 404
            return director, 200
        except Exception:
            return Constants.server_error, 500

    @staticmethod
    def delete(did: int):
        try:
            if not db.session.query(Directors).filter(Directors.id == did).delete():
                return Constants.not_found, 404
            db.session.commit()
            return '', 204
        except Exception:
            return Constants.server_error, 500

    @staticmethod
    def put(did: int):
        try:
            try:
                data = request.get_json()
                director = db.session.query(Directors).filter(Directors.id == did).first()
                if not director:
                    return Constants.not_found, 404
                director.name = data.get('name')
                db.session.add(director)
                db.session.commit()
                return redirect(request.base_url, 200)
            except Exception:
                return Constants.bad_request, 400
        except Exception:
            return Constants.server_error, 500
