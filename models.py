from flask_sqlalchemy import SQLAlchemy
from flask import Flask


db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    email_user = db.Column(db.String(60), unique=True, nullable=False)
    rol = db.Column(db.String(20), nullable=False)

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

categorias_curso = db.Table('categorias_curso', 
    db.Column('curso_id', db.Integer, db.ForeignKey('curso.id'), primary_key=True),
    db.Column('categoria_id', db.Integer, db.ForeignKey('categoria.id'), primary_key=True)
    )

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    categorias = db.relationship('Categoria', secondary=categorias_curso,
                                 backref=db.backref('cursos', lazy='dynamic'))

    def __repr__(self):
        return f"Curso: {self.title} // Descrpcion: {self.description}"

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Categoria: {self.name}"

