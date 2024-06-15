from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    email_user = db.Column(db.String(60), unique=True, nullable=False)

    def __repr__(self):
        return f"User: {self.username} Email: {self.email_user}"
    
    # Metodos por flask_login
    