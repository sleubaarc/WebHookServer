from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost/webhook'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importation des routes
    from .routes.home import home_bp
    from .routes.webhook import webhook_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(webhook_bp)

    return app
