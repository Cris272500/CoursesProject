from flask_sqlalchemy import SQLAlchemy
from flask import Flask


db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    email_user = db.Column(db.String(60), unique=True, nullable=False)

    def __repr__(self):
        return f"User: {self.username} Email: {self.email_user}"
    
    # Metodos por flask_login
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)


class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth = db.Column(db.Integer, nullable=False)
    directors = db.relationship('Director', backref='persona', lazy='dynamic')
    actors = db.relationship('Actor', backref='persona', lazy='dynamic')

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable=False)

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable=False)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    directors = db.relationship('Director', backref='movie', lazy='dynamic')
    actors = db.relationship('Actor', backref='movie', lazy='dynamic')
