import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Lire les variables d'environnement
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    # Configuration de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import des blueprints
    from app.routes.home import home_bp
    from app.routes.events import events_bp

    # Enregistrement des blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(events_bp)

    return app
