from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# initialisation unique de SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration de la base de données
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Lier SQLAlchemy à l'application Flask
    db.init_app(app)

    # Import des modèles
    from app.models import WebhookEvent

    # Créer la base de données après l'initialisation de l'application
    with app.app_context():
        db.create_all()

    # Import des blueprints
    from app.routes import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app
