from sqlalchemy.orm import relationship

from app_settings.database import db


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

    def __repr__(self):
        return f'{self.id} -> {self.title}'
