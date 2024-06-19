from flask import Flask
from flask_migrate import Migrate
from models import db, Usuario, Persona, Director, Actor, Movie
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
