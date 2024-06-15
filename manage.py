from flask import Flask
from flask_migrate import Migrate
from models import db, Usuario
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

